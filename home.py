from flet import *
from navFooter import build
from flet import UserControl, View, Text, Page, FilledButton
from flet_route import Params, Basket
from parser_drum import Parser_valut

# pip install -e .
# flet build apk


class Home(UserControl):
    def __init__(self, flet, page, loader):
        super().__init__()
        self.flet = flet
        self.page = page
        self.loader = loader
        
    def view(self, page: Page, params: Params, basket: Basket) -> View:
        def batton_clicked(e: self.flet.ControlEvent) -> None:
            self.page.clean()
            # loader img
            aler_info.controls.append(
                self.flet.Image(
                    src=self.loader,
                    width=160,
                    height=20,
                    fit=self.flet.ImageFit.CONTAIN,
                )
            )
            self.page.update()
            get_data_bank = Parser_valut("https://www.rate.am/ru/armenian-dram-exchange-rates/banks").DRUM_bank()
            show_result.value = get_data_bank
            get_data_obmenniki = Parser_valut("https://www.rate.am/ru/armenian-dram-exchange-rates/exchange-points").DRUM_obmennik()
            
            if get_data_bank:
                aler_info.controls.clear()
                
                min_max_row.controls.append(
                    self.flet.Text(
                            "Банки: ",
                            size=20,
                            spans=[
                                    self.flet.TextSpan(
                                        f'{get_data_bank[1]} - {get_data_bank[0]}',
                                        self.flet.TextStyle(
                                            weight=self.flet.FontWeight.BOLD,
                                            decoration=self.flet.TextDecoration.UNDERLINE,
                                        ),
                                    ),
                                  ],
                    ),
                )
                
                min_max_row.controls.append(
                    self.flet.Text(
                            "Обменники: ",
                            size=20,
                            spans=[
                                    self.flet.TextSpan(
                                        f'{get_data_obmenniki[1]} - {get_data_obmenniki[0]}',
                                        self.flet.TextStyle(
                                            weight=self.flet.FontWeight.BOLD,
                                            decoration=self.flet.TextDecoration.UNDERLINE,
                                        ),
                                    ),
                                  ],
                    ),
                )
                table_row.controls.append(
                    table_state(self, get_data_bank[1:]),
                )
                
                self.page.update()
                
                USD, EUR = Parser_valut("https://myfin.by/currency/cb-rf").USD_EUR_parse()
                usd_eur_row.controls.append(
                    self.flet.Text(f'USD: {USD}  EUR: {EUR}', color="ORANGE_800", size=20)
                )
                
            self.page.update()
        
        def table_state(self, get_data_bank: tuple[dict[str, str], dict[str, tuple[str, str]]]) -> Control:
            if get_data_bank:
                table = DataTable(
                    columns=[
                        DataColumn(Text("Название")),
                        DataColumn(Text("Пок-ка"), 
                                    on_sort=lambda e: [# Select the column itself
                                        e.control.parent.__setattr__("sort_column_index" , e.column_index),
                                        # Toggle the sort (ascending / descending)
                                        e.control.parent.__setattr__("sort_ascending" , False) if e.control.parent.sort_ascending else e.control.parent.__setattr__("sort_ascending" , True) ,
                                        # Sort the table rows according above
                                        e.control.parent.rows.sort(key=lambda x: x.cells[e.column_index].content.value,reverse = e.control.parent.sort_ascending) ,
                                        # Update table
                                        e.control.parent.update()
                                    ],
                                    
                        ),
                    ],
                    heading_row_color=self.flet.colors.BLUE_GREY_50,  # цвет шапки таблицы
                    border=border.all(1, "black"),
                    divider_thickness=0, # толщина_разделителя
                    sort_column_index=1,
                    sort_ascending=True, # сортировка_по_возрастанию
                    border_radius=10,
                    
                    expand=True,
                    rows=[]
                )
                for name, prices in get_data_bank[1].items():
                    if not prices or len(prices) < 1:
                        raise ValueError(f"Invalid price data for {name}")

                    names = name
                    price_sel = prices[0]
                    table.rows.append(
                        DataRow(
                            cells=[
                                DataCell(Text(names)),
                                DataCell(Text(price_sel)),
                            ],
                        )
                    )
                return table
        
        
        show_result = self.flet.Text(color="green")
        aler_info = self.flet.Row(
                        alignment=self.flet.MainAxisAlignment.END,  # align to center
                        wrap=True,
                    )
        usd_eur_row = self.flet.Row(
                        alignment=self.flet.MainAxisAlignment.END,  # align to center
                        wrap=True,
                    )
        min_max_row = self.flet.Row(
                        alignment=self.flet.MainAxisAlignment.END,  # align to center
                        wrap=True,
                    )
        
        table_row = self.flet.Row(
                        alignment=self.flet.MainAxisAlignment.END,  # align to center
        )
        
        button_text = self.flet.CupertinoFilledButton(
                content=self.flet.Text("Запросить"),
                opacity_on_click=0.3,
                on_click=batton_clicked,
                width=page.window.width-100,
        ) 
                # style=self.flet.ButtonStyle(
                #     color={
                #         self.flet.MaterialState.HOVERED: self.flet.Colors.BLACK,
                #         # self.flet.MaterialState.FOCUSED: self.flet.Colors.BLUE,
                #         self.flet.MaterialState.DEFAULT: self.flet.Colors.WHITE,
                #         self.flet.MaterialState.PRESSED: self.flet.Colors.GREEN,
                #     },
                #     # color=colors.WHITE,
                #     # bgcolor=colors.GREEN,
                
        
        
        # выводим на экран построково
        return self.flet.Column(
                [
                self.flet.AppBar(
                    leading_width=20,
                    title=self.flet.Text("Курс Драма к Рублю", color="BLACK", size=30, weight="bold"),
                    center_title=True,
                    # bgcolor=self.flet.Colors.BLUE_GREY_300,
                ),
                    self.flet.Divider(height=1, color="green"), # линия разделения
                    self.flet.Row(
                        controls=[
                            self.flet.Container(
                                content=aler_info,
                                alignment=self.flet.alignment.center,
                                # width=page.window.width,
                                # height=page.window.height,
                            ),
                            self.flet.Container(
                                content=min_max_row,
                                alignment=self.flet.alignment.center,
                                # width=50,
                                # height=50,
                                border_radius=10,
                                bgcolor=self.flet.Colors.AMBER_500,
                            ),
                            self.flet.Container(
                                content=usd_eur_row,
                                alignment=self.flet.alignment.center,
                                # width=50,
                                # height=50,
                                border_radius=10,
                                bgcolor=self.flet.Colors.GREEN_200,
                            ),
                            table_row,
                        ],
                            # alignment=self.flet.MainAxisAlignment.CENTER,
                        alignment="spaceBetween",
                        wrap=True,
                        expand=True,
                    ),
                    
                    # self.flet.Row(expand=True),
                    self.flet.Row(
                        controls=[
                            button_text,
                        ],
                        # wrap=True,
                        alignment=self.flet.MainAxisAlignment.CENTER,  # align to center
                    ),
                    
                    build(page),
                ],
                scroll=True,
                # width=page.window.width,
                # height=page.window.height,
                # alignment=self.flet.MainAxisAlignment.CENTER,
                # horizontal_alignment=self.flet.CrossAxisAlignment.CENTER,
            )
        
            
        # return Stack(
        #     controls=[
        #         self.flet.Row(
        #             controls=[
        #                 Text("Курс Драмм к Рублю", size=30, weight="bold"),
        #             ],
        #             alignment=self.flet.MainAxisAlignment.CENTER,  # align to center
        #         ),
        #         # результат
        #          self.flet.Row(
        #             controls=[
        #                 self.flet.Container(
        #                     show_result,
        #                     width=page.window.width,
        #                     # height=page.window.height,
        #                 ),
        #             ],
        #             alignment=self.flet.MainAxisAlignment.CENTER,  # align to center
        #             wrap=True,  # necessary for centering
        #         ),
                 
        #         #кнопка
        #         self.flet.Row(
        #             [
        #                 column_with_horiz_alignment(self.flet.CrossAxisAlignment.END)
        #              ]
        #             # controls=[
        #             #     self.flet.Container(
        #             #         button_text, 
        #             #         width=page.window.width
        #             #     ),
        #             # ],
        #             # alignment=self.flet.MainAxisAlignment.CENTER,  # align to center
        #             # wrap=True,  # necessary for centering
        #         ),
                
        #         build(page),
        #     ]
        # )
