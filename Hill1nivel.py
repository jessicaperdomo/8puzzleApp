import time

class Estado:
    def __init__(self, matriz, custo):
        self.matriz = matriz
        self.custo = custo

class BuscaHillClimbing:
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

    def encontrar_solucao(self, estado_inicial, estado_final):
        start_time = time.time()
        numeros_de_pecas_fora_do_lugar = self.numeros_de_pecas_fora_do_lugar(estado_inicial, estado_final)

        if numeros_de_pecas_fora_do_lugar == 0:
            elapsed_time = time.time() - start_time
            return {
                'quantidade_de_passos': 0,
                'solucao_encontrada': estado_final,
                'tempo_gasto': elapsed_time,
                'nos_visitados': 0
            }
        else:
            return self.busca_hill_climbing(estado_inicial, estado_final, start_time)

    def busca_hill_climbing(self, estado_inicial, estado_final, start_time):
        estados_percorridos = []
        pilha = []
        custo = self.numeros_de_pecas_fora_do_lugar(estado_inicial, estado_final)

        pilha.append(Estado(estado_inicial, custo))
        estados_percorridos.append(estado_inicial)

        passos = 0
        nos_visitados = 0
        while pilha:
            estado = pilha.pop()
            caminho_percorrido = estado.matriz

            if estado.custo == 0:
                tempo_gasto = time.time() - start_time
                return {
                    "solucao_encontrada": estados_percorridos,
                    "quantidade_de_passos": passos,
                    "tempo_gasto": tempo_gasto,
                    "nos_visitados": nos_visitados
                }

            menor_custo = float('inf')
            melhor_possibilidade = None
            possibilidades = self.obter_possibilidades(caminho_percorrido)

            for possibilidade in possibilidades:
                custo = self.numeros_de_pecas_fora_do_lugar(possibilidade, estado_final)

                if possibilidade not in estados_percorridos:
                    if custo < menor_custo:
                        menor_custo = custo
                        melhor_possibilidade = possibilidade
                    elif custo == menor_custo:
                        if (self.obter_soma_das_distancias_manhattan(possibilidade, estado_final) <
                                self.obter_soma_das_distancias_manhattan(melhor_possibilidade, estado_final)):
                            melhor_possibilidade = possibilidade

            passos += 1

            if melhor_possibilidade is not None:
                estados_percorridos.append(melhor_possibilidade)
                pilha.append(Estado(melhor_possibilidade, menor_custo))
                nos_visitados += 1

                if passos > 10000:
                    return {
                        "solucao_encontrada": None,
                        "quantidade_de_passos": None,
                        "tempo_gasto": 0,
                        "nos_visitados": nos_visitados
                    }

        tempo_gasto = time.time() - start_time
        return {
            "solucao_encontrada": estados_percorridos,
            "quantidade_de_passos": passos,
            "tempo_gasto": tempo_gasto,
            "nos_visitados": nos_visitados
        }

    def numeros_de_pecas_fora_do_lugar(self, estado_inicial, estado_final):
        return sum(1 for i in range(len(estado_inicial)) if estado_inicial[i] != estado_final[i])

    def obter_possibilidades(self, estado_atual):
        indice_caixa_vazia = self.obter_indice_da_caixa_vazia(estado_atual)
        possibilidades = []

        for movimento in self.movimentos_permitidos[indice_caixa_vazia]:
            estado_aux = estado_atual[:]
            estado_aux[indice_caixa_vazia], estado_aux[movimento] = estado_aux[movimento], estado_aux[indice_caixa_vazia]
            possibilidades.append(estado_aux)

        return possibilidades

    def obter_indice_da_caixa_vazia(self, estado_atual):
        return estado_atual.index(0)

    def obter_soma_das_distancias_manhattan(self, estado_atual, estado_final):
        soma_das_distancias = 0
        for i, numero in enumerate(estado_atual):
            if numero != 0:
                posicao_final = estado_final.index(numero)
                x1, y1 = divmod(i, 3)
                x2, y2 = divmod(posicao_final, 3)
                soma_das_distancias += abs(x2 - x1) + abs(y2 - y1)
        return soma_das_distancias

if __name__ == "__main__":
    matriz_inicial = [1, 2, 3, 0, 4, 5, 6, 7, 8]
    matriz_final = [1, 2, 3, 4, 5, 6, 7, 8, 0]

    busca = BuscaHillClimbing()
    resultado = busca.encontrar_solucao(matriz_inicial, matriz_final)
    print(f"Solução Encontrada: {resultado['solucao_encontrada']}")
    print(f"Quantidade de Passos: {resultado['quantidade_de_passos']}")
    print(f"Tempo Gasto: {resultado['tempo_gasto']} segundos")
    print(f"Nós: {resultado['nos_visitados']}")
