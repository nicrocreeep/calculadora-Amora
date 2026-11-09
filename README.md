# 🍓 Calculadora iFood — Amora Confeitaria

Aplicativo simples em Streamlit para estimar o preço único que deve ser cadastrado no iFood para atingir um repasse desejado na faixa de 0 a 3 km e visualizar quanto sobra nas demais faixas de distância.

## O que o aplicativo faz

- Recebe o valor líquido que a Amora deseja preservar por unidade (por exemplo, o preço de venda na loja física).
- Calcula o preço sugerido para cadastrar no iFood considerando a comissão percentual e a comissão variável de 0 a 3 km.
- Arredonda o preço para cima (por padrão, para múltiplos de R$ 0,10), evitando ficar abaixo da meta.
- Mostra o repasse estimado nas faixas de 0–3 km, 3–5 km, 5–7 km e acima de 7 km, mantendo o mesmo preço de venda.
- Permite preencher custo de produção + embalagem para estimar a sobra após taxas e custo informado.
- Deixa todas as taxas editáveis na barra lateral.

## Taxas preenchidas inicialmente

Os valores padrão refletem o formulário de contratação enviado pela Amora:

| Taxa | Padrão |
|---|---:|
| Comissão fixa | 12% |
| Pagamento online | 3,2% |
| 0–3 km | R$ 3,99 |
| 3–5 km | R$ 5,99 |
| 5–7 km | R$ 7,99 |
| Acima de 7 km | R$ 9,99 |

**Importante:** o preço único é calculado para atingir a meta na faixa de 0–3 km. Nas faixas mais distantes, o repasse será menor por causa da comissão variável. O aplicativo não configura o iFood nem altera a taxa cobrada do consumidor; ele apenas simula a precificação e os repasses com as taxas informadas.

## Rodar no computador

Recomendado: Python 3.10 ou superior.

```bash
pip install -r requirements.txt
streamlit run app.py
```

O navegador abrirá o aplicativo localmente.

## Publicar no GitHub e Streamlit Community Cloud

1. Extraia o ZIP em uma pasta.
2. Crie um repositório no GitHub (por exemplo, `amora-calculadora-ifood`).
3. Envie para o repositório todos os arquivos e a pasta `.streamlit`.
4. Acesse [share.streamlit.io](https://share.streamlit.io/) e entre com sua conta GitHub.
5. Clique em **Create app**.
6. Selecione o repositório, a branch (normalmente `main`) e o arquivo principal `app.py`.
7. Clique em **Deploy**.

O Streamlit Community Cloud instalará as dependências de `requirements.txt` automaticamente.

## Testar os cálculos

Sem precisar instalar Streamlit, é possível testar o módulo de cálculo:

```bash
python -m unittest discover -s tests -v
```

## Limitações e cuidados

- O resultado é uma simulação baseada nas taxas preenchidas. Confira o detalhamento financeiro de cada pedido no Portal do Parceiro.
- Não inclui mensalidade, impostos, promoções, estornos, ajustes, cupons ou outras cobranças não informadas.
- O repasse não é lucro. Para estimar a sobra depois do produto, preencha custo de produção + embalagem. Ainda podem existir outros custos operacionais.
- Atualize as taxas na barra lateral sempre que o contrato ou o plano do iFood mudar.
