import flet as ft
import json
import os
from datetime import datetime

class View(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__()
        self.page = page
        self.route = "/estatisticas"
        self.bgcolor = ft.colors.WHITE
        self.padding = 0

        # Carrega todas as sessões de jogo do arquivo
        self.todas_as_sessoes = self._carregar_estatisticas()

        # Componentes da UI que precisam ser atualizados
        self.dropdown_sessoes = None
        self.detalhes_container = ft.Column(expand=True, scroll=ft.ScrollMode.ADAPTIVE)

        # Constrói o layout principal
        self.controls = [self._criar_layout_principal()]
        
        # Exibe os detalhes da sessão mais recente por padrão, se houver alguma
        if self.todas_as_sessoes:
            self._atualizar_detalhes(self.todas_as_sessoes[-1])

    def _carregar_estatisticas(self):
        """Carrega e retorna todas as sessões de jogo do arquivo JSON."""
        try:

            # --- CORREÇÃO DO CAMINHO ---
            # Encontra o caminho para o diretório 'routes' onde o arquivo está
            diretorio_atual = os.path.dirname(os.path.abspath(__file__))
            # Constrói o caminho para a pasta 'storage' (sobe um nível para 'src' e entra em 'storage')
            caminho_storage = os.path.abspath(os.path.join(diretorio_atual, "..", "storage"))
            # Cria o caminho completo para o arquivo estatisticas.json
            arquivo_estatisticas = os.path.join(caminho_storage, "estatisticas.json")
            # --------------------------

            if os.path.exists(arquivo_estatisticas) and os.path.getsize(arquivo_estatisticas) > 0:
                with open(arquivo_estatisticas, "r", encoding="utf-8") as f:
                    # Ordena as sessões da mais antiga para a mais recente
                    return sorted(json.load(f), key=lambda x: x.get("data_hora_fim", ""))
            return []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _sessao_selecionada(self, e):
        """Chamado quando uma nova sessão é selecionada no Dropdown."""
        index_selecionado = int(e.control.value)
        jogo_selecionado = self.todas_as_sessoes[index_selecionado]
        self._atualizar_detalhes(jogo_selecionado)
        self.page.update()

    def _atualizar_detalhes(self, jogo_selecionado):
        """Limpa e reconstrói o container de detalhes com os dados da sessão selecionada."""
        self.detalhes_container.controls.clear()
        
        # Adiciona o resumo geral da sessão
        pontuacao_total = jogo_selecionado.get("pontuacao_total", 0)
        usuario = jogo_selecionado.get("usuario", "N/A")
        data_fim = jogo_selecionado.get("data_hora_fim", "N/A")
        
        resumo_geral = ft.Container(
            content=ft.Column([
                ft.Text(f"Análise da Sessão de {data_fim}", size=22, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Text(f"Usuário: {usuario}", size=18),
                ft.Text(f"Pontuação Final: {pontuacao_total}", size=18, weight=ft.FontWeight.BOLD),
            ]),
            padding=15,
            margin=ft.margin.only(bottom=10),
            border_radius=10,
            bgcolor=ft.colors.with_opacity(0.05, ft.colors.BLUE),
        )
        self.detalhes_container.controls.append(resumo_geral)
        
        # Adiciona o card de detalhes para cada fase
        for fase in jogo_selecionado.get("resumo_fases", []):
            self.detalhes_container.controls.append(self._criar_card_fase(fase))

    def _criar_card_fase(self, fase):
        """Cria um Card com todas as estatísticas de uma única fase."""
        
        # Dados principais
        nome_fase = fase.get("fase", "N/A")
        pontuacao = fase.get("pontuacao", 0)
        tentativas = fase.get("tentativas_incorretas_total", 0)
        tempo_total = fase.get("tempo_total_gasto", 0)

        # Métricas comportamentais
        tempo_reacao = fase.get("tempo_reacao_primeiro_clique", 0)
        tempo_deliberacao = fase.get("tempo_medio_deliberacao_entre_cliques", 0)
        uso_dicas = fase.get("frequencia_uso_dica", 0)

        # Padrão de tentativas
        sequencia_final = " ".join(fase.get("sequencia_final_cliques", []))
        sequencias_erradas = fase.get("tentativas_com_sequencias_erradas", [])
        
        # Conteúdo do painel de análise de cliques
        conteudo_analise_cliques = [
            ft.Text("Sequência Correta de Cliques:", weight=ft.FontWeight.BOLD),
            ft.Text(sequencia_final, font_family="monospace", color=ft.colors.GREEN_800),
            ft.Divider(height=10, color=ft.colors.TRANSPARENT)
        ]
        if sequencias_erradas:
            conteudo_analise_cliques.append(ft.Text("Tentativas com Sequência Incorreta:", weight=ft.FontWeight.BOLD))
            for i, tentativa in enumerate(sequencias_erradas):
                conteudo_analise_cliques.append(ft.Text(f"{i+1}: {tentativa}", font_family="monospace", color=ft.colors.RED_800))
        else:
            conteudo_analise_cliques.append(ft.Text("Nenhuma sequência incorreta foi submetida.", italic=True))

        return ft.Card(
            elevation=4,
            content=ft.Container(
                padding=15,
                content=ft.Column([
                    ft.Text(nome_fase, size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    # Métricas Principais
                    ft.Row([
                        ft.Text(f"🏆 Pontos: {pontuacao}", size=16),
                        ft.Text(f"❌ Tentativas Incorretas: {tentativas}", size=16),
                        ft.Text(f"⏱️ Tempo Total: {tempo_total}s", size=16),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(),
                    # Métricas Comportamentais
                    ft.Text("Métricas Comportamentais", size=16, weight=ft.FontWeight.BOLD, italic=True),
                    ft.Text(f"- Tempo de Reação (1º clique): {tempo_reacao}s"),
                    ft.Text(f"- Tempo Médio entre Cliques: {tempo_deliberacao}s"),
                    ft.Text(f"- Dicas Usadas: {uso_dicas} vez(es)"),
                    ft.Divider(),
                    # Análise de Cliques (Expansível)
                    ft.ExpansionPanelList(
                        expand_icon_color=ft.colors.BLUE,
                        elevation=0,
                        controls=[
                            ft.ExpansionPanel(
                                header=ft.Text("Analisar Padrão de Tentativas", weight=ft.FontWeight.BOLD),
                                content=ft.Column(conteudo_analise_cliques),
                            )
                        ]
                    )
                ])
            )
        )

    def _criar_layout_principal(self):
        """Cria a estrutura principal da página, com o seletor e o container de detalhes."""
        
        # Cria as opções para o Dropdown
        opcoes_dropdown = [
            ft.dropdown.Option(key=str(i), text=f"Sessão de {jogo.get('data_hora_fim', 'Data Desconhecida')}")
            for i, jogo in enumerate(self.todas_as_sessoes)
        ]

        # Cria o Dropdown, se houver sessões para mostrar
        if opcoes_dropdown:
            self.dropdown_sessoes = ft.Dropdown(
                label="Selecione uma Sessão de Jogo para Analisar",
                options=opcoes_dropdown,
                value=str(len(self.todas_as_sessoes) - 1),  # Seleciona a mais recente por padrão
                on_change=self._sessao_selecionada,
                border_color=ft.colors.BLUE
            )
        
        # Layout final
        main_column = ft.Column(
            [
                ft.Text("📊 Estatísticas de Desempenho", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row(
                    [
                        self.dropdown_sessoes if self.dropdown_sessoes else ft.Text("Nenhum jogo foi finalizado ainda."),
                        ft.ElevatedButton("🏠 Voltar ao Menu", on_click=lambda e: self.page.go("/play"), icon=ft.icons.HOME)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),
                ft.Divider(height=20, thickness=2),
                self.detalhes_container, # Container que será preenchido dinamicamente
            ],
            spacing=10,
            width=800,  # Largura fixa para melhor legibilidade
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
        
        # Container para centralizar a coluna principal
        return ft.Container(
            content=main_column,
            alignment=ft.alignment.top_center,
            padding=20,
            expand=True,
        )