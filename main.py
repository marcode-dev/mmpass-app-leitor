import flet as ft

from login import tela_login
from home import tela_home
from evento import tela_evento

from components import *

async def ir_home(page):
    conteudo.controls.clear()
    conteudo.controls.append(await tela_home(page, abrir_evento, logout))
    page.update()

async def logout(page):
    from state import usuario_logado
    usuario_logado.clear()
    await page.shared_preferences.remove("usuario") # Limpa persistência
    
    conteudo.controls.clear()
    conteudo.controls.append(tela_login(page, ir_home))
    page.update()

async def abrir_evento(ev, page, auto_code=None):
    from scan import tela_scan
    # Se tiver auto_code, a tela_scan vai processar na inicialização (via query)
    conteudo.controls.clear()
    conteudo.controls.append(await tela_evento(ev, page, abrir_evento, ir_home))
    page.update()

async def main(page: ft.Page):
    page.title = "MMReader"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT

    # -------------------------
    # RESTAURAR SESSÃO
    # -------------------------
    from state import usuario_logado
    import json
    
    saved_user = await page.shared_preferences.get("usuario")
    if saved_user:
        usuario_logado.update(json.loads(saved_user))

    # -------------------------
    # START
    # -------------------------
    page.add(conteudo)

    # Verifica se estamos voltando de um scan via URL
    # Ex: /?code=123&evento_id=456
    try:
        code = page.query.get("code") if hasattr(page.query, "get") else None
        evento_id = page.query.get("evento_id") if hasattr(page.query, "get") else None
    except:
        code = None
        evento_id = None

    if usuario_logado:

        if code and evento_id:
            await ir_home(page)
        else:
            await ir_home(page)
    else:
        conteudo.controls.clear()
        conteudo.controls.append(tela_login(page, ir_home))

    page.update()


# Usando ft.app que é o padrão moderno
try:
    ft.app(target=main, assets_dir="assets")
except Exception:
    import flet.app
    ft.run(main, assets_dir="assets")
