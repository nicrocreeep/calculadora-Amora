from decimal import Decimal
import streamlit as st

from calculadora import (
    calcular_faixas,
    calcular_preco_para_repasse,
    formatar_brl,
)

st.set_page_config(
    page_title="Calculadora iFood | Amora Confeitaria",
    page_icon="🍓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Identidade visual delicada, inspirada na Amora Confeitaria.
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700&display=swap');
      html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
      .stApp { background: #fbf8f5; }
      [data-testid="stHeader"] { background: rgba(251,248,245,0.92); }
      .main .block-container { max-width: 1180px; padding-top: 2rem; padding-bottom: 3rem; }
      .amora-eyebrow { color: #9b5362; text-transform: uppercase; letter-spacing: .16em; font-size: .75rem; font-weight: 800; }
      .amora-title { font-family: 'Playfair Display', serif; color: #542936; font-size: clamp(2rem, 4vw, 3.2rem); line-height: 1.1; margin: .15rem 0 .45rem 0; }
      .amora-subtitle { color: #78696a; font-size: 1rem; margin-bottom: 1.2rem; }
      .amora-card { background: white; border: 1px solid #eadfe0; border-radius: 18px; padding: 1.1rem 1.25rem; box-shadow: 0 5px 18px rgba(77,37,48,.045); }
      .amora-label { color: #80666b; font-size: .83rem; font-weight: 700; margin-bottom: .25rem; }
      .amora-value { color: #542936; font-size: 1.8rem; font-weight: 800; line-height: 1.25; }
      .amora-highlight { background: linear-gradient(135deg, #6e263c, #913d55); color: white; border-radius: 20px; padding: 1.35rem 1.5rem; box-shadow: 0 9px 24px rgba(110,38,60,.16); }
      .amora-highlight .small { color: #f7dfe4; font-size: .86rem; font-weight: 600; }
      .amora-highlight .big { color: white; font-size: clamp(2rem, 4vw, 2.8rem); font-weight: 800; line-height: 1.2; }
      .amora-highlight .note { color: #f8e9ec; font-size: .86rem; margin-top: .3rem; }
      .amora-section { color: #542936; font-family: 'Playfair Display', serif; font-size: 1.45rem; font-weight: 700; margin: .2rem 0 .6rem 0; }
      .amora-foot { color: #887b7c; font-size: .78rem; }
      div[data-testid="stMetric"] { background: white; border: 1px solid #eadfe0; padding: 1rem; border-radius: 14px; }
      div[data-testid="stMetric"] label { color: #80666b; }
      div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #542936; }
      .stButton button[kind="primary"] { background: #7d3048; border: 0; }
      .stButton button[kind="primary"]:hover { background: #64253a; border: 0; }
      div[data-testid="stDataFrame"] { border: 1px solid #eadfe0; border-radius: 12px; overflow: hidden; }
      section[data-testid="stSidebar"] { background: #f4ece8; border-right: 1px solid #eadfe0; }
    </style>
    """,
    unsafe_allow_html=True,
)


def D(value: float | int | str) -> Decimal:
    return Decimal(str(value))


def brl_num(value: Decimal) -> float:
    return float(value)


with st.sidebar:
    st.markdown("## 🍓 Amora Confeitaria")
    st.caption("Calculadora de preços para o iFood")
    st.divider()
    st.markdown("### Taxas do iFood")
    st.caption("Valores iniciais copiados do contrato enviado. Edite se o contrato mudar.")
    comissao = st.number_input("Comissão fixa (%)", min_value=0.0, max_value=99.0, value=12.0, step=0.1, format="%.2f")
    pagamento = st.number_input("Pagamento online (%)", min_value=0.0, max_value=99.0, value=3.2, step=0.1, format="%.2f")
    st.divider()
    st.markdown("### Comissão variável por distância")
    taxa_0_3 = st.number_input("0 a 3 km (R$)", min_value=0.0, value=3.99, step=0.10, format="%.2f")
    taxa_3_5 = st.number_input("3 a 5 km (R$)", min_value=0.0, value=5.99, step=0.10, format="%.2f")
    taxa_5_7 = st.number_input("5 a 7 km (R$)", min_value=0.0, value=7.99, step=0.10, format="%.2f")
    taxa_mais_7 = st.number_input("Acima de 7 km (R$)", min_value=0.0, value=9.99, step=0.10, format="%.2f")
    st.divider()
    arredondamento_label = st.selectbox(
        "Arredondar o preço sugerido para cima",
        ["R$ 0,01 (centavos)", "R$ 0,10", "R$ 0,50", "R$ 1,00"],
        index=1,
    )
    arredondamentos = {
        "R$ 0,01 (centavos)": D("0.01"),
        "R$ 0,10": D("0.10"),
        "R$ 0,50": D("0.50"),
        "R$ 1,00": D("1.00"),
    }
    arredondamento = arredondamentos[arredondamento_label]
    st.caption("A mensalidade, promoções, estornos e outros ajustes não estão incluídos nesta simulação.")

st.markdown('<div class="amora-eyebrow">Ferramenta de precificação</div>', unsafe_allow_html=True)
st.markdown('<div class="amora-title">Quanto cobrar no iFood? 🍓</div>', unsafe_allow_html=True)
st.markdown('<div class="amora-subtitle">Informe quanto a Amora quer receber por unidade. A calculadora encontra um preço único para cadastrar e mostra o repasse estimado em cada distância.</div>', unsafe_allow_html=True)

left, right = st.columns([1.05, 1], gap="large")
with left:
    with st.container(border=True):
        st.markdown("#### 1. Dados do produto")
        valor_desejado_num = st.number_input(
            "Quanto vocês querem receber por unidade? (R$)",
            min_value=0.01,
            value=12.00,
            step=0.50,
            format="%.2f",
            help="Use o preço da loja física ou o valor líquido que desejam preservar depois das taxas do iFood.",
        )
        custo_num = st.number_input(
            "Custo de produção + embalagem (opcional, R$)",
            min_value=0.0,
            value=0.0,
            step=0.50,
            format="%.2f",
            help="Preencha para estimar quanto sobra depois das taxas do iFood e do custo informado.",
        )
        nome_produto = st.text_input("Nome do produto (opcional)", placeholder="Ex.: Empadão de frango 300g")

if nome_produto.strip():
    st.caption(f"Produto em cálculo: **{nome_produto.strip()}**")

faixas = [
    ("0 a 3 km", D(taxa_0_3)),
    ("3 a 5 km", D(taxa_3_5)),
    ("5 a 7 km", D(taxa_5_7)),
    ("Acima de 7 km", D(taxa_mais_7)),
]

with right:
    try:
        preco_exato, preco_sugerido = calcular_preco_para_repasse(
            D(valor_desejado_num), D(comissao), D(pagamento), D(taxa_0_3), arredondamento
        )
        resultados = calcular_faixas(
            preco_sugerido, D(comissao), D(pagamento), faixas, D(custo_num)
        )
        st.markdown(
            f'<div class="amora-highlight"><div class="small">PREÇO ÚNICO SUGERIDO PARA CADASTRAR NO IFOOD</div><div class="big">{formatar_brl(preco_sugerido)}</div><div class="note">Preço calculado exato: {formatar_brl(preco_exato)} · Arredondado para cima para não ficar abaixo da meta.</div></div>',
            unsafe_allow_html=True,
        )
        st.write("")
        st.metric("Repasse estimado na faixa de 0 a 3 km", formatar_brl(resultados[0]["repasse"]))
    except ValueError as exc:
        st.error(str(exc))
        resultados = []
        preco_sugerido = D("0")

if resultados:
    st.markdown('<div class="amora-section">2. Quanto sobra conforme a distância?</div>', unsafe_allow_html=True)
    st.caption(f"Preço único considerado: {formatar_brl(preco_sugerido)}. O cliente paga o mesmo preço do produto; o repasse da loja muda conforme a comissão variável da distância.")
    header = st.columns([1.3, 1, 1, 1.25])
    for col, title in zip(header, ["Distância", "Taxa variável", "Repasse iFood", "Após custo informado"]):
        col.markdown(f"**{title}**")
    for idx, item in enumerate(resultados):
        cols = st.columns([1.3, 1, 1, 1.25])
        if idx == 0:
            cols[0].markdown("**🟢 0 a 3 km**")
        else:
            cols[0].write(item["distancia"])
        cols[1].write(formatar_brl(item["taxa_variavel"]))
        cols[2].markdown(f"**{formatar_brl(item['repasse'])}**")
        if custo_num > 0:
            sobra = item["sobra_apos_custo"]
            cor = "#247a4a" if sobra >= 0 else "#bd3030"
            cols[3].markdown(f"<span style='color:{cor};font-weight:800'>{formatar_brl(sobra)}</span>", unsafe_allow_html=True)
        else:
            cols[3].caption("Informe o custo")
        st.divider()

    if custo_num > 0:
        st.info("A coluna ‘Após custo informado’ é uma estimativa depois das taxas do iFood e do custo de produção + embalagem preenchido. Ainda não considera mensalidade, impostos, perdas ou outras despesas.")
    else:
        st.info("Preencha o custo de produção + embalagem para estimar a sobra por pedido. Sem esse dado, o repasse não deve ser confundido com lucro.")

    st.markdown('<div class="amora-section">3. Como a conta é feita</div>', unsafe_allow_html=True)
    pct_total = D(comissao) + D(pagamento)
    st.markdown(
        f"O cálculo usa **{pct_total:.2f}%** de taxas percentuais ({D(comissao):.2f}% + {D(pagamento):.2f}%) e a comissão variável de **{formatar_brl(D(taxa_0_3))}** da faixa de 0 a 3 km para definir o preço-base."
    )
    st.latex(r"\text{Preço sugerido}=\frac{\text{Valor desejado}+\text{Taxa variável (0–3 km)}}{1-\frac{\text{Comissão fixa}+\text{Pagamento online}}{100}}")

st.divider()
st.markdown(
    '<div class="amora-foot">Amora Confeitaria · Simulação de repasse, não garantia de recebimento. Confira o extrato de cada pedido e mantenha as taxas atualizadas conforme o contrato vigente.</div>',
    unsafe_allow_html=True,
)
