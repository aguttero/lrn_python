from sqlalchemy import event

# El evento after_flush debe ubicarse en tu archivo de configuración de base de datos (database.py), después de que la clase Session (o sessionmaker) haya sido definida.

@event.listens_for(Session, 'after_flush')
def receive_after_flush(session, flush_context):
    for obj in session.new: # Registra nuevos registros
        log_change(obj, "INSERT")
    for obj in session.dirty: # Registra modificaciones
        log_change(obj, "UPDATE")

## OTRO EJEMPLO MAS COMPLETO:

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

