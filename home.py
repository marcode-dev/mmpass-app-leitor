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
                padding=12,
                border_radius=20,
                bgcolor="white",
                shadow=ft.BoxShadow(
                    blur_radius=10,
                    color="#10000000",
                    offset=ft.Offset(0, 4)
                ),
                on_click=on_evento_click,
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

    async def on_logout_click(e):
        await logout(page)

    layout = ft.Stack([
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
                                on_click=on_logout_click,
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

    # Se viemos de um scan, abre o evento automaticamente
    try:
        ev_id_query = page.query.get("evento_id") if hasattr(page.query, "get") else None
    except:
        ev_id_query = None
        
    if ev_id_query:
        for e in eventos:
            if str(e["id"]) == str(ev_id_query):
                # Abre o evento que estávamos escaneando
                await abrir_evento(e, page)
                break
                
    return layout
