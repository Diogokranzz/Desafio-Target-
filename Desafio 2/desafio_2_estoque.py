from datetime import datetime
from pathlib import Path
from uuid import uuid4
import json


class GerenciadorEstoque:
    def __init__(self, caminho_estoque, caminho_movimentacoes):
        self.caminho_estoque = Path(caminho_estoque)
        self.caminho_movimentacoes = Path(caminho_movimentacoes)
        self.produtos = self._carregar_produtos()
        self.movimentacoes = self._carregar_movimentacoes()

    def _ler_json(self, caminho, valor_padrao):
        if not caminho.exists():
            return valor_padrao
        with caminho.open("r", encoding="utf8") as arquivo:
            return json.load(arquivo)

    def _gravar_json(self, caminho, dados):
        temporario = caminho.with_suffix(".tmp")
        with temporario.open("w", encoding="utf8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        temporario.replace(caminho)

    def _carregar_produtos(self):
        dados = self._ler_json(self.caminho_estoque, {"estoque": []})
        produtos = dados.get("estoque")
        if not isinstance(produtos, list):
            raise ValueError("O arquivo de estoque está inválido")
        return produtos

    def _carregar_movimentacoes(self):
        dados = self._ler_json(self.caminho_movimentacoes, [])
        if not isinstance(dados, list):
            raise ValueError("O arquivo de movimentações está inválido")
        return dados

    def listar_produtos(self):
        return sorted(self.produtos, key=lambda produto: produto["codigoProduto"])

    def localizar_produto(self, codigo):
        for produto in self.produtos:
            if produto.get("codigoProduto") == codigo:
                return produto
        raise ValueError("Produto não encontrado")

    def movimentar(self, codigo, tipo, quantidade, descricao):
        tipo_normalizado = tipo.strip().lower()
        descricao_normalizada = descricao.strip()

        if tipo_normalizado not in {"entrada", "saida"}:
            raise ValueError("O tipo deve ser entrada ou saida")
        if quantidade <= 0:
            raise ValueError("A quantidade deve ser maior que zero")
        if not descricao_normalizada:
            raise ValueError("A descrição da movimentação é obrigatória")

        produto = self.localizar_produto(codigo)
        estoque_anterior = int(produto["estoque"])
        variacao = quantidade if tipo_normalizado == "entrada" else quantidade * int("-1")
        estoque_final = estoque_anterior + variacao

        if estoque_final < 0:
            raise ValueError(f"Estoque insuficiente. Quantidade disponível: {estoque_anterior}")

        movimentacao = {
            "identificador": str(uuid4()),
            "dataHora": datetime.now().astimezone().isoformat(timespec="seconds"),
            "codigoProduto": codigo,
            "produto": produto["descricaoProduto"],
            "tipo": tipo_normalizado,
            "descricao": descricao_normalizada,
            "quantidade": quantidade,
            "estoqueAnterior": estoque_anterior,
            "estoqueFinal": estoque_final
        }

        produto["estoque"] = estoque_final
        self.movimentacoes.append(movimentacao)

        try:
            self._gravar_json(self.caminho_estoque, {"estoque": self.produtos})
            self._gravar_json(self.caminho_movimentacoes, self.movimentacoes)
        except Exception:
            produto["estoque"] = estoque_anterior
            self.movimentacoes.pop()
            raise

        return movimentacao


def ler_inteiro(mensagem):
    valor = input(mensagem).strip()
    try:
        return int(valor)
    except ValueError as erro:
        raise ValueError("Informe um número inteiro válido") from erro


def executar():
    diretorio = Path(__file__).parent
    gerenciador = GerenciadorEstoque(diretorio / "estoque.json", diretorio / "movimentacoes.json")

    print("Produtos disponíveis")
    for produto in gerenciador.listar_produtos():
        print(f"Código: {produto['codigoProduto']} | Produto: {produto['descricaoProduto']} | Estoque: {produto['estoque']}")

    print()
    codigo = ler_inteiro("Código do produto: ")
    tipo = input("Tipo da movimentação, entrada ou saida: ")
    quantidade = ler_inteiro("Quantidade: ")
    descricao = input("Descrição da movimentação: ")

    movimento = gerenciador.movimentar(codigo, tipo, quantidade, descricao)

    print()
    print("Movimentação concluída")
    print(f"Identificador: {movimento['identificador']}")
    print(f"Produto: {movimento['produto']}")
    print(f"Estoque anterior: {movimento['estoqueAnterior']}")
    print(f"Estoque final: {movimento['estoqueFinal']}")


if __name__ == "__main__":
    try:
        executar()
    except Exception as erro:
        print(f"Não foi possível realizar a movimentação: {erro}")
