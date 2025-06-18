import flet as ft
import json
import os
from time import sleep

def View(page: ft.Page):
    def validar_login(e):
        email = campo_email.value
        senha = campo_senha.value
        
        # --- CORREÇÃO DO CAMINHO (IGUAL AO CADASTRO.PY) ---
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        caminho_storage = os.path.abspath(os.path.join(diretorio_atual, "..", "storage"))
        arquivo_users = os.path.join(caminho_storage, "users.json")
        # --------------------------------------------------

        # Carregar dados do arquivo JSON
        try:
            with open(arquivo_users, "r") as f:
                usuarios = json.load(f)
        except FileNotFoundError:
            usuarios = []
        
        # Verificar credenciais
        for usuario in usuarios:
            if usuario["email"] == email and usuario["senha"] == senha:
                # Login bem sucedido
                mensagem.value = "Login realizado com sucesso! Carregando o jogo..."
                mensagem.color = ft.colors.GREEN_700
                page.update()
                
                # Aguardar 3 segundos e redirecionar
                sleep(3)
                page.go("/")
                return
        
        # Login falhou
        mensagem.value = "Email ou senha inválidos!"
        mensagem.color = ft.colors.RED
        page.update()

    def ir_para_cadastro(e):
        page.go("/cadastro")

    # Logo
    imagem_logo = ft.Image(
        src="../assets/logo.png",
        width=300,
        fit=ft.ImageFit.CONTAIN
    )

    # Campos de entrada
    campo_email = ft.TextField(
        label="Email",
        width=300,
        border_color=ft.colors.RED_700
    )

    campo_senha = ft.TextField(
        label="Senha",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.colors.RED_700
    )

    # Botões
    botao_entrar = ft.ElevatedButton(
        text="ENTRAR",
        on_click=validar_login,
        width=300,
        height=50,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.RED_700
    )

    botao_cadastro = ft.TextButton(
        text="Não tem uma conta? Cadastre-se",
        on_click=ir_para_cadastro
    )

    # Mensagem de feedback
    mensagem = ft.Text(
        value="",
        size=16,
        text_align=ft.TextAlign.CENTER
    )

    # Container principal
    container = ft.Container(
        expand=True,
        alignment=ft.alignment.center,
        content=ft.Column(
            controls=[
                imagem_logo,
                campo_email,
                campo_senha,
                botao_entrar,
                botao_cadastro,
                mensagem
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    return ft.View(
        route="/login",
        controls=[container]
    ) 