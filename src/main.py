import flet as ft
from flet_audio.audio import Audio # Adicione esta linha
# Seus imports de rotas podem ser diferentes, ajuste se necessário
from routes import play, login, cadastro, estatisticas 
import random
import json
import time
from datetime import datetime
import os

# Estrutura das fases do jogo
FASES = [
    {
        "imagem": "tucunare.jpg",
        "palavra": "TUCUNARÉ",
        "nome": "Tucunaré"
    },
    {
        "imagem": "forte_pauxis.jpg",
        "palavra": "FORTE PAUXIS",
        "nome": "Forte Pauxis"
    },
    {
        "imagem": "museu.jpg",
        "palavra": "MUSEU",
        "nome": "Museu"
    },
    {
        "imagem": "obidos.jpg",
        "palavra": "ÓBIDOS",
        "nome": "Óbidos"
    },
    {
        "imagem": "casa_da_cultura.jpg",
        "palavra": "CASA DA CULTURA",
        "nome": "Casa da Cultura"
    }
]

def salvar_estatisticas(estatisticas_gerais):
    # Encontra o caminho absoluto para o diretório onde main.py está (a pasta 'src')
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    # Cria o caminho completo para a pasta 'storage' dentro de 'src'
    caminho_storage = os.path.join(diretorio_base, "storage")
    os.makedirs(caminho_storage, exist_ok=True) # Garante que a pasta exista
    
    # Define o caminho completo para o arquivo de estatísticas
    arquivo = os.path.join(caminho_storage, "estatisticas.json")
    
    try:
        if os.path.exists(arquivo) and os.path.getsize(arquivo) > 0:
            with open(arquivo, "r", encoding="utf-8") as f:
                dados = json.load(f)
        else:
            dados = []
    except (json.JSONDecodeError, FileNotFoundError):
        dados = []
    
    dados.append(estatisticas_gerais)
    
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def main(page: ft.Page):
    page.title = "Desafio Pauxis"
    page.bgcolor = ft.Colors.GREY_900
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 0
    page.window_full_screen = True

    # --- SUGESTÃO: Carregando fonte e sons ---
    page.fonts = {
        "Nunito": "https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap"
    }
    audio_acerto = Audio(src="assets/acerto.mp3", autoplay=False)
    audio_clique = Audio(src="assets/clique.mp3", autoplay=False)
    page.overlay.extend([audio_acerto, audio_clique])
    # -----------------------------------------

    # --- Variáveis de Controle do Jogo (Existentes) ---
    fase_atual = 0
    tentativas_incorretas = 0
    tempo_inicio_fase = None
    estatisticas_fase = []
    pontuacao_total = 0
    campos_resposta = []
    botoes_letras = []
    dica_visivel = False

    # --- Variáveis para Coleta de Estatísticas Detalhadas ---
    tempo_reacao_primeiro_clique = None
    timestamp_ultimo_clique = None
    tempos_entre_cliques = []
    timestamp_erro = None
    tempos_pos_erro = []
    sequencia_de_cliques = []
    frequencia_dicas = 0
    tentativas_com_sequencia_errada = []


    # --- SUGESTÃO: Aplicando a fonte nos elementos da UI ---
    resultado_text = ft.Text(size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, font_family="Nunito")
    pontuacao_text = ft.Text(f"Pontuação: {pontuacao_total}", size=22, color=ft.Colors.WHITE, font_family="Nunito")
    fase_text = ft.Text(f"Fase {fase_atual + 1} de {len(FASES)}", size=20, color=ft.Colors.WHITE, font_family="Nunito")
    dica_text = ft.Text(value="", size=20, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD, visible=False, font_family="Nunito")
    
    # --- NOVO: Botão para tentar novamente, inicialmente invisível ---
    def limpar_e_tentar_novamente(e):
        # Limpa os campos de resposta
        for campo in campos_resposta:
            if isinstance(campo, ft.TextField):
                campo.value = ""
        
        # Reativa todos os botões de letras
        for botao in botoes_letras:
            botao.disabled = False
            botao.bgcolor = botao.data # Restaura a cor original que salvamos
        
        # Esconde o botão "Tentar Novamente" e a mensagem de erro
        botao_tentar_novamente.visible = False
        resultado_text.value = ""
        
        page.update()
    
    

    
    # -------------------------------------------------------------------

    # --- SUGESTÃO: Função de animação para o acerto ---
    def animar_acerto():
        campos_de_texto = [c for c in campos_resposta if isinstance(c, ft.TextField)]
        for _ in range(3): # Pisca 2 vezes
            for campo in campos_de_texto:
                campo.bgcolor = ft.Colors.GREEN_500
            page.update()
            time.sleep(0.2)
            for campo in campos_de_texto:
                campo.bgcolor = ft.Colors.WHITE # Volta à cor original
            page.update()
            time.sleep(0.2)

    # --- Funções do Jogo ---

    def proxima_fase(e):
        nonlocal fase_atual
        if fase_atual < len(FASES) - 1:
            fase_atual += 1
            iniciar_fase()

    

    def criar_campos_resposta():
        nonlocal campos_resposta
        campos_resposta = []
        palavra_correta = FASES[fase_atual]['palavra']
        campos_resposta_row = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=5)
        
        for char in palavra_correta:
            if char == " ":
                campo = ft.Container(width=40, height=80)
            else:
                campo = ft.TextField(
                    width=70, height=80, text_align=ft.TextAlign.CENTER, read_only=True,
                    text_style=ft.TextStyle(size=30, weight=ft.FontWeight.BOLD, font_family="Nunito"),
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    animate_scale=ft.animation.Animation(300, "ease") # Prepara para animação
                )
            campos_resposta.append(campo)
            campos_resposta_row.controls.append(campo)
        return campos_resposta_row

    # --- NOVO: Função para apagar a última letra digitada ---
    def apagar_letra(e):
        # Encontra o último campo preenchido, de trás para frente
        for campo in reversed(campos_resposta):
            if isinstance(campo, ft.TextField) and campo.value:
                letra_removida = campo.value
                campo.value = ""
                
                # Reativa o botão correspondente à letra removida
                for botao in botoes_letras:
                    if botao.text == letra_removida and botao.disabled:
                        botao.disabled = False
                        botao.bgcolor = botao.data # Restaura a cor original
                        break
                page.update()
                break # Para após apagar uma única letra
    # ---------------------------------------------------------

    def criar_botoes_letras():
        nonlocal botoes_letras
        botoes_letras = []
        palavra_sem_espacos = FASES[fase_atual]['palavra'].replace(" ", "")
        letras_embaralhadas = list(palavra_sem_espacos)
        random.shuffle(letras_embaralhadas)
        
        botoes_letras_row = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        
        # --- Cores fortes ---
        cores = [
            # Cores Originais
            "#FF6F61",  # Coral Vivo
            "#F9A825",  # Amarelo Manga
            "#00BFA5",  # Verde Água Forte
            "#448AFF",  # Azul Céu Intenso
            "#E040FB",  # Roxo Orquídea
            "#F50057",  # Pink Vibrante
            
            # Novas Cores Adicionadas
            "#F44336",  # Vermelho Tomate
            "#8BC34A",  # Verde Folha
            "#FF9800",  # Laranja Pôr do Sol
            "#00BCD4",  # Azul Turquesa
            "#CDDC39",  # Verde Limão
            "#673AB7",  # Roxo Real
        ]
        
        for letra in letras_embaralhadas:
            def criar_callback(botao_ref, letra_ref):
                def on_click(e):
                    inserir_letra(letra_ref)
                    botao_ref.disabled = True
                    botao_ref.bgcolor = ft.Colors.GREY_400
                    botao_ref.color = ft.Colors.BLACK54
                    page.update()
                return on_click

            cor_do_botao = random.choice(cores) # Guarda a cor sorteada
            botao = ft.ElevatedButton(
                text=letra, 
                bgcolor=cor_do_botao, 
                color=ft.Colors.BLACK87, # Melhor contraste com cores claras
                width=80, height=80,
                # --- MUDANÇA: Salva a cor original no 'data' do botão ---
                data=cor_do_botao,
                # --------------------------------------------------------
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=12),
                    elevation=6,
                    shadow_color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
                    text_style=ft.TextStyle(size=26, weight=ft.FontWeight.BOLD, font_family="Nunito")
                )
            )
            botao.on_click = criar_callback(botao, letra)
            botoes_letras.append(botao)
            botoes_letras_row.controls.append(botao)

        return botoes_letras_row

    def mostrar_dica(e):
        nonlocal dica_visivel, frequencia_dicas
        frequencia_dicas += 1
        dica_visivel = not dica_visivel
        dica_text.value = f"Dica: {FASES[fase_atual]['palavra']}" if dica_visivel else ""
        dica_text.visible = dica_visivel
        page.update()

    def verificar_resposta():
        nonlocal timestamp_erro
        palavra_digitada = ""
        for campo in campos_resposta:
            if isinstance(campo, ft.TextField):
                palavra_digitada += campo.value or "_"
            elif isinstance(campo, ft.Container):
                palavra_digitada += " "
        
        if palavra_digitada.upper() == FASES[fase_atual]['palavra']:
            atualizar_pontuacao(True)
        else:
            timestamp_erro = time.time()
            tentativas_com_sequencia_errada.append(palavra_digitada)
            atualizar_pontuacao(False)
        page.update()

    def inserir_letra(letra):
        nonlocal tempo_reacao_primeiro_clique, timestamp_ultimo_clique, timestamp_erro
        
        audio_clique.play() # <--- SUGESTÃO: Som de clique
        
        if tempo_reacao_primeiro_clique is None:
            tempo_reacao_primeiro_clique = time.time() - tempo_inicio_fase

        if timestamp_ultimo_clique is not None:
            tempo_deliberacao = time.time() - timestamp_ultimo_clique
            tempos_entre_cliques.append(round(tempo_deliberacao, 2))
        
        if timestamp_erro is not None:
            tempo_recuperacao = time.time() - timestamp_erro
            tempos_pos_erro.append(round(tempo_recuperacao, 2))
            timestamp_erro = None 

        sequencia_de_cliques.append(letra)
        timestamp_ultimo_clique = time.time()
        
        for campo in campos_resposta:
            if isinstance(campo, ft.TextField) and not campo.value:
                campo.value = letra

                # --- SUGESTÃO: Animação de "pulo" da letra ---
                campo.scale = 0.5
                campo.update()
                time.sleep(0.05)
                campo.scale = 1.0
                # ----------------------------------------------
                break
        page.update()
        
        campos_de_letra = [c for c in campos_resposta if isinstance(c, ft.TextField)]
        if all(campo.value for campo in campos_de_letra):
            verificar_resposta()

    def atualizar_pontuacao(acertou: bool):
        nonlocal pontuacao_total, tentativas_incorretas
        if acertou:
            animar_acerto() # <--- SUGESTÃO: Animação de acerto
            audio_acerto.play() # <--- SUGESTÃO: Som de acerto

            palavra_da_fase = FASES[fase_atual]['palavra']
            letras_na_palavra = len(palavra_da_fase.replace(" ", ""))
            pontuacao_fase = letras_na_palavra * 10
            pontuacao_total += pontuacao_fase
            
            estatisticas_detalhadas = {
                "fase": FASES[fase_atual]['nome'],
                "palavra_correta": palavra_da_fase,
                "complexidade_palavra": len(palavra_da_fase.replace(" ", "")),
                "pontuacao": pontuacao_fase,
                "acertou": True,
                "tempo_total_gasto": round(time.time() - tempo_inicio_fase, 2),
                "tentativas_incorretas_total": tentativas_incorretas,
                "tempo_reacao_primeiro_clique": round(tempo_reacao_primeiro_clique, 2) if tempo_reacao_primeiro_clique else 0,
                "tempo_medio_deliberacao_entre_cliques": round(sum(tempos_entre_cliques) / len(tempos_entre_cliques), 2) if tempos_entre_cliques else 0,
                "tempos_recuperacao_pos_erro_secs": tempos_pos_erro,
                "frequencia_uso_dica": frequencia_dicas,
                "sequencia_final_cliques": sequencia_de_cliques,
                "tentativas_com_sequencias_erradas": tentativas_com_sequencia_errada
            }
            estatisticas_fase.append(estatisticas_detalhadas)

            resultado_text.value = "🎉 Parabéns, você acertou!"
            resultado_text.color = ft.Colors.GREEN_ACCENT_400

            # --- MUDANÇA: Garante que o botão de tentar novamente está escondido ---
            botao_tentar_novamente.visible = False
            # ---------------------------------------------------------------------
            
            if fase_atual < len(FASES) - 1:
                botao_proxima_fase.visible = True
            else:
                salvar_estatisticas({
                    "usuario": "raila@gmail.com",
                    "pontuacao_total": pontuacao_total, 
                    "data_hora_fim": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "resumo_fases": estatisticas_fase
                })
                mostrar_tela_final()
        else:
            tentativas_incorretas += 1
            resultado_text.value = "💪 Tente novamente! Você consegue!"
            resultado_text.color = ft.Colors.RED_500

            # --- MUDANÇA: Mostra o botão para tentar novamente ---
            botao_tentar_novamente.visible = True
            # ----------------------------------------------------
        
        pontuacao_text.value = f"🏆 Pontuação: {pontuacao_total}"
        page.update()
    
    botao_tentar_novamente = ft.ElevatedButton(
        text="Tentar Novamente",
        on_click=limpar_e_tentar_novamente,
        visible=False,
        bgcolor=ft.Colors.ORANGE_700,
        color=ft.Colors.WHITE
    )

    # --- BOTÃO DE APAGAR DEFINIDO AQUI ---
    botao_apagar = ft.IconButton(
        icon=ft.Icons.BACKSPACE_OUTLINED,
        on_click=apagar_letra, # A função apagar_letra já existe
        icon_size=40,
        icon_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.RED_700,
        tooltip="Apagar última letra"
    )
    # -----------------------------------

    botao_proxima_fase = ft.ElevatedButton(
        text="Próxima Fase",
        visible=False, width=200, height=50,
        color=ft.Colors.WHITE, bgcolor=ft.Colors.GREEN_700,
        on_click=proxima_fase,
        style=ft.ButtonStyle(
            text_style=ft.TextStyle(size=20, weight=ft.FontWeight.BOLD, font_family="Nunito"),
            shadow_color=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
            elevation=8,
        )
    )

    def mostrar_tela_final():
        media_tentativas = sum(f['tentativas_incorretas_total'] for f in estatisticas_fase) / len(estatisticas_fase) if estatisticas_fase else 0
        media_tempo = sum(f['tempo_total_gasto'] for f in estatisticas_fase) / len(estatisticas_fase) if estatisticas_fase else 0
        
        estatisticas_container = ft.Container(
            content=ft.Column([
                ft.Text("🎉 Parabéns! Você completou todas as fases! 🎉", size=30, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER, font_family="Nunito"),
                ft.Text(f"🏆 Pontuação Total: {pontuacao_total}", size=24, text_align=ft.TextAlign.CENTER, font_family="Nunito"),
                ft.Text(f"🎯 Média de Tentativas: {media_tentativas:.1f}", size=22, text_align=ft.TextAlign.CENTER, font_family="Nunito"),
                ft.Text(f"⏱️ Tempo Médio por Fase: {media_tempo:.1f}s", size=22, text_align=ft.TextAlign.CENTER, font_family="Nunito"),
                ft.Row([
                    ft.ElevatedButton("📊 Ver Estatísticas", on_click=lambda e: page.go("/estatisticas"), width=250, height=50, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, font_family="Nunito"))),
                    ft.ElevatedButton("🏠 Voltar ao Menu", on_click=lambda e: page.go("/play"), width=250, height=50, bgcolor=ft.Colors.BLUE_700, color=ft.Colors.WHITE, style=ft.ButtonStyle(text_style=ft.TextStyle(size=18, weight=ft.FontWeight.BOLD, font_family="Nunito")))
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            padding=30, bgcolor=ft.Colors.with_opacity(0.95, ft.Colors.WHITE), border_radius=10, alignment=ft.alignment.center
        )
        
        page.views.clear()
        page.views.append(ft.View(route="/final", controls=[ft.Stack([ft.Image(src='obidos_sem_cor.png', expand=True, fit=ft.ImageFit.COVER), ft.Container(content=estatisticas_container, alignment=ft.alignment.center, expand=True)])], vertical_alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER))
        page.update()

    def montar_tela_jogo():
        # --- SUGESTÃO: Adicionando sombra aos elementos ---
        sombra_padrao = ft.BoxShadow(
            spread_radius=1, blur_radius=10,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            offset=ft.Offset(0, 4),
        )

        img = ft.Container(
            content=ft.Image(src=FASES[fase_atual]['imagem'], width=350, fit=ft.ImageFit.COVER, border_radius=20),
            border_radius=20, alignment=ft.alignment.center, shadow=sombra_padrao
        )
        campos_resposta_row = criar_campos_resposta()
        botoes_letras_row = criar_botoes_letras()
        
        return ft.ListView(
            controls=[
                ft.Container(content=ft.Text("Complete a palavra:", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, font_family="Nunito"), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=5, border_radius=10, alignment=ft.alignment.center),
                ft.Container(content=fase_text, alignment=ft.alignment.center),
                ft.Container(content=img, alignment=ft.alignment.center),
                ft.Container(content=ft.Row([ft.Text("Precisa de ajuda?", size=20, color=ft.Colors.WHITE, font_family="Nunito"), ft.IconButton(icon=ft.Icons.VISIBILITY, icon_color=ft.Colors.WHITE, tooltip="Ver dica", on_click=mostrar_dica)], alignment=ft.MainAxisAlignment.CENTER), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=ft.padding.symmetric(vertical=4, horizontal=10), border_radius=10, alignment=ft.alignment.center),
                ft.Container(content=dica_text, alignment=ft.alignment.center),
                # --- MUDANÇA AQUI ---
                ft.Container(
                    content=ft.Row(
                        [
                            campos_resposta_row, # Os campos da palavra
                            botao_apagar         # O botão de apagar ao lado
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    alignment=ft.alignment.center,
                    padding=ft.padding.symmetric(horizontal=20)
                ),
                # --------------------
                ft.Container(content=ft.Text("Clique nas letras para completar:", size=25, color=ft.Colors.YELLOW, weight=ft.FontWeight.BOLD, font_family="Nunito"), bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.BLACK), padding=3, border_radius=10, alignment=ft.alignment.center),
                ft.Container(content=botoes_letras_row, alignment=ft.alignment.center, padding=ft.padding.symmetric(horizontal=20)),
                ft.Container(content=resultado_text, alignment=ft.alignment.center, padding=10),
                # --- NOVO: Container para o botão de tentar novamente ---
                ft.Container(content=botao_tentar_novamente, alignment=ft.alignment.center),
                # -------------------------------------------------------
                ft.Container(content=pontuacao_text, alignment=ft.alignment.center),
                ft.Container(content=botao_proxima_fase, alignment=ft.alignment.center)
            ], spacing=3, padding=20, expand=True, auto_scroll=True
        )

    caixa_jogo = ft.Container(alignment=ft.alignment.center, border_radius=5, bgcolor=ft.Colors.WHITE12, content=montar_tela_jogo(), expand=True)
    
    def iniciar_fase():
        nonlocal tempo_inicio_fase, tentativas_incorretas, dica_visivel
        nonlocal tempo_reacao_primeiro_clique, timestamp_ultimo_clique, tempos_entre_cliques
        nonlocal timestamp_erro, tempos_pos_erro, sequencia_de_cliques, frequencia_dicas
        nonlocal tentativas_com_sequencia_errada

        tempo_reacao_primeiro_clique = None
        timestamp_ultimo_clique = None
        tempos_entre_cliques.clear()
        timestamp_erro = None
        tempos_pos_erro.clear()
        sequencia_de_cliques.clear()
        frequencia_dicas = 0
        tentativas_com_sequencia_errada.clear()

        tempo_inicio_fase = time.time()
        tentativas_incorretas = 0
        dica_visivel = False
        fase_text.value = f"Fase {fase_atual + 1} de {len(FASES)}"
        botao_proxima_fase.visible = False
        dica_text.visible = False
        dica_text.value = ""
        resultado_text.value = ""
        pontuacao_text.value = f"🏆 Pontuação: {pontuacao_total}"
        
        # --- MUDANÇA: Garante que o botão de tentar novamente também seja resetado ---
        botao_tentar_novamente.visible = False
        # --------------------------------------------------------------------------

        caixa_jogo.content = montar_tela_jogo()
        page.update()

    def main_view(page):
        nonlocal fase_atual, pontuacao_total, estatisticas_fase
        fase_atual = 0
        pontuacao_total = 0
        estatisticas_fase = []
        iniciar_fase()
        return ft.View(route="/", controls=[ft.Stack(controls=[ft.Image(src='obidos_sem_cor.png', expand=True, fit=ft.ImageFit.FILL), caixa_jogo], expand=True)])
        
    def route_change(e):
        page.views.clear()
        if page.route == "/play":
            page.views.append(play.View(page))
        elif page.route == "/login":
            page.views.append(login.View(page))
        elif page.route == "/cadastro":
            page.views.append(cadastro.View(page))
        elif page.route == "/":
            page.views.append(main_view(page))
        elif page.route == "/estatisticas":
            page.views.append(estatisticas.View(page))
        page.update()

    page.on_route_change = route_change
    page.go("/play")

ft.app(target=main, assets_dir="assets")