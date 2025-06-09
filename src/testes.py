import flet as ft

def main(page: ft.Page):

    campo1 = ft.TextField(
        width=70,
        height=80,
        text_align=ft.TextAlign.CENTER,
        read_only=True,
        border_radius=8,
        border_color=ft.Colors.BLACK,
        border_width=3,
        text_style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD),
    )
  
    campo2 = ft.Container(
        border=ft.border.all(3, ft.colors.BLACK),
        border_radius=8,
        padding=2,
        content=ft.TextField(
            width=70,
            height=80,
            text_align=ft.TextAlign.CENTER,
            read_only=True,
            text_style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD),
            border_width=0 
        )
    )

    campo3 = ft.Stack(
        width=80,
        height=90,
        controls=[
            ft.Image(
                src="imagem_pontilhada2.png",
                fit=ft.ImageFit.COVER,
                width=80,
                #height=80
            ),
            ft.Container(
                padding=2,
                alignment=ft.alignment.center,
                content=ft.TextField(
                    width=80,
                    height=90,
                    text_align=ft.TextAlign.CENTER,
                    read_only=True,
                    text_style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD),
                    border_width=0
                )
            )
        ]
    )

    texto_borda = ft.Stack(
        controls=[
            ft.Text(  # texto de contorno (atrás)
                "Clique nas letras para completar:",
                size=20,
                color=ft.Colors.BLACK,
                weight=ft.FontWeight.BOLD,
                top=1,  # leve deslocamento pra simular borda
                left=1,
            ),
            ft.Text(  # texto principal (na frente)
                "Clique nas letras para completar:",
                size=20,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD,
            ),
        ]
    )

    texto_fundo = ft.Container(
            content=ft.Text(
                "Clique nas letras para completar:",
                size=20,
                color=ft.Colors.WHITE,
                weight=ft.FontWeight.BOLD
            ),
            padding=8,
            bgcolor=ft.Colors.BLACK54,
            border_radius=8
        )

    page.add(
        ft.Text("Com relação aos campos:"),
        campo1,
        campo2,
        campo3,
        ft.Text("Com relação as bordas:"),
        texto_borda,
        texto_fundo
    )

ft.app(target=main)