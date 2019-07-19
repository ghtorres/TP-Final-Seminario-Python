
# Copyright (C) <2019>  <Delsanto, Julián Horacio / Landivar, Melina / Torres, Gastón Hernán>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import PySimpleGUI as sg
from funciones_muestra_temperatura import mostrar


#  -----Configuro al GUI-----
layout = [[sg.Text('Muestra Ambiental', size=(28, 2), font='Arial', text_color='black')],
          [sg.Button('Comenzar', key='comenzar', size=(20, 1), button_color=('white', 'red'),
                     font=('Arial', 12, 'bold')),
           sg.CloseButton('Cerrar', size=(20, 1), button_color=('white', 'red'), font=('Arial', 12, 'bold'),
                          key='cerrar')]]

#  -----Muestro la GUI-----
window = sg.Window('Muestra Ambiental', element_padding=(0, 2), auto_size_buttons=False,
                   grab_anywhere=True).Layout(layout)
while True:
    event, values = window.Read()
    if event is None:
        break
    if event == 'comenzar':
        #  -----Llama a funcion que ejecuta los modulos-----#
        mostrar()
