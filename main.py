# Если требует Git: установить .exe его и прописать путь в (cmd-> sysdm.cpl) https://www.youtube.com/watch?v=loyYdgRlrqc
# Создадим проект: fft create myapp-conter --description "Drumm" --template default

# Много страниц пример https://www.youtube.com/watch?v=Iv5frxp55TM
# pip install flet-route  это для переключения окон
#------Запускать командой-------------------------------------
# flet run -d -r .\myapp-conter\src\main.py
#-------------------------------------------------------------

from flet import *
import flet as flet
# для перехода по окнам
from flet_route import Routing, path
from views.about import About # Here IndexView is imported from views/index_view.py
from views.home import Home # Here NextView is imported from views/next_view.py
from navFooter import *
import os


def main(page: Page):
    page.title = "Routes Example"
    page.scroll = "hidden" 
    page.window.width = 400        # window's width is 200 px
    page.window.height = 600       # window's height is 200 px
    page.vertical_alignment = "center"
    page.horizontal_alignment = "center"
    page.window.left = 1060  # место где появляется оно на экране при старте
    page.window.top = 40
    page.theme_mode = ft.ThemeMode.LIGHT
    loader = "Loader_line_circles.gif" # Loader img
    page.update()
    
    
    app_routes = [
        path(
            url="/",
            clear=True,
            view=Home(flet, page, loader).view
        ),
        path(
            url="/about",
            clear=True,
            view=About().view
        ),
    ]
    
    Routing(
        page=page, # Здесь вам нужно передать страницу. Которая будет найдена как параметр во всех ваших представлениях
        app_routes=app_routes, # Здесь необходимо передать список, в котором мы определили маршрутизацию приложений, например app_routes.
        )
    page.go(page.route)
   

flet.app(target=main, assets_dir="assets")
