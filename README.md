# TP-Final-Seminario-Python


-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

           *  *  *  *  *  S E M I N A R I O  D E  L E N G U A J E  -  P Y T H O N  *  *  *  *  *

                                          T R A B A J O  F I N A L

-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------
 Trabajo final para la asignatura 'Seminario de Lenguaje - Python' de la Facultad de Informática de la UNLP 


* I N T E G R A N T E S


    Delsanto, Julián Horacio  |   Legajo 14137/3

    Landivar, Melina          |   Legajo 15773/2

    Torres, Gastón Hernán     |   Legajo 14889/9


-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

                                *  *  *  *  *  L I C E N S E  *  *  *  *  *

-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

Copyright (C) <2019>  <Delsanto, Julián Horacio / Landivar, Melina / Torres, Gastón Hernán>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU 
General Public License as published by the Free Software Foundation, either version 3 of the License, or 
(at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the 
implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License 
for more details.

You should have received a copy of the GNU General Public License along with this program.  If not, 
see <https://www.gnu.org/licenses/>.


-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

                                *  *  *   S O P A  D E  L E T R A S   *  *  *

-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------


* I N T R O D U C C I Ó N

  “Soupe à l'oignon” es una aplicación educativa pensada para estudiantes que cursan el primer ciclo educativo 
  de nivel primario que consiste en una sopa de letras (Word Search) en la que no sólo se deben encontrar una 
  cantidad determinada de palabras, sino que, además, estas deben ser clasificadas en adjetivos, sustantivos o
  verbos.
  La aplicación permite al docente determinar cómo será el desarrollo del juego mediante un menú de configuración 
  simple e intuitivo.


* C O N S I D E R A C I O N E S

  - El archivo a ejecutar es Main.py 

  - La contraseña para acceder al menu de configuración es: infounlp

  - Los archivos, tanto los .JSON como los .TXT, tienen que estar en el mismo directorio que
  los archivos .PY

  - La imagen letras.png también debe estar en el mismo directorio que los archivos .PY

  - No debe eliminarse ningún archivo (.json|.txt|.py|.png)
  
  - En el archivo "Guía de Usuario.pdf" se incluye un manual que detalla cómo usar la
  aplicación.

  - El look_and_feel está determinado por los datos de las oficinas del archivo datos-oficinas.json que
  se puede modificar eligiendo la oficina en el menu de configuración (solo hay 2 oficinas). Para
  ver reflejados los cambios, una vez realizadas las configuraciones, reiniciar el programa. En la
  guía de usuario se puede ver en detalle cómo se verá la interfaz con cada configuración del
  look_and_feel.

  - El archivo "reporte.txt" inicia en blanco, el cual viene incluído en los archivos .zip que contienen
  la aplicación. No obstante, si se opta por descargar los archivos del directorio "Sopa de Letras", se
  debe crear un archivo llamado "reporte.txt" en blanco para el óptimo funcionamiento de la aplicación.
  
  - La aplicación corre tanto en Windows como en Linux.
  
  - El archivo "TP Final - Sopa de Letras.zip" contiene una versión antigua de la aplicación. Usar la
  versión del archivo "Trabajo Final - Sopa de Letras + Raspberry Pi.zip" o bien utilizar los archivos del
  directorio "Sopa de Letras".


-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

                                 *  *  *   R A S P B E R R Y  P I   *  *  *

-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

* I N T R O D U C C I Ó N

  “Registro Ambiental” y “Muestra Datos” son dos aplicaciones meteorológicas. La primera permite registrar la 
  temperatura y humedad ambiente (mediante un sensor conectado a una Raspberry Pi) y la segunda posibilita la 
  muestra de los datos recabados en una matriz led al detectar un sonido.


* C O N S I D E R A C I O N E S

  - Se incluyen 2 archivos principales a ejecutar:
     
     - muestra_datos.py (permite la toma de datos y la muestra en las pantallas LED)
     
     - registro_ambiental.py (almacena en el archivo datos-oficinas.json los datos de la
     medición de la oficina ingresada)

  - Si bien las mediciones debían realizarse cada 60 segundos, por cuestiones prácticas a la hora de
  probar el programa se definió que las mediciones sean cada 10 segundos. Para modificar esto, no se
  necesita más que cambiar la línea 146 del archivo registro_ambiental.py:
     Línea 146: time.sleep(10) ---->  time.sleep(60)

  - Los archivos, tanto los .JSON como los .PY, tienen que estar en el mismo directorio.

  - No debe eliminarse ningún archivo (.json|.py)

