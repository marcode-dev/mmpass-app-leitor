import flet as ft
from components import *
from services.api import get_eventos

# -------------------------
# HOME  
# -------------------------

def tela_home(page, abrir_evento, logout):
    from state import usuario_logado
    eventos = get_eventos(usuario_logado["id"])
    nome = usuario_logado.get("nome", "Usuário")

    lista = ft.Column(
        scroll="auto",
        expand=True,
        spacing=10
    )

    if not eventos:
        lista.controls.append(
            ft.Text("Nenhum evento encontrado", color="grey")
        )

    for e in eventos:
        lista.controls.append(
            ft.Container(
                padding=12,
                border_radius=20,
                bgcolor="white",
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color="#10000000",
                    offset=ft.Offset(0, 4)
                ),
                on_click=lambda _, ev=e: abrir_evento(ev, page),
                content=ft.Row(
                    spacing=10,
                    controls=[
                        ft.Image(
                            src=e.get("imagem") or "https://via.placeholder.com/60",
                            width=60,
                            height=60,
                            fit=ft.BoxFit.COVER
                        ),
                        ft.Column(
                            spacing=2,
                            controls=[
                                ft.Text(e["nome"], weight="bold", size=14),
                                ft.Text(
                                    f'{e["data"]} • {e["local"]}',
                                    size=11,
                                    color="grey"
                                ),
                                ft.Text(
                                    f'R$ {e["preco"]}',
                                    size=12,
                                    color="#EF4444"
                                )
                            ]
                        )
                    ]
                )
            )
        )

    return ft.Stack([
        fundo(),

        ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                expand=True,
                spacing=15,
                controls=[

                    # 🔥 HEADER COM LOGOUT
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(
                                spacing=2,
                                controls=[
                                    ft.Text(
                                        f"Olá, {nome}",
                                        size=20,
                                        weight="bold"
                                    ),
                                    ft.Text(
                                        "Seus eventos",
                                        size=14,
                                        color="grey"
                                    ),
                                ]
                            ),

                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                border_radius=20,
                                bgcolor="#FEE2E2",
                                on_click=lambda e: logout(e, page),
                                content=ft.Text(
                                    "Sair",
                                    color="red",
                                    weight="bold"
                                )
                            )
                        ]
                    ),

                    # 📋 LISTA
                    lista
                ]
            )
        )
    ])