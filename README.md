# Actividad de Analizador Léxico con Python

## Descripción del proyecto

Este proyecto implementa un analizador léxico escrito en Python que recorre un fragmento de código fuente y lo transforma en una secuencia de tokens. El sistema reconoce palabras reservadas, identificadores, números, cadenas, operadores y delimitadores, además de producir tokens de error con retroalimentación cuando encuentra lexemas inválidos.

El repositorio está planteado como una actividad académica para estudiar la etapa de análisis léxico dentro de un compilador o intérprete, manteniendo una separación clara entre el motor principal del lexer y las clases que representan cada categoría de token.

## Objetivo del proyecto

El objetivo principal es mostrar, de forma práctica, cómo construir un analizador léxico modular capaz de:

- leer una entrada secuencial carácter por carácter.
- identificar patrones léxicos válidos.
- registrar la posición de cada token por línea y columna.
- reportar errores léxicos de manera comprensible.
- validar el comportamiento mediante pruebas automatizadas.

## Funcionalidades principales

- Reconocimiento de palabras reservadas: `if`, `else`, `while`, `return`, `int`, `float`.
- Reconocimiento de identificadores válidos con letras, dígitos y guiones bajos.
- Soporte para números enteros y decimales.
- Soporte para números hexadecimales con prefijo `0x`.
- Soporte para cadenas delimitadas por comillas dobles, incluyendo espacios y delimitadores internos.
- Reconocimiento de operadores aritméticos, relacionales, lógicos y de asignación.
- Reconocimiento de delimitadores como paréntesis, llaves, coma y punto y coma.
- Seguimiento de línea y columna para cada token generado.
- Generación de `ErrorToken` con mensajes de retroalimentación según el tipo de error detectado.
- Emisión de un token final `EOF` para marcar el fin del análisis.

## Arquitectura general

La arquitectura sigue un diseño sencillo y modular:

- `Lexer.py` concentra la lógica de escaneo, mantiene el estado del recorrido y decide cuándo un lexema acumulado se convierte en token válido o en error.
- La carpeta `Tokens/` contiene una jerarquía de clases donde cada archivo define una categoría concreta de token y su lógica de validación.
- `run_lexer_task.py` funciona como punto de entrada rápido para ejecutar un caso de ejemplo y visualizar la salida del lexer.
- `test_lexer.py` valida el comportamiento esperado mediante pruebas unitarias e integradas.

En términos conceptuales, el flujo de responsabilidad se plantea de la siguiente manera:

```text
Código fuente -> Lexer -> Clases de token en Tokens/ -> Lista de tokens -> Salida / pruebas
```

## Flujo general

1. Se entrega una cadena fuente al constructor de `Lexer`.
2. El lexer inicializa su posición actual, línea, columna y la lista de tokens.
3. Para cada nuevo lexema potencial, genera un conjunto de clases candidatas que intentan validar el contenido acumulado.
4. El código fuente se consume carácter por carácter.
5. Cuando aparece un espacio, salto de línea o delimitador, el lexer decide cuál clase candidata representa el token correcto.
6. Si ninguna clase valida el lexema acumulado, se crea un `ErrorToken` con retroalimentación inferida.
7. Si el carácter actual es un delimitador, se agrega también su token correspondiente.
8. Al terminar la entrada, se agrega un token `EOF`.

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
- Las pruebas se ejecutan desde la raíz del repositorio con el comando:

```bash
python3 -m unittest -v test_lexer.py
```

## Estructura general del proyecto

```text
.
|-- Lexer.py
|-- run_lexer_task.py
|-- test_lexer.py
`-- Tokens/
    |-- token.py
    |-- keyword_token.py
    |-- identifier_token.py
    |-- number_token.py
    |-- hexadecimal_number_token.py
    |-- string_token.py
    |-- math_token.py
    |-- relational_token.py
    |-- logical_token.py
    |-- assignation_token.py
    |-- delimiter_token.py
    |-- EOF_token.py
    `-- error_token.py
```

## Descripción de archivos clave

### `Lexer.py`

Archivo central del proyecto. Implementa la clase `Lexer`, el recorrido secuencial de la entrada, la resolución del tipo de token más adecuado y la generación de errores y del token `EOF`.

### `run_lexer_task.py`

Script de demostración. Ejecuta el lexer sobre un programa de ejemplo y muestra la secuencia de tokens con su información básica.

### `test_lexer.py`

Conjunto principal de pruebas. Incluye casos válidos, casos de error y un escenario integrado con múltiples tipos de tokens y errores en un mismo programa.

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
- `math_token.py`: operadores aritméticos.
- `relational_token.py`: operadores relacionales.
- `logical_token.py`: operadores lógicos.
- `assignation_token.py`: asignación.
- `delimiter_token.py`: símbolos separadores.
- `EOF_token.py`: fin de archivo.

## Valor académico del proyecto

Este repositorio tiene un valor académico claro porque permite estudiar varios conceptos fundamentales de compiladores y procesamiento de lenguajes:

- separación entre análisis léxico y representación de tokens.
- diseño orientado a objetos para encapsular reglas de validación.
- manejo de errores léxicos con retroalimentación contextual.
- seguimiento de posiciones para diagnóstico.
- validacion automatizada mediante pruebas unitarias.

También sirve como base para futuras extensiones, por ejemplo: agregar más palabras reservadas, soportar nuevos símbolos o conectar este lexer con una etapa sintáctica posterior.

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