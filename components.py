import flet as ft
"""
from login import tela_login
from home import tela_home
from evento import tela_evento
"""

# -------------------------
# FUNDO COM BOLHAS
# -------------------------
def fundo():
    return ft.Stack([
        ft.Container(
            expand=True,
            gradient=ft.LinearGradient(
                begin=ft.Alignment(-1, -1),
                end=ft.Alignment(1, 1),
                colors=["#D1F5F7", "#F2E9F3"], # Cores claras originais
            ),
        ),
        ft.Container(width=400, height=400, bgcolor="#90E0EF",
                        border_radius=200, left=-150, top=-100, opacity=0.3, blur=ft.Blur(50, 50)),
        ft.Container(width=350, height=350, bgcolor="#C8B6FF",
                        border_radius=175, right=-120, top=100, opacity=0.3, blur=ft.Blur(50, 50)),
    ])



# -------------------------
# BOTÕES
# -------------------------
def botao_gradiente(texto, funcao):
    return ft.Container(
        height=54,
        border_radius=16,
        alignment=ft.Alignment(0, 0),
        gradient=ft.LinearGradient(colors=["#5EEAD4", "#A78BFA"]), # Cores vibrantes
        shadow=ft.BoxShadow(
            blur_radius=15,
            color="#00000022", # Sombra cinza neutra
            offset=ft.Offset(0, 5)
        ),

        animate=ft.Animation(300, ft.AnimationCurve.DECELERATE),
        content=ft.Text(texto, color="white", weight="w700", size=16),
        on_click=funcao
    )



def botao_voltar(funcao):
    return ft.Container(
        padding=ft.Padding(12, 6, 12, 6),
        border_radius=20,
        bgcolor="#E0F2FE",
        on_click=funcao,
        content=ft.Row(
            spacing=5,
            controls=[
                ft.Text("←", weight="bold"),
                ft.Text("Voltar")
            ]
        )
    )


conteudo = ft.Column(expand=True)