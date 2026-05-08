import flet as ft
from components import *
from services.api import login as api_login

# -------------------------
# LOGIN
# -------------------------
def tela_login(page, ir_home):
    email = ft.TextField(
        hint_text="Email",
        width=300,
        border_radius=12,
        filled=True,
        bgcolor="#F3F4F6",
        border_color="transparent",
    )

    senha = ft.TextField(
        hint_text="Senha",
        password=True,
        can_reveal_password=True,
        width=300,
        border_radius=12,
        filled=True,
        bgcolor="#F3F4F6",
        border_color="transparent",
    )

    mensagem = ft.Text("", color="red")

    async def login_click(e):
        from state import usuario_logado

        if not email.value or not senha.value:
            mensagem.value = "Preencha todos os campos"
            page.update()
            return

        r = api_login(email.value, senha.value)
        
        if r["status"] == "sucesso":
            import json
            usuario_logado.update(r["usuario"])
            # Salva no navegador para persistir após reload
            await page.shared_preferences.set("usuario", json.dumps(r["usuario"]))
            await ir_home(page)
        else:
            mensagem.value = r.get("msg", "Erro no login")
            page.update()


    card_login = ft.Container(
        width=340,
        padding=35,
        border_radius=28,
        bgcolor="#FFFFFF",
        shadow=ft.BoxShadow(
            blur_radius=40,
            color="#00000033",
            offset=ft.Offset(0, 20)
        ),
        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=5,
                    controls=[
                        ft.Text("MMPass", size=42, weight="w800", color="#A78BFA"),
                        ft.Text(
                            "REDE DE ACESSO",
                            size=12,
                            weight="w600",
                            color="#94A3B8"

                        ),
                    ]
                ),
                ft.Column(
                    spacing=12,
                    controls=[
                        email,
                        senha,
                    ]
                ),
                mensagem,
                ft.Column(
                    spacing=10,
                    controls=[
                        botao_gradiente("Acessar Painel", login_click),
                        ft.Text(
                            "Esqueceu sua senha?",
                            size=12,
                            color="#64748B",
                            text_align="center",
                            weight="w500"
                        ),
                    ]
                )
            ]
        )
    )


    return ft.Stack(
        expand=True,
        controls=[
            fundo(),  # bolhas

            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),  # CENTRO REAL
                content=card_login
            )
        ]
    )