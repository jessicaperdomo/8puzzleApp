import buscas
import tkinter as tk
import random
from tkinter import messagebox

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Game")
        self.root.geometry("600x600")
        self.root.eval('tk::PlaceWindow . center')

        self.initial_board_frame = tk.Frame(self.root)
        self.initial_board_frame.grid(row=0, column=0, padx=20, pady=20)

        self.final_board_frame = tk.Frame(self.root)
        self.final_board_frame.grid(row=0, column=1, padx=20, pady=20)

        self.board = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]

        self.final_state = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]

        self.final_state = []
        self.selected_pieces = []
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.final_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.solution_steps = []
        self.tempo_gasto = 0
        self.quantidade_de_passos = 0
        self.nos_visitados = 0
        self.solution_buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_step = 0

        self.criar_ini()
        self.criar_final()

        button_frame = tk.Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        shuffle_button = tk.Button(button_frame, text="Embaralhar", command=self.embaralha, bg="lightyellow")
        shuffle_button.grid(row=0, column=0, padx=5)

        set_final_button = tk.Button(button_frame, text="Definir Estado Final", command=self.estado_final, bg="lightyellow")
        set_final_button.grid(row=1, column=0, padx=5)

        options_frame = tk.Frame(button_frame)
        options_frame.grid(row=2, column=0, padx=5, sticky='w')

        self.search_type_var = tk.StringVar(value="A*")
        search_type_label = tk.Label(options_frame, text="Escolher Tipo de Busca:", bg="lightyellow")
        search_type_label.grid(row=0, column=0, sticky='w')

        search_type_menu = tk.OptionMenu(options_frame, self.search_type_var,
                                         "Hill Climbing", "A*")
        search_type_menu.grid(row=0, column=1)

        self.level_var = tk.StringVar(value="1º Nível")
        level_label = tk.Label(options_frame, text="Escolher Nível:", bg="lightyellow")
        level_label.grid(row=1, column=0, sticky='w')

        level_frame = tk.Frame(options_frame)
        level_frame.grid(row=1, column=1)

        level1_radio = tk.Radiobutton(level_frame, text="1º Nível", variable=self.level_var, value="1º Nível")
        level1_radio.pack(side=tk.LEFT)

        level2_radio = tk.Radiobutton(level_frame, text="2º Nível", variable=self.level_var, value="2º Nível")
        level2_radio.pack(side=tk.LEFT)

        show_solution_button = tk.Button(button_frame, text="Mostrar Solução", command=self.mostrar_solucao, bg="lightblue")
        show_solution_button.grid(row=3, column=0, padx=5, pady=(10, 0))

        clear_final_button = tk.Button(button_frame, text="Limpar Estado Final", command=self.limpar_estado_final,
                                       bg="lightyellow")
        clear_final_button.grid(row=4, column=0, padx=5, pady=(10, 0))

    def criar_ini(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    self.buttons[i][j] = tk.Button(
                        self.initial_board_frame,
                        text=str(self.board[i][j]),
                        font=('Helvetica', 20),
                        width=4, height=2,
                        command=lambda i=i, j=j: self.mover(i, j)
                    )
                    self.buttons[i][j].grid(row=i, column=j)
                else:
                    self.buttons[i][j] = tk.Button(
                        self.initial_board_frame,
                        text="",
                        font=('Helvetica', 20),
                        width=4, height=2,
                        state='disabled'
                    )
                    self.buttons[i][j].grid(row=i, column=j)

    def criar_final(self):
        for i in range(3):
            for j in range(3):
                self.final_buttons[i][j] = tk.Button(
                    self.final_board_frame,
                    text="",
                    font=('Helvetica', 20),
                    width=4, height=2,
                    state='normal',
                    command=lambda i=i, j=j: self.selecionar_peca(i, j)
                )
                self.final_buttons[i][j].grid(row=i, column=j)

    def mover(self, i, j):
        messagebox.showinfo("Move", f"Move peça em ({i},{j})")

    def embaralha(self):
        while True:
            flattened_board = [num for row in self.board for num in row]
            random.shuffle(flattened_board)

            inversions = 0
            for i in range(len(flattened_board)):
                for j in range(i + 1, len(flattened_board)):
                    if flattened_board[i] != 0 and flattened_board[j] != 0 and flattened_board[i] > flattened_board[j]:
                        inversions += 1

            if inversions % 2 == 0:
                break

        for i in range(3):
            for j in range(3):
                self.board[i][j] = flattened_board.pop(0)

        self.update_ini()

    def limpar_estado_final(self):
        self.final_state = [[0, 0, 0] for _ in range(3)]
        self.selected_pieces.clear()
        self.update_final()

        for i in range(3):
            for j in range(3):
                self.final_buttons[i][j].config(state='normal')

    def update_ini(self):
        for i in range(3):
            for j in range(3):
                if self.board[i][j] != 0:
                    self.buttons[i][j].config(text=str(self.board[i][j]), state='normal')
                else:
                    self.buttons[i][j].config(text="", state='disabled')

    def contar_inversoes(self, matriz):
        """Conta o número de inversões na matriz."""
        flattened = [num for row in matriz for num in row if num != 0]
        inversoes = 0
        for i in range(len(flattened)):
            for j in range(i + 1, len(flattened)):
                if flattened[i] > flattened[j]:
                    inversoes += 1
        return inversoes

    def estado_final(self):
        self.final_state.clear()
        messagebox.showinfo("Estado Final", "Clique nas posições do tabuleiro final para definir os números (1-8).")

        if self.final_state:
            inversoes = self.contar_inversoes(self.final_state)
            if inversoes % 2 != 0:
                messagebox.showwarning("Estado Final Inválido", "O estado final não tem solução (inversões ímpares).")
                self.final_state = []
                self.update_final()

    def selecionar_peca(self, i, j):
        if len(self.final_state) < 8:
            if self.final_buttons[i][j]['text'] == "":
                piece_window = tk.Toplevel(self.root)
                piece_window.title("Escolher Peça")
                piece_window.geometry("400x200")

                frame1 = tk.Frame(piece_window)
                frame1.pack(pady=10)

                for num in range(1, 5):
                    piece_button = tk.Button(frame1,
                                             text=str(num),
                                             font=('Helvetica', 20),
                                             width=4, height=2,
                                             command=lambda num=num, i=i, j=j: self.colocar_peca(num, i, j,
                                                                                                 piece_window),
                                             bg="lightblue")
                    piece_button.pack(side=tk.LEFT, padx=5)

                frame2 = tk.Frame(piece_window)
                frame2.pack(pady=10)
                for num in range(5, 9):
                    piece_button = tk.Button(frame2,
                                             text=str(num),
                                             font=('Helvetica', 20),
                                             width=4, height=2,
                                             command=lambda num=num, i=i, j=j: self.colocar_peca(num, i, j,
                                                                                                 piece_window),
                                             bg="lightblue")
                    piece_button.pack(side=tk.LEFT, padx=5)

                close_button = tk.Button(piece_window, text="Fechar", command=piece_window.destroy)
                close_button.pack(pady=10)

    def colocar_peca(self, num, i, j, piece_window):
        if num not in self.selected_pieces:
            self.selected_pieces.append(num)
            self.final_buttons[i][j].config(text=str(num))

            if len(self.final_state) < 3:
                self.final_state.append([0, 0, 0])

            self.final_state[i][j] = num

            piece_window.destroy()
            self.desabilita_selecionada(num)

            if len(self.selected_pieces) == 8:
                messagebox.showinfo("Estado Final", "Estado final definido com sucesso!")
                self.update_final()

                inversoes = self.contar_inversoes(self.final_state)
                if inversoes % 2 != 0:
                    messagebox.showwarning("Estado Final Inválido",
                                           "O estado final não tem solução (inversões ímpares).")
                    self.final_state = []
                    self.update_final()

    def desabilita_selecionada(self, num):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") == str(num):
                widget.config(state='disabled')

    def update_final(self):
        for i in range(3):
            for j in range(3):
                self.final_buttons[i][j].config(text=str(self.final_state[i][j]) if self.final_state[i][j] != 0 else "",
                                                state='disabled' if self.final_state[i][j] == 0 else 'normal')

    def mostrar_solucao(self):
        self.processar()

        if self.solution_steps:
            self.solucao()
        else:
            messagebox.showwarning("Solução Não Encontrada", "Não foi possível encontrar uma solução.")

    def solucao(self):
        solution_window = tk.Toplevel(self.root)
        solution_window.title("Solução do Jogo")
        solution_window.geometry("600x600")

        solution_frame = tk.Frame(solution_window)
        solution_frame.pack(pady=10)

        self.solution_buttons = [[None for _ in range(3)] for _ in range(3)]

        for i in range(3):
            for j in range(3):
                button = tk.Button(solution_frame,
                                   text=str(self.final_buttons[i][j]['text']) if self.final_buttons[i][j][
                                                                                     'text'] != "" else "",
                                   font=('Helvetica', 20),
                                   width=4, height=2,
                                   state='disabled')
                button.grid(row=i, column=j)
                self.solution_buttons[i][j] = button

        nav_frame = tk.Frame(solution_window)
        nav_frame.pack(pady=10)

        self.previous_button = tk.Button(nav_frame, text="Anterior", command=lambda: self.navegar_solucao(-1),
                                         state='disabled')
        self.previous_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(nav_frame, text="Próximo",
                                     command=lambda: self.navegar_solucao(1) if self.current_step < len(
                                         self.solution_steps) - 1 else None)
        self.next_button.pack(side=tk.LEFT)

        if len(self.solution_steps) > 1:
            self.next_button.config(state='normal')

        info_frame = tk.Frame(solution_window)
        info_frame.pack(pady=20)

        self.passos_label = tk.Label(info_frame, text=f"Passos: {self.current_step}/{self.quantidade_de_passos}",
                                     font=("Arial", 12), fg="blue")
        self.passos_label.pack(pady=5)

        nos_visitados_label = tk.Label(info_frame, text=f"Nós Visitados: {self.nos_visitados}", font=("Arial", 12),
                                       fg="blue")
        nos_visitados_label.pack(pady=5)

        tempo_label = tk.Label(info_frame, text=f"Tempo Gasto: {self.tempo_gasto:.24f} segundos", font=("Arial", 12),
                               fg="blue")
        tempo_label.pack(pady=5)

        self.atualizar_botoes_solucao()

    def navegar_solucao(self, direction):
        self.current_step += direction
        self.atualizar_botoes_solucao()

        if self.current_step == 0:
            self.previous_button.config(state='disabled')
        else:
            self.previous_button.config(state='normal')

        if self.current_step == len(self.solution_steps) - 1:
            self.next_button.config(state='disabled')
        else:
            self.next_button.config(state='normal')

        self.passos_label.config(text=f"Passos: {self.current_step}/{self.quantidade_de_passos}")

    def atualizar_botoes_solucao(self):
        if self.solution_steps:
            for i in range(3):
                for j in range(3):
                    text_value = str(self.solution_steps[self.current_step][i][j]) if \
                    self.solution_steps[self.current_step][i][j] != 0 else ""
                    self.solution_buttons[i][j].config(text=text_value)

    def processar(self):
        ini_matrix = [row[:] for row in self.board]
        final_matrix = self.final_state.copy()
        tipo = self.search_type_var.get()
        nivel = self.level_var.get()

        resultado = buscas.processar_busca(ini_matrix, final_matrix, tipo, nivel)

        self.solution_steps = resultado.get("solucao_encontrada", [])
        self.tempo_gasto = resultado.get("tempo_gasto", 0)
        self.quantidade_de_passos = resultado.get("quantidade_de_passos", 0)
        self.nos_visitados = resultado.get("nos_visitados", 0)
        self.formatar_solucao_steps()
        self.current_step = 0

    def formatar_solucao_steps(self):
        formatted_steps = []
        for step in self.solution_steps:
            matriz = [step[i:i + 3] for i in range(0, len(step), 3)]
            formatted_steps.append(matriz)
        self.solution_steps = formatted_steps

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()
