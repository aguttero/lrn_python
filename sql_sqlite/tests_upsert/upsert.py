from sqlalchemy.dialects.sqlite import insert

# 1. Crear la sentencia de inserción inicial
stmt = insert(mi_tabla).values(id=1, nombre="Nuevo Nombre", stock=10)

# 2. Definir el comportamiento ante un conflicto
# index_elements: columnas que forman el índice único o clave primaria
# set_: diccionario con los campos a actualizar si hay conflicto
upsert_stmt = stmt.on_conflict_do_update(
    index_elements=['id'],
    set_=dict(
        nombre=stmt.excluded.nombre,  # 'excluded' refiere al valor que se intentó insertar
        stock=stmt.excluded.stock
    )
)

# 3. Ejecutar
with engine.begin() as conn:
    conn.execute(upsert_stmt)
