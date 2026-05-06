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
                colors=["#D1F5F7", "#F2E9F3"],
            ),
        ),
        ft.Container(width=400, height=400, bgcolor="#90E0EF",
                        border_radius=200, left=-150, top=-100, opacity=0.3),
        ft.Container(width=350, height=350, bgcolor="#C8B6FF",
                        border_radius=175, right=-120, top=100, opacity=0.3),
        ft.Container(width=300, height=300, bgcolor="#FFD6FF",
                        border_radius=150, left=40, bottom=-80, opacity=0.3),
    ])

# -------------------------
# BOTÕES
# -------------------------
def botao_gradiente(texto, funcao):
    return ft.Container(
        height=50,
        border_radius=20,
        alignment=ft.Alignment(0, 0),
        gradient=ft.LinearGradient(colors=["#5EEAD4", "#A78BFA"]),
        content=ft.Text(texto, color="white", weight="w600"),
        on_click=funcao
    )

def botao_voltar(funcao):
    return ft.Container(
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
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