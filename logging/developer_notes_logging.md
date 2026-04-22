## Youtube Tutorials
basic:
https://www.youtube.com/watch?v=-ARI4Cz-awo
advanced:
https://www.youtube.com/watch?v=jxmzY9soFXg

## Logging levels:

1. DEBUG: Detailed information, typically of interest only when diagnosing problems.
2. INFO: Confirmation that things are working as expected.
3. WARNING: An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). The software is still working as expected.
4. ERROR: Due to a more serious problem, the software has not been able to perform some function.
5. CRITICAL: A serious error, indicating that the program itself may be unable to continue running.

* Default level: 3 -> WARNING or Higer

## Documentation
# Log record attributes:
https://docs.python.org/3/library/logging.html#logrecord-attributes

## Enterprise Level Logging

En una aplicación empresarial, el nivel de detalle de los logs debe equilibrar la capacidad de diagnóstico con la seguridad y el costo de almacenamiento. 
* La industria se rige por las guías de OWASP (Logging Cheat Sheet) y las mejores prácticas de observabilidad. 

1. Niveles de Log Estándar 
Debes usar niveles de severidad para filtrar la información según el entorno (producción vs. desarrollo): 

* FATAL / CRITICAL: El sistema no puede continuar (ej: caída de base de datos).
* ERROR: Algo falló en una operación específica, pero la app sigue viva (ej: fallo al guardar un registro).
* WARN: Comportamientos inesperados que no cortan el flujo pero requieren atención (ej: reintentos de conexión, uso de APIs obsoletas).
* INFO: (Nivel estándar en producción) Eventos significativos del negocio (ej: "Usuario X inició sesión", "Transacción Y completada").
* DEBUG / TRACE: Detalles técnicos exhaustivos (queries SQL exactas, volcados de objetos). Desactivados en producción para evitar ruido y riesgos de seguridad. 

2. ¿Qué loggear en una transacción de API?
Para cada petición a tu API, deberías generar un registro estructurado (preferiblemente en JSON) que contenga: 

Datos del Contexto 	        Datos de la Transacción	        Identificadores de Rastreo
Timestamp (ISO 8601)	    Método HTTP (GET, POST...)	    Correlation ID: ID único para rastrear la petición en todos los microservicios.

IP del Cliente	            Endpoint (URL) accedido	        User ID: Quién realizó la acción (sin datos sensibles).

User-Agent (navegador/app)	Status Code (200, 404, 500)	    Request ID: ID único de la sesión actual.

Nivel de Log (INFO, ERROR)	Tiempo de respuesta (ms)	

3. Lo que JAMÁS debes loggear (Seguridad y Cumplimiento)
Por normativas como GDPR o PCI DSS, está estrictamente prohibido guardar: 

* Contraseñas o tokens de sesión en texto plano.
* Números de tarjetas de crédito completos.
* Datos de salud o información personalmente identificable (PII) sensible.
* Llaves privadas o secretos de configuración.

Recomendación Estratégica
* Implementa Logs Estructurados. En lugar de escribir texto libre, usa pares clave=valor. Esto permite que herramientas como el Elastic Stack (ELK) o CloudWatch Logs filtren instantáneamente todos los errores de un usuario específico o todas las peticiones que tardaron más de 500ms. 

## Ejemplo en Python:
Para implementar un log empresarial robusto en Python, lo ideal es usar logs estructurados en formato JSON. Esto permite que herramientas de análisis (como ELK, Splunk o Datadog) filtren y busquen datos específicos sin necesidad de procesar texto plano.
A continuación, te presento una implementación profesional utilizando el módulo estándar logging y un formateador personalizado:
Implementación de Log Estructurado

```python
import logging
import json
import uuid
from datetime import datetime

class StructuredFormatter(logging.Formatter):
    """Formatea el registro de log como un objeto JSON estructurado."""
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "correlation_id": getattr(record, "correlation_id", "N/A"),
            "user_id": getattr(record, "user_id", "anonymous")
        }
        
        # Incluir detalles de la excepción si existen
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_record)

# 1. Configuración del Logger
logger = logging.getLogger("AppEmpresarial")
handler = logging.StreamHandler()
handler.setFormatter(StructuredFormatter())
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# 2. Función de ejemplo para llamadas a la API
def registrar_llamada_api(metodo, endpoint, status, duracion_ms, usuario_id):
    # El Correlation ID permite rastrear esta petición en toda la infraestructura
    corr_id = str(uuid.uuid4()) 
    
    # Pasamos datos contextuales usando el argumento 'extra'
    contexto = {
        "correlation_id": corr_id,
        "user_id": usuario_id
    }
    
    mensaje = f"API {metodo} {endpoint} finalizada"
    
    # Agregamos datos técnicos al registro
    logger.info(
        f"{mensaje} | Status: {status} | Latencia: {duracion_ms}ms",
        extra=contexto
    )

# Ejecución de prueba
registrar_llamada_api("GET", "/api/v1/usuarios", 200, 145, "id_empleado_88")
```

# Por qué esta estructura es "Nivel Empresarial"
* Correlation ID: Generamos un ID único por petición. Si un usuario reporta un error, puedes buscar este ID y ver exactamente qué pasó en la API, la base de datos y los microservicios relacionados.
Contexto Dinámico: El uso de extra en la llamada del logger permite inyectar metadatos (como el user_id) sin ensuciar el mensaje principal de texto.
* Formato JSON: Al ser una cadena JSON, es directamente compatible con sistemas de agregación de logs modernos.
* Manejo de Tiempos: Se incluye la latencia (duracion_ms), lo cual es crítico para monitorear el rendimiento (SLA) de la aplicación empresarial. 

# Bibliotecas Alternativas
Si buscas algo más avanzado o con menos configuración manual, puedes considerar:
Structlog: La biblioteca estándar de facto para logs estructurados en Python.
Loguru: Muy popular por su sintaxis simplificada y manejo automático de rotación de archivos

## LECTURA DE LOGS

1. Visualización y Análisis (Paneles de Control)
Estas herramientas permiten buscar, filtrar y crear gráficas a partir de tus logs (como el JSON que configuramos antes). 
* Grafana Loki: Muy popular actualmente. Es como "Prometheus pero para logs". Es extremadamente eficiente porque no indexa el contenido completo de los logs, solo los metadatos, lo que reduce drásticamente el costo de almacenamiento.
* ELK Stack (Elasticsearch, Logstash, Kibana): El estándar de la industria. Kibana es la interfaz visual donde puedes realizar búsquedas potentes sobre millones de registros en segundos.
* Graylog Open: Excelente alternativa enfocada en la facilidad de uso y seguridad. Incluye alertas y gestión de usuarios de forma más intuitiva que ELK en su versión gratuita. 

2. Herramientas Ligeras y Modernas (Cloud-Native)
Si buscas algo más rápido de instalar o para entornos de contenedores:
* OpenObserve: Se promociona como una alternativa a Elasticsearch que consume hasta 140 veces menos almacenamiento. Es una solución "todo en uno" (logs, métricas y trazas) muy fácil de desplegar localmente con Docker.
* SigNoz: Una plataforma de observabilidad completa basada en OpenTelemetry. Permite correlacionar logs con trazas de la aplicación para ver exactamente qué línea de código causó un error. 

3. Recopiladores y Procesadores (Los que "mueven" el log)
Estas herramientas no son para "leer" el log con ojos humanos, sino para tomar el JSON que genera tu Python y enviarlo a las herramientas de arriba.
* Fluentd / Fluent Bit: Especialmente útiles en Kubernetes para recolectar logs de muchos contenedores y centralizarlos.
* Vector: Una herramienta de alto rendimiento escrita en Rust para construir tuberías de datos de observabilidad. 

4. Lectura Rápida en Terminal (CLI)
Si solo quieres ver tus logs JSON de forma legible mientras desarrollas:
* lnav: El "Log File Navigator". Es una herramienta de terminal que detecta automáticamente formatos (incluyendo JSON), resalta sintaxis y permite filtrar por errores en tiempo real.
* jq: No es una herramienta de logs per se, pero es el estándar para filtrar y "embellecer" cualquier salida JSON en la terminal.

## ENVIO DE ALERTAS 
En una arquitectura profesional, lo más escalable y limpio es generar alertas mediante la lectura del log (asíncronamente), pero manteniendo un buen manejo de excepciones interno.

1. El flujo recomendado: Observabilidad (Log → Alerta)
No conviene que tu main tenga la lógica de "enviar un mensaje a Slack o Teams". Si el sistema de mensajería falla o está lento, bloqueas tu proceso principal de sincronización.

* Paso A (Tu App): El main captura el raise de los módulos y simplemente hace un logger.error("Mensaje detallado", extra={"error_code": "DB_CONN_FAIL"}).
* Paso B (La Herramienta de Logs): Una herramienta como Grafana Loki, Graylog o OpenObserve "lee" ese log en tiempo real.
* Paso C (La Alerta): Configuras una regla en esa herramienta: "Si aparece un log con nivel ERROR más de 3 veces en 1 minuto, enviar alerta a Slack".

# Ventajas:
* Desacoplamiento: Tu código Python no necesita saber si usas Slack, PagerDuty o Email.
* Control de Fatiga: Puedes configurar que no te envíe 1,000 mensajes si fallan 1,000 inserts, sino un solo resumen.

2. ¿Cuándo sí usar el raise hacia el main?
El raise es fundamental para el control de flujo, no para la notificación externa.
* Los módulos (api.py, db.py) deben lanzar excepciones personalizadas si ocurre algo que ellos no pueden resolver.
* El main decide si reintenta la operación o detiene el programa.
Ejemplo de estructura ideal:
```python
# main.py
try:
    usuarios = api.obtener_usuarios(token)
    db.guardar_usuarios(usuarios)
except APIError as e:
    # Solo loggeamos el error. 
    # El sistema de logs se encargará de avisar al humano.
    logger.critical(f"Fallo crítico en sincronización: {e}", extra={"contexto": "AdobeAPI"})
except Exception as e:
    logger.error(f"Error inesperado: {e}")
```

3. Comparativa de Estrategias
Característica  Alerta en el Código (Main)	                        Alerta via Lectura de Logs
Complejidad	    Alta (debes programar el cliente de Slack/Email)	Baja (es configuración de la herramienta)
Rendimiento	    Afecta (la app espera a que se envíe el mensaje)	No afecta (es un proceso independiente)
Flexibilidad	Mala (tienes que recompilar para cambiar de canal)	Excelente (cambias la regla en un panel)
Fiabilidad	    Si la app muere, no hay alerta	                    Si la app muere, el sistema de logs detecta la ausencia de datos

## Resumen de la "Mejor Práctica"
1. Módulos: Hacen raise de excepciones específicas.
2. Main: Captura excepciones y genera un Log de nivel ERROR o CRITICAL con formato JSON.
3. Herramienta (Loki/Graylog): Escanea los logs y dispara la notificación al humano.

## Estructura Modular de loggers logging
Para una aplicación con múltiples módulos, la mejor práctica en Python es aprovechar la jerarquía de loggers. No necesitas un logger "global" en un util.py que importes en todos lados; en su lugar, debes configurar el Root Logger una sola vez al inicio y dejar que los demás módulos "hereden" esa configuración. 

1. Estructura recomendada
La clave es separar la configuración (qué hacer con los logs) de la emisión (generar los logs). 

En main.py (Punto de entrada)
Es aquí donde debes configurar cómo quieres que se vean los logs (formato, archivo, consola). Hazlo lo más pronto posible antes de importar otros módulos que usen el logger

```python
import logging
# Configuración única en el punto de entrada
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("app.log")
    ]
)

import api, db  # Los módulos importados después ya usarán esta config
```

En cada módulo (api.py, db.py, models.py)
No vuelvas a configurar nada. Simplemente crea un logger específico para ese archivo usando __name__. Esto permitirá que en los logs aparezca exactamente qué archivo generó el mensaje (ej: db o api.models)

```python
import logging
# Crea un logger con el nombre del módulo actual
logger = logging.getLogger(__name__)

def mi_funcion():
    logger.info("Iniciando proceso en este módulo")
```

2. ¿Conviene un util.py?
Solo si tu configuración es muy compleja (por ejemplo, si usas dictConfig con muchos handlers y formatos diferentes). En ese caso, puedes crear una función setup_logging() en util.py o config.py y llamarla solo una vez en tu main.py

3. Resumen de qué incorporar en cada parte
Archivo 	Qué incorporar	                        Por qué
main.py	    logging.basicConfig() o dictConfig()	Centraliza el control de dónde van los logs (consola, archivo, etc.).
api.py	    logger = logging.getLogger(__name__)	Permite rastrear errores específicos del tráfico de la API.
db.py	    logger = logging.getLogger(__name__)	Útil para debuguear queries o problemas de conexión.
models.py	logger = logging.getLogger(__name__)	Para loguear validaciones de datos o errores de lógica de negocio.

Pro-tip: Al usar logging.getLogger(__name__), si en el futuro decides que solo quieres ver logs de db.py en nivel DEBUG pero mantener el resto en INFO, puedes hacerlo desde main.py sin tocar el código de los otros archivos

## EJEMPLO

1. ¿Por qué en main.py también?
Si usas logging.info("mensaje") directamente en main.py, estarás usando el Root Logger. En los logs, el nombre del emisor aparecerá como root.

En cambio, si usas logger = logging.getLogger(__name__), en tus logs aparecerá __main__ (que es el nombre que Python le da al archivo que se ejecuta). Esto te ayuda a diferenciar qué mensajes vienen del flujo principal y cuáles de los módulos (api, db, etc.).

2. Estructura final en main.py
```python
# 1. Configuración global (se hace una sola vez)
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 1.2 importar los otros módulos
import api  # Tus otros módulos
import db

# 2. Logger específico para este archivo
logger = logging.getLogger(__name__)

def start_app():
    logger.info("Iniciando la aplicación...") # Aparecerá como __main__
    db.connect()
    api.run()

if __name__ == "__main__":
    start_app()
```

3. Ventaja visual en los Logs
Al hacerlo así en todos tus archivos, tu consola o archivo de texto se verá mucho más claro:
2023-10-27... - __main__ - INFO - Iniciando la aplicación...
2023-10-27... - db - INFO - Conexión exitosa a la base de datos
2023-10-27... - api - WARNING - Intento de acceso no autorizado

#Resumen rápido:
* En main.py: Haces el basicConfig (la configuración) Y creas el logger = logging.getLogger(__name__) (para los mensajes propios de main).
* En los módulos: SOLO creas el logger = logging.getLogger(__name__).

## Decorator logging
Imagina que tu jefe te pide que cada vez que una función falle, se guarde un registro (Log) con el tipo de error.
## Opción A: El método Manual (Lo que NO queremos)
Aquí, el programador tiene que escribir el try/except y el print (o log) en cada una de las funciones.

```python
def guardar_usuario():
    try:
        # lógica...
        print("Guardando...")
    except DatabaseError as e:
        print(f"[ERROR NIVEL: CRÍTICO] Falló la base de datos: {e}")
def llamar_api():
    try:
        # lógica...
        print("Llamando...")
    except APIError as e:
        print(f"[ERROR NIVEL: ALTO] Falló la API: {e}")
```

El problema: Si mañana el jefe dice: "Ahora quiero que el log incluya la hora", ¡tienes que cambiar 100 funciones a mano! Es aburrido y vas a cometer errores.
------------------------------
## Opción B: El Decorador (El estándar profesional)
Un decorador es como una "funda" o un "escudo" que le pones a cualquier función para darle superpoderes sin modificar su interior. [1] 
Vamos a crear un decorador que use tus clases de error (AppError, DatabaseError, etc.) para decidir qué tan grave es el log. [2] 

```python
import functools
# Este es nuestro "Ayudante de Log"
def estandarizar_log(func):
    @functools.wraps(func)
    def envoltorio(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseError as e:
            print(f"[LOG - NIVEL CRÍTICO]: {e}. Origen: {e.original_exc}")
            raise # Volvemos a lanzar el error para que la app sepa que falló
        except APIError as e:
            print(f"[LOG - NIVEL ALTO]: {e}. Status: {e.status_code}")
            raise
        except AppError as e:
            print(f"[LOG - NIVEL MEDIO]: {e}")
            raise
    return envoltorio
# --- AHORA MIRA QUÉ LIMPIO QUEDA TU CÓDIGO ---

@estandarizar_log
def guardar_en_db():
    # Simulamos un error de base de datos
    raise DatabaseError("No hay espacio en disco", original_exc="OSError: Disk Full")

@estandarizar_log
def consultar_servicio():
    # Simulamos un error de API
    raise APIError("Timeout", status_code=504)
```

## ¿Por qué esto es mejor? (La explicación para el junior)

   1. Centralización: Si quieres cambiar el formato del log (por ejemplo, enviarlo a un archivo .txt), solo cambias el código dentro del decorador una sola vez.
   2. Limpieza: Tus funciones como guardar_en_db() solo tienen la lógica del negocio. No están "sucias" con códigos de logs por todos lados.
   3. Consistencia: Te aseguras de que todos los errores de base de datos se vean igual en los logs, sin importar qué programador escribió la función.

¿Te das cuenta de cómo el decorador "atrapa" el error por ti y sabe qué nivel ponerle según la clase de la excepción?
¿Te gustaría intentar escribir una función pequeña y aplicarle este decorador para ver cómo reacciona?**
