import flet as ft
from flet import *

    
def build(page: Page) -> ft.Control:
  def change_page(e, page):
    print(page.route)
    print(e.control.selected_index)
    
    if e.control.selected_index == 0:
      page.go('/')
      page.update()
    if e.control.selected_index == 1:
      page.go('/about')
      page.update()
    page.update()
    
  navitem = NavigationBar(
      on_change=lambda e: change_page(e, page),
      bgcolor=ft.colors.BLUE,
      destinations=[
				NavigationBarDestination(icon=icons.HOME, label="home"),
				NavigationBarDestination(icon=icons.EXPLORE, label="about"),
			]
		)
  
  return navitem

