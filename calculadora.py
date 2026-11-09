"""Regras de cálculo da calculadora da Amora Confeitaria.

Módulo independente do Streamlit para facilitar testes e manutenção.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP
from typing import Iterable

CENT = Decimal("0.01")


def dec(value: object) -> Decimal:
    """Converte números ou strings para Decimal sem imprecisão binária."""
    return Decimal(str(value))


def calcular_preco_para_repasse(
    valor_desejado: Decimal,
    percentual_fixo: Decimal,
    taxa_pagamento: Decimal,
    taxa_distancia_base: Decimal,
    arredondamento: Decimal = CENT,
) -> tuple[Decimal, Decimal]:
    """Retorna (preço exato, preço sugerido arredondado para cima).

    Fórmula: (repasse desejado + taxa variável da faixa-base) /
             (1 - percentual fixo - taxa de pagamento).
    Os percentuais devem ser informados como percentuais comuns (ex.: 12, 3.2).
    """
    valores = (valor_desejado, percentual_fixo, taxa_pagamento, taxa_distancia_base, arredondamento)
    if any(v < 0 for v in valores):
        raise ValueError("Os valores não podem ser negativos.")
    if arredondamento <= 0:
        raise ValueError("O arredondamento precisa ser maior que zero.")

    percentual_total = (percentual_fixo + taxa_pagamento) / Decimal("100")
    fator_liquido = Decimal("1") - percentual_total
    if fator_liquido <= 0:
        raise ValueError("A soma dos percentuais precisa ser menor que 100%.")

    preco_exato = (valor_desejado + taxa_distancia_base) / fator_liquido
    preco_sugerido = (preco_exato / arredondamento).to_integral_value(rounding=ROUND_CEILING) * arredondamento
    return preco_exato.quantize(CENT, rounding=ROUND_HALF_UP), preco_sugerido.quantize(CENT, rounding=ROUND_HALF_UP)


def calcular_repasse(
    preco_venda: Decimal,
    percentual_fixo: Decimal,
    taxa_pagamento: Decimal,
    taxa_distancia: Decimal,
) -> Decimal:
    """Calcula o repasse estimado após taxas percentuais e taxa por distância."""
    if any(v < 0 for v in (preco_venda, percentual_fixo, taxa_pagamento, taxa_distancia)):
        raise ValueError("Os valores não podem ser negativos.")
    percentual_total = (percentual_fixo + taxa_pagamento) / Decimal("100")
    if percentual_total >= 1:
        raise ValueError("A soma dos percentuais precisa ser menor que 100%.")
    liquido = preco_venda * (Decimal("1") - percentual_total) - taxa_distancia
    return liquido.quantize(CENT, rounding=ROUND_HALF_UP)


def calcular_faixas(
    preco_venda: Decimal,
    percentual_fixo: Decimal,
    taxa_pagamento: Decimal,
    faixas: Iterable[tuple[str, Decimal]],
    custo_unitario: Decimal = Decimal("0"),
) -> list[dict[str, Decimal | str]]:
    """Calcula repasse e sobra após custo informado para cada faixa."""
    resultados: list[dict[str, Decimal | str]] = []
    for nome, taxa in faixas:
        repasse = calcular_repasse(preco_venda, percentual_fixo, taxa_pagamento, taxa)
        resultados.append({
            "distancia": nome,
            "taxa_variavel": taxa.quantize(CENT),
            "repasse": repasse,
            "sobra_apos_custo": (repasse - custo_unitario).quantize(CENT, rounding=ROUND_HALF_UP),
        })
    return resultados


def formatar_brl(valor: Decimal) -> str:
    """Formata Decimal como moeda brasileira: R$ 1.234,56."""
    valor = valor.quantize(CENT, rounding=ROUND_HALF_UP)
    texto = f"{valor:,.2f}"
    texto = texto.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"
