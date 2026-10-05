from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import json

CENTAVOS = Decimal("0.01")


def carregar_vendas(caminho):
    arquivo = Path(caminho)
    if not arquivo.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {arquivo}")

    with arquivo.open("r", encoding="utf8") as entrada:
        dados = json.load(entrada)

    vendas = dados.get("vendas")
    if not isinstance(vendas, list):
        raise ValueError("O JSON deve possuir uma lista chamada vendas")

    return vendas


def calcular_comissao(valor):
    if valor < Decimal("100.00"):
        percentual = Decimal("0.00")
    elif valor < Decimal("500.00"):
        percentual = Decimal("0.01")
    else:
        percentual = Decimal("0.05")

    return (valor * percentual).quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def consolidar_comissoes(vendas):
    resultado = defaultdict(lambda: {"total_vendido": Decimal("0.00"), "comissao": Decimal("0.00"), "quantidade": 0})

    for indice, venda in enumerate(vendas, start=1):
        vendedor = venda.get("vendedor")
        valor_bruto = venda.get("valor")

        if not isinstance(vendedor, str) or not vendedor.strip():
            raise ValueError(f"Vendedor inválido no registro {indice}")

        try:
            valor = Decimal(str(valor_bruto))
        except Exception as erro:
            raise ValueError(f"Valor inválido no registro {indice}") from erro

        if valor < 0:
            raise ValueError(f"A venda do registro {indice} não pode ser negativa")

        nome = vendedor.strip()
        resultado[nome]["total_vendido"] += valor
        resultado[nome]["comissao"] += calcular_comissao(valor)
        resultado[nome]["quantidade"] += 1

    return resultado


def formatar_moeda(valor):
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def exibir_resultado(resultado):
    print("Resultado das comissões")
    print()

    for vendedor in sorted(resultado):
        dados = resultado[vendedor]
        total = dados["total_vendido"].quantize(CENTAVOS, rounding=ROUND_HALF_UP)
        comissao = dados["comissao"].quantize(CENTAVOS, rounding=ROUND_HALF_UP)
        print(f"Vendedor: {vendedor}")
        print(f"Quantidade de vendas: {dados['quantidade']}")
        print(f"Total vendido: {formatar_moeda(total)}")
        print(f"Comissão: {formatar_moeda(comissao)}")
        print()


def executar():
    caminho = Path(__file__).with_name("vendas.json")
    vendas = carregar_vendas(caminho)
    resultado = consolidar_comissoes(vendas)
    exibir_resultado(resultado)


if __name__ == "__main__":
    try:
        executar()
    except Exception as erro:
        print(f"Não foi possível calcular as comissões: {erro}")
