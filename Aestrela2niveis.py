import time
from queue import PriorityQueue

class EstadoA:
    def __init__(self, matriz, custo, caminhos):
        self.matriz = matriz
        self.custo = custo
        self.caminhos = caminhos

    def __lt__(self, other):
        return self.custo < other.custo

class BuscaAEstrelaDoisNiveis:
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

        resultado = self.busca_a_estrela_dois_niveis(matriz_inicial, matriz_final)

        elapsed_time = time.time() - start_time
        resultado['tempo_gasto'] = elapsed_time
        return resultado

    def busca_a_estrela_dois_niveis(self, estado_inicial, estado_final):
        fila = PriorityQueue()
        fila.put(EstadoA(estado_inicial, 0, [estado_inicial]))
        achou = False
        caminhos_percorridos = []
        nos_visitados = 0

        while not fila.empty() and not achou:
            estado = fila.get()
            ultimo_estado = estado.matriz
            caminhos_percorridos.append(estado.caminhos[-1])
            nos_visitados += 1

            if ultimo_estado != estado_final:
                possibilidades = self.obter_possibilidades(ultimo_estado, estado.caminhos)
                possibilidades = self.calcular_segundo_nivel(possibilidades, estado_final)

                for poss in possibilidades:
                    fila.put(poss)
            else:
                caminhos_percorridos.clear()
                caminhos_percorridos.extend(estado.caminhos)
                achou = True

            if fila.qsize() > 100000:
                return {'solucao_encontrada': [], 'quantidade_de_passos': 0, 'tempo_gasto': 0, 'nos_visitados': nos_visitados}

        return {
            'solucao_encontrada': caminhos_percorridos,
            'quantidade_de_passos': len(caminhos_percorridos)-1,
            'nos_visitados': nos_visitados
        }

    def obter_possibilidades(self, estado_atual, caminho_percorridos):
        indice_caixa_vazia = self.obter_indice_da_caixa_vazia(estado_atual)
        possibilidades = []

        for movimento in self.movimentos_permitidos[indice_caixa_vazia]:
            estado_aux = estado_atual[:]
            estado_aux[indice_caixa_vazia], estado_aux[movimento] = estado_aux[movimento], estado_aux[
                indice_caixa_vazia]

            if not self.visitou(estado_aux, caminho_percorridos):
                caminhos = caminho_percorridos[:] + [estado_aux]
                possibilidades.append(EstadoA(estado_aux, 0, caminhos))

        return possibilidades

    def visitou(self, estado_atual, caminho_percorridos):
        return any(caminho == estado_atual for caminho in caminho_percorridos)

    def obter_indice_da_caixa_vazia(self, estado_atual):
        return estado_atual.index(0)

    def calcular_soma_das_distancias_manhattan(self, possibilidade, estado_final):
        soma_das_distancias = 0

        for i in range(len(estado_final)):
            if possibilidade[i] != 0:
                posicao = estado_final.index(possibilidade[i])
                x1, y1 = divmod(i, 3)
                x2, y2 = divmod(posicao, 3)
                soma_das_distancias += abs(x2 - x1) + abs(y2 - y1)

        return soma_das_distancias

    def obter_soma_das_distancias_manhattan(self, possibilidades, estado_final):
        for poss in possibilidades:
            poss.custo = self.calcular_soma_das_distancias_manhattan(poss.matriz, estado_final)
        return possibilidades

    def calcular_segundo_nivel(self, possibilidades, estado_final):
        for possibilidade in possibilidades:
            possibilidades_aux = self.obter_possibilidades(possibilidade.matriz, possibilidade.caminhos)

            if not possibilidades_aux:
                possibilidade.custo = float('inf')
                continue

            possibilidades_aux = self.obter_soma_das_distancias_manhattan(possibilidades_aux, estado_final)
            menor_custo = min(possibilidade.custo for possibilidade in possibilidades_aux)
            possibilidade.custo = menor_custo
        return possibilidades


if __name__ == "__main__":
    estado_inicial = [1, 2, 3, 4, 0, 5, 7, 8, 6]
    estado_final = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    busca = BuscaAEstrelaDoisNiveis()
    resultado = busca.encontrar_solucao(estado_inicial, estado_final)

    print(f"Solução encontrada: {resultado['solucao_encontrada']}")
    print(f"Quantidade de passos: {resultado['quantidade_de_passos']}")
    print(f"Tempo gasto: {resultado['tempo_gasto']:.24f} segundos")
    print(f"Nós: {resultado['nos_visitados']}")
