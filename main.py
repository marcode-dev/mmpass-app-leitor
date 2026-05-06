import flet as ft

from login import tela_login
from home import tela_home
from evento import tela_evento

from components import *

def ir_home(page):
    conteudo.controls.clear()
    conteudo.controls.append(tela_home(page, abrir_evento, logout))
    page.update()

def logout(page):
    from state import usuario_logado
    usuario_logado.clear()
    
    conteudo.controls.clear()
    conteudo.controls.append(tela_login(page, ir_home))
    page.update()

def abrir_evento(ev, page):
    conteudo.controls.clear()
    conteudo.controls.append(tela_evento(ev, page, abrir_evento, ir_home))
    page.update()
    

def main(page: ft.Page):
    page.title = "MMReader"
    page.padding = 0
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # -------------------------
    # START
    # -------------------------
    page.add(conteudo)

    conteudo.controls.clear()
    conteudo.controls.append(tela_login(page, ir_home))


ft.run(main)