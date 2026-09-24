import customtkinter as ctk
from tkinter import messagebox
import sqlite3


def abrir_agendamento():

    janela = ctk.CTkToplevel()
    janela.title("Agendamento - Barbearia Black")
    janela.geometry("500x650")
    janela.resizable(False, False)

    janela.configure(fg_color="#0d0d0d")

    # Título
    titulo = ctk.CTkLabel(
        janela,
        text=" AGENDAR HORÁRIO",
        font=("Arial", 28, "bold"),
        text_color="#ff1e1e"
    )
    titulo.pack(pady=30)

    # Cliente
    cliente = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="Nome do cliente"
    )
    cliente.pack(pady=8)

    # Telefone
    telefone = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="Telefone"
    )
    telefone.pack(pady=8)

    # Serviço
    servico = ctk.CTkComboBox(
        janela,
        width=350,
        height=45,
        values=[
            "Corte masculino",
            "Barba",
            "Corte + Barba",
            "Sobrancelha"
        ]
    )
    servico.set("Corte masculino")
    servico.pack(pady=8)

    # Data
    data = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="Data: DD/MM/AAAA"
    )
    data.pack(pady=8)

    # Horário
    horario = ctk.CTkComboBox(
        janela,
        width=350,
        height=45,
        values=[
            "08:00",
            "09:00",
            "10:00",
            "11:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
            "18:00"
        ]
    )
    horario.set("08:00")
    horario.pack(pady=8)

    # Preço
    preco = ctk.CTkEntry(
        janela,
        width=350,
        height=45,
        placeholder_text="Preço: R$ 30,00"
    )
    preco.pack(pady=8)

    # Função salvar
    def salvar():

        nome = cliente.get()
        fone = telefone.get()
        serv = servico.get()
        dt = data.get()
        hora = horario.get()
        valor = preco.get()

        if not nome or not fone or not dt or not valor:

            messagebox.showwarning(
                "Atenção",
                "Preencha todos os campos!"
            )

            return

        try:
            valor = float(valor.replace(",", "."))
        except ValueError:

            messagebox.showerror(
                "Erro",
                "Digite um preço válido."
            )

            return

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
            SELECT id FROM agendamentos
            WHERE data = ?
            AND horario = ?
            AND status = 'Agendado'
        """, (dt, hora))

        if cursor.fetchone():

            conn.close()

            messagebox.showerror(
                "Horário ocupado",
                "Esse horário já está ocupado."
            )

            return

        cursor.execute("""
            INSERT INTO agendamentos
            (cliente, telefone, servico, data, horario, preco, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            nome,
            fone,
            serv,
            dt,
            hora,
            valor,
            "Agendado"
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo(
            "Sucesso",
            "Agendamento realizado!"
        )

        janela.destroy()

    # Botão
    botao = ctk.CTkButton(
        janela,
        text=" CONFIRMAR AGENDAMENTO",
        width=350,
        height=50,
        fg_color="#e50914",
        hover_color="#b20710",
        font=("Arial", 15, "bold"),
        command=salvar
    )

    botao.pack(pady=25)

    janela.grab_set()