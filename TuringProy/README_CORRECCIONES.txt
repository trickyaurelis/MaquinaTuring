CORRECCIONES REALIZADAS

1. Se agregó soporte para resta binaria con el operador '-'.
   Ejemplos aceptados:
   - 101-10 = 11
   - 1110-101 = 1001

2. Se actualizó el validador del lenguaje:
   L = { x op y | x, y ∈ {0,1}+, op ∈ {+, -} }

3. Se actualizó la interfaz:
   - Título: suma y resta binaria.
   - Placeholder: 101+11 o 101-10.

4. Se actualizó la evidencia exportada:
   - Ahora menciona suma y resta.
   - Los archivos de evidencia aceptan nombres con _menos_.

5. Se probó desde consola:
   - 101+10 -> 111
   - 111+1 -> 1000
   - 101-10 -> 11
   - 1110-101 -> 1001
   - 10-101 -> ERROR, resta negativa no permitida.

Para ejecutar:
python main.py
