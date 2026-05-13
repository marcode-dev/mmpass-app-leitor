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

async def abrir_evento(ev, page):
    from evento import tela_evento
    conteudo.controls.clear()
    conteudo.controls.append(await tela_evento(ev, page, abrir_evento, ir_home))
    page.update()

async def abrir_scan_direto(ev, page, code):
    from scan import tela_scan
    # Primeiro carregamos a estrutura do evento para ter as referências de UI
    from evento import tela_evento
    # Criamos a tela de evento mas não a exibimos ainda, apenas para pegar os componentes
    # Na verdade, é melhor ir para a tela de evento e de lá para o scan
    conteudo.controls.clear()
    # Mockando os componentes que o scan precisa
    contador = ft.Text("...", size=24, weight="w800", color="#1E293B")
    porcento = ft.Text("...%", size=24, weight="w800", color="#6366F1")
    mural = ft.Column(spacing=8)
    from scan import tela_scan
    conteudo.controls.append(await tela_scan(ev, contador, porcento, mural, page, abrir_evento))
    page.update()

async def main(page: ft.Page):
    page.title = "MMReader"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = None

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
            from services.api import get_eventos
            eventos = get_eventos(usuario_logado["id"])
            evento = next((e for e in eventos if str(e["id"]) == str(evento_id)), None)
            if evento:
                await abrir_scan_direto(evento, page, code)
            else:
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

