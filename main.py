# Importação da biblioteca tkinter
import tkinter as tk
from tkinter import ttk, font, messagebox
from tkinter import PhotoImage

# Configuração da Janela Principal
janela = tk.Tk()
janela.title("APP TASKS")
janela.configure(bg="#f0f0f0")
janela.geometry("550x600")

# Gerenciamento de tarefas
frame_em_edicao = None

def adicionar_tarefa():
    global frame_em_edicao
    tarefa = entrada_tarefa.get().strip()
    if tarefa and tarefa != "Escreva sua tarefa aqui":
        if frame_em_edicao is not None:
            atualizar_tarefa(tarefa)
            frame_em_edicao = None
        else:
            adicionar_item_tarefa(tarefa)
        entrada_tarefa.delete(0, tk.END)
    else:
        messagebox.showwarning("Entrada Inválida", "Digite uma tarefa válida!")

def adicionar_item_tarefa(tarefa):
    frame_tarefa = tk.Frame(canvas_interior, bg="white", bd= 3, relief= tk.SOLID)

    label_tarefa = tk.Label(frame_tarefa, text=tarefa, font=("Garamond", 16), bg="white", width=25, height=2, anchor="w")
    label_tarefa.pack(side=tk.LEFT, fill=tk.X, padx=10, pady=5)

    # Botão de Editar TASKS
    botao_editar = tk.Button(frame_tarefa, image=icon_editar, command=lambda f=frame_tarefa, l=label_tarefa: preparar_edicao(f, l), bg="white", relief=tk.FLAT)
    botao_editar.pack(side=tk.RIGHT, padx=5)

    # Botão de Deletar TASKS
    botao_deletar = tk.Button(frame_tarefa, image=icon_deletar, command=lambda: deletar_tarefa(frame_tarefa), bg="white", relief=tk.FLAT)
    botao_deletar.pack(side=tk.RIGHT, padx=5)

    # Botão Check Task
    checkbutton = ttk.Checkbutton(frame_tarefa, command=lambda label=label_tarefa: alternar_sublinhado(label))
    checkbutton.pack(side=tk.RIGHT, padx=5)

    frame_tarefa.pack(fill=tk.X, padx=10, pady=5)

    # Scroll
    canvas_interior.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def preparar_edicao(frame_tarefa, label_tarefa):
    global frame_em_edicao
    frame_em_edicao = frame_tarefa
    entrada_tarefa.delete(0, tk.END)
    entrada_tarefa.insert(0, label_tarefa["text"])

def atualizar_tarefa(nova_tarefa):
    if frame_em_edicao is not None:
        for widget in frame_em_edicao.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(text=nova_tarefa)

def deletar_tarefa(frame_tarefa):
    frame_tarefa.destroy()
    canvas_interior.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

def alternar_sublinhado(label):
    fonte_atual = font.Font(font=label.cget("font"))
    if fonte_atual.actual("underline"):
        fonte_atual.config(underline=0)
    else:
        fonte_atual.config(underline=1)
    label.config(font=fonte_atual)

# Entrada de tarefa
def entrada(event):
    if entrada_tarefa.get() == "Escreva sua tarefa aqui":
        entrada_tarefa.delete(0, tk.END)
        entrada_tarefa.configure(fg="black")

def saida(event):
    if not entrada_tarefa.get().strip():
        entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
        entrada_tarefa.configure(fg="grey")

# Carregar ícones
try:
    icon_editar = PhotoImage(file="editar.png").subsample(3, 3)
    icon_deletar = PhotoImage(file="deletar.png").subsample(3, 3)
except Exception:
    icon_editar = PhotoImage(width=1, height=1)  # Placeholder caso as imagens não sejam encontradas
    icon_deletar = PhotoImage(width=1, height=1)

# Criar uma fonte para o cabeçalho
fonte_cabecalho = font.Font(family="Arial", size=24, weight="bold")

# Criar um rótulo de cabeçalho
rotulo_cabecalho = tk.Label(janela, text="APP TASKS", font=fonte_cabecalho, bg="#f0f0f0")
rotulo_cabecalho.pack(pady=20)

# Frame para entrada e botão de adicionar
frame = tk.Frame(janela, bg="#F0F0F0")
frame.pack(pady=10)

entrada_tarefa = tk.Entry(frame, font=("Garamond", 14), relief=tk.FLAT, bg="white", fg="grey", width=30)
entrada_tarefa.insert(0, "Escreva sua tarefa aqui")
entrada_tarefa.bind("<FocusIn>", entrada)
entrada_tarefa.bind("<FocusOut>", saida)
entrada_tarefa.pack(side=tk.LEFT, padx=10)

botao_adicionar = tk.Button(frame, text="Adicionar Tarefa", command=adicionar_tarefa, bg="#4CAF50", fg="white", height=1, width=15, font=("Arial", 12), relief=tk.FLAT)
botao_adicionar.pack(side=tk.LEFT, padx=10)

# Criar a lista de tarefas com barra de rolagem
frame_lista_tarefas = tk.Frame(janela, bg="white")
frame_lista_tarefas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(frame_lista_tarefas, bg="white")
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_lista_tarefas, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)
canvas_interior = tk.Frame(canvas, bg="white")
canvas.create_window((0, 0), window=canvas_interior, anchor="nw")
canvas_interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Rodapé
janela.mainloop()
