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

    # ---------------- UI PREMIUM ----------------

    area_scan = ft.Container(
        height=240,
        border_radius=24,
        bgcolor="#F8FAFC",
        border=ft.Border.all(2, "#E2E8F0"),
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
            controls=[
                ft.Container(
                    padding=20,
                    border_radius=50,
                    bgcolor="#EEF2FF",
                    content=ft.Icon(ft.Icons.QR_CODE_SCANNER, size=40, color="#6366F1"),
                ),
                ft.Column([
                    ft.Text("PRONTO PARA SCAN", size=14, weight="w700", color="#1E293B"),
                    status,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=5),
            ]
        )
    )

    botao_scan = ft.ElevatedButton(
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Icon(ft.Icons.CAMERA_ALT, color="white", size=20),
                ft.Text("ABRIR SCANNER NO NAVEGADOR", color="white", weight="w700", size=14)
            ]
        ),
        bgcolor="#6366F1",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=16),
            padding=20,
            elevation=10,
            shadow_color="#00000022"
        ),
        url=f"scanner.html?evento_id={evento['id']}",
        on_click=iniciar_leitura
    )

    return ft.Stack([
        fundo(),

        ft.Container(
            expand=True,
            alignment=ft.Alignment(0, 0),
            content=ft.Container(
                width=380,
                padding=35,
                border_radius=32,
                bgcolor="#FFFFFF",
                shadow=ft.BoxShadow(
                    blur_radius=50,
                    color="#0000001A",
                    offset=ft.Offset(0, 20)
                ),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=25,
                    controls=[
                        ft.Row(
                            alignment=ft.MainAxisAlignment.START,
                            controls=[botao_voltar(voltar)],
                        ),

                        ft.Column([
                            ft.Text("MMPass", size=32, weight="w800", color="#6366F1"),
                            ft.Text("VALIDAÇÃO DE ACESSO", size=11, color="#94A3B8", weight="w700"),
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),

                        ft.Text(
                            "A verificação agora é feita via navegador para maior estabilidade e performance.",
                            size=12,
                            color="#64748B",
                            text_align="center",
                            weight="w500"
                        ),

                        area_scan,

                        botao_scan
                    ]
                )
            )
        )
    ])
