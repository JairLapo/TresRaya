import flet as ft
import json


def main(page: ft.Page):
    # Propiedades de ventana
    page.title = "Tres en raya"
    page.window_width = 300
    page.window_height = 360
    page.window_frameless = True
    page.window_center()

    player_red = []
    player_blue = []
    fields_left = [13, 15, 17,
                   19, 21, 23,
                   25, 27, 29]
    fields_border = []

    # creación de lista para líneas horizontales
    horizontal_lines = [[13, 15, 17],
                        [19, 21, 23],
                        [25, 27, 29]]

    # creación de lista para líneas verticales
    vertical_lines = [[13, 19, 25],
                      [15, 21, 27],
                      [17, 23, 29]]

    # creación de lista apra líneas diagonales
    diagonal_lines = [[13, 21, 29],
                      [17, 21, 25]]

    # combinación de líneas en una sola lista
    lines = horizontal_lines + vertical_lines + diagonal_lines

    def close(e):
        page.window_close()

    def win(player):
        """
        Función llamada al decidir el ganador
        Es estética simplemente para el mensaje final
        """
        # Se asigna el color del texto según el jugador ganador
        c = "blue" if player == "Azul" else "red"
        page.window_frameless = False
        page.clean()
        page.add(
            ft.Column(
                [
                    ft.Container(
                        ft.Text(f"Jugador {player} ganó!", size=25,
                                color=c), alignment=ft.alignment.center),
                    ft.Container(
                        ft.IconButton(
                            icon=ft.icons.CLOSE,  icon_size=100, on_click=close,

                        ), alignment=ft.alignment.center),
                ]),
        )

        page.update()

    def drag_accept(e):
        """
        Función de arrastre de los cuadros,
        valida si existe un jugador que ha ganado aún o no
        """
        src = page.get_control(e.src_id)
        field = int(e.target[1:])
        e.control.content.bgcolor = src.content.bgcolor
        # e.control.content.border = None

        id_player = int(json.loads(e.data)['src_id'][1:])

        if field in fields_left:
            e.control.update()

        if field not in fields_border:

            # ID:10 Jugador Rojo
            if id_player == 10 and field in fields_left:
                player_red.append(field)
                player_red.sort()

            elif id_player == 10:
                if field in player_blue:
                    player_blue.remove(field)
                    player_red.append(field)
                    e.control.content.border = ft.border.all(
                        5,  ft.colors.BLUE_200
                    )
                else:
                    e.control.content.border = ft.border.all(
                        5,  ft.colors.RED_200
                    )
                fields_border.append(field)

            # ID: 6 Jugador azul
            if id_player == 6 and field in fields_left:
                player_blue.append(field)
                player_blue.sort()

            elif id_player == 6:
                if field in player_red:
                    player_red.remove(field)
                    player_blue.append(field)
                    e.control.content.border = ft.border.all(
                        5, ft.colors.RED_200
                    )
                else:
                    e.control.content.border = ft.border.all(
                        5, ft.colors.BLUE_200
                    )
                fields_border.append(field)

            if field in fields_left:
                fields_left.remove(field)

            e.control.update()

        for line in lines:
            # Verificación si la línea ya está llena para el jugador rojo
            if all(num in player_red for num in line):
                win("Rojo")

            # Verificación si la línea ya está llena para el jugador azul
            if all(num in player_blue for num in line):
                win("Azul")

    page.add(
        ft.Row(
            [
                ft.Row(
                    [


                        ft.Draggable(
                            group="color",
                            content=ft.Container(
                                width=50,
                                height=50,
                                bgcolor=ft.colors.BLUE,
                                border_radius=5,
                            ),
                        ),
                        ft.Container(
                            ft.IconButton(
                                icon=ft.icons.CLOSE, on_click=close,

                            ), margin=ft.margin.only(left=60)),

                        ft.Draggable(
                            group="color",
                            content=ft.Container(
                                margin=ft.margin.only(left=60),
                                width=50,
                                height=50,
                                bgcolor=ft.colors.RED,
                                border_radius=5,
                            ),
                        ),

                    ]
                ),


            ]
        )
    )

    grid = ft.GridView(
        expand=1,
        runs_count=5,
        max_extent=100,
        child_aspect_ratio=1.0,
        spacing=5,
        run_spacing=5,
    )

    page.add(grid)

    for _ in range(0, 9):
        grid.controls.append(
            ft.DragTarget(
                group="color",
                content=ft.Container(
                    width=50,
                    height=50,
                    bgcolor=ft.colors.BLUE_GREY_100,
                    border_radius=5,
                ),
                on_accept=drag_accept,
            ),
        )
        page.update()


ft.app(target=main)