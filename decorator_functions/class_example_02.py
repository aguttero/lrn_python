class Jugador:
    def __init__(self, nombre, puntos_vida):
        self.nombre = nombre
        self._vida = puntos_vida  # Usamos guion bajo para decir "es privado"

    # --- EJERCICIO 1: @property ---
    @property
    def estado(self):
        """Muestra si el jugador está vivo o muerto sin usar ()"""
        if self._vida > 0:
            return f"❤️ {self.nombre} está activo con {self._vida} HP"
        return f"💀 {self.nombre} ha sido derrotado"

    # --- EJERCICIO 2: @classmethod ---
    @classmethod
    def crear_boss(cls, nombre):
        """Atajo para crear un enemigo poderoso de una vez"""
        print(f"--- Generando un Jefe Final: {nombre} ---")
        return cls(nombre, puntos_vida=500)

# --- PRUEBA EL CÓDIGO ---

# 1. Creamos un jugador normal
player = Jugador("Link", 100)

# Mira: No usamos paréntesis en .estado porque es una @property
print("player.estado: ",player.estado ) 

# 2. Creamos un Boss usando el @classmethod
enemigo = Jugador.crear_boss("Ganondorf")
print("enemigo.estado: ",enemigo.estado ) 
print(enemigo.estado)
