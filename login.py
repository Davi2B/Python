import customtkinter as ctk
import sqlite3
from tkinter import messagebox

from cadastro import abrir_cadastro
from agendamento import abrir_agendamento


def abrir_login():

    janela = ctk.CTk()

    janela.title("Barbearia Black - Login")
    janela.geometry("500x650")
    janela.resizable(False, False)
    janela.configure(fg_color="#0d0d0d")

    titulo = ctk.CTkLabel(
        janela,
        text="✂ BARBEARIA BLACK",
        font=("Arial", 30, "bold"),
        text_color="#ff1e1e"
    )
    titulo.pack(pady=(70, 10))

    subtitulo = ctk.CTkLabel(
        janela,
        text="Entre na sua conta",
        font=("Arial", 18),
        text_color="white"
    )
    subtitulo.pack(pady=(0, 35))

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

    def entrar():

        e = email.get().strip()
        s = senha.get()

        if not e or not s:
            messagebox.showwarning(
                "Atenção",
                "Digite seu e-mail e sua senha."
            )
            return

        conn = sqlite3.connect("barbearia.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT nome
            FROM usuarios
            WHERE email = ?
            AND senha = ?
        """, (e, s))

        usuario = cursor.fetchone()
        conn.close()

        if usuario:
            nome_usuario = usuario[0]

            janela.withdraw()

            abrir_painel(nome_usuario, janela)

        else:
            messagebox.showerror(
                "Login inválido",
                "E-mail ou senha incorretos."
            )

    botao_login = ctk.CTkButton(
        janela,
        text="ENTRAR",
        width=350,
        height=50,
        fg_color="#e50914",
        hover_color="#b20710",
        font=("Arial", 16, "bold"),
        command=entrar
    )
    botao_login.pack(pady=30)

    botao_cadastro = ctk.CTkButton(
        janela,
        text="CRIAR CONTA",
        width=350,
        height=45,
        fg_color="white",
        hover_color="#dddddd",
        text_color="black",
        font=("Arial", 15, "bold"),
        command=abrir_cadastro
    )
    botao_cadastro.pack()

    janela.mainloop()


def abrir_painel(nome_usuario, login):

    painel = ctk.CTkToplevel()

    painel.title("Painel - Barbearia Black")
    painel.geometry("1000x700")
    painel.configure(fg_color="#0d0d0d")

    titulo = ctk.CTkLabel(
        painel,
        text="✂ BARBEARIA BLACK",
        font=("Arial", 32, "bold"),
        text_color="#ff1e1e"
    )
    titulo.pack(pady=(30, 5))

    boas_vindas = ctk.CTkLabel(
        painel,
        text=f"Olá, {nome_usuario}!",
        font=("Arial", 18),
        text_color="white"
    )
    boas_vindas.pack(pady=(0, 20))

    # =========================
    # BOTÃO NOVO AGENDAMENTO
    # =========================

    botao_agendar = ctk.CTkButton(
        painel,
        text="📅 NOVO AGENDAMENTO",
        width=300,
        height=45,
        fg_color="#e50914",
        hover_color="#b20710",
        font=("Arial", 15, "bold"),
        command=abrir_agendamento
    )
    botao_agendar.pack(pady=10)

    # =========================
    # ÁREA DE AGENDAMENTOS
    # =========================

    frame = ctk.CTkFrame(
        painel,
        width=900,
        height=400,
        fg_color="#161616"
    )
    frame.pack(pady=20, padx=30, fill="both", expand=True)

    titulo_agendamentos = ctk.CTkLabel(
        frame,
        text="📋 AGENDAMENTOS",
        font=("Arial", 22, "bold"),
        text_color="white"
    )
    titulo_agendamentos.pack(pady=15)

    lista = ctk.CTkScrollableFrame(
        frame,
        width=850,
        height=320,
        fg_color="#101010"
    )
    lista.pack(padx=20, pady=10, fill="both", expand=True)

    def carregar_agendamentos():

        for widget in lista.winfo_children():
            widget.destroy()

        conn = sqlite3.connect("barbearia.db")
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS agendamentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente TEXT,
                telefone TEXT,
                servico TEXT,
                data TEXT,
                horario TEXT,
                preco REAL,
                status TEXT
            )
        """)

        cursor.execute("""
            SELECT id, cliente, telefone, servico,
                   data, horario, preco, status
            FROM agendamentos
            ORDER BY id DESC
        """)

        agendamentos = cursor.fetchall()

        conn.close()

        if not agendamentos:

            vazio = ctk.CTkLabel(
                lista,
                text="Nenhum agendamento encontrado.",
                font=("Arial", 16),
                text_color="#aaaaaa"
            )

            vazio.pack(pady=40)

            return

        for agendamento in agendamentos:

            (
                id_agendamento,
                cliente,
                telefone,
                servico,
                data,
                horario,
                preco,
                status
            ) = agendamento

            card = ctk.CTkFrame(
                lista,
                fg_color="#222222",
                corner_radius=10
            )
            card.pack(
                fill="x",
                padx=10,
                pady=8
            )

            texto = (
                f"👤 {cliente}\n"
                f"💇 {servico}\n"
                f"📅 {data}  🕐 {horario}\n"
                f"📱 {telefone}\n"
                f"💰 R$ {preco:.2f}\n"
                f"📌 Status: {status}"
            )

            info = ctk.CTkLabel(
                card,
                text=texto,
                justify="left",
                anchor="w",
                font=("Arial", 14),
                text_color="white"
            )
            info.pack(
                side="left",
                padx=15,
                pady=12
            )

            # =========================
            # BOTÃO CONCLUIR
            # =========================

            if status != "Realizado":

                def concluir(id_agendamento=id_agendamento):

                    conn = sqlite3.connect("barbearia.db")
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE agendamentos
                        SET status = 'Realizado'
                        WHERE id = ?
                    """, (id_agendamento,))

                    conn.commit()
                    conn.close()

                    carregar_agendamentos()

                botao_concluir = ctk.CTkButton(
                    card,
                    text="✓ CONCLUIR",
                    width=120,
                    height=35,
                    fg_color="#198754",
                    hover_color="#146c43",
                    command=concluir
                )

                botao_concluir.pack(
                    side="right",
                    padx=15
                )

    carregar_agendamentos()

    # =========================
    # ATUALIZAR
    # =========================

    botao_atualizar = ctk.CTkButton(
        painel,
        text="🔄 ATUALIZAR",
        width=150,
        height=35,
        fg_color="#333333",
        hover_color="#444444",
        command=carregar_agendamentos
    )
    botao_atualizar.pack(pady=5)

    # =========================
    # SAIR
    # =========================

    def sair():

        painel.destroy()
        login.deiconify()

    botao_sair = ctk.CTkButton(
        painel,
        text="SAIR",
        width=150,
        height=35,
        fg_color="#333333",
        hover_color="#555555",
        command=sair
    )
    botao_sair.pack(pady=(0, 15))

    painel.protocol(
        "WM_DELETE_WINDOW",
        sair
    )