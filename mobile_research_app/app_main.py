import flet as ft
import random
import os
from assets_manager import get_experiment_images
from session_handler import ExperimentSession

def main(page: ft.Page):
    page.title = "Pesquisa de Percepção IA"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 450
    page.window_height = 800
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Estado global do app
    state = {
        "sessao": None,
        "user_info": {"id": f"ID-{random.randint(1000, 9999)}", "perfil": None}
    }

    def navegar_para(layout):
        page.clean()
        page.add(layout)
        page.update()

    def iniciar_experimento(perfil):
        state["user_info"]["perfil"] = perfil
        lista = get_experiment_images()
        if lista:
            state["sessao"] = ExperimentSession(lista)
            navegar_para(tela_gameplay())
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao carregar imagens!"), open=True)
            page.update()

    # --- TELAS ---
    def tela_inicial():
        return ft.Column([
            ft.Icon(ft.Icons.ANALYTICS, size=80, color=ft.Colors.BLUE_400),
            ft.Text("CAPTCHA TRUST AI", size=28, weight="bold"),
            ft.Container(height=40),
            ft.Button("INICIAR PESQUISA", width=280, height=60, 
                      on_click=lambda _: navegar_para(tela_cadastro())),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def tela_cadastro():
        return ft.Column([
            ft.Text("SELECIONE SEU PERFIL", size=22, weight="bold"),
            ft.Container(height=20),
            ft.Button("SOU ESTUDANTE", width=300, height=55, on_click=lambda _: iniciar_experimento("Estudante")),
            ft.Button("SOU PROFESSOR / TÉCNICO", width=300, height=55, on_click=lambda _: iniciar_experimento("Professor")),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def tela_gameplay():
        sessao = state["sessao"]
        img_data = sessao.get_current_image()
        
        if not img_data:
            return tela_final()

        # Lógica de Rounds: 20 rounds de 4 imagens (Total 80)
        idx = sessao.index_atual
        num_round = (idx // 4) + 1
        num_img_round = (idx % 4) + 1
        
        sessao.iniciar_cronometro()

        return ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(f"ROUND {num_round}/20", size=20, weight="bold", color="blue400"),
                    ft.Text(f"Imagem {num_img_round}/4", size=14, color="grey"),
                ], spacing=0),
                ft.Text(state["user_info"]["id"], size=12)
            ], alignment="spaceBetween", width=350),
            
            ft.ProgressBar(value=(idx + 1) / len(sessao.lista_imagens), width=350),
            
            ft.Container(
                content=ft.Image(src=img_data["url"], width=320, height=320, fit="cover"),
                border=ft.Border.all(2, "grey800"),
                border_radius=15,
            ),
            
            ft.Text("Esta imagem é Humana ou IA?", size=16),
            
            ft.Row([
                ft.Button("HUMANO", bgcolor="blue900", color="white", expand=True, height=60,
                          on_click=lambda _: registrar("human")),
                ft.Button("IA", bgcolor="red900", color="white", expand=True, height=60,
                          on_click=lambda _: registrar("ai")),
            ], width=350),
        ], horizontal_alignment="center", spacing=20)

    def registrar(escolha):
        state["sessao"].registrar_resposta(escolha)
        navegar_para(tela_gameplay())

    def tela_final():
        return ft.Column([
            ft.Icon(ft.Icons.CHECK_CIRCLE, color="green", size=80),
            ft.Text("OBRIGADO!", size=30, weight="bold"),
            ft.Text("Seus dados foram processados."),
            ft.Button("SAIR", on_click=lambda _: page.window_destroy())
        ], horizontal_alignment="center")

    page.add(tela_inicial())

if __name__ == "__main__":
    # Caminho local (já que você deu o 'cp' para a pasta assets)
    import os
    assets_path = os.path.join(os.getcwd(), "assets")
    ft.app(target=main, assets_dir=assets_path, view=ft.AppView.WEB_BROWSER, port=8550)
