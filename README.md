# Actividad de Analizador Léxico con Python

## Descripción del proyecto

Este proyecto implementa un analizador léxico escrito en Python que recorre un fragmento de código fuente y lo transforma en una secuencia de tokens. Además del reconocimiento léxico, incorpora validaciones semánticas básicas relacionadas con declaración de variables, compatibilidad de tipos y alcance por bloques.

El sistema reconoce palabras reservadas, identificadores, números, cadenas, booleanos, comentarios, operadores y delimitadores, y también produce `ErrorToken` con retroalimentación cuando detecta lexemas inválidos o inconsistencias semánticas simples.

El repositorio está planteado como una actividad académica para estudiar la etapa de análisis léxico dentro de un compilador o intérprete, extendida con una tabla de símbolos y verificaciones elementales de tipos para enriquecer el análisis.

## Objetivo del proyecto

El objetivo principal es mostrar, de forma práctica, cómo construir un analizador léxico modular capaz de:

- leer una entrada secuencial carácter por carácter.
- identificar patrones léxicos válidos.
- registrar la posición de cada token por línea y columna.
- reportar errores léxicos de manera comprensible.
- mantener una tabla de símbolos con soporte de alcance por bloques.
- detectar uso de variables no declaradas.
- validar compatibilidad de tipos en asignaciones y expresiones relacionales simples.
- validar el comportamiento mediante pruebas automatizadas.

## Funcionalidades principales

- Reconocimiento de palabras reservadas: `if`, `else`, `while`, `return`, `int`, `float`, `double`, `string`, `char`, `bool`, `for`, `do`.
- Reconocimiento de identificadores válidos con letras, dígitos y guiones bajos.
- Soporte para números enteros y decimales.
- Soporte para números hexadecimales con prefijo `0x`.
- Soporte para cadenas delimitadas por comillas dobles, incluyendo espacios y delimitadores internos.
- Reconocimiento de literales booleanos `true` y `false`.
- Reconocimiento de comentarios de una línea (`// ...`) y de múltiples líneas (`/* ... */`).
- Reconocimiento de operadores aritméticos: `+`, `-`, `*`, `/`, `%`, `++`, `--`.
- Reconocimiento de operadores relacionales: `<`, `<=`, `>`, `>=`, `==`, `===`, `!=`.
- Reconocimiento de operadores lógicos: `&&`, `||`, `!`.
- Reconocimiento del operador de asignación `=`.
- Reconocimiento de delimitadores como paréntesis, llaves, coma y punto y coma.
- Seguimiento de línea y columna para cada token generado.
- Generación de `ErrorToken` con mensajes de retroalimentación según el tipo de error detectado.
- Declaración de variables en tabla de símbolos cuando un identificador aparece después de un tipo válido.
- Búsqueda de identificadores en todos los alcances activos.
- Manejo de alcance por bloques mediante llaves `{` y `}`.
- Tratamiento especial del bloque `do { ... } while (...) ;` para conservar el alcance hasta terminar la condición del `while`.
- Detección de uso de variables no declaradas.
- Detección de asignaciones a variables no declaradas.
- Validación de compatibilidad de tipos en asignaciones a variables declaradas.
- Validación de compatibilidad de tipos en expresiones relacionales simples entre literales asignables e identificadores.
- Emisión de un token final `EOF` para marcar el fin del análisis.

## Arquitectura general

La arquitectura sigue un diseño sencillo y modular:

- `Lexer.py` concentra la lógica de escaneo, mantiene el estado del recorrido, resuelve el tipo de token más adecuado y ejecuta validaciones semánticas básicas durante la tokenización.
- `SymbolTable.py` implementa la tabla de símbolos con pila de alcances para variables declaradas.
- `datatype_checker.py` centraliza la validación de tipos soportados y la inferencia simple del tipo de un valor.
- La carpeta `Tokens/` contiene una jerarquía de clases donde cada archivo define una categoría concreta de token y su lógica de validación.
- `run_lexer_task.py` funciona como punto de entrada rápido para ejecutar un caso de ejemplo y visualizar la salida del lexer.
- `test_lexer.py` valida el comportamiento esperado mediante pruebas unitarias, semánticas e integradas.

En términos conceptuales, el flujo de responsabilidad se plantea de la siguiente manera:

```text
Código fuente -> Lexer -> Clases de token en Tokens/ -> Tabla de símbolos / validación de tipos -> Lista de tokens -> Salida / pruebas
```

## Flujo general

1. Se entrega una cadena fuente al constructor de `Lexer`.
2. El lexer inicializa su posición actual, línea, columna y la lista de tokens.
3. Para cada nuevo lexema potencial, genera un conjunto de clases candidatas que intentan validar el contenido acumulado.
4. El código fuente se consume carácter por carácter.
5. Cuando aparece un espacio, salto de línea o delimitador, el lexer decide cuál clase candidata representa el token correcto.
6. Si ninguna clase valida el lexema acumulado, se crea un `ErrorToken` con retroalimentación inferida.
7. Si el token reconocido es un identificador después de un tipo válido, el nombre se registra en la tabla de símbolos del alcance actual.
8. Si el token reconocido representa uso o asignación sobre un identificador, se consulta la tabla de símbolos para verificar su declaración previa.
9. Si el token corresponde a un valor asignado o participa en una expresión relacional simple, se valida la compatibilidad de tipos.
10. Si el carácter actual es un delimitador, se agrega también su token correspondiente y, cuando aplica, se abre o cierra un alcance.
11. Al terminar la entrada, se agrega un token `EOF`.

## Requisitos técnicos

- Python 3.9 o superior.
- Ejecución desde la raíz del proyecto para que los imports del módulo `Tokens` funcionen sin ajustes adicionales.
- Consola o terminal para correr el script de demostración y las pruebas.

## Software base

- Lenguaje principal: Python.
- Framework de pruebas: `unittest` de la biblioteca estandar.
- Entorno de trabajo sugerido: VS Code o cualquier editor capaz de ejecutar scripts de Python.

## Configuración relevante

- No existe un archivo de configuración externo; el comportamiento actual del lexer está definido directamente en el código.
- La entrada de ejemplo está embebida en `run_lexer_task.py` y también en el bloque `if __name__ == "__main__":` de `Lexer.py`.
- El lexer actual depende de espacios o delimitadores para cerrar correctamente un token. Por ejemplo, `intx=42;` no se analiza igual que `int x = 42 ;`.
- El sistema de tipos soporta `int`, `float`, `double`, `string`, `char` y `bool`.
- Los literales booleanos válidos son `true` y `false`.
- Los literales de cadena usan comillas dobles.
- No existe un token específico para literales `char`; los valores entre comillas dobles se reconocen como `STRING`, por lo que la validación de tipos sigue ese comportamiento actual.
- El manejo de alcance se basa en bloques con llaves y en una regla especial para `do ... while`.
- Las pruebas se ejecutan desde la raíz del repositorio con el comando:

```bash
python3 -m unittest -v test_lexer.py
```

## Estructura general del proyecto

```text
.
|-- Lexer.py
|-- datatype_checker.py
|-- run_lexer_task.py
|-- SymbolTable.py
|-- test_lexer.py
`-- Tokens/
    |-- assignation_token.py
    |-- boolean_token.py
    |-- delimiter_token.py
    |-- EOF_token.py
    |-- error_token.py
    |-- token.py
    |-- keyword_token.py
    |-- identifier_token.py
    |-- number_token.py
    |-- hexadecimal_number_token.py
    |-- string_token.py
    |-- math_token.py
    |-- relational_token.py
    |-- logical_token.py
    |-- multi_line_comment_token.py
    `-- single_line_token.py
```

## Descripción de archivos clave

### `Lexer.py`

Archivo central del proyecto. Implementa la clase `Lexer`, el recorrido secuencial de la entrada, la resolución del tipo de token más adecuado, la gestión del alcance por bloques, la interacción con la tabla de símbolos, la validación básica de tipos y la generación de errores y del token `EOF`.

### `SymbolTable.py`

Implementa la tabla de símbolos basada en una pila de diccionarios, con operaciones para entrar y salir de alcances, declarar variables y consultarlas desde el alcance más interno hacia el más externo.

### `datatype_checker.py`

Contiene la lógica auxiliar para validar tipos soportados, comprobar si un nombre de tipo existe y deducir el tipo simple asociado a un valor reconocido por el lexer.

### `run_lexer_task.py`

Script de demostración. Ejecuta el lexer sobre un programa de ejemplo y muestra la secuencia de tokens con su información básica.

### `test_lexer.py`

Conjunto principal de pruebas. Incluye casos válidos, casos de error léxico, validaciones sobre alcance, detección de variables no declaradas, comprobaciones de compatibilidad de tipos y un escenario integrado con múltiples tipos de tokens y errores en un mismo programa.

### `Tokens/token.py`

Define la clase abstracta base `Token`, que establece la interfaz común para verificar validez, anexar caracteres y representar tokens.

### `Tokens/error_token.py`

Define `ErrorToken`, utilizado para reportar lexemas inválidos y mostrar mensajes de retroalimentación cuando se habilita su impresión extendida.

### Archivos especializados dentro de `Tokens/`

Cada uno encapsula las reglas de validación para una familia de tokens concreta:

- `keyword_token.py`: palabras reservadas.
- `identifier_token.py`: identificadores.
- `number_token.py`: números decimales.
- `hexadecimal_number_token.py`: números hexadecimales.
- `string_token.py`: cadenas.
- `boolean_token.py`: literales booleanos.
- `math_token.py`: operadores aritméticos.
- `relational_token.py`: operadores relacionales.
- `logical_token.py`: operadores lógicos.
- `assignation_token.py`: asignación.
- `delimiter_token.py`: símbolos separadores.
- `multi_line_comment_token.py`: comentarios multilínea.
- `single_line_token.py`: comentarios de una línea.
- `EOF_token.py`: fin de archivo.

## Valor académico del proyecto

Este repositorio tiene un valor académico claro porque permite estudiar varios conceptos fundamentales de compiladores y procesamiento de lenguajes:

- separación entre análisis léxico y representación de tokens.
- diseño orientado a objetos para encapsular reglas de validación.
- manejo de errores léxicos con retroalimentación contextual.
- seguimiento de posiciones para diagnóstico.
- uso de tabla de símbolos para vincular identificadores con tipos.
- manejo de alcance estático básico por bloques.
- comprobación elemental de tipos en asignaciones y comparaciones.
- validacion automatizada mediante pruebas unitarias.

También sirve como base para futuras extensiones, por ejemplo: agregar más palabras reservadas, soportar nuevos símbolos, introducir literales de `char` diferenciados o conectar este lexer con una etapa sintáctica posterior.

## Ejecución rápida

Para ejecutar el ejemplo incluido:

```bash
python3 run_lexer_task.py
```

O también:

```bash
python3 Lexer.py
```

Para ejecutar las pruebas:

```bash
python3 -m unittest -v test_lexer.py
```