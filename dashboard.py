import customtkinter as ctk
from agendamento import Agendamento


class Dashboard(ctk.CTk):

    def __init__(self, nome):
        super().__init__()

        self.title("Barbearia Black")
        self.geometry("900x600")
        self.configure(fg_color="#0d0d0d")

        titulo = ctk.CTkLabel(
            self,
            text=" BARBEARIA BLACK",
            font=("Arial", 32, "bold"),
            text_color="#ff1e1e"
        )
        titulo.pack(pady=(50, 10))

        boas_vindas = ctk.CTkLabel(
            self,
            text=f"Olá, {nome}!",
            font=("Arial", 22),
            text_color="white"
        )
        boas_vindas.pack(pady=10)

        btn_agendar = ctk.CTkButton(
            self,
            text="📅 AGENDAR HORÁRIO",
            width=350,
            height=60,
            fg_color="#e50914",
            hover_color="#b20710",
            font=("Arial", 18, "bold"),
            command=self.abrir_agendamento
        )
        btn_agendar.pack(pady=30)

        btn_sair = ctk.CTkButton(
            self,
            text="SAIR",
            width=350,
            height=50,
            fg_color="#ffffff",
            hover_color="#dddddd",
            text_color="black",
            command=self.destroy
        )
        btn_sair.pack()

    def abrir_agendamento(self):
        Agendamento(self)