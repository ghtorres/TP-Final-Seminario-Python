
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

import json
import time
import PySimpleGUI as sg
from lector_temperatura import leer_temp


def interfaz_PysimpleGUI():
    """Funcion que retorna una lista con constantes para configurar la interfaz en PySimpleGui
    interfaz[0] -> color botones /// interfaz[1] -> color texto /// interfaz[2] -> look_and_feel
    interfaz[3] -> frame text color /// interfaz[4] -> frame font /// interfaz[5] ->  aceptar button text font
    interfaz[6] -> regular text font /// interfaz[7] -> radio text font
    interfaz[8] -> finalizar button text font /// interfaz[9] -> input size /// interfaz[10] -> frame border"""

    #  -----Inicializo la lista interfaz-----
    interfaz = []

    #  -----Defino las constantes que configuran la GUI-----
    button_color = ('white', 'darkblue')
    text_color = 'darkblue'
    frame_text_color = 'blue'
    #  -----GreenTan, LightGreen, BluePurple, Purple, BlueMono, GreenMono ,BrownBlue, BrightColors,
    #  NeutralBlue, Kayak, SandyBeach, TealMono-----
    look_and_feel = 'SandyBeach'
    frame_font = ('Any 20', 30)
    aceptar_button_text_font = ('Any 20', 12)
    regular_text_font = ('Any 20', 12)
    radio_text_font = ('Any 20', 12)
    finalizar_button_text_font = ('Any 20', 18)
    input_size = (27, 1)
    frame_border_width = 3

    #  -----Agrego a la lista interfaz las constantes-----
    interfaz.append(button_color)
    interfaz.append(text_color)
    interfaz.append(look_and_feel)
    interfaz.append(frame_text_color)
    interfaz.append(frame_font)
    interfaz.append(aceptar_button_text_font)
    interfaz.append(regular_text_font)
    interfaz.append(radio_text_font)
    interfaz.append(finalizar_button_text_font)
    interfaz.append(input_size)
    interfaz.append(frame_border_width)
    return interfaz


def crear_archivo_oficinas(datos):
    """Funcion que crea un archivo json con un diccionario donde las claves son oficinas
    y los valores listas de diccionarios con datos de las mismas"""

    file = open('datos-oficinas.json', 'w')
    json.dump(datos, file)
    file.close()


def abrir_archivo_oficinas():
    """Funcion que abre un archivo json con datos de una oficina y los retorna en
    forma de diccionario donde las claves son las oficinas y los valores la informacion
    (es una lista de diccionarios)"""

    archivo = open('datos-oficinas.json', 'r')
    datos = json.load(archivo)
    archivo.close()
    return datos


def registrar_temperatura(datos, nombre_lugar):
    """Funcion que recibe un diccionario y el nombre de una oficina y retorna un diccionario
    en donde las claves son las oficinas de donde se registró la información y los valores son
    listas con los datos obtenidos"""

    #  -----Obtengo la lista de claves del diccionario del archivo-----
    lista_claves = list(datos.keys())

    #  -----Si el len(lista_claves) < 1 significa que el archivo estaba vacío-----
    if len(lista_claves) < 1:
        lista_medicion = []
        datos = {}
    #  -----Si el archivo no estaba vacío pero la oficina es nueva-----
    elif nombre_lugar not in lista_claves:
        lista_medicion = []
    #  -----Si el archivo no estaba vacío y la oficina ya existe en el mismo-----
    else:
        lista_medicion = datos[nombre_lugar]

    temp = leer_temp()
    lista_medicion.append(temp)
    datos[nombre_lugar] = lista_medicion
    return datos


#  -----Configuro la GUI-----

interfaz = interfaz_PysimpleGUI()

sg.ChangeLookAndFeel(interfaz[2])

frame_layout_t = [[sg.T('¿Desea hacer una lectura?', text_color=interfaz[1], font=interfaz[6])],
                  [sg.Radio('Si', group_id='lectura', key='lectura_si', text_color=interfaz[1], font=interfaz[7]),
                   sg.Radio('No', group_id='lectura', key='lectura_no', default=True, text_color=interfaz[1],
                            font=interfaz[7])]]

frame_layout_o = [sg.Text('Ingrese Nombre Oficina', text_color=interfaz[1], font=interfaz[6])], \
                 [sg.In(size=interfaz[9], key='lugar', do_not_clear=False)], \
                 [sg.Submit('Aceptar', bind_return_key=True, key='aceptar', button_color=interfaz[0],
                            font=interfaz[5], pad=(5, 10))]

input_screen = [[sg.Frame('Lectura', frame_layout_t, font=interfaz[4], title_color=interfaz[3], pad=(10, 10),
                          border_width=interfaz[10])],
                [sg.Frame('Oficina', frame_layout_o, font=interfaz[4], title_color=interfaz[3], pad=(10, 10),
                          border_width=interfaz[10])],
                [sg.Button('Finalizar', bind_return_key=True, key='finalizar', button_color=interfaz[0],
                           font=interfaz[8], pad=(70, 10))]]

#  -----Muestro la GUI-----
window = sg.Window('Panel Control', grab_anywhere=True).Layout(input_screen)

while True:
    event, values = window.Read()
    if event is None or event == 'finalizar':
        break
    try:
        temp = values['lectura_si']
        nombre_lugar = str(values['lugar'])
        if temp and nombre_lugar != "":
            datos = abrir_archivo_oficinas()
            diccionario_oficinas = registrar_temperatura(datos, nombre_lugar)
            crear_archivo_oficinas(diccionario_oficinas)
            #  -----Puse 10 segundos en vez de 60 porque es más práctico a la hora de probar el programa-----
            time.sleep(10)
    except TypeError:
        break


