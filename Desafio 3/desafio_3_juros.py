from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

CENTAVOS = Decimal("0.01")
MULTA_DIARIA = Decimal("0.025")


def converter_valor(texto):
    normalizado = texto.strip().replace("R$", "").replace(" ", "")
    if "," in normalizado:
        normalizado = normalizado.replace(".", "").replace(",", ".")

    try:
        valor = Decimal(normalizado)
    except InvalidOperation as erro:
        raise ValueError("Informe um valor monetário válido") from erro

    if valor <= 0:
        raise ValueError("O valor deve ser maior que zero")

    return valor.quantize(CENTAVOS, rounding=ROUND_HALF_UP)


def converter_data(texto):
    try:
        return datetime.strptime(texto.strip(), "%d/%m/%Y").date()
    except ValueError as erro:
        raise ValueError("Informe a data no formato dia, mês e ano") from erro


def calcular_multa(valor, vencimento, data_calculo=None):
    hoje = data_calculo or date.today()
    dias_atraso = (hoje - vencimento).days

    if dias_atraso <= 0:
        return {
            "dataCalculo": hoje,
            "diasAtraso": 0,
            "valorOriginal": valor,
            "valorMulta": Decimal("0.00"),
            "valorAtualizado": valor
        }

    multa = (valor * MULTA_DIARIA * Decimal(dias_atraso)).quantize(CENTAVOS, rounding=ROUND_HALF_UP)
    atualizado = (valor + multa).quantize(CENTAVOS, rounding=ROUND_HALF_UP)

    return {
        "dataCalculo": hoje,
        "diasAtraso": dias_atraso,
        "valorOriginal": valor,
        "valorMulta": multa,
        "valorAtualizado": atualizado
    }


def formatar_moeda(valor):
    texto = f"{valor:,.2f}"
    return "R$ " + texto.replace(",", "X").replace(".", ",").replace("X", ".")


def executar():
    valor = converter_valor(input("Valor original: "))
    vencimento = converter_data(input("Data de vencimento: "))
    resultado = calcular_multa(valor, vencimento)

    print()
    print("Cálculo da multa")
    print(f"Data do cálculo: {resultado['dataCalculo'].strftime('%d/%m/%Y')}")
    print(f"Dias de atraso: {resultado['diasAtraso']}")
    print(f"Valor original: {formatar_moeda(resultado['valorOriginal'])}")
    print(f"Valor da multa: {formatar_moeda(resultado['valorMulta'])}")
    print(f"Valor atualizado: {formatar_moeda(resultado['valorAtualizado'])}")


if __name__ == "__main__":
    try:
        executar()
    except Exception as erro:
        print(f"Não foi possível concluir o cálculo: {erro}")
