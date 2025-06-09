import flet as ft
from routes import comeco, home
import random

def main(page: ft.Page):
    page.title = "Desafio Pauxiando"
    #page.window.width = 900
    #page.window.height = 1100
    page.bgcolor = ft.Colors.WHITE
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    #======Atualizar conforme imagem e palavra do jogo (implementar lógica)======
    palavra_correta = "TUCUNARÉ"
    #imagem_correta = ft.Image(src="tucunare.jpg", width=400)
    imagem_correta = ft.Container(
        content=ft.Image(src="tucunare.jpg", width=400, fit=ft.ImageFit.COVER),
        border_radius=20  # pra consgeuir mexer na borda
    )
    #============================================================================

    letras_embaralhadas = list(palavra_correta)
    random.shuffle(letras_embaralhadas)

    pontuacao = 0
    campos_resposta = []
    letras_clicadas = []
    botoes_letras = []

    resultado_text = ft.Text(size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
    pontuacao_text = ft.Text(f"Pontuação: {pontuacao}", size=22, color=ft.Colors.WHITE)

    def atualizar_pontuacao(acertou: bool):
        nonlocal pontuacao
        if acertou:
            if len(letras_clicadas) == len(palavra_correta):
                pontuacao += 10
            else:
                pontuacao += 5
        pontuacao_text.value = f"Pontuação: {pontuacao}"
        page.update()

    def verificar_resposta():
        resposta = ''.join([campo.value or "_" for campo in campos_resposta])
        if resposta.upper() == palavra_correta:
            resultado_text.value = "Parabéns! Você acertou! 🎉"
            atualizar_pontuacao(True)
        else:
            resultado_text.value = "Tente novamente!"
            atualizar_pontuacao(False)
        page.update()

    def criar_jogo():
        nonlocal campos_resposta, letras_clicadas, botoes_letras
        campos_resposta.clear()
        letras_clicadas.clear()
        botoes_letras.clear()

        campos = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        for _ in palavra_correta:
            #======Campo de preenchimento das palavras=====
            campo = ft.TextField(
                width=70, 
                height=80, 
                text_align=ft.TextAlign.CENTER, 
                read_only=True,
                text_style=ft.TextStyle(
                    size=30,  
                    weight=ft.FontWeight.BOLD  
                )
                )
            campos_resposta.append(campo)
            campos.controls.append(campo)

        botoes = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        cores = [ft.Colors.BLUE, ft.Colors.GREEN, ft.Colors.RED, ft.Colors.ORANGE, ft.Colors.PINK, ft.Colors.PURPLE]

        for letra in letras_embaralhadas:
            cor = random.choice(cores)
            # =====Botão das palavras embaralhadas=======
            botao = ft.ElevatedButton(
                text=letra,
                bgcolor=cor,
                color=ft.Colors.WHITE,
                width=80,
                height=80,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(
                        size=26,  
                        weight=ft.FontWeight.BOLD  
                    )
                )
            )

            def criar_callback(botao_ref, letra_ref):
                def on_click(e):
                    inserir_letra(letra_ref)
                    botao_ref.disabled = True
                    botao_ref.bgcolor = ft.Colors.GREY_400
                    botao_ref.color = ft.Colors.BLACK
                    page.update()
                return on_click

            botao.on_click = criar_callback(botao, letra)
            botoes_letras.append(botao)
            botoes.controls.append(botao)

        return campos, botoes

    def inserir_letra(letra):
        for campo in campos_resposta:
            if not campo.value:
                campo.value = letra
                letras_clicadas.append(letra)
                break
        page.update()
        if all(campo.value for campo in campos_resposta):
            verificar_resposta()

    # ==============Elementos jogo========
    img = imagem_correta
    campos, botoes = criar_jogo()

    coluna_jogo = ft.Column(
            controls=[
                ft.Text("Complete a palavra:", size=26, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                img,
                campos,
                ft.Text("Clique nas letras para completar:", size=25, color=ft.Colors.YELLOW, weight=ft.FontWeight.BOLD),
                botoes,
                resultado_text,
                pontuacao_text
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    #=====Caixa responsável por permitir exibição da imagem no fundo dp jogo======
    caixa = ft.Stack(
    controls=[
            ft.Image(src='obidos_sem_cor.png', expand=True, fit=ft.ImageFit.COVER),

            ft.Container(
                alignment=ft.alignment.center,
                border_radius=5,
                bgcolor=ft.Colors.WHITE12,
                blur=3, #borrado da imagem
                content=ft.Column(
                    controls=[
                        coluna_jogo
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                )
            )
    ],
    alignment=ft.alignment.center,
    expand=True
    )

    # =====Rota dessa página======= 
    def main_view(page):

        return ft.View(
            route="/",
            controls=[caixa]
        )
        
    # =====Configurações de rotas========
    def route_change(e):
        page.views.clear()

        if page.route == "/comeco":
            page.views.append(comeco.View(page))

        elif page.route == "/home":
            page.views.append(home.View(page))

        elif page.route == "/":
            page.views.append(main_view(page))
    
        page.update()

    page.on_route_change = route_change
    page.go("/comeco")

ft.app(target=main)