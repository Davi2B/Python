import customtkinter as ctk
import sqlite3
from tkinter import messagebox


def abrir_cadastro():

    janela = ctk.CTkToplevel()
    janela.title("Criar Conta")
    janela.geometry("500x600")
    janela.resizable(False, False)
    janela.configure(fg_color="#0d0d0d")

    titulo = ctk.CTkLabel(
        janela,
        text="CRIAR CONTA",
        font=("Arial", 30, "bold"),
        text_color="#ff1e1e"
    )
    titulo.pack(pady=40)

    nome = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="Nome completo"
    )
    nome.pack(pady=10)

    email = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="E-mail"
    )
    email.pack(pady=10)

    senha = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="Senha",
        show="*"
    )
    senha.pack(pady=10)

    confirmar = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="Confirmar senha",
        show="*"
    )
    confirmar.pack(pady=10)

    def cadastrar():

        n = nome.get().strip()
        e = email.get().strip()
        s = senha.get()
        c = confirmar.get()

        if not n or not e or not s or not c:
            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos."
            )
            return

        if s != c:
            messagebox.showerror(
                "Erro",
                "As senhas não são iguais."
            )
            return

        conn = sqlite3.connect("barbearia.db")
        cursor = conn.cursor()

        try:

            cursor.execute("""
                INSERT INTO usuarios
                (nome, email, senha)
                VALUES (?, ?, ?)
            """, (n, e, s))

            conn.commit()

            messagebox.showinfo(
                "Sucesso",
                "Conta criada com sucesso!"
            )

            janela.destroy()

        except sqlite3.IntegrityError:

            messagebox.showerror(
                "Erro",
                "Esse e-mail já está cadastrado."
            )

        conn.close()

    botao = ctk.CTkButton(
        janela,
        text="CRIAR CONTA",
        width=350,
        height=50,
        fg_color="#e50914",
        hover_color="#b20710",
        font=("Arial", 16, "bold"),
        command=cadastrar
    )

    botao.pack(pady=30)