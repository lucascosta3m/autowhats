# DESENVOLVIDO POR LUCAS COSTA #

import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Criar variável global para o WebDriver
driver = None

# Conectar ao banco de dados SQLite e criar a tabela se necessário
banco_dados = "contatos.db"
conn = sqlite3.connect(banco_dados)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS contatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cidade TEXT,
    nome TEXT,
    telefone TEXT,
    mensagem TEXT
)
''')
conn.commit()
conn.close()

# Função para carregar contatos do banco de dados
def carregar_contatos():
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()
    cursor.execute("SELECT id, cidade, nome, telefone, mensagem FROM contatos")
    contatos = [{"ID": row[0], "Cidade": row[1], "Nome": row[2], "Telefone": row[3], "Mensagem": row[4]} for row in cursor.fetchall()]
    conn.close()
    return contatos

# Função para adicionar um novo contato
def adicionar_contato():
    def adicionar():
        nova_cidade = cidade_entry.get()
        novo_nome = nome_entry.get()
        novo_telefone = telefone_entry.get()
        nova_mensagem = mensagem_entry.get("1.0", tk.END).strip()

        if nova_cidade and novo_nome and novo_telefone and nova_mensagem:
            conn = sqlite3.connect(banco_dados)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO contatos (cidade, nome, telefone, mensagem) VALUES (?, ?, ?, ?)",
                           (nova_cidade, novo_nome, novo_telefone, nova_mensagem))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Contato adicionado com sucesso!")
            atualizar_interface()
            janela_adicionar.destroy()

    janela_adicionar = tk.Toplevel(root)
    janela_adicionar.title("Adicionar Contato")

    tk.Label(janela_adicionar, text="Cidade:").pack()
    cidade_entry = tk.Entry(janela_adicionar)
    cidade_entry.pack()

    tk.Label(janela_adicionar, text="Nome:").pack()
    nome_entry = tk.Entry(janela_adicionar)
    nome_entry.pack()

    tk.Label(janela_adicionar, text="Telefone (com DDD):").pack()
    telefone_entry = tk.Entry(janela_adicionar)
    telefone_entry.pack()

    tk.Label(janela_adicionar, text="Mensagem padrão:").pack()
    mensagem_entry = tk.Text(janela_adicionar, height=5, width=30)
    mensagem_entry.pack()

    tk.Button(janela_adicionar, text="Adicionar", command=adicionar).pack()

# Função para excluir um contato
def excluir_contato():
    contato_id = simpledialog.askinteger("Excluir Contato", "Digite o ID do contato a ser excluído:")
    
    if contato_id:
        conn = sqlite3.connect(banco_dados)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contatos WHERE id = ?", (contato_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sucesso", "Contato excluído com sucesso!")
        atualizar_interface()

# Criar a janela principal
root = tk.Tk()
root.title("AutoWhats - Envio de mensagens automáticas no WhatsApp")
root.geometry("700x550")

# Criar um frame principal
main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Criar um Canvas para conter os contatos
canvas = tk.Canvas(main_frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Criar uma barra de rolagem
scrollbar = tk.Scrollbar(main_frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrollbar = tk.Scrollbar(main_frame, orient=tk.HORIZONTAL, command=canvas.xview, width=20)
scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

canvas.configure(yscrollcommand=scrollbar.set)

frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Configurar o Canvas para rolar com o Frame interno
frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))

# Adicionar evento de rolagem do mouse
def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

canvas.bind_all("<MouseWheel>", _on_mousewheel)

checkbox_vars = []
colunas = 6

# Atualizar a interface ao adicionar ou excluir contatos
def atualizar_interface():
    global checkbox_vars
    for widget in frame.winfo_children():
        widget.destroy()

    checkbox_vars = []
    contatos = carregar_contatos()
    contatos_por_cidade = {}

    for contato in contatos:
        cidade = contato.get("Cidade", "Outros")
        if cidade not in contatos_por_cidade:
            contatos_por_cidade[cidade] = []
        contatos_por_cidade[cidade].append(contato)

    for cidade, lista_contatos in contatos_por_cidade.items():
        tk.Label(frame, text=f" {cidade}", font=("Arial", 10, "bold")).pack(anchor="w", pady=(10, 2))

        sub_frame = tk.Frame(frame)
        sub_frame.pack(anchor="w")

        for index, contato in enumerate(lista_contatos):
            var = tk.BooleanVar(value=False)
            chk = tk.Checkbutton(sub_frame, text=f"[ID: {contato['ID']}] {contato['Nome']} ({contato['Telefone']})", variable=var)

            linha = index // colunas
            coluna = index % colunas

            chk.grid(row=linha, column=coluna, sticky="w", padx=5, pady=2)
            checkbox_vars.append((var, contato))

    # Atualizar a região de rolagem do Canvas
    frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))

atualizar_interface()

# Função para selecionar todos os contatos
def selecionar_todos():
    for var, _ in checkbox_vars:
        var.set(True)

# Função para desmarcar todos os contatos
def desmarcar_todos():
    for var, _ in checkbox_vars:
        var.set(False)

botoes_frame = tk.Frame(root)
botoes_frame.pack(pady=5)

btn_selecionar_todos = tk.Button(botoes_frame, text="Selecionar Todos", command=selecionar_todos, bg="blue", fg="white")
btn_selecionar_todos.pack(side=tk.LEFT, padx=5)

btn_desmarcar_todos = tk.Button(botoes_frame, text="Desmarcar Todos", command=desmarcar_todos, bg="red", fg="white")
btn_desmarcar_todos.pack(side=tk.LEFT, padx=5)

btn_adicionar = tk.Button(botoes_frame, text="Adicionar Contato", command=adicionar_contato, bg="green", fg="white")
btn_adicionar.pack(side=tk.LEFT, padx=5)

btn_excluir = tk.Button(botoes_frame, text="Excluir Contato", command=excluir_contato, bg="darkred", fg="white")
btn_excluir.pack(side=tk.LEFT, padx=5)

mensagem_entry = tk.Text(root, height=5, width=50)
mensagem_entry.pack(pady=5)


# Função para enviar mensagens
def enviar_mensagens():
    global driver
    contatos_selecionados = [contato for var, contato in checkbox_vars if var.get()]

    if not contatos_selecionados:
        messagebox.showwarning("Aviso", "Selecione pelo menos um contato!")
        return

    mensagem_padrao = mensagem_entry.get("1.0", tk.END).strip()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://web.whatsapp.com/")

    messagebox.showinfo("Atenção", "Faça login no WhatsApp Web e pressione OK para continuar.")

    for contato in contatos_selecionados:
        mensagem = mensagem_padrao if mensagem_padrao else contato["Mensagem"]
        url = f"https://web.whatsapp.com/send?phone={contato['Telefone']}&text={mensagem}"
        driver.get(url)
        try:
            input_box = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
            )
            input_box.send_keys(Keys.ENTER)
            time.sleep(2)
        except Exception as e:
            print(f"Erro ao enviar mensagem para {contato['Nome']}: {e}")
        time.sleep(3)

    driver.quit()
    messagebox.showinfo("Concluído", "Mensagens enviadas com sucesso!")

botao_enviar = tk.Button(root, text="Enviar Mensagens", command=enviar_mensagens, bg="green", fg="white")
botao_enviar.pack(pady=10)

# LUCAS COSTA
label = tk.Label(root, text='Desenvolvido por Lucas Costa')
label.pack()

root.mainloop()