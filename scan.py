import flet as ft
from components import *
from services.api import validar_qr    

# -------------------------
# SCAN
# -------------------------
async def tela_scan(evento, contador, porcento, mural, page, abrir_evento):
    status = ft.Text("Aguardando leitura...", size=12, color="#6B7280")

    async def voltar(e):
        # Desinscreve para evitar múltiplas execuções se a tela for aberta novamente
        page.pubsub.unsubscribe_all()
        await abrir_evento(evento, page)

    async def processar_codigo(qr):
        # Evita processar se não for um código válido
        if not qr:
            return
            
        # Faz validação
        r = validar_qr(qr, evento["id"])

        if r["status"] == "ok":
            mural.controls.insert(
                0,
                ft.Container(
                    content=ft.Text(f"✔ {r['nome']}", color="green", weight="bold"),
                    animate_opacity=300
                )
            )
            total = r["total"]
            contador.value = str(total)
            porcento.value = (
                f"{int((total/evento['capacidade'])*100)}%"
            )
            status.value = f"Liberado: {r['nome']}"
            status.color = "green"
        else:
            mural.controls.insert(
                0,
                ft.Text(f"❌ {r['msg']}", color="red")
            )
            status.value = r["msg"]
            status.color = "red"
        
        page.update()

    # Se inscreve para receber os códigos vindos do scanner via JS Bridge (se suportado)
    try:
        page.pubsub.subscribe(processar_codigo)
    except:
        pass

    async def iniciar_leitura(e):
        status.value = "Abrindo câmera..."
        status.color = "#6B7280"
        page.update()


    # ---------------------------------------------------------
    # LÓGICA DE RETORNO VIA URL (COMPATIBILIDADE)
    # ---------------------------------------------------------
    try:
        query_code = page.query.get("code") if hasattr(page.query, "get") else None
        query_ev_id = page.query.get("evento_id") if hasattr(page.query, "get") else None
    except:
        query_code = None
        query_ev_id = None
    
    if query_code and str(query_ev_id) == str(evento["id"]):
        # Se voltamos do scanner via redirecionamento
        await processar_codigo(query_code)
    # ---------------------------------------------------------

    # ---------------- UI BONITA ----------------



    area_scan = ft.Container(
        height=220,
        border_radius=25,
        bgcolor="#F3F4F6",
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.QR_CODE, size=50, color="#9CA3AF"),
                ft.Text("Scanner Browser Ativo", size=16, weight="bold", color="#4B5563"),
                status
            ]
        )
    )

    botao_scan = ft.ElevatedButton(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.CAMERA_ALT, color="white", size=20),
                ft.Text("Abrir Câmera no Navegador", color="white", weight="bold")
            ]
        ),
        bgcolor="#5EEAD4",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=25),
            padding=15,
        ),
        # A propriedade 'url' é nativa para abrir links em novas abas
        url=f"scanner.html?evento_id={evento['id']}",
        on_click=iniciar_leitura
    )



    return ft.Stack([
        fundo(),

        ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                width=350,
                padding=25,
                border_radius=30,
                bgcolor="white",
                shadow=ft.BoxShadow(
                    blur_radius=25,
                    color="#12000000",
                    offset=ft.Offset(0, 10)
                ),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[

                        botao_voltar(voltar),

                        ft.Text(
                            "MMPass",
                            size=26,
                            weight="bold",
                            color="#8B5CF6"
                        ),

                        ft.Text(
                            "Leitor de QR Code",
                            size=14,
                            color="#6B7280"
                        ),

                        ft.Text(
                            "A verificação agora é feita via navegador para maior compatibilidade.",
                            size=11,
                            color="#9CA3AF",
                            text_align="center"
                        ),

                        area_scan,

                        botao_scan,

                        ft.Text("ou", size=12, color="grey"),

                        ft.Container(
                            padding=10,
                            border_radius=20,
                            border=ft.border.all(1, "#D1D5DB"),
                            content=ft.Row(
                                alignment=ft.MainAxisAlignment.CENTER,
                                controls=[
                                    ft.Icon(ft.Icons.IMAGE, size=16, color="#6B7280"),
                                    ft.Text("Selecionar da Galeria", size=12)
                                ]
                            )
                        )
                    ]
                )
            )
        )
    ])
