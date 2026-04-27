# SETUP ORM Database and Engine
ver `sql_lite/test_upsert/`



# ORM Mapping model
## session.add (ORM) vs session.execute (CORE)

En SQLAlchemy, la elección depende de si quieres trabajar con objetos (ORM) o con rendimiento puro (Core).
Aquí tienes la comparativa de session.add() vs. session.execute(insert(...)):
## 1. session.add(objeto_instancia) (Estilo ORM)
Es la forma estándar de trabajar con clases Mapped. Creas una instancia de tu clase y la añades a la sesión.

* Pros:
* Identidad: El objeto queda vinculado a la sesión. Si cambias un atributo después del .add(), SQLAlchemy lo detectará y actualizará automáticamente en el siguiente flush.
   * Relaciones: Maneja automáticamente las relaciones (p. ej., si insertas un "Padre" con una lista de "Hijos", SQLAlchemy se encarga de las llaves foráneas).
   * Facilidad: Recuperas el ID generado inmediatamente en el objeto tras hacer session.commit() o flush().
* Contras:
* Velocidad: Es más lento para inserciones masivas (miles de registros) porque SQLAlchemy debe rastrear el estado de cada objeto individualmente.

## 2. session.execute(insert(Modelo).values(...)) (Estilo Core/Bulk)
Aquí tratas a la base de datos de forma más directa, enviando un comando SQL INSERT.

* Pros:
* Rendimiento: Es significativamente más rápido para inserciones masivas (Bulk Inserts). Envía los datos directamente sin crear instancias pesadas de Python para cada fila.
   * Menos Memoria: No carga los objetos en el "Identity Map" de la sesión, lo que ahorra RAM.
* Contras:
* Desconexión: Los datos insertados no se convierten automáticamente en objetos que puedas seguir usando en tu código; son solo registros en la DB.
   * Manual: No gestiona automáticamente las relaciones complejas ni la cascada de datos.

------------------------------
## Resumen comparativo

| Característica | session.add() | session.execute(insert()) |
|---|---|---|
| Uso principal | Lógica de negocio y pocos registros. | Carga masiva de datos (Batch). |
| Rastreo (Tracking) | Sí, el objeto vive en la sesión. | No, es una operación de "dispara y olvida". |
| Velocidad | Lenta (overhead de objetos). | Muy alta (directo a SQL). |
| Relaciones | Automáticas. | Manuales. |

Recomendación: Usa .add() por defecto para mantener la integridad de tu lógica de objetos. Solo cambia a .execute() si notas que tu script se vuelve lento al procesar miles de filas a la vez.
¿Estás trabajando con procesamiento de datos por lotes o es una interacción normal de usuario (un registro a la vez)? Bolding




# CASCADE DELETE - THREE APROACHS
## Tres estrategias principales dependiendo de qué quieras que pase con los "hijos" (las cosas) cuando eliminas al "padre" (la persona).


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

Si una "Cosa" siempre debe pertenecer a alguien, define la columna como nullable=False. Así, SQLite impedirá que el owner se convierta en NULL

* Requiere el event listener activado para el PRAGMA 
* Requiere el campo FK como nullable=False -> CONTROL EN SQLITE 

* Por perfomance y limpieza de logs es buena practica que la relación en la tabla de Persona tenga passive_deletes = "all"
Por defecto, SQLAlchemy intenta "ayudar" seteando los hijos en NULL (Cargando en RAM). Para que sea SQLite quien tome el control y bloquee la operación, debes indicarle a la relación que no intervenga.

La solución definitiva para la Estrategia 2:
Si quieres que explote el error y no se borre nada, usa nullable=False en la FK. Si por alguna razón necesitas que el campo sea opcional pero que no se pueda borrar el dueño si tiene cosas, entonces la clave es el passive_deletes="all".



```python
class Persona(Base):
    __tablename__ = 'people'
    id = Column(Integer, primary_key=True)
    # passive_deletes="all" evita que SQLAlchemy setee en NULL los hijos en memoria
    things = relationship("Cosa", back_populates="owner", passive_deletes="all")
```




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

## Escenario de Nullable = True y Passive Delete = all

# Escenario:
Restringir el borrado, pero permitir registros huérfanos voluntarios".

Tiene sentido cuando quieres que la relación sea opcional, pero no quieres que se rompa por accidente.

# El escenario de negocio: "Activos en Stock"
Imagina un sistema de inventario donde tienes Empleados y Laptops.

* La regla: Una Laptop puede no estar asignada a nadie (nullable=True), esperando en el almacén.
* El conflicto: Si una Laptop sí está asignada a "Juan", no quieres que alguien borre a "Juan" del sistema y la laptop quede asignada a un ID fantasma. Quieres que el sistema te obligue a quitarle la laptop a Juan antes de poder despedirlo (borrarlo).

# Por qué usar passive_deletes="all" con nullable=True:
* Sin passive_deletes: Si borras a Juan, SQLAlchemy pondrá el owner_id de la laptop en NULL automáticamente. Juan desaparece y la laptop vuelve al stock "en silencio".
* Con passive_deletes="all" (y el PRAGMA activo): Al intentar borrar a Juan, SQLAlchemy no toca la laptop. SQLite detecta que la laptop todavía apunta a Juan y bloquea el borrado.

* Resultado: El sistema te obliga a ser consciente. Debes entrar a la ficha de la laptop, poner el dueño en NULL manualmente (desvincularlo), y entonces ya puedes borrar a Juan.

# Beneficio para el negocio:
* Evita pérdida de rastro: Impide que registros importantes (como activos, contratos o expedientes) pierdan su referencia histórica de forma automática y silenciosa.
* Integridad referencial estricta: Aseguras que si un dato apunta a otro, ese "otro" existe, aunque la relación sea opcional.

# Resumen técnica:
Configuración	                        Comportamiento al borrar al Padre
nullable=True + Default	                Los hijos se ponen en NULL (desvinculación automática).
nullable=True + passive_deletes="all"	Error de Integridad (bloqueo hasta desvinculación manual).

# Aclaración Beneficios passive_deletes = "all"
Entonces, ¿para qué sirve passive_deletes="all" si ya tengo nullable=False?

Sirve principalmente por rendimiento y limpieza de logs:

* Evitas consultas innecesarias: Sin passive_deletes, SQLAlchemy intentará cargar todos los objetos hijos en la memoria de Python solo para "ver qué hace con ellos" antes de borrar al padre. Si una persona tiene 10,000 "cosas", SQLAlchemy traerá 10,000 objetos a RAM innecesariamente. Con passive_deletes="all", SQLAlchemy ni siquiera mira los hijos; lanza el DELETE del padre directamente y deja que la DB falle rápido.

* Logs de SQL más limpios: Verás en tu consola un solo DELETE fallido, en lugar de una ráfaga de UPDATEs fallidos seguidos de un DELETE.

* Consistencia Total: Es la forma de decirle a SQLAlchemy: "No intentes gestionar la integridad tú, confío plenamente en las reglas que puse en SQLite".

En resumen:
nullable=False: Es tu seguro de vida (la regla física).
passive_deletes="all": Es una optimización (evita que Python trabaje de más intentando "ayudar" donde no debe).
En una app empresarial, se usan ambos para que el sistema sea robusto y eficiente.

# Qué pasa si quitas el Event Listener pero dejas el passive_deletes?

Sucedería lo peor para una app empresarial: corrupción de integridad referencial.

* SQLAlchemy enviará el DELETE de la Persona (sin tocar las Cosas, porque es "pasivo").

* SQLite recibirá el DELETE. Como no tiene el "interruptor" (PRAGMA) encendido, borrará a la Persona sin rechistar.

* Resultado: Tus registros en la tabla Cosas ahora tienen un owner_id que apunta a alguien que ya no existe. Tus datos están rotos.

* La combinación ganadora:
Para que tu sistema sea de nivel empresarial, necesitas la cadena de mando completa:
* PRAGMA foreign_keys=ON (vía Event Listener): Activa la vigilancia en el motor.
* nullable=False: Crea la regla física de que no puede haber hijos sin padre.
* passive_deletes="all": Optimiza a SQLAlchemy para que no trabaje de más y deje que la DB haga su trabajo.

En resumen: El passive_deletes solo tiene sentido si hay alguien en la base de datos escuchando (el PRAGMA). Si apagas al guardia (el listener), el comando pasivo simplemente deja la puerta abierta para que los datos se desordenen.