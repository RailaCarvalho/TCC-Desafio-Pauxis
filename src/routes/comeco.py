import flet as ft

def View(page: ft.Page):
    def entrar(e):
        page.go("/")

    imagem_menu = ft.Image(
        src="../assets/OUTROBG.png",
        width=700,
        fit=ft.ImageFit.CONTAIN
    )

    botao_comecar = ft.ElevatedButton(
        text="JOGAR", 
        on_click=entrar, 
        width=300, 
        height=80, 
        color=ft.Colors.WHITE, 
        bgcolor=ft.Colors.RED_700,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(
                size=26, 
                weight=ft.FontWeight.BOLD 
            )
        )
    )

    #=======Configurações do menu========
    menu = ft.Container(
        expand=True,  
        alignment=ft.alignment.center,  
        content=ft.Column(
            controls=[imagem_menu, botao_comecar],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  
            spacing=30
        )
    )

    return ft.View(
        route="/comeco",
        controls = [
            menu
        ]
    )

