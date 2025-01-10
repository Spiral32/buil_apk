from flet import *
from navFooter import build
from flet import UserControl, View, Text, Page
from flet_route import Params, Basket


class About(UserControl):
    def __init__(self):
        super().__init__()

    def view(self, page: Page, params: Params, basket: Basket) -> View:
        return View(
            controls=[
                Text("About", size=30, weight="bold"),
                build(page),
            ]
        )

