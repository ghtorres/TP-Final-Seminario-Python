# TP-Final-Seminario-Python


-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

           *  *  *  *  *  S E M I N A R I O  D E  L E N G U A J E  -  P Y T H O N  *  *  *  *  *

                                          T R A B A J O  F I N A L

-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------
 Trabajo final para la asignatura 'Seminario de Lenguaje - Python' de la Facultad de Informática de la UNLP 


* I N T E G R A N T E S *


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


* C O N S I D E R A C I O N E S *


  - El archivo a ejecutar es Main.py 

  - La contraseña para acceder al menu de configuración es: infounlp

  - Los archivos, tanto los .JSON como los .TXT, tienen que estar en el mismo directorio que
  los archivos .PY

  - La imagen letras.png también debe estar en el mismo directorio que los archivos .PY

  - No debe eliminarse ningún archivo (.json|.txt|.py|.png)

  - El look_and_feel está determinado por los datos de las oficinas del archivo datos-oficinas.json
  Se puede modificar eligiendo la oficina en el menu de configuración (solo hay 2 oficinas). Para
  ver reflejados los cambios, una vez realizadas las configuraciones, reiniciar el programa.

  - El archivo reporte.txt inicia en blanco.


-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------

                                 *  *  *   R A S P B E R R Y  P I   *  *  *

-------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------


* C O N S I D E R A C I O N E S *

  - Se incluyen 2 archivos principales a ejecutar:
     
     - muestra_datos.py (permite la toma de datos y la muestra en las pantallas LED)
     
     - registro_ambiental.py (almacena en el archivo datos-oficinas.json los datos de la
     medición de la oficina ingresada)

  - Si bien las mediciones debían realizarse cada 60 segundos, por cuestiones prácticas a la hora de
  probar el programa se definió que las mediciones sean cada 10 segundos. Para modificar esto, no se
  necesita más que cambiar la línea 128 del archivo registro_ambiental.py:
     Línea 128: time.sleep(10) ---->  time.sleep(60)

  - Los archivos, tanto los .JSON como los .PY, tienen que estar en el mismo directorio

  - No debe eliminarse ningún archivo (.json|.py)

