import flet as ft
from components import *
import cv2
import threading
import time
from services.api import login as validar_qr    

# -------------------------
# SCAN
# -------------------------
def tela_scan(evento, contador, porcento, mural, page, abrir_evento):
    rodando = True
    ultimo = None

    status = ft.Text("Aguardando leitura...", size=12, color="#6B7280")

    def voltar(e):
        nonlocal rodando
        rodando = False
        abrir_evento(evento, page)

    
    def scan():
        nonlocal rodando, ultimo

        cap = cv2.VideoCapture(0)
        detector = cv2.QRCodeDetector()

        if not cap.isOpened():
            status.value = "Erro ao acessar câmera"
            page.update()
            return
        while rodando:
            ret, frame = cap.read()
            if not ret:
                break

            # Detecta QR Code
            data, bbox, _ = detector.detectAndDecode(frame)
            # Se encontrou QR
            if data:
                qr = data.strip()
                # Evita leituras repetidas
                if qr == ultimo:
                    cv2.imshow("ESC para sair", frame)
                    if cv2.waitKey(1) == 27:
                        break
                    continue
                ultimo = qr

                # Faz validação
                r = validar_qr(qr, evento["id"])

                if r["status"] == "ok":
                    mural.controls.insert(
                        0,
                        ft.Text(f"✔ {r['nome']}", color="green")
                    )
                    total = r["total"]
                    contador.value = str(total)
                    porcento.value = (
                        f"{int((total/evento['capacidade'])*100)}%"
                    )
                    status.value = "Entrada liberada"
                else:
                    mural.controls.insert(
                        0,
                        ft.Text(f"❌ {r['msg']}", color="red")
                    )
                    status.value = r["msg"]
                page.update()
                # Pequeno delay para evitar múltiplas leituras
                time.sleep(1)

            # Desenha área detectada
            if bbox is not None:
                pontos = bbox.astype(int)
                for i in range(len(pontos[0])):
                    pt1 = tuple(pontos[0][i])
                    pt2 = tuple(pontos[0][(i + 1) % len(pontos[0])])
                    cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

            cv2.imshow("ESC para sair", frame)
            if cv2.waitKey(1) == 27:
                break
        cap.release()
        cv2.destroyAllWindows()

    

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
                ft.Text("⌁ ⌁", size=30, color="#9CA3AF"),
                status
            ]
        )
    )

    botao_scan = ft.Container(
        height=50,
        border_radius=25,
        alignment=ft.Alignment(0, 0),
        gradient=ft.LinearGradient(
            colors=["#5EEAD4", "#A78BFA"]
        ),
        on_click=lambda e: threading.Thread(target=scan, daemon=True).start(),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text("📷", size=16),
                ft.Text("Iniciar leitura", color="white", weight="bold")
            ]
        )
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
                            "Aponte a câmera para o QR Code",
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
                                    ft.Text("🖼"),
                                    ft.Text("Selecionar da Galeria", size=12)
                                ]
                            )
                        )
                    ]
                )
            )
        )
    ])