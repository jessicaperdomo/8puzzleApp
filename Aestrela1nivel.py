from queue import PriorityQueue
import time

class Estado:
    def __init__(self, matriz, custo, caminho):
        self.matriz = matriz
        self.custo = custo
        self.caminho = caminho

    def __lt__(self, other):
        return self.custo < other.custo

class BuscaAEstrela:
    def __init__(self):
        self.movimentos_permitidos = [
            [1, 3],
            [0, 2, 4],
            [1, 5],
            [0, 4, 6],
            [1, 3, 5, 7],
            [2, 4, 8],
            [3, 7],
            [4, 6, 8],
            [5, 7]
        ]

    def encontrar_solucao(self, matriz_inicial, matriz_final):
        start_time = time.time()
        caminhos = self.busca_a_estrela(matriz_inicial, matriz_final)
        tempo_gasto = time.time() - start_time

        return {
            "solucao_encontrada": caminhos["caminhos_percorridos"],
            "quantidade_de_passos": len(caminhos["caminhos_percorridos"]) - 1,
            "tempo_gasto": tempo_gasto,
            "nos_visitados": caminhos["nos_visitados"],
            "nos_gerados": caminhos["nos_gerados"]
        }

    def busca_a_estrela(self, estado_inicial, estado_final):
        fila = PriorityQueue()
        fila.put(Estado(estado_inicial, 0, [estado_inicial]))
        achou = False
        caminhos_percorridos = []
        nos_visitados = 0
        nos_gerados = 0

        while not fila.empty() and not achou:
            estado = fila.get()
            nos_visitados += 1

            if estado.matriz == estado_final:
                caminhos_percorridos = estado.caminho
                achou = True
                break

            possibilidades = self.obter_possibilidades(estado.matriz, estado.caminho)
            possibilidades = self.obter_soma_das_distancias_manhattan(possibilidades, estado_final)

            for poss in possibilidades:
                fila.put(poss)
                nos_gerados += 1

        return {
            "caminhos_percorridos": caminhos_percorridos,
            "nos_visitados": nos_visitados,
            "nos_gerados": nos_gerados
        }

    def obter_possibilidades(self, estado_atual, caminho_percorridos):
        indice_caixa_vazia = estado_atual.index(0)
        possibilidades = []

        for movimento in self.movimentos_permitidos[indice_caixa_vazia]:
            estado_aux = estado_atual[:]
            estado_aux[indice_caixa_vazia], estado_aux[movimento] = estado_aux[movimento], estado_aux[indice_caixa_vazia]

            if not self.visitou(estado_aux, caminho_percorridos):
                caminhos = caminho_percorridos + [estado_aux]
                possibilidades.append(Estado(estado_aux, 0, caminhos))

        return possibilidades

    def visitou(self, estado_atual, caminho_percorridos):
        return any(caminho == estado_atual for caminho in caminho_percorridos)

    def obter_soma_das_distancias_manhattan(self, possibilidades, estado_final):
        for poss in possibilidades:
            poss.custo = self.calcular_soma_das_distancias_manhattan(poss.matriz, estado_final)
        return possibilidades

    def calcular_soma_das_distancias_manhattan(self, possibilidade, estado_final):
        soma_das_distancias = 0

        for i in range(len(estado_final)):
            if possibilidade[i] != 0:
                posicao = estado_final.index(possibilidade[i])
                x1, y1 = divmod(i, 3)
                x2, y2 = divmod(posicao, 3)
                soma_das_distancias += abs(x2 - x1) + abs(y2 - y1)

        return soma_das_distancias

if __name__ == "__main__":
    matriz_inicial = [1, 2, 3, 0, 4, 5, 6, 7, 8]
    matriz_final = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    busca = BuscaAEstrela()
    resultado = busca.encontrar_solucao(matriz_inicial, matriz_final)
    print(f"Solução Encontrada: {resultado['solucao_encontrada']}")
    print(f"Quantidade de Passos: {resultado['quantidade_de_passos']}")
    print(f"Tempo Gasto: {resultado['tempo_gasto']} segundos")
