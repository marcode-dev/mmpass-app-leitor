import flet as ft
from components import *
from services.api import get_eventos

# -------------------------
# HOME  
# -------------------------

async def tela_home(page, abrir_evento, logout):
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
        async def on_evento_click(ev_target, ev_data=e):
            await abrir_evento(ev_data, page)

        lista.controls.append(
            ft.Container(
                padding=16,
                border_radius=22,
                bgcolor="#FFFFFF",
                shadow=ft.BoxShadow(
                    blur_radius=20,
                    color="#0000000D",
                    offset=ft.Offset(0, 4)
                ),
                on_click=on_evento_click,
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
                content=ft.Row(
                    spacing=15,
                    controls=[
                        ft.Container(
                            width=64,
                            height=64,
                            border_radius=16,
                            content=ft.Image(
                                src=e.get("imagem") or "https://via.placeholder.com/64",
                                fit=ft.BoxFit.COVER,
                                border_radius=16
                            )
                        ),

                        ft.Column(
                            expand=True,
                            spacing=4,
                            controls=[
                                ft.Text(e["nome"], weight="w700", size=16, color="#1E293B"),
                                ft.Row([
                                    ft.Icon(ft.Icons.CALENDAR_MONTH, size=14, color="#64748B"),
                                    ft.Text(e["data"], size=12, color="#64748B"),
                                    ft.Icon(ft.Icons.LOCATION_ON, size=14, color="#64748B"),
                                    ft.Text(e["local"], size=12, color="#64748B"),
                                ], spacing=5),
                                ft.Text(
                                    f'A partir de R$ {e["preco"]}',
                                    size=13,
                                    weight="w600",
                                    color="#6366F1"
                                )
                            ]
                        ),
                        ft.Icon(ft.Icons.CHEVRON_RIGHT, color="#CBD5E1")
                    ]
                )
            )
        )

    async def on_logout_click(e):
        await logout(page)

    layout = ft.Stack([
        fundo(),

        ft.Container(
            expand=True,
            padding=ft.Padding(20, 50, 20, 20),
            content=ft.Column(
                expand=True,
                spacing=25,
                controls=[

                    # 🔥 HEADER PREMIUM
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        f"Bem-vindo,",
                                        size=14,
                                        color="#94A3B8",
                                        weight="w500"
                                    ),
                                    ft.Text(
                                        nome,
                                        size=28,
                                        weight="w800",
                                        color="#1E293B"
                                    ),
                                ]
                            ),

                            ft.Container(
                                padding=12,
                                border_radius=15,
                                bgcolor="#FEE2E2",
                                on_click=on_logout_click,
                                content=ft.Icon(ft.Icons.LOGOUT, color="#EF4444", size=20)
                            )

                        ]
                    ),



                    
                    ft.Text("Eventos sob sua gestão", size=14, color="#94A3B8", weight="w600"),

                    # 📋 LISTA
                    lista
                ]
            )
        )
    ])


    return layout
