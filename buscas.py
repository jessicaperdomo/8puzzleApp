import Aestrela1nivel
import Aestrela2niveis
import Hill1nivel
import Hill2niveis

def processar_busca(ini_matrix, final_matrix, tipo, nivel):
    matriz_inicial = transformar_matriz_para_lista(ini_matrix)
    matriz_final = transformar_matriz_para_lista(final_matrix)

    if tipo == "A*":
        if nivel == "1º Nível":
            busca = Aestrela1nivel.BuscaAEstrela()
            passos = busca.encontrar_solucao(matriz_inicial, matriz_final)
        elif nivel == "2º Nível":
            busca = Aestrela2niveis.BuscaAEstrelaDoisNiveis()
            passos = busca.encontrar_solucao(matriz_inicial, matriz_final)
    elif tipo == "Hill Climbing":
        if nivel == "1º Nível":
            busca = Hill1nivel.BuscaHillClimbing()
            passos = busca.encontrar_solucao(matriz_inicial, matriz_final)
        elif nivel == "2º Nível":
            busca = Hill2niveis.BuscaHillClimbing()
            passos = busca.encontrar_solucao(matriz_inicial, matriz_final)
    return passos

def transformar_matriz_para_lista(matriz):
    return [numero for linha in matriz for numero in linha]

