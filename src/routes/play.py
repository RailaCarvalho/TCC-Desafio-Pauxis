import flet as ft
import time

def View(page: ft.Page):
    def entrar(e):
        page.go("/login")

    imagem_menu = ft.Image(
        src="../assets/capa_entrada.png",
        width=700,
        fit=ft.ImageFit.CONTAIN
    )

    imagem_carregamento = ft.Image(
        src="../assets/carregamento.png",
        width=200,
        fit=ft.ImageFit.CONTAIN
    )

    # Timer para redirecionamento automático
    def iniciar_timer():
        time.sleep(4)
        page.go("/login")

    # Inicia o timer em uma thread separada
    import threading
    timer_thread = threading.Thread(target=iniciar_timer)
    timer_thread.daemon = True
    timer_thread.start()

    #=======Configurações do menu========
    menu = ft.Container(
        expand=True,  
        alignment=ft.alignment.center,  
        bgcolor=ft.Colors.LIGHT_BLUE_100,
        content=ft.Column(
            controls=[imagem_menu, imagem_carregamento],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,  
            spacing=30
        )
    )

    return ft.View(
        route="/play",
        controls = [
            menu
        ]
    ) 