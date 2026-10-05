# Desafios em Python

Projeto composto por três desafios independentes em Python, com foco em processamento de
dados, controle de estoque e cálculo financeiro. Cada desafio está em sua própria pasta
e pode ser executado separadamente.

## Requisitos

- Python 3.10 ou superior.
- PowerShell, Prompt de Comando ou outro terminal.
- Nenhuma biblioteca externa é necessária. Os programas utilizam apenas a biblioteca
  padrão do Python.

Para verificar a versão instalada:

```powershell
python --version
```

Se o comando `python` não estiver disponível, tente `py --version`.

## Estrutura do projeto

```text
D:\Testes Desafios\
├── INSTRUCOES.txt
├── readme.md
├── Desafio 1\
│   ├── desafio_1_comissoes.py
│   └── vendas.json
├── Desafio 2\
│   ├── desafio_2_estoque.py
│   ├── estoque.json
│   └── movimentacoes.json
└── Desafio 3\
    └── desafio_3_juros.py
```

O arquivo [INSTRUCOES.txt](./INSTRUCOES.txt) contém somente os comandos para abrir cada
pasta e executar cada desafio. Este README descreve o projeto e suas regras de negócio.

## Desafio 1 - Cálculo de comissões

### Objetivo do cálculo de comissões

Ler as vendas armazenadas em `vendas.json`, calcular a comissão de cada venda e
consolidar os resultados por vendedor.

### Entrada

O arquivo contém um objeto com a propriedade `vendas`, cujo valor é uma lista de
registros:

```json
{
  "vendedor": "João Silva",
  "valor": 1200.50
}
```

### Regras de comissão

| Valor da venda | Comissão |
| --- | ---: |
| Menor que R$ 100,00 | 0% |
| De R$ 100,00 até abaixo de R$ 500,00 | 1% |
| A partir de R$ 500,00 | 5% |

A comissão é calculada individualmente e depois os valores são agrupados por vendedor.
O resultado apresenta quantidade de vendas, total vendido e total de comissão, ordenado
por nome. Os cálculos usam `Decimal` e arredondamento comercial para centavos.

### Validações

- O arquivo deve existir e conter JSON válido.
- `vendas` deve ser uma lista.
- O vendedor deve ser um texto não vazio.
- O valor deve ser numérico e não negativo.

### Componentes

- `carregar_vendas`: lê e valida o JSON.
- `calcular_comissao`: aplica a faixa correspondente.
- `consolidar_comissoes`: consolida os resultados por vendedor.
- `formatar_moeda` e `exibir_resultado`: formatam e exibem o relatório.

## Desafio 2 - Controle de estoque

### Objetivo do controle de estoque

Permitir entradas e saídas de produtos, mantendo o saldo atual e um histórico completo
das operações.

### Arquivos de dados

`estoque.json` armazena os produtos:

```json
{
  "estoque": [
    {
      "codigoProduto": 101,
      "descricaoProduto": "Caneta Azul",
      "estoque": 150
    }
  ]
}
```

`movimentacoes.json` armazena o histórico:

```json
[
  {
    "identificador": "uuid",
    "dataHora": "2026-10-05T09:51:14-03:00",
    "codigoProduto": 101,
    "produto": "Caneta Azul",
    "tipo": "entrada",
    "descricao": "Reposição",
    "quantidade": 20,
    "estoqueAnterior": 150,
    "estoqueFinal": 170
  }
]
```

### Fluxo

O programa lista os produtos disponíveis e solicita o código do produto, o tipo
(`entrada` ou `saida`), a quantidade inteira e uma descrição. Entradas aumentam o saldo;
saídas reduzem o saldo.

### Regras e garantias

- O código deve corresponder a um produto cadastrado.
- O tipo deve ser `entrada` ou `saida`, sem distinção entre maiúsculas e minúsculas.
- A quantidade deve ser inteira e maior que zero.
- A descrição é obrigatória.
- Uma saída não pode deixar o estoque negativo.
- Cada movimentação recebe um UUID exclusivo e a data/hora local.
- O histórico registra estoque anterior e estoque final.
- Os JSONs são gravados por arquivo temporário e substituição.
- Se a gravação falhar, o estado em memória é revertido.

A classe `GerenciadorEstoque` carrega os dados, lista e localiza produtos, valida
movimentações e persiste as alterações nos dois arquivos.

## Desafio 3 - Cálculo de juros por atraso

### Objetivo do cálculo de juros

Calcular uma multa simples de 2,5% por dia de atraso sobre uma dívida.

### Entrada e fórmula

O programa solicita o valor original e a data de vencimento no formato `dd/mm/aaaa`.
O valor aceita formatos como `1000`, `1000,50` e `R$ 1.000,50`.

Quando há atraso:

```text
multa = valor original × 0,025 × dias de atraso
valor atualizado = valor original + multa
```

Multa e valor atualizado são arredondados para centavos com `ROUND_HALF_UP`. Se o
vencimento for hoje ou futuro, os dias de atraso e a multa serão zero.

### Resultado e validações

O programa exibe data do cálculo, dias de atraso, valor original, multa e valor
atualizado. O valor deve ser maior que zero e a data deve ser válida.

As funções `converter_valor`, `converter_data`, `calcular_multa` e `formatar_moeda`
separam conversão, validação, cálculo e apresentação.

## Organização técnica

Os programas utilizam:

- `pathlib.Path` para localizar arquivos;
- `json` para persistência;
- `Decimal` para cálculos monetários precisos;
- funções pequenas para conversão, validação e cálculo;
- tratamento de exceções no ponto de entrada;
- bloco `if __name__ == "__main__"` para execução direta.

Os desafios não compartilham estado. Alterações nos JSONs de um desafio não afetam os
demais.

## Execução

Os comandos completos estão em [INSTRUCOES.txt](./INSTRUCOES.txt). Resumo:

```powershell
cd "D:\Testes Desafios\Desafio 1"
python .\desafio_1_comissoes.py

cd "D:\Testes Desafios\Desafio 2"
python .\desafio_2_estoque.py

cd "D:\Testes Desafios\Desafio 3"
python .\desafio_3_juros.py
```

As aspas são necessárias porque os nomes das pastas contêm espaços.
