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
import Funciones as ff


#  -----Determino el look_and_feel según los datos de la oficina configurada-----
data_file_configuracion = ff.abrir_archivo_configuracion()
sg.ChangeLookAndFeel(data_file_configuracion['look_and_feel'])

#  -----Configuro al GUI-----
layout = [[sg.Image(filename='letras.png', size=(620, 400))],
          [sg.Button('Jugar', key='jugar', size=(20, 1), button_color=('white', 'violet'),
                     font=('Comic Sans MS', 12, 'bold')),
           sg.Button('Configurar', key='config', size=(20, 1), button_color=('white', 'violet'),
                     font=('Comic Sans MS', 12, 'bold')),
           sg.CloseButton('Cerrar', size=(20, 1), button_color=('white', 'violet'),
                          font=('Comic Sans MS', 12, 'bold'), key='cerrar')]]

#  -----Muestro la GUI-----
window = sg.Window('Sopa de Letras', element_padding=(0, 2), auto_size_buttons=False,
                   grab_anywhere=True, no_titlebar=True).Layout(layout)

#  -----Lista con claves para habilitar/deshabilitar botones mediante funciones lambda-----
lista_claves_botones = ['cerrar', 'jugar', 'config']

while True:
    event, values = window.Read()
    if event is None:
        break
    if event == 'config':
        list(map(lambda element: window.Element(element).Update(disabled=True), lista_claves_botones))
        password = ff.password_input()
        if password:
            ff.configuration_menu()
        list(map(lambda element: window.Element(element).Update(disabled=False), lista_claves_botones))
    if event == 'jugar':
        window.Close()
        datos_partida = ff.jugar_sopa_letras()
        ff.controlar_jugada(datos_partida)
        break
