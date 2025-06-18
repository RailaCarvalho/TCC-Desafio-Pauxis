import flet as ft
import json
import os

def View(page: ft.Page):
    def cadastrar_usuario(e):
        email = campo_email.value
        senha = campo_senha.value
        confirmar_senha = campo_confirmar_senha.value

        # Validações básicas
        if not email or not senha or not confirmar_senha:
            mensagem.value = "Todos os campos são obrigatórios!"
            mensagem.color = ft.colors.RED
            page.update()
            return

        if senha != confirmar_senha:
            mensagem.value = "As senhas não coincidem!"
            mensagem.color = ft.colors.RED
            page.update()
            return

        # --- CORREÇÃO DO CAMINHO ---
        # Encontra o caminho para o diretório 'routes' onde o arquivo está
        diretorio_atual = os.path.dirname(os.path.abspath(__file__))
        # Constrói o caminho para a pasta 'storage' (sobe um nível para 'src' e entra em 'storage')
        caminho_storage = os.path.abspath(os.path.join(diretorio_atual, "..", "storage"))
        # Garante que a pasta storage exista
        os.makedirs(caminho_storage, exist_ok=True)
        # Cria o caminho completo para o arquivo users.json
        arquivo_users = os.path.join(caminho_storage, "users.json")
        # --------------------------

        # Carregar usuários existentes
        try:
            with open(arquivo_users, "r") as f:
                usuarios = json.load(f)
        except FileNotFoundError:
            usuarios = []

        # Verificar se email já existe
        for usuario in usuarios:
            if usuario["email"] == email:
                mensagem.value = "Este email já está cadastrado!"
                mensagem.color = ft.colors.RED
                page.update()
                return

        # Adicionar novo usuário
        usuarios.append({
            "email": email,
            "senha": senha
        })

        # Salvar no arquivo JSON
        with open(arquivo_users, "w") as f:
            json.dump(usuarios, f, indent=4)

        # Sucesso
        mensagem.value = "Cadastro realizado com sucesso!"
        mensagem.color = ft.colors.GREEN
        page.update()

        # Limpar campos
        campo_email.value = ""
        campo_senha.value = ""
        campo_confirmar_senha.value = ""
        page.update()

    def voltar_login(e):
        page.go("/login")

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

    campo_confirmar_senha = ft.TextField(
        label="Confirmar Senha",
        password=True,
        can_reveal_password=True,
        width=300,
        border_color=ft.colors.RED_700
    )

    # Botões
    botao_cadastrar = ft.ElevatedButton(
        text="CADASTRAR",
        on_click=cadastrar_usuario,
        width=300,
        height=50,
        color=ft.colors.WHITE,
        bgcolor=ft.colors.RED_700
    )

    botao_voltar = ft.TextButton(
        text="Já tem uma conta? Faça login",
        on_click=voltar_login
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
                campo_confirmar_senha,
                botao_cadastrar,
                botao_voltar,
                mensagem
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )
    )

    return ft.View(
        route="/cadastro",
        controls=[container]
    ) 