## INSTALL
```curl
curl -fsSL https://opencode.ai/install | bash
```

-f (fail silently): Si hay un error en el servidor, no muestra el código de error HTML; simplemente falla sin hacer nada.

-s (silent): Oculta la barra de progreso y los mensajes de estado.

-S (show error): Si el comando falla (aunque esté en modo silencio), sí te mostrará el mensaje del error.

-L (location): Si la página se movió (redirección), curl seguirá el nuevo enlace automáticamente.
https://opencode.ai/install: Es la dirección donde vive el script de instalación.

| (pipe): Envía la "salida" del primer comando (el código del script descargado) como "entrada" al siguiente comando.
bash: Es el intérprete de comandos que lee el script recibido y lo ejecuta inmediatamente en tu computadora. 

# Descarga Segura:
1. Descarga
```bash
curl -LO https://opencode.ai/install
```
-L: Sigue las redirecciones (necesario porque muchas URLs de instalación apuntan a GitHub u otros servidores).

-O (O mayúscula): Guarda el archivo en tu computadora con el mismo nombre que tiene en el servidor (en este caso, se guardará un archivo llamado install).

2. Revisar contenido (Opcional)

```bash
less install
```
* q para salir del visor

3. Ejecutar script manualmente
 ```bash
 bash install
 ```

 * Nota técnica: Si usas -o (o minúscula), debes especificar un nombre para el archivo, por ejemplo: curl -L https://opencode.ai -o mi_instalador.sh.

# Pistas sobre codigo malicioso:
Aquí tienes los puntos clave que debes buscar al abrir el archivo con less install o nano install:

1. Comandos de Red y Descargas Ocultas
Busca si el script intenta descargar otros archivos de fuentes desconocidas o enviar tus datos a un servidor externo.

* Qué buscar: curl, wget, nc (netcat), o direcciones IP extrañas.
* Peligro: Que el script sea solo una "puerta de entrada" para descargar un virus más pesado que no estaba en el archivo original.

2. Ofuscación (Código que no se entiende)
Si ves bloques de texto que parecen basura o letras al azar, es una señal roja inmediata.
* Qué buscar: Cadenas largas en Base64 (parecen ZXhwcmVzc2lvbg==) o el comando eval.

* Peligro: Los atacantes usan base64 para esconder comandos maliciosos que no quieren que leas. El comando eval ejecuta ese código escondido.

3. Modificación de Archivos de Inicio
Un script legítimo puede añadir una ruta al PATH, pero uno malicioso intentará mantenerse en tu sistema para siempre.

* Qué buscar: Referencias a .bashrc, .zshrc, .profile o carpetas como /etc/cron.d (tareas programadas).

* Peligro: Que el programa se ejecute automáticamente cada vez que enciendas la computadora o abras una terminal, incluso si crees que lo borraste.

4. Permisos de Superusuario (Sudo)
Mira dónde pide permisos de administrador.
* Qué buscar: El uso de sudo seguido de comandos de movimiento de archivos como mv o cp hacia carpetas del sistema (como /usr/bin o /etc).
* Peligro: Si el script intenta reemplazar archivos vitales del sistema operativo por versiones modificadas.

5. Acceso a SSH o Claves
Un instalador de IA no debería tocar tus llaves de seguridad.
* Qué buscar: La carpeta .ssh, archivos como id_rsa o authorized_keys.
* Peligro: Robo de tus credenciales para entrar a tus servidores de forma remota.

# Resumen rápido de búsqueda:
Dentro del editor, puedes presionar / (en less o vi) para buscar estas palabras clave:
/base64
/eval
/.ssh
/curl (para ver a qué otras URLs conecta)

## Configuracion Ollama
opencode.json debe estar en una ubicación específica dependiendo de cómo planees usarlo:

1. Ubicación Estándar (Global para tu usuario)
La mayoría de las herramientas de CLI modernas buscan su configuración en el directorio de inicio del usuario. Debes guardarlo en: 

* Ruta: ~/.opencode.json
En Windows (PowerShell): $HOME\.opencode.json
Esta es la mejor opción si quieres que OpenCode funcione igual sin importar en qué carpeta de proyectos estés trabajando.

2. Ubicación por Proyecto (Específica)
Si tienes un proyecto que requiere un modelo diferente (por ejemplo, usar Claude para un proyecto web y GPT-4 para análisis de datos), puedes guardarlo en:
Ruta: El directorio raíz de tu proyecto (donde está el archivo .git o el package.json).

3. Estructura recomendada del archivo
Asegúrate de que el contenido tenga un formato válido de JSON. Un ejemplo básico se ve así:

* buscar en opeconde.ai docs > Providers

```json
{
  "model": "gpt-4",
  "api_key": "tu-llave-aqui",
  "provider": "openai"
}
```

¿Cómo moverlo rápidamente?
Si ya creaste el archivo y quieres moverlo a la ubicación global, usa este comando:
```bash
mv opencode.json ~/.opencode.json
```

Un consejo extra: Si vas a subir tu código a GitHub, asegúrate de añadir opencode.json a tu archivo .gitignore para no filtrar accidentalmente tus llaves de API.

## EJEMPLO opencode.json

```json
{
    "$schema": "https://opencode.ai/config.json",
    "provider":{
        "ollama": {
            "npm": "@ai-sdk/openai-compatible",
            "name": "Ollama (local)" ,
            "options": {
                "baseURL": "http://localhost:11434/v1"
            },
            "models":{
                "qwen3:8b": {"name": "qwen3:8b"}

            }
        }
    },
    "permission": {
        "edit": "ask",
        "bash": {
            "*": "ask",
            "ls": "allow"
        }
        },
    "plugin": ["@mohak34/opencode-notifier@latest"]
}
```

## OLLAMA Requirements:

Ollama debe estar corriendo de fondo antes de abrir el editor.
OpenCode no "enciende" Ollama por ti; actúa como un cliente que envía peticiones a una dirección local (servidor) que Ollama habilita al ejecutarse.

Aquí tienes los pasos exactos para dejarlo funcionando:

1. Preparar el motor (Ollama)
* Instalación: Si ya lo tienes, asegúrate de que el icono de Ollama aparezca en la barra de tareas (Windows/Mac) o que el servicio esté activo en Linux.
* ejecutar ollama: Ollama list para ver lista de modelos descargados


* Descargar el modelo: Abre una terminal y descarga el modelo que elegiste (por ejemplo, Qwen 3 Coder):

One tip: for 8GB Macs, set conservative Ollama settings — OLLAMA_MAX_RAM=6GB and OLLAMA_NUM_PARALLEL=1 Localaimaster to avoid RAM pressure from your OS competing with the model.

```bash
ollama pull qwen2.5-coder:7b
ollama pull deepseek-r1:7b
ollama pull phi4-mini
ollama pull yi-coder
```

Para mas de 8G
```bash
ollama pull qwen3-coder:7b
ollama pull qwen3:8b
```

* Verificación: Ejecuta ollama list para confirmar que el modelo está en tu disco.

2. Configurar el "Servidor" de Ollama
Por defecto, Ollama corre en http://localhost:11434.
Hacer ping para ver si está running

* Importante: No necesitas ejecutar ollama run [modelo] para que la extensión funcione. Solo con que el proceso de Ollama esté abierto en segundo plano es suficiente. La extensión llamará al modelo automáticamente cuando lo necesite.

3. Vincular OpenCode con Ollama
Dentro de Visual Studio Code, sigue estos pasos en la configuración de la extensión:
+ Abre los Ajustes: Ve a la pestaña de extensiones, busca OpenCode y entra en su configuración (Extension Settings).

+ Selecciona el Proveedor: Busca la opción de "Provider" o "Backend" y cámbiala de OpenAI/Anthropic a Ollama.

+ Define la URL: Asegúrate de que la URL del servidor sea http://localhost:11434 (suele venir por defecto).

+ Escribe el nombre del modelo: En el campo "Model", escribe exactamente el nombre que viste en la terminal, por ejemplo: qwen3-coder:7b.

4. ¿Debo ejecutar algo más?
No es necesario ejecutar comandos adicionales cada vez. El flujo diario sería:
+ Encender tu PC (Ollama suele iniciar solo).
+ Abrir VS Code.
+ Empezar a programar.

Tip Pro: Si notas que la extensión no responde, abre tu navegador y ve a http://localhost:11434. Si ves un mensaje que dice "Ollama is running", el problema está en el nombre del modelo dentro de los ajustes de VS Code.