
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
import random
import json
import string
import sys
import unicodedata
from pattern.web import Wiktionary
from pattern.es import parse, split


def password_input():
    """Funcion que muestra una pantalla de ingreso de contraseña"""

    #  -----Configuro la GUI-----
    password_screen = [[sg.Text('Ingrese la Contraseña')],
                       [sg.In(size=(21, 1), key='pass', do_not_clear=False)],
                       [sg.Submit('Aceptar', bind_return_key=True, button_color=('white', 'violet'),
                                  font=('Comic Sans MS', 12), key='aceptar'),
                        sg.CloseButton('Cerrar', button_color=('white', 'violet'), font=('Comic Sans MS', 12))]]

    #  -----Muestro la GUI-----
    window = sg.Window('Password Panel', password_screen, grab_anywhere=True)
    clave = False
    while True:
        try:
            event, values = window.Read()
            password = str(values['pass'])
            if event is None:
                break
            if password == 'infounlp' and event == 'aceptar':
                clave = True
                window.Close()
                break
        except TypeError:
            break
    return clave


def abrir_archivo_datos_oficinas():
    """Funcion que abre un archivo json con datos de una oficina y los retorna en
    forma de diccionario donde las claves son las oficinas y los valores la informacion"""

    archivo = open('datos-oficinas.json', 'r')
    datos = json.load(archivo)
    archivo.close()
    return datos


def look_and_feel_configuration(oficina):
    """Funcion que recibe como parametro una oficina, abre un archivo de datos y en
    base a estos configura el look_and_feel de la GUI"""

    #  -----Inicialio y abro el archivo-----
    lista_temperaturas = []
    datos_oficinas = abrir_archivo_datos_oficinas()

    #  -----Proceso los datos si la oficina existe-----
    if oficina not in datos_oficinas:
        sg.Popup('La oficina ingresada no existe', button_color=('white', 'violet'),
                 font=('Comic Sans MS', 12))
    else:
        datos_oficina_elegida = datos_oficinas[oficina]
        cantidad_temperaturas_tomadas = len(datos_oficina_elegida)
        for medicion in datos_oficina_elegida:
            temperatura = medicion["temp"]
            lista_temperaturas.append(temperatura)

        #  -----Calculo el promedio de temperaturas-----
        aux = sum(lista_temperaturas)
        promedio = aux / cantidad_temperaturas_tomadas

        #  -----Según el promedio se determina el look_and_feel-----
        config_look_and_feel = 'LightGreen' if promedio < 20 else 'SandyBeach'

        return config_look_and_feel


def crear_archivo_colores(datos):
    """Funcion que crea un archivo json con un diccionario en donde las claves son
    las categorías y los colores son los valores de cada una"""

    file = open('colores_categorias.json', 'w')
    json.dump(datos, file)
    file.close()


def abrir_archivo_colores():
    """Funcion que abre un archivo json con datos de colores y los retorna en forma
    de diccionario donde las claves son las categorias y los colores los valores asociados"""

    archivo = open('colores_categorias.json', 'r')
    datos = json.load(archivo)
    archivo.close()
    return datos


def configurar_colores():
    """Funcion que abre un archivo json con datos de colores y modifica colores
    asociados a categorias"""

    #  -----Abro el archivo y defino variables con los valores de las claves-----
    datos = abrir_archivo_colores()
    adj_color = datos['adjetivos']
    sus_color = datos['sustantivos']
    ver_color = datos['verbos']
    lista_colores = [adj_color, sus_color, ver_color]

    #  -----Configuro la GUI-----
    frame_layout_a = [[sg.T('Elige el color de los Adjetivos')],
                      [sg.ColorChooserButton('Configurar', key='adjColor', button_color=('white', 'violet'),
                                             font=('Comic Sans MS', 12))], []]

    frame_layout_s = [[sg.T('Elige el color de los Sustantivos')],
                      [sg.ColorChooserButton('Configurar', key='susColor', button_color=('white', 'violet'),
                                             font=('Comic Sans MS', 12))]]

    frame_layout_v = [[sg.T('Elige el color de los Verbos')],
                      [sg.ColorChooserButton('Configurar', key='verColor', button_color=('white', 'violet'),
                                             font=('Comic Sans MS', 12))]]

    colors_config_screen = [[sg.Frame('Adjetivos', frame_layout_a, font='Any 20', title_color='violet')],
                            [sg.Frame('Sustantivos', frame_layout_s, font='Any 20', title_color='violet')],
                            [sg.Frame('Verbos', frame_layout_v, font='Any 20', title_color='violet')],
                            [sg.Submit('Aceptar', bind_return_key=True, button_color=('white', 'violet'),
                                       font=('Comic Sans MS', 12), key='aceptar')]]

    #  -----Muestro la GUI-----
    window = sg.Window('Menu de Configuración de Colores', colors_config_screen, element_padding=(5, 5),
                       grab_anywhere=True)
    diccionario = {}

    while True:
        event, values = window.Read()
        adj_color = values['adjColor']
        sus_color = values['susColor']
        ver_color = values['verColor']
        if event is None:
            window.Close()
            break
        if adj_color == "":
            adj_color = '#0000ff'
        if sus_color == "":
            sus_color = '#ff0000'
        if ver_color == "":
            ver_color = '#ffff00'
        if event == 'aceptar':
            lista_colores = [['#000000', adj_color], ['#000000', sus_color], ['#000000', ver_color]]
            window.Close()
            break

    #  -----Guardo en un diccionario los nuevos valores y los guardo en el archivo-----
    diccionario["adjetivos"] = lista_colores[0]
    diccionario["sustantivos"] = lista_colores[1]
    diccionario["verbos"] = lista_colores[2]
    crear_archivo_colores(diccionario)


def crear_archivo_palabras(datos):
    """Funcion que recibe un diccionario en donde las claves son palabras y los
    valores su categoria y lo guarda en un archivo json"""

    file = open('palabras_categorias.json', 'w')
    json.dump(datos, file)
    file.close()


def abrir_archivo_palabras():
    """Funcion que abre un archivo json y retorna un diccionario en donde las claves
    son palabras y los valores su definicion"""

    archivo = open('palabras_categorias.json', 'r')
    datos = json.load(archivo)
    archivo.close()
    return datos


def crear_archivo_categorias(datos):
    """Funcion que recibe una lista de diccionarios (donde las claves son categorias y
    los valores listas que contienen palabras pertenecientes a esa categoria)
    y crea un archivo json"""

    file = open('categorias.json', 'w')
    json.dump(datos, file)
    file.close()


def abrir_archivo_categorias():
    """Funcion que abre un archivo json y retorna una lista de diccionarios donde
    las claves son categorias y los listas que contienen palabras pertenecientes
    a esa categoria"""

    archivo = open('categorias.json', 'r')
    datos = json.load(archivo)
    archivo.close()
    return datos


def crear_archivo_definiciones(datos):
    """Funcion que recibe un diccionario donde las claves son palabras y los
    valores sus definiciones y lo guarda en un archivo json"""

    file = open('definiciones_palabras.json', 'w')
    json.dump(datos, file)
    file.close()


def abrir_archivo_definiciones():
    """Funcion que abre un archivo json y retorna un diccionario donde las claves
    son palabras y los valores sus definiciones"""

    archivo = open('definiciones_palabras.json', 'r')
    datos = json.load(archivo)
    archivo.close()
    return datos


def definicion_palabra(palabra, tipo_palabra):
    """Funcion que recibe una palabra y el tipo (adjetivo, sustantivo o verbo) y retorna
    la definicion de la palabra"""

    ok = True
    tipo_palabra = tipo_palabra.capitalize()
    engine = Wiktionary(license=None, throttle=5.0, language='es')
    article = engine.search(palabra)
    for section in article.sections:
        if tipo_palabra in section.title and ok:
            #  -----Obtengo el contenido del artículo-----
            definicion = section.string
            ok = False

            #  -----Las definiciones suelen estar después del primer '1',
            #  entonces obtengo esa 'posicion'-----
            posicion = definicion.find('1')

    #  -----Creo una cadena que va desde el final hasta 'posicion+1 para no tomar el '1'-----
    nueva_cadena = definicion[posicion + 1:-1]

    # -----Obtengo la posición del primer salto de línea-----
    posicion_nuevalinea = nueva_cadena.find('\n')

    #  -----Creo una cadena que va desde ese salto de línea hasta el comienzo de la cadena
    definicion = nueva_cadena[:posicion_nuevalinea]

    #  -----Le saco los tildes y 'ñ' a la cadena-----
    definicion2 = unicodedata.normalize("NFKD", definicion).encode("ascii", "ignore").decode("ascii")

    return definicion2


def consulta_wiktionary(palabra):
    """Funcion que recibe una palabra y devuelve el tipo que es (adjetivo,
    sustantivo o verbo)"""

    engine = Wiktionary(license=None, throttle=5.0, language='es')
    article = engine.search(palabra)
    ok = True
    tipo_palabra = None

    #  -----Si se produce un AtributeError es porque la palabra no existe
    #  en Wiktionary entonces tipo_palabra = None-----
    try:
        for section in article.sections:
            if ok:
                if 'Sustantivo' in section.title:
                    tipo_palabra = 'sustantivo'
                    ok = False
                elif 'Adjetivo' in section.title:
                    tipo_palabra = 'adjetivo'
                    ok = False
                if 'Verbo' in section.title:
                    tipo_palabra = 'verbo'
                    ok = False
    except AttributeError:
        tipo_palabra = None

    return tipo_palabra


def consulta_pattern(palabra):
    """Funcion que recibe una palabra y retorna la clasificación (adjetivo, sustantivo
    o verbo) segun el modulo pattern"""

    tipo_palabra = None
    pal = parse(palabra)

    #  -----Clasifico la palabra-----
    if pal.find('VB') != -1:
        tipo_palabra = 'verbo'
    elif pal.find('NN') != -1:
        tipo_palabra = 'sustantivo'
    if pal.find('JJ') != -1:
        tipo_palabra = 'adjetivo'

    return tipo_palabra


def crear_archivo_reporte(datos):
    """Función que recibe una lista con errores y crea un archivo de texto plano
    con el contenido de la lista"""

    file = open('reporte.txt', 'w')
    for element in datos:
        file.write(element)
        file.write('\n')
    file.close()


def abrir_archivo_reporte():
    """Funcion que abre un archivo de texto plano y retorna una lista donde cada elemento
    es una linea del texto contenido en el archivo"""

    archivo = open("reporte.txt", "r")
    lista = []
    for linea in archivo.readlines():
        lista.append(linea)
    archivo.close()
    return lista


def configurar_palabras():
    """Funcion que abre un archivo de palabras, permite que se agreguen o eliminen las
    mismas y crea, además, un archivo de las palabras categorizadas en adjetivos,
    sustantivos o verbos"""

    #  -----Abro el archivo e inicializo las variables contenedoras-----
    palabras = abrir_archivo_palabras()
    lista_reporte = abrir_archivo_reporte()
    adjetivos = []
    sustantivos = []
    verbos = []
    categorias = {}
    definiciones = {}
    lista_palabras = (list(palabras.keys()))
    palabras = {}

    #  -----Configuro la GUI-----
    frame_layout_lp = [[sg.T('Estas palabras podrán formar la Sopa de Letras')],
                       [sg.Listbox(values=lista_palabras, size=(30, 5), key='tabla', font=('Comic Sans MS', 12))]]

    frame_layout_ap = [[sg.T('Escriba la palabra que desee agregar a la lista')],
                       [sg.In(size=(38, 1), key='agregar', do_not_clear=False)],
                       [sg.Submit('OK', bind_return_key=True, button_color=('white', 'violet'),
                                  font=('Comic Sans MS', 12), pad=(5, 7))]]

    frame_layout_ep = [[sg.T('Escriba la palabra que desee eliminar de la lista')],
                       [sg.In(size=(38, 1), key='eliminar', do_not_clear=False)],
                       [sg.Button('Ok', key='deletebutton', button_color=('white', 'violet'),
                                  font=('Comic Sans MS', 12), pad=(5, 7))]]

    words_config_screen = [[sg.Frame('Lista de Palabras', frame_layout_lp, font='Any 20', title_color='violet')],
                           [sg.Frame('Agregar Palabra', frame_layout_ap, font='Any 20', title_color='violet')],
                           [sg.Frame('Eliminar Palabra', frame_layout_ep, font='Any 20', title_color='violet')],
                           [sg.Button('Aceptar', bind_return_key=True, button_color=('white', 'violet'),
                                      font=('Comic Sans MS', 12), key='aceptar')]]

    #  -----Muestro la GUI-----
    window = sg.Window('Menu de Configuración de Colores', words_config_screen, grab_anywhere=True)

    while True:
        event, values = window.Read()
        agregar = str(values['agregar'])
        eliminar = str(values['eliminar'])
        if event is None:
            break
        #  -----Si la palabra no está en la lista la agrego-----
        if agregar != '' and agregar not in lista_palabras:
            lista_palabras.append(agregar.lower())
            lista_palabras.sort()
            window.Element('tabla').Update(lista_palabras)

        #  -----Si la palabra está en la lista la elimino-----
        if event == 'deletebutton' and eliminar in lista_palabras and len(lista_palabras) > 1:
            lista_palabras.remove(eliminar)
            window.Element('tabla').Update(lista_palabras)
        if event == 'aceptar':
            window.Close()
            break

    for palabra in lista_palabras:
        tipo_palabra_wiktionary = consulta_wiktionary(palabra)

        #  -----Si el tipo no es 'None' quiere decir que existe en Wiktionary
        if tipo_palabra_wiktionary is not None:

            #  -----Consulto si la clasificación de Wiktionary coincide con la de Pattern.
            #  Si no coinciden, lo informo en el reporte-----
            tipo_palabra_pattern = consulta_pattern(palabra)
            coinciden = True if tipo_palabra_wiktionary == tipo_palabra_pattern else False
            if not coinciden:
                error = 'La clasificacion de la palabra ' + str(palabra) + ' en Wiktionary no coincide ' \
                                                                           'con la clasificacion de Pattern'
                lista_reporte.append(error)

            palabras[palabra] = tipo_palabra_wiktionary

            #  -----Dependiendo del tipo de palabra la agrego a la lista correspondiente-----
            if tipo_palabra_wiktionary == 'adjetivo':
                adjetivos.append(palabra)
            elif tipo_palabra_wiktionary == 'sustantivo':
                sustantivos.append(palabra)
            else:
                verbos.append(palabra)

            #  -----Obtengo la definición de la palabra-----
            definicion = definicion_palabra(palabra, tipo_palabra_wiktionary)
            definiciones[palabra] = definicion

        #  -----Sino lo informo en el reporte-----
        else:
            error = 'La palabra ' + str(palabra) + ' no está definida en Wiktionary'
            lista_reporte.append(error)

    #  -----Guardo las modificaciones en los distintos archivos-----
    categorias['adjetivos'] = adjetivos
    categorias['sustantivos'] = sustantivos
    categorias['verbos'] = verbos
    data_archivo_categorias = [categorias]
    crear_archivo_categorias(data_archivo_categorias)
    crear_archivo_palabras(palabras)
    crear_archivo_definiciones(definiciones)
    crear_archivo_reporte(lista_reporte)


def crear_archivo_configuracion(datos):
    """Funcion que recibe un diccionario (donde las claves son las caracteristicas de
    la sopa de letras y los valores sus parametros de configuracion) y lo guarda en
    un archivo json"""

    file = open('configuracion.json', 'w')
    json.dump(datos, file)
    file.close()


def abrir_archivo_configuracion():
    """Funcion que abre un archivo json y retorna un diccionario donde las claves
    son las caracteristicas de la sopa de letras y los valores sus parametros de
    configuracion"""

    archivo = open('configuracion.json', 'r')
    datos = json.load(archivo)
    archivo.close()
    return datos


def mostrar_reporte(font_reporte):
    """Funcion que abre un archivo de texto plano y muestra su contenido
    en pantalla"""

    #  -----Abro el archivo del reporte-----
    reporte = abrir_archivo_reporte()

    #  -----Configuro la GUI-----
    frame_layout_r = [[sg.T('Reporte Wiktionary/Pattern')],
                      [sg.Listbox(values=reporte, pad=(10, 10), size=(60, 10), key='tabla',
                                  font=font_reporte)]]

    report_screen = [[sg.Frame('Reporte', frame_layout_r, font='Any 20', title_color='violet')]]

    #  -----Muestro la GUI-----
    window = sg.Window('Reporte Wiktionary/Pattern', report_screen, grab_anywhere=True)
    while True:
        event, values = window.Read()
        if event is None:
            break


def configuration_menu():
    """Funcion que muestra en pantalla un menu de configuracion de las caracteriasticas
    que tendra la sopa de letras"""

    #  -----Abro el archivo de configuracion e inicializo las variables con los valores del mismo-----
    dato = abrir_archivo_configuracion()
    orientacion = dato.get('orientacion')
    formato = dato.get('formato')
    ayuda = dato.get('ayuda')
    cantidad_adj = dato.get('cantidad_adjetivos')
    cantidad_sus = dato.get('cantidad_sustantivos')
    cantidad_ver = dato.get('cantidad_verbos')

    #  -----Lista con claves para habilitar/deshabilitar botones mediante funciones lambda-----
    lista_claves_botones = ['palabras', 'colores', 'reporte', 'aceptar']

    #  -----Configuro la GUI-----
    frame_layout_p = [[sg.T('Agrega o Elimina Palabras')],
                      [sg.Button('Palabras', key='palabras', button_color=('white', 'violet'),
                                 font=('Comic Sans MS', 12), pad=(45, 5))]]

    frame_layout_c = [[sg.T('Elige el color de las Categorías')],
                      [sg.Button('Colores', key='colores', button_color=('white', 'violet'),
                                 font=('Comic Sans MS', 12), pad=(55, 5))]]

    frame_layout_o = [[sg.T('Elige la orientación de las Palabras')],
                      [sg.Radio('Horizontal', group_id='orient', default=True, key='hori'),
                       sg.Radio('Vertical', group_id='orient', key='vert')]]

    frame_layout_asv = [[sg.T('Elige la cantidad de cada Categoría')],
                        [sg.T('Adjetivos'), sg.In(key='cantadj', pad=(18, 10))],
                        [sg.T('Sustantivos'), sg.In(key='cantsus', pad=(0, 10))],
                        [sg.T('Verbos'), sg.In(key='cantver', pad=(28, 10))]]

    frame_layout_m = [[sg.T('Elige el formato de las Palabras')],
                      [sg.Radio('Mayúscula', group_id='format', default=True, key='mayus'),
                       sg.Radio('Minúscula', group_id='format', key='minus')]]

    frame_layout_a = [[sg.T('Elige la configuración de Ayuda')],
                      [sg.Radio('Sin Ayuda', group_id='ayuda', default=True, key='sinayuda'),
                       sg.Radio('Definiciones', group_id='ayuda', key='definiciones'),
                       sg.Radio('Lista de Palabras', group_id='ayuda', key='listapalabras')]]

    frame_layout_oficina = [[sg.T('Elige la Oficina que determinará el Look and Feel')],
                            [sg.In(default_text='oficina1',key='oficina', pad=(0, 10))]]

    frame_layout_r = [[sg.T('Presione Ok para ver el Reporte')],
                      [sg.Button('Ok', key='reporte', button_color=('white', 'violet'),
                                 font=('Comic Sans MS', 12), pad=(70, 5))]]

    frame_layout_t = [[sg.T('Elige la tipografia del Reporte')],
                      [sg.Radio('Comic Sans', group_id='report_font', default=True, key='comicsans'),
                       sg.Radio('Any 20', group_id='report_font', key='any20'),
                       sg.Radio('Verdana', group_id='report_font', key='verdana')]]

    columna_1 = [[sg.Frame('Orientacion', frame_layout_o, font='Any 20', title_color='violet')],
                 [sg.Frame('Tipografias', frame_layout_t, font='Any 20', title_color='violet')],
                 [sg.Frame('Oficina', frame_layout_oficina, font='Any 20', title_color='violet')],
                 [sg.Frame('Ayuda', frame_layout_a, font='Any 20', title_color='violet')]]

    columna_2 = [sg.Frame('Palabras', frame_layout_p, font='Any 20', title_color='violet'),
                 sg.Frame('Ver Reporte', frame_layout_r, font='Any 20', title_color='violet')], \
                [sg.Frame('Cantidad por Categoría', frame_layout_asv, font='Any 20', title_color='violet')], \
                [sg.Frame('Colores', frame_layout_c, font='Any 20', title_color='violet'),
                 sg.Frame('Formato', frame_layout_m, font='Any 20', title_color='violet', pad=(5, 0))], \
                [sg.Submit('Aceptar', bind_return_key=True, button_color=('white', 'violet'),
                           font=('Comic Sans MS', 18), key='aceptar', pad=(0, 10))]

    configuration_screen = [[sg.Text('Menu de Configuracion', pad=(260, 10), font=('Any 20', 30, 'bold', 'underline'),
                                     text_color='violet')], [sg.Column(columna_1), sg.Column(columna_2)]]

    #  -----Muestro la GUI-----
    window = sg.Window('Menu de Configuracion', configuration_screen, grab_anywhere=True, no_titlebar=True)

    while True:
        try:
            event, values = window.Read()
            orient_h = values['hori']
            format_mayus = values['mayus']
            ayuda_sin = values['sinayuda']
            ayuda_def = values['definiciones']
            cantidad_adj = values['cantadj']
            cantidad_sus = values['cantsus']
            cantidad_ver = values['cantver']
            oficina = values['oficina']
            font_comicsans = values['comicsans']
            font_verdana = values['verdana']
            if event is None:
                break
            if orient_h:
                orientacion = 'horizontal'
            else:
                orientacion = 'vertical'
            if format_mayus:
                formato = 'mayuscula'
            else:
                formato = 'minuscula'
            if ayuda_sin:
                ayuda = 'sinayuda'
            elif ayuda_def:
                ayuda = 'definiciones'
            else:
                ayuda = 'listapalabras'
            if font_comicsans:
                font_reporte = ('Comic Sans MS', 12)
            elif font_verdana:
                font_reporte = ('Verdana', 12)
            else:
                font_reporte = ('Any 20', 12)
            if event == 'colores':
                list(map(lambda element: window.Element(element).Update(disabled=True), lista_claves_botones))
                configurar_colores()
                list(map(lambda element: window.Element(element).Update(disabled=False), lista_claves_botones))
            if event == 'palabras':
                list(map(lambda element: window.Element(element).Update(disabled=True), lista_claves_botones))
                configurar_palabras()
                list(map(lambda element: window.Element(element).Update(disabled=False), lista_claves_botones))
            if event == 'reporte':
                list(map(lambda element: window.Element(element).Update(disabled=True), lista_claves_botones))
                mostrar_reporte(font_reporte)
                list(map(lambda element: window.Element(element).Update(disabled=False), lista_claves_botones))
            if event == 'aceptar':
                window.Close()
                break
        except TypeError:
            break

    #  -----Informo el valor por defecto de las categorías no configuradas-----
    if cantidad_adj == '':
        cantidad_adj = '3'
        sg.Popup('¡No configuraste la cantidad de Adjetivos! El valor predeterminado será: 3',
                 button_color=('white', 'violet'))
    if cantidad_sus == '':
        cantidad_sus = '3'
        sg.Popup('¡No configuraste la cantidad de Sustantivos! El valor predeterminado será: 3',
                 button_color=('white', 'violet'))
    if cantidad_ver == '':
        cantidad_ver = '3'
        sg.Popup('¡No configuraste la cantidad de Verbos! El valor predeterminado será: 3',
                 button_color=('white', 'violet'))

    #  -----Actualizo los datos de configuración y los guardo en el archivo-----
    datos_configuracion = {}
    if oficina != '':
        datos_configuracion['look_and_feel'] = look_and_feel_configuration(oficina)
    datos_configuracion['orientacion'] = orientacion
    datos_configuracion['formato'] = formato
    datos_configuracion['ayuda'] = ayuda
    datos_configuracion['cantidad_adjetivos'] = cantidad_adj
    datos_configuracion['cantidad_sustantivos'] = cantidad_sus
    datos_configuracion['cantidad_verbos'] = cantidad_ver
    crear_archivo_configuracion(datos_configuracion)


def menu_ayuda_definiciones(palabras):
    """Funcion que recibe la lista de palabras que están en la sopa de letras y
    muestra en pantalla la lista de definiciones pertenecientes a las mismas"""

    #  -----Abro el archivo de definiciones e inicializo la lista a mostrar-----
    diccionario = abrir_archivo_definiciones()
    definiciones = []
    for palabra in palabras:
        definicion = diccionario[palabra.lower()]
        definiciones.append(definicion)
    random.shuffle(definiciones)
    definiciones = list(map(lambda element: element.capitalize(), definiciones))

    #  -----Configuro la GUI-----
    frame_layout_d = [[sg.T('Definiciones de las palabras a buscar')],
                      [sg.Listbox(values=definiciones, pad=(10, 10), size=(60, 10), key='tabla',
                                  font=('Comic Sans MS', 12))]]

    definitions_screen = [[sg.Frame('Lista de Definiciones', frame_layout_d, font='Any 20', title_color='violet')]]

    #  -----Muestro la GUI-----
    window = sg.Window('Ayuda - Lista de Definiciones', definitions_screen, grab_anywhere=True)
    while True:
        event, values = window.Read()
        if event is None:
            break


def menu_ayuda_palabras(palabras):
    """Funcion que recibe la lista de palabras de la sopa de letras
    y las muestra en pantalla"""

    # -----Ordeno las palabras alfabéticamente y les aplico capitalize()-----
    palabras.sort()
    palabras = list(map(lambda element: element.capitalize(), palabras))

    #  -----Configuro la GUI-----
    frame_layout_lp = [[sg.T('Lista de palabras a buscar')],
                       [sg.Listbox(values=palabras, pad=(10, 10), size=(30, 5), key='tabla',
                                   font=('Comic Sans MS', 12))]]

    definitions_screen = [[sg.Frame('Lista de Palabras', frame_layout_lp, font='Any 20', title_color='violet')]]

    #  -----Muestro la GUI-----
    window = sg.Window('Ayuda - Lista de Palabras', definitions_screen, grab_anywhere=True)
    while True:
        event, values = window.Read()
        if event is None:
            break


def menu_ayuda_sinayuda(cantidades_categorias):
    """Funcion que recibe una lista con la cantidad de palabras por categoria
    y la muestra en pantalla"""

    #  -----Configuro la GUI-----
    frame_layout_lp = [[sg.T('Cantidad de Palabras por Categoría')],
                       [sg.Listbox(values=cantidades_categorias, size=(30, 5), pad=(10, 10), key='tabla',
                                   font=('Comic Sans MS', 12))]]

    definitions_screen = [[sg.Frame('Categorías', frame_layout_lp, font='Any 20', title_color='violet')]]

    #  -----Muestro la GUI-----
    window = sg.Window('Ayuda - Cantidad de Palabras', definitions_screen, grab_anywhere=True)
    while True:
        event, values = window.Read()
        if event is None:
            break


def orientacion_vertical(lista_filas, largo_maximo):
    """Funcion que recibe la lista de filas con letras orientadas de manera horizontal y
    el largo de las filas. Retorna las filas modificadas para que puedan mostrarse con
    orientacion vertical"""

    aux = 0
    lista_columnas = []

    #  -----Obtengo el primer elemento de cada fila y los agrupo en una nueva fila
    #  Luego repito el mismo procedimiento con los elementos siguientes-----
    while largo_maximo != 0:
        columna = []
        for fila in lista_filas:
            columna.append(fila[aux])
        aux = aux + 1
        largo_maximo = largo_maximo - 1
        lista_columnas.append(columna)
    return lista_columnas


def rellenar_fila(largo, largo_maximo, fila, formato, boton_text):
    """Funcion que recibe el largo de una fila de botones, el largo maximo que puede llegar a
    alcanzar, la fila y el formato(mayuscula/minuscula). Retorna la fila de botones con
    agregados de botones que no pertenecen a ninguna palabra"""

    #  -----Obtengo la cantidad de botones que debo agregarle a la fila y en dónde-----
    diferencia = largo_maximo - largo
    forma_de_rellenar = random.randrange(2)

    #  -----Si forma_de_rellenar es 0 los botones se agregarán al final de la fila-----
    if forma_de_rellenar == 0:
        while diferencia != 0:
            char = random.choice(string.ascii_letters).lower()
            if formato == 'mayuscula':
                char = char.upper()
            k = random.randrange(1000000)
            k = k * -1
            letra = sg.Button(str(char), button_color=('black', 'white'), font=('arial', boton_text, 'bold'),
                              size=(2, 1), key=k)
            fila.append(letra)
            diferencia = diferencia - 1

    #  -----Sino los botones se agregarán al comienzo de la fila-----
    else:
        while diferencia != 0:
            char = random.choice(string.ascii_letters).lower()
            if formato == 'mayuscula':
                char = char.upper()
            k = random.randrange(1000000)
            k = k * -1
            letra = sg.Button(str(char), button_color=('black', 'white'), font=('arial', boton_text, 'bold'),
                              size=(2, 1), key=k)
            fila.insert(0, letra)
            diferencia = diferencia - 1
    return fila


def unir_filas(lista_filas):
    """Funcion que recibe una lista de filas. Une de a pares las filas para crear
    filas más largas. Retorna una lista de las filas unidas"""

    seguir = True
    lista_final = []
    while seguir:
        lista1 = lista_filas[0]
        lista2 = lista_filas[1]
        lista3 = lista1 + lista2
        lista_final.append(lista3)
        lista_filas.pop(0)
        lista_filas.pop(0)
        if not lista_filas:
            seguir = False
    return lista_final


def crear_sopa_letras(data_configuracion):
    """Funcion que recibe un diccionario con los datos de configuracion (donde
    las claves son las caracteristicas de la sopa de letras y los valores sus
    parametros de configuracion) y retorna una lista de filas con botones,
    un diccionario (donde las claves son el id de cada boton y los valores son
    listas de datos), la configuración de ayuda, la orientación, la lista de
    palabras que aparecerán y la cantidad por categoría"""

    #  -----Inicializo las variables con los datos de la configuracion-----
    orientacion = data_configuracion['orientacion']
    formato = data_configuracion['formato']
    ayuda = data_configuracion['ayuda']
    cant_adjetivos = int(data_configuracion['cantidad_adjetivos'])
    cant_sustantivos = int(data_configuracion['cantidad_sustantivos'])
    cant_verbos = int(data_configuracion['cantidad_verbos'])
    palabras = []

    #  -----Abro el archivo de categorias e inicializo las variables con los datos del mismo-----
    data_categorias = abrir_archivo_categorias()
    categorias = data_categorias[0]
    lista_adjetivos = categorias['adjetivos']
    lista_sustantivos = categorias['sustantivos']
    lista_verbos = categorias['verbos']

    #  -----Corroboro que haya suficientes palabras por categoria. Sino uso las que hay-----
    if cant_adjetivos > len(lista_adjetivos):
        cant_adjetivos = len(lista_adjetivos)
    if cant_sustantivos > len(lista_sustantivos):
        cant_sustantivos = len(lista_sustantivos)
    if cant_verbos > len(lista_verbos):
        cant_verbos = len(lista_verbos)

    #  -----Para mostrar en el menu de ayuda si la configuración fue 'sinayuda'-----
    cantidades_categorias = ['Adjetivos: ' + str(cant_adjetivos), 'Sustantivos: ' + str(cant_sustantivos),
                             'Verbos: ' + str(cant_verbos)]
    cant_palabras = cant_adjetivos + cant_sustantivos + cant_verbos

    #  -----Mezclo las listas para luego elegir la cantidad configurada por categoría y
    #  añadirlas a la lista de palabras que aparecerán en la sopa de letras -----
    random.shuffle(lista_adjetivos)
    random.shuffle(lista_sustantivos)
    random.shuffle(lista_verbos)
    for i in range(cant_adjetivos):
        palabras.append(lista_adjetivos[i])
    for i in range(cant_sustantivos):
        palabras.append(lista_sustantivos[i])
    for i in range(cant_verbos):
        palabras.append(lista_verbos[i])

    #  -----Si el formato fue 'mayuscula' le aplico upper() a todas las palabras-----
    if formato == 'mayuscula':
        palabras = list(map(lambda element: element.upper(), palabras))

    #  -----Acorde a la cantidad de palabras defino la cantidad de filas extras que se agregarán-----
    filas_extras = cant_palabras // 2

    largo_maximo = 0
    lista_filas = []
    diccionario = {}
    aux = 0
    boton_text = 15

    #  -----Calculo el largo de la palabra más larga-----
    for palabra in palabras:
        if len(palabra) > largo_maximo:
            largo_maximo = len(palabra)

    #  -----Divido cada palabra en letras. Cada letra constituirá un botón que
    #  tendrá una clave única. Todos los botones que pertenezcan a una misma palabra
    #  serán depositados en una fila-----
    for palabra in palabras:
        fila = []
        largo = len(palabra)
        for caracter in palabra:
            k = random.randrange(1000000)
            #  -----El formato del diccionario es {"claveNumerica": [caracter, palabra, categoría, siFueActivado]}
            diccionario[k] = [caracter, palabra, None, False]
            boton = sg.Button(str(caracter), button_color=('black', 'white'), font=('arial', boton_text, 'bold'),
                              size=(2, 1), key=k)
            fila.append(boton)

        #  -----Agrego a cada fila botones con letras al azar siempre y cuando
        #  no sea la palabra más larga-----
        if largo < largo_maximo:
            fila = rellenar_fila(largo, largo_maximo, fila, formato, boton_text)
        lista_filas.append(fila)
        aux = aux + 1

    #  -----Creo filas que no contengan ninguna palabra-----
    fila = []
    for i in range(filas_extras):
        fila = rellenar_fila(0, largo_maximo, fila, formato, boton_text)
        lista_filas.append(fila)
        fila = []

    #  -----Mezclo la lista de filas para que cada vez aparezcan de manera diferente
    random.shuffle(lista_filas)

    #  -----Si la cantidad total de filas es impar, agrego una mas por si la orientación
    #  es horizontal(por el proceso unir_filas)-----
    if (len(lista_filas) % 2) > 0:
        fila = rellenar_fila(0, largo_maximo, fila, formato, boton_text)
        lista_filas.append(fila)

    #  -----Si la orientacion configurada era vertical, reorganizo las filas-----
    if orientacion == 'vertical':
        lista_filas = orientacion_vertical(lista_filas, largo_maximo)
    #  -----Sino, uno filas para que entren en la pantalla-----
    else:
        lista_filas = unir_filas(lista_filas)

    #  -----Porque las claves de los diccionarios están en minúscula-----
    palabras = list(map(lambda palabra: palabra.lower(), palabras))

    return lista_filas, diccionario, ayuda, palabras, cantidades_categorias


def asignar_categoria(aux, color, colores):
    """Funcion que recibe la lista de valores asociados a la clave única de cada boton
    y retorna esos valores modificados en la posición correspondiente a la categoría"""

    if color == colores['adjetivos']:
        aux[2] = 'adjetivo'
    elif color == colores['sustantivos']:
        aux[2] = 'sustantivo'
    else:
        aux[2] = 'verbo'
    return aux


def jugar_sopa_letras():
    """Funcion que muestra en pantalla la sopa de letras y que retorna un diccionario
    (donde las claves son el id de cada boton y los valores listas con datos modificados
    a partir de a jugada), la lista de palabras que había que encontrar y una lista con
    los id de los botones de las letras clickeadas que no pertenecían a ninguna palabra"""

    #  -----Abro el archivo de configuracion y creo la sopa de letras-----
    data_file_configuracion = abrir_archivo_configuracion()
    datos = crear_sopa_letras(data_file_configuracion)

    #  -----Inicializo las variables con los datos de la sopa ya creada-----
    filas = datos[0]
    dic = datos[1]
    ayuda = datos[2]
    palabras = datos[3]
    cantidades_categorias = datos[4]
    colores = abrir_archivo_colores()

    color = ('black', 'white')
    eligio_categoria = False
    errores = []

    #  -----Listas con claves para habilitar/deshabilitar botones mediante funciones lambda-----
    lista_claves_botones = ['adj', 'sus', 'ver', 'ayuda', 'controlar']
    lista_claves_grilla = list(dic.keys())

    #  -----Configuro la GUI-----
    botones = [[sg.Button('ADJ', pad=(10, 10), button_color=colores['adjetivos'], font=('Any 20', 20), key='adj',
                          auto_size_button=True, border_width=3)],
               [sg.Button('SUS', pad=(10, 10), button_color=colores['sustantivos'], font=('Any 20', 20), key='sus',
                          auto_size_button=True, border_width=3)],
               [sg.Button('VER', pad=(10, 10), button_color=colores['verbos'], font=('Any 20', 20), key='ver',
                          auto_size_button=True, border_width=3)],
               [sg.Button('Ayuda', pad=(10, 10), button_color=('white', 'violet'), font=('Any 20', 20),
                          key='ayuda', auto_size_button=True, border_width=3)],
               [sg.Button('Controlar', pad=(10, 10), button_color=('white', 'violet'), font=('Any 20', 20),
                          key='controlar', auto_size_button=True, border_width=3)]]

    sg.SetOptions(element_padding=(0, 0))

    grilla = [[sg.Column(filas, pad=(10, 10)), sg.Column(botones)]]
    layout = [[sg.Frame('Sopa de Letras', grilla, font=('Any 20', 30, 'bold'), title_color='violet',
                        border_width=5, pad=(20, 20))]]

    #  -----Muestro la GUI-----
    window = sg.Window('Sopa de Letras', grab_anywhere=False).Layout(layout)

    while True:
        event, values = window.Read()
        if event is None:
            sys.exit()

        #  -----El color estará definido por la categoría elegida-----
        if event == 'adj':
            color = colores['adjetivos']
            eligio_categoria = True
        if event == 'sus':
            color = colores['sustantivos']
            eligio_categoria = True
        if event == 'ver':
            color = colores['verbos']
            eligio_categoria = True

        #  -----El menu de ayuda dependerá de la configuración
        if event == 'ayuda':
            window.DisableClose = True
            list(map(lambda element: window.Element(element).Update(disabled=True), lista_claves_botones))
            if ayuda == 'sinayuda':
                menu_ayuda_sinayuda(cantidades_categorias)
            elif ayuda == 'definiciones':
                menu_ayuda_definiciones(palabras)
            else:
                menu_ayuda_palabras(palabras)
            window.DisableClose = False
            list(map(lambda element: window.Element(element).Update(disabled=False), lista_claves_botones))

        if event == 'controlar':
            #  -----Se inhabilitan los botones de la ventana de juego antes de mostrar los resultados para
            #  que no se pueda modificar la grilla-----
            list(map(lambda element: window.Element(element).Update(disabled=True), lista_claves_botones))
            list(map(lambda element: window.Element(element).Update(disabled=True), lista_claves_grilla))
            break

        #  -----Si se clickea un botón se modificarán los valores asociados a su clave en el
        #  diccionario de datos-----
        if event in dic and eligio_categoria:
            key = event
            aux = dic[key]
            #  -----Si el botón no fue clickeado-----
            if not aux[3]:
                aux[3] = True
                aux = asignar_categoria(aux, color, colores)
                dic[key] = aux
                window.Element(key).Update(button_color=color)
            #  -----Si el botón ya habia sido clickeado, se reinician sus valores
            else:
                aux[3] = False
                aux[2] = None
                dic[key] = aux
                window.Element(key).Update(button_color=('black', 'white'))

        #  -----Si se clickeó un botón con key negativa quiere decir que ese boton
        #  no pertenece a ninguna palabra-----
        try:
            if int(event) < 0 and eligio_categoria and event not in errores:
                errores.append(event)
                window.Element(event).Update(button_color=color)
            elif int(event) < 0 and event in errores:
                errores.remove(event)
                window.Element(event).Update(button_color=('black', 'white'))
        except ValueError:
            ''
    return dic, palabras, errores


def resultados_jugada(palabras_completas, palabras_incompletas, palabras_acertadas, palabras_erradas,
                      cantidad_letras_random):
    """Funcion que recibe la lista de palabras que se completaron, la lista de palabras que
    no se completaron, la lista de palabras categorizadas correctamente, la lista de palabras
    mal categorizadas y la cantidad de letras clickeadas que no pertenecen a ninguna palabra"""

    #  -----Aplico a todas las listas capitalize() para la muestra en los listbox-----
    palabras_completas = list(map(lambda element: element.capitalize(), palabras_completas))
    palabras_incompletas = list(map(lambda element: element.capitalize(), palabras_incompletas))
    palabras_acertadas = list(map(lambda element: element.capitalize(), palabras_acertadas))
    palabras_erradas = list(map(lambda element: element.capitalize(), palabras_erradas))

    #  -----Ordeno alfabéticamente las listas-----
    palabras_completas.sort()
    palabras_incompletas.sort()
    palabras_acertadas.sort()
    palabras_erradas.sort()

    #  -----Configuro la GUI-----
    frame_layout_pc = [[sg.T('Palabras completadas')],
                       [sg.Listbox(values=palabras_completas, pad=(10, 10), size=(30, 5), key='tabla',
                                   font=('Comic Sans MS', 12))]]

    frame_layout_pi = [[sg.T('Palabras no completadas')],
                       [sg.Listbox(values=palabras_incompletas, pad=(10, 10), size=(30, 5), key='tabla',
                                   font=('Comic Sans MS', 12))]]

    frame_layout_pa = [[sg.T('Palabras categorizadas correctamente')],
                       [sg.Listbox(values=palabras_acertadas, pad=(10, 10), size=(30, 5), key='tabla',
                                   font=('Comic Sans MS', 12))]]

    frame_layout_pe = [[sg.T('Palabras categorizadas incorrectamente o no categorizadas')],
                       [sg.Listbox(values=palabras_erradas, pad=(10, 10), size=(30, 5), key='tabla',
                                   font=('Comic Sans MS', 12))]]

    frame_layout_lr = [[sg.T('Cantidad de letras extras marcadas:'), sg.T(str(cantidad_letras_random))]]

    columna_1 = [[sg.Frame('Palabras Completadas', frame_layout_pc, font='Any 20', title_color='violet')],
                 [sg.Frame('Palabras Incompletas', frame_layout_pi, font='Any 20', title_color='violet', pad=(0, 10))],
                 [sg.Frame('Letras mal Marcadas', frame_layout_lr, font='Any 20', title_color='violet', pad=(0, 10))]]

    columna_2 = [[sg.Frame('Palabras Acertadas', frame_layout_pa, font='Any 20', title_color='violet')],
                 [sg.Frame('Palabras Erradas', frame_layout_pe, font='Any 20', title_color='violet', pad=(0, 10))],
                 [sg.Submit('Aceptar', bind_return_key=True, button_color=('white', 'violet'),
                            font=('Comic Sans MS', 20), key='aceptar', pad=(100, 10))]]

    results_screen = [[sg.Text('Resultados del Juego', font=('Any 20', 25, 'bold', 'underline'),
                               text_color='violet', pad=(250, 10))], [sg.Column(columna_1, pad=(30, 10)),
                                                                      sg.Column(columna_2, pad=(0, 10))]]

    #  -----Muestro la GUI-----
    window = sg.Window('Resultados del Juego', results_screen, grab_anywhere=True, no_titlebar=True)

    while True:
        event, values = window.Read()
        if event is None:
            sys.exit()
        if event == 'aceptar':
            sys.exit()


def controlar_jugada(datos_partida):
    """Funcion que recibe una lista con un diccionario (con los datos de la jugada), la lista
    de palabras utilizadas en la sopa de letras y la lista de claves negativas (que corresponden
    a los botones de las letras no pertenecientes a ninguna palabra)"""

    #  -----Inicializo las variables con los datos de la jugada-----
    diccionario_jugada = datos_partida[0]
    lista_palabras = datos_partida[1]

    #  -----Para informe de los resultados de la jugada-----
    cantidad_letras_random = len(datos_partida[2])
    palabras_completas = []
    palabras_incompletas = []
    palabras_acertadas = []
    palabras_erradas = []

    lista_claves = list(diccionario_jugada.keys())
    acumulador = {}

    #  -----Abro el archivo en donde cada clave es una palabra y su valor
    #  la categoría a la que pertenece-----
    data_categorias = abrir_archivo_palabras()
    dicionario_categorias = data_categorias

    #  -----En el acumulador cada palabra sera una clave y los valores una lista con
    #  contadores en donde se almacenarán la cantidad de letras clickeadas de esa palabra
    #  y cuantas fueron categorizadas adecuadamente-----
    for palabra in lista_palabras:
        coincidencias_letras = 0
        coincidencias_categorias = 0
        acumulador[palabra] = [coincidencias_letras, coincidencias_categorias]

    #  -----Proceso la información de cada botón perteneciente a las palabras-----
    for clave in lista_claves:
        aux = diccionario_jugada[clave]
        palabra = aux[1]
        categoria = aux[2]
        clave_activada = aux[3]
        #  -----Si fue clickeado aumenta el contador 'coincidencias_letras'-----
        if clave_activada:
            dato = acumulador[palabra.lower()]
            dato[0] = int(dato[0]) + 1
            categoria_real = dicionario_categorias[palabra.lower()]
            #  -----Si la categoría asignada a ese botón coincide con la categoría del archivo
            #  de categorías, aumenta el contador 'coincidencias_categorías-----
            if categoria == categoria_real:
                dato[1] = int(dato[1]) + 1
            acumulador[palabra.lower()] = dato

    #  -----Dependiendo de los contadores agrego cada palabra a la lista correspondiente-----
    for palabra in lista_palabras:
        coincidencias = acumulador[palabra]
        #  -----Si 'coincidencias_letras' es igual al largo de la palabras quiere decir
        #  que se clickearon todos sus botones-----
        if coincidencias[0] == len(palabra):
            palabras_completas.append(palabra)
        else:
            palabras_incompletas.append(palabra)
        #  -----Si 'coincidencias_categorías' es igual al largo de la palabra quiere decir
        #  que todas las letras fueron categorizadas correctamente-----
        if coincidencias[1] == len(palabra):
            palabras_acertadas.append(palabra)
        else:
            palabras_erradas.append(palabra)

    #  -----Agrego a la lista de palabras erradas la categoría real de cada palabra-----
    aux = len(palabras_erradas)
    palabras_por_categorias = abrir_archivo_palabras()
    for i in range(aux):
        palabra = palabras_erradas[i]
        palabras_erradas[i] = str(palabra) + ' es un ' + str(palabras_por_categorias[palabra])

    #  -----Invoco al proceso que mostrará los resultados-----
    resultados_jugada(palabras_completas, palabras_incompletas, palabras_acertadas, palabras_erradas,
                      cantidad_letras_random)
