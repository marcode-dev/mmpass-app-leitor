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
        width=320,
        padding=25,
        border_radius=30,
        bgcolor="#FFFFFF",
        border=ft.border.all(1, "#F1F5F9"),
        shadow=ft.BoxShadow(
            blur_radius=25,
            color="#12000000",
            offset=ft.Offset(0, 8)
        ),
        content=ft.Column(
            tight=True,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("MMReader", size=36, weight="w700", color="#5EEAD4"),
                ft.Text(
                    "Sua próxima experiência começa aqui.",
                    size=12,
                    color="#9CA3AF",
                    text_align="center"
                ),
                ft.Container(height=15),
                email,
                senha,
                mensagem,
                ft.Container(height=8),
                botao_gradiente("Entrar", login_click),
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