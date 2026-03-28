## ENFORCE INTEGRITY
Para que tu código sea mantenible y siga estándares profesionales, la ubicación depende de la complejidad de tu proyecto. Aquí tienes las dos formas de organizarlo:

1. Proyecto Pequeño (Un solo archivo)
Si todo tu código vive en un app.py o main.py, colócalo inmediatamente después de crear el engine y antes de definir tus clases o llamar a sessionmaker.

```python
# app.py
engine = create_engine("sqlite:///datos.db")

# EL LISTENER VA AQUÍ (Configuración global del motor)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Luego sigue el resto...
Base = declarative_base()
Session = sessionmaker(bind=engine)
```

2. Proyecto Empresarial (Estructura de Carpetas)
En una aplicación real, lo ideal es separar la infraestructura de la lógica de negocio. Esta es la estructura recomendada:

mi_proyecto/
├── app/
│   ├── database.py    <-- AQUÍ va el código del engine y el listener
│   ├── models.py      <-- Aquí tus tablas (Cosa, Persona)
│   ├── crud.py        <-- Funciones para insertar/consultar
│   └── main.py        <-- Punto de entrada de la app
└── requirements.txt

En database.py:
Define el engine y registra el evento del PRAGMA. Otros archivos importarán el engine o la Session desde aquí.

En models.py:
Importas la Base desde database.py para definir tus tablas.

¿Por qué hacerlo así?
1. Evitas registros duplicados: Si pones el listener en un archivo que se importa muchas veces (como en los modelos), podrías terminar registrando el mismo evento varias veces por accidente.
2. Orden de ejecución: El Engine debe estar configurado antes de que la primera Session intente tocar la base de datos.
3. Modularidad: Si mañana decides cambiar SQLite por PostgreSQL, solo tienes que modificar el archivo database.py y borrar el listener (ya que Postgres sí tiene FK activas por defecto), sin tocar tus modelos ni tu lógica.

___
## LOG
El evento after_flush también debe ubicarse en tu archivo de configuración de base de datos (database.py), pero después de que la clase Session (o sessionmaker) haya sido definida.

Aquí tienes la estructura ideal para organizar ambos eventos en un entorno profesional:
Estructura en database.py

```python
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine

# 1. Configuración del Motor (Engine)
engine = create_engine("sqlite:///mi_empresa.db")

# EVENTO A NIVEL DE ENGINE (Configuración técnica: PRAGMAs)
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# 2. Configuración de la Fábrica de Sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# EVENTO A NIVEL DE SESSION (Lógica de Negocio: Auditoría/Logs)
# Usamos Session (la clase) para que afecte a todas las instancias creadas
@event.listens_for(Session, 'after_flush')
def audit_log_event(session, flush_context):
    for obj in session.new:
        print(f"[LOG] Insertado nuevo registro en {obj.__tablename__}")
    for obj in session.dirty:
        print(f"[LOG] Actualizado registro en {obj.__tablename__}")
    for obj in session.deleted:
        print(f"[LOG] Borrado registro en {obj.__tablename__}")
```

Por qué ubicarlos ahí y no en otro lado:
1. Centralización: Al mantener todos los listeners en el mismo archivo donde defines el acceso a datos (database.py), cualquier parte de tu app que importe SessionLocal ya tendrá activada la auditoría y las claves foráneas.
2. Evitar Importaciones Circulares: Si pones los eventos en models.py, y tus modelos necesitan importar algo de la base de datos, podrías romper el programa. Mantener la infraestructura (eventos, motor, sesión) separada de los datos (modelos) es una regla de oro en arquitectura limpia.
3. Rendimiento: El evento after_flush es potente porque ocurre justo antes de que los datos se graben permanentemente (commit), permitiéndote registrar cambios de forma masiva en lugar de hacerlo fila por fila.
4. Un detalle clave: En una app empresarial, dentro de audit_log_event, en lugar de un print(), llamarías a una función que inserte esos cambios en una tabla de auditoría dedicada.

## Estrategias de Log Enterprise Apps

Para una aplicación de nivel empresarial, la "mejor práctica" no es una sola herramienta, sino una estrategia de capas. No debes confiar solo en el .db-journal de SQLite, ya que es para recuperación técnica, no para auditoría de negocio.

Aquí tienes los tres pilares de un log de transacciones robusto:
1. Auditoría a nivel de Aplicación (SQLAlchemy Events)
En lugar de escribir print() o logging.info() manualmente en cada ruta, usa los eventos de SQLAlchemy. Esto garantiza que cada INSERT, UPDATE o DELETE quede registrado automáticamente.
*Implementación: Usa el evento after_flush o before_commit.
*Qué guardar: Quién lo hizo (user_id), qué cambió (valores viejos vs. nuevos), cuándo (timestamp) y en qué tabla.

```python
from sqlalchemy import event

@event.listens_for(Session, 'after_flush')
def receive_after_flush(session, flush_context):
    for obj in session.new: # Registra nuevos registros
        log_change(obj, "INSERT")
    for obj in session.dirty: # Registra modificaciones
        log_change(obj, "UPDATE")
```

2. Tablas de Auditoría (Shadow Tables)
No guardes los logs en un archivo de texto plano si necesitas reportes. Crea tablas de espejo. Por cada tabla importante (ej. prices), ten una tabla prices_audit.
* Ventaja: Puedes consultar quién cambió un precio hace 6 meses directamente con SQL.
* Librería recomendada: SQLAlchemy-Continuum o SQLAlchemy-Audit. Estas librerías gestionan el versionado de cada fila automáticamente.

3. Log de Diagnóstico (Tratamiento de Errores)
Para errores técnicos y transacciones fallidas, usa el módulo logging de Python configurado para escribir en un servicio externo (como ELK Stack, Datadog o Sentry).
* Configuración: Captura los IntegrityError y OperationalError de SQLAlchemy.
* Seguridad: Asegúrate de anonimizar datos sensibles (como passwords o tarjetas) antes de que lleguen al log.

Resumen de Arquitectura
Capa	        Herramienta	            Propósito
Recuperación	SQLite Journal/WAL	    Evitar que la DB se corrompa.
Auditoría	    Shadow Tables / Events	Saber "quién cambió qué" para cumplimiento (Compliance).
Monitoreo	    Python Logging + Sentry	Detectar errores en tiempo real.