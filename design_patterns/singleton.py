from typing_extensions import Self
import uuid


class MySingleton:
    _instance = None
    dato = "dato"
    id = None

    def __new__(cls) -> Self:
        if cls._instance is None:
            print("Creating new Singleton's instance")
            cls._instance = super(MySingleton, cls).__new__(cls) # Usa el method new de la clase padre
            cls.id = uuid.uuid4()
        return cls._instance
    
singleton = MySingleton()
singleton.dato = "dato cambiado"
singleton_2 = MySingleton()

print("singleton_2.dato: ", singleton_2.dato)
print("singleton_2.id: ", singleton_2.id)

## EXAMPLE
## Sistema de registro de eventos y queremos asegurarnos de que haya una única instancia de la clase EventLogger para garantizar que todos los eventos se registren de manera centralizada.
## Implementación para un sistema de login

import datetime
class EventLogger:
    _instance = None
    _event_logs = []

    def __new__(cls) -> Self:
        if cls._instance is None:
            cls._instance = super(EventLogger, cls).__new__(cls)
        return cls._instance
    
    def log_event (self, event_message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        self._event_logs.append(f"{timestamp}: {event_message}")

    def display_logs (self):
        for log in self._event_logs:
            print(log)

logger = EventLogger()
logger.log_event("starting app")
logger.log_event("executing task 1")

logger2 = EventLogger()
logger2.log_event("Finish task 1 desde logger 2")
logger2.log_event("End main run")

logger3 = EventLogger()
logger3.display_logs()

class SingleThreadSingleton():
    _instance = None
    # ver en el curso de Udemy
    pass




