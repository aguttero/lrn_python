## CASCADE DELETE - THREE APROACHS
# Tres estrategias principales dependiendo de qué quieras que pase con los "hijos" (las cosas) cuando eliminas al "padre" (la persona).

1. La Opción Profesional: "Cascade Delete"
Si tu lógica de negocio dicta que si una persona desaparece, sus cosas ya no tienen sentido, debes configurar el cascada en tu modelo. Esto delega la responsabilidad a SQLAlchemy para que borre todo en orden.
Configuración en el Modelo:

```python
class Persona(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    # cascade="all, delete-orphan" asegura que al borrar la persona, se borren sus cosas.
    # SQLAlchemy maneja el borrado
    things = relationship("Cosa", back_populates="owner", cascade="all, delete-orphan")
```

Código para eliminar:

```python
persona_a_borrar = session.get(Persona, 1) # Obtener persona con ID 1
if persona_a_borrar:
    session.delete(persona_a_borrar)
    session.commit() # SQLAlchemy borrará primero las 'Cosas' y luego la 'Persona'
```


2. La Opción de Seguridad (Restrict)
Si quieres evitar que se borre una persona si todavía tiene cosas asignadas (para proteger la integridad de los datos), debes confiar en el Foreign Key de SQLite que activamos con el PRAGMA.

* Requiere el event listener activado para el PRAGMA 

Código para manejar el error:
```python
from sqlalchemy.exc import IntegrityError

try:
    persona = session.get(Persona, 1)
    session.delete(persona)
    session.commit()
except IntegrityError:
    session.rollback()
    print("No se puede eliminar: La persona todavía tiene objetos asociados.")
```
---
```python
from sqlalchemy.exc import IntegrityError

# El @event.listens_for(Engine, "connect") ya debe estar en database.py

def borrar_persona_seguro(persona_id):
    persona = session.get(Persona, persona_id)
    if not persona:
        return "Persona no encontrada"

    try:
        session.delete(persona)
        session.commit() # Aquí es donde SQLite valida y lanza el error
        print("Persona eliminada con éxito.")
    except IntegrityError:
        session.rollback() # IMPORTANTE: Limpia la sesión tras el fallo
        print("BLOQUEADO: No puedes borrar a esta persona porque tiene 'cosas' asociadas.")
        print("Sugerencia: Borra primero sus 'cosas' o reasígnalas a otro dueño.")

```






3. La Opción Manual (Sin Cascadas)
Si no configuraste el cascade en el modelo, debes limpiar los hijos manualmente antes de borrar al padre para evitar errores de clave foránea:

```python
persona = session.get(Persona, 1)
if persona:
    # 1. Borrar o desvincular las cosas primero
    for cosa in persona.things:
        session.delete(cosa) 
    
    # 2. Ahora borrar a la persona
    session.delete(persona)
    session.commit()
```
# Resumen de Mejores Prácticas:
* Nivel Empresarial: Usa cascade="all, delete-orphan" si los datos están estrictamente ligados.
* Seguridad: Si los datos son valiosos (ej: facturas), no uses cascada; captura el IntegrityError y obliga al usuario a reasignar o borrar los registros relacionados manualmente.
* Soft Delete: En empresas grandes, a veces no se borra nada. Se usa una columna is_active = Column(Boolean, default=True) y solo se "oculta" el registro.

# Aclaraciones
El parámetro cascade="all, delete-orphan" se define específicamente para la primera estrategia (Borrado en Cascada Automático), pero es importante entender dónde y por qué:

1. ¿Dónde se declara?
Solo en la definición de la relationship() en tu modelo de SQLAlchemy (ORM). No se pone en la columna ForeignKey ni en la tabla física de la base de datos.

2. ¿Qué pasa en las otras estrategias?
* Estrategia 2 (Restringir/Error): No usas cascade. Al no tenerlo, si intentas borrar una Persona que tiene Cosas, SQLAlchemy intentará borrar solo a la persona. Como activamos el PRAGMA foreign_keys=ON, SQLite saltará con un IntegrityError porque hay "huérfanos" prohibidos.
* Estrategia 3 (Manual): No usas cascade. Tú mismo escribes el código para buscar las cosas, borrarlas una por una con session.delete(cosa) y finalmente borrar a la persona.

3. Diferencia Crítica: Cascada en DB vs. Cascada en ORM
Hay una confusión común aquí:
* cascade en relationship (ORM): SQLAlchemy busca los hijos en memoria y envía comandos DELETE individuales para cada uno antes de borrar al padre. Es más lento pero activa todos tus logs de auditoría (after_flush).
* ondelete="CASCADE" en ForeignKey (DB): Esto se pone en la columna del SQL. Es la base de datos la que borra todo instantáneamente. Es rapidísimo, pero SQLAlchemy no se "entera" de qué registros desaparecieron, lo que puede romper tus logs de auditoría.

Recomendación empresarial: Usa siempre el cascade de la relationship (Estrategia 1), ya que mantiene la lógica de negocio y tus logs de auditoría sincronizados con lo que pasa en el disco.