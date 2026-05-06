import flet as ft
from components import *
from scan import tela_scan

# -------------------------
# EVENTO
# -------------------------
def tela_evento(evento, page, abrir_evento, ir_home):
    total = evento.get("ingressos_vendidos", 0)
    capacidade = evento.get("capacidade", 100)

    # Labels formatadas
    contador = ft.Text(str(total), size=24, weight="bold", color="#1F2937")
    porcento = ft.Text(f"{int((total/capacidade)*100)}%", size=24, weight="bold", color="#1F2937")
    
    mural = ft.Column(spacing=5)

    def ir_scan(e):
        conteudo.controls.clear()
        conteudo.controls.append(tela_scan(evento, contador, porcento, mural, page, abrir_evento))
        page.update()

    # Card Centralizado
    card_evento = ft.Container(
        width=350,
        padding=25,
        border_radius=30,
        bgcolor="#FFFFFF",
        shadow=ft.BoxShadow(
            blur_radius=25,
            color="#12000000",
            offset=ft.Offset(0, 8)
        ),
        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                # Cabeçalho com botão voltar
                ft.Row(
                    alignment=ft.MainAxisAlignment.START,
                    controls=[botao_voltar(lambda e: ir_home(page))]
                ),
                
                # Título do Evento
                ft.Text(evento["nome"], size=28, weight="w700", color="#8B5CF6", text_align="center"),
                
                # Imagem com bordas arredondadas (estilo banner)
                ft.Container(
                    content=ft.Image(
                        src=evento.get("imagem"), 
                        height=160, 
                        fit=ft.BoxFit.COVER,
                        border_radius=15
                    ),
                    border_radius=15,
                ),

                # Grid de Informações (Ingressos | Ocupação | Status)
                ft.Container(
                    padding=15,
                    bgcolor="#F8FAFC",
                    border_radius=20,
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        controls=[
                            ft.Column([ft.Text("Ingressos", size=11, color="#64748B"), contador], horizontal_alignment="center"),
                            ft.VerticalDivider(color="#E2E8F0"),
                            ft.Column([ft.Text("Ocupação", size=11, color="#64748B"), porcento], horizontal_alignment="center"),
                            ft.VerticalDivider(color="#E2E8F0"),
                            ft.Column([
                                ft.Text("Status", size=11, color="#64748B"), 
                                ft.Text("Ativo", size=16, weight="bold", color="#10B981")
                            ], horizontal_alignment="center"),
                        ]
                    )
                ),

                # Botão de Ação Principal
                botao_gradiente("Iniciar Leitura", ir_scan),

                # Lista de entradas recentes
                ft.Column(
                    controls=[
                        ft.Text("Entradas Recentes", size=14, weight="bold", color="#4B5563"),
                        ft.Container(
                            content=mural,
                            height=100, # Limita altura para não quebrar o layout
                            padding=5
                        )
                    ]
                )
            ]
        )
    )

    return ft.Stack([
        fundo(), # Mantém o fundo de bolhas consistente
        ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            content=card_evento
        )
    ])