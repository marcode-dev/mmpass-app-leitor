import flet as ft
from components import *
from scan import tela_scan

# -------------------------
# EVENTO
# -------------------------
async def tela_evento(evento, page, abrir_evento, ir_home):
    total = evento.get("ingressos_vendidos", 0)
    capacidade = evento.get("capacidade", 100)

    # Labels formatadas
    contador = ft.Text(str(total), size=24, weight="w800", color="#1E293B")
    porcento = ft.Text(f"{int((total/capacidade)*100)}%", size=24, weight="w800", color="#6366F1")
    
    mural = ft.Column(spacing=8)

    async def on_back(e):
        await ir_home(page)

    async def ir_scan(e):
        conteudo.controls.clear()
        conteudo.controls.append(await tela_scan(evento, contador, porcento, mural, page, abrir_evento))
        page.update()

    # Card Centralizado
    card_evento = ft.Container(
        width=400,
        padding=30,
        border_radius=30,
        bgcolor="#FFFFFF",
        shadow=ft.BoxShadow(
            blur_radius=40,
            color="#0000001A",
            offset=ft.Offset(0, 10)
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=25,
            controls=[
                # Cabeçalho com botão voltar
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[botao_voltar(on_back)]
                ),
                
                # Banner e Título
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=12,
                    controls=[
                        ft.Container(
                            width=100,
                            height=100,
                            border_radius=22,
                            content=ft.Image(
                                src=evento.get("imagem") or "https://via.placeholder.com/100",
                                fit=ft.BoxFit.COVER,
                                border_radius=22
                            ),
                            shadow=ft.BoxShadow(blur_radius=20, color="#00000011")
                        ),

                        ft.Text(evento["nome"], size=28, weight="w800", color="#1E293B", text_align="center"),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Icon(ft.Icons.CALENDAR_MONTH, size=16, color="#64748B"),
                                ft.Text(evento["data"], size=14, color="#64748B"),
                                ft.Container(width=10),
                                ft.Icon(ft.Icons.LOCATION_ON, size=16, color="#64748B"),
                                ft.Text(evento["local"], size=14, color="#64748B"),
                            ]
                        )
                    ]
                ),

                # Estatísticas
                ft.Container(
                    padding=20,
                    border_radius=22,
                    bgcolor="#F8FAFC",
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        controls=[
                            ft.Column([
                                ft.Text("PRESENTES", size=10, color="#94A3B8", weight="w700"),
                                contador,
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            ft.VerticalDivider(color="#E2E8F0"),
                            ft.Column([
                                ft.Text("CAPACIDADE", size=10, color="#94A3B8", weight="w700"),
                                ft.Text(str(evento["capacidade"]), size=24, weight="w800", color="#1E293B"),
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                            ft.VerticalDivider(color="#E2E8F0"),
                            ft.Column([
                                ft.Text("OCUPAÇÃO", size=10, color="#94A3B8", weight="w700"),
                                porcento,
                            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                        ]
                    )
                ),

                # Mural
                ft.Column([
                    ft.Text("ÚLTIMAS ENTRADAS", size=11, weight="w700", color="#94A3B8"),
                    ft.Column([mural], height=100, scroll="auto")
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),

                botao_gradiente("Iniciar Leitura", ir_scan)
            ]
        )
    )

    layout = ft.Stack([
        fundo(),
        ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            content=card_evento
        )
    ])

    return layout