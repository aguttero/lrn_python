## CODEBSE exceptions.py
```python
class AppError(Exception):
    pass

class DatabaseError(AppError):
    def __init__(self, message, original_exc=None):
        super().__init__(message)
        self.original_exc = original_exc

class APIError(AppError):
    def __init__(self, message, status_code=None, original_exc=None):
        super().__init__(message)
        self.status_code = status_code
        self.original_exc = original_exc

class AuthError(AppError):         # <-- new
    def __init__(self, message, original_exc=None):
        super().__init__(message)
        self.original_exc = original_exc
```

Lo que estás viendo aquí es un Árbol de Excepciones Personalizado. Vamos a desglosarlo paso a paso.
## 1. La "Base": AppError

```python
class AppError(Exception):
    pass
```

* Qué es: Estamos creando nuestro propio "molde" de error basado en el Exception estándar de Python.
* Por qué así: Sirve como una "etiqueta" global. Si en algún lugar de tu código quieres atrapar cualquier error que tú hayas definido (pero ignorar errores de Python como que se acabe la memoria), puedes usar except AppError. Es el padre de todos tus errores.

## 2. La Herencia: ¿Por qué DatabaseError(AppError)?
Fíjate que las otras clases tienen (AppError) entre paréntesis. Esto es herencia.

* Significa que un DatabaseError es un AppError.
* Esto permite que tu código sea muy organizado. Puedes ser específico ("atrapa solo fallos de base de datos") o general ("atrapa cualquier error de mi aplicación").

## 3. El Constructor: __init__ y super()
Miremos DatabaseError por dentro:

```python
def __init__(self, message, original_exc=None):
    super().__init__(message)
    self.original_exc = original_exc
```

* message: Es el texto amigable que explica qué pasó (ej: "No se pudo conectar al servidor").
* super().__init__(message): Esto le dice a Python: "Oye, toma este mensaje y dáselo a la clase padre para que se comporte como un error normal".
* original_exc=None: ¡Esto es clave! A veces el error ocurre porque otro error falló antes (ej: un error de conexión de red). Aquí guardamos ese "error original" para no perder el rastro de la causa raíz.

## 4. Especialización: El caso de APIError

```python
class APIError(AppError):
    def __init__(self, message, status_code=None, original_exc=None):
        ...
        self.status_code = status_code
```

* Diferenciación: Nota que APIError tiene algo que los demás no: status_code.
* Por qué: Los errores de base de datos no tienen códigos HTTP (como el famoso 404 o 500), pero las APIs sí. Al estructurarlo así, puedes guardar información extra que es específica para ese tipo de problema.

------------------------------
## ¿Por qué se estructura de esta manera? (El "Por qué" profesional)

   1. Legibilidad: Cuando lees raise DatabaseError, sabes exactamente en qué capa del software falló algo, sin tener que adivinar.
   2. Captura Selectiva: Puedes hacer esto en tu código:
   
   ```python
   try:
       # código que usa la base de datos y la API
    except DatabaseError:
       # "Reintenta la conexión..."
    except APIError:
       # "Muestra el código de estado al usuario..."
    except AppError:
       # "Algo genérico de la app falló..."
   ```

   3. Depuración (Debugging): Gracias a original_exc, aunque tú lances un error amigable, el programador puede ver qué error técnico (el "sucio") causó todo el lío originalmente.


## Como funciona ```python super().__init__(message)```
¡Esa línea es como una "llamada telefónica" al padre.
Para entender super().__init__(message), primero debemos recordar que en programación, cuando una clase hereda de otra, la clase hija hereda las habilidades de la madre.
## 1. El problema: ¿Quién guarda el mensaje?
La clase base de Python, Exception, ya sabe perfectamente cómo guardar un mensaje de error y mostrarlo en la pantalla (la famosa "traza" roja que ves cuando algo falla).
Si tú escribes tu propio __init__ en DatabaseError, estás reemplazando el comportamiento de Python. Si solo hicieras self.message = message, la funcionalidad interna de Python para manejar excepciones se quedaría "vacía".
## 2. La solución: super()
super() es una función especial que significa: "Busca a mi padre (la clase de arriba)".
Entonces, super().__init__(message) hace lo siguiente:

   1. Contacta al padre: Va a AppError (o directamente a Exception).
   2. Ejecuta su código: Llama al constructor original que Python ya escribió para las excepciones.
   3. Le pasa el recado: Le entrega el message para que el sistema de Python lo registre correctamente.

## Una analogía simple:
Imagina que heredas el negocio de pizzas de tu papá.

* Tu papá (la clase padre) sabe hacer la masa.
* Tú (la clase hija) quieres añadirle piña (tu toque especial).

Cuando un cliente pide una pizza, tú no aprendes a hacer masa desde cero. Tú usas super().hacer_masa() y luego tú le pones la piña.
En el código:

* super().__init__(message) hace la "masa" (configura el error básico en Python).
* self.original_exc = original_exc le pone la "piña" (tu dato extra).

Sin esa línea, tu error sería como una pizza sin masa: algo le faltaría para ser una excepción completa.
¿Te queda más claro por qué necesitamos avisarle al "padre" que estamos creando el error?**


## APP ERROR RAISE
Tal como está escrito tu código en este momento, sí, al AppError solo podrías pasarle el mensaje.
Pero aquí viene lo interesante de ser el "arquitecto" de tu propio código. Vamos a analizar qué pasa según cómo lo uses:
## 1. Si lo dejas como está
Como AppError tiene un pass, no tiene su propio __init__. Eso significa que usa directamente el de su padre (Exception).

```python
# Solo acepta el mensaje
raise AppError("Algo salió mal") 
```

## 2. ¿Qué pasa si quieres que TODOS tengan original_exc?
Si te das cuenta de que siempre vas a querer guardar el error original, lo mejor es subir esa lógica a la base. Así no tienes que repetirla en cada clase hija.
Mira este cambio:
```python
class AppError(Exception):
    def __init__(self, message, original_exc=None):
        super().__init__(message)
        self.original_exc = original_exc
class DatabaseError(AppError):
    pass # ¡Ahora DatabaseError ya sabe manejar original_exc automáticamente!
```

## 3. La ventaja de la flexibilidad
Con el código que pusiste al principio, la estructura te permite decidir:

* AppError: Es para errores genéricos o simples (solo mensaje).
* DatabaseError: Es para cuando necesitas rastrear el culpable (original_exc).
* APIError: Es el más completo (mensaje + código de estado + error original).

## Resumen para tu aprendizaje:
Si haces un raise AppError("msj"), solo guardas el mensaje. Si intentas pasarle un segundo argumento (como el status_code), Python te dará un error porque el molde de AppError no tiene un espacio para guardar eso.
¿Te gustaría ver cómo se vería un bloque try/except real donde capturamos un error de Python y lo "envolvemos" en tu DatabaseError usando el original_exc?**


## MAS DE UN ERROR
En Python (y en la mayoría de los lenguajes), solo puede "volar" un error a la vez.

Imagínalo como una alarma de incendio: aunque se rompan tres ventanas y fallen dos tuberías, la alarma suena por una razón principal que detiene la ejecución en ese momento.

Aquí te explico los dos escenarios posibles cuando tienes "varios" errores:
## 1. El error que ocurre primero gana
Python ejecuta el código línea por línea. En cuanto encuentra el primer problema, lanza la excepción y se sale de esa función. Lo que esté abajo ya no se ejecuta.

```python
def mi_api():
    # Línea 1: Falla la autenticación
    raise AuthError("Token vencido")
    
    # Línea 2: Falla el servidor (esto nunca se ejecutará)
    raise APIError("Error de servidor", status_code=500)
```

En este caso, solo verás el AuthError. El segundo error es como si no existiera.
## 2. El "Encadenamiento" (El error que causa otro error)
A veces, un error provoca el siguiente. Aquí es donde brilla tu variable original_exc.
Imagina este flujo:

   1. Falla la conexión a internet (Error de Python: ConnectionError).
   2. Tú capturas ese error y lanzas tu propio APIError.

```python
try:
    # 1. Error de "bajo nivel" (Internet)
    solicitar_datos_web() except ConnectionError as e:
    # 2. Tú "envuelves" ese error en el tuyo de "alto nivel"
    raise APIError("No puedo conectar a la API", original_exc=e)
```
¿Qué "sube"?
Sube el APIError, pero gracias a que guardaste el original_exc, el desarrollador puede investigar y ver que la causa raíz fue la conexión a internet. Es como una caja dentro de otra caja.
## ¿Y si quiero reportar varios errores a la vez?
Si estás validando un formulario (donde fallan el email, el nombre y la edad a la vez), los programadores no lanzan un raise de inmediato. Lo que hacen es:

   1. Crear una lista vacía: errores = [].
   2. Ir agregando los errores: errores.append(APIError("Email inválido")).
   3. Al final, si la lista no está vacía, lanzan un solo error que contenga toda la lista.

¿Te hace sentido que el código se detenga en el primer error que encuentra?**

