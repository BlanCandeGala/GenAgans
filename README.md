# GenAgans
GenAgans es una aplicación que le permitirá realizar el flujo de trabajo de análisis de variantes genéticas en humanos a partir de lecturas pareadas de forma interactiva, intuitiva y personalizada.

GenAgans ha sido probado en Ubuntu-22.04 y Conda 23.9.0.

Si encontrase algún problema para ejecutarlo, repórtelo, por favor.

## Intrucciones para ejecutar GenAgans
1. Abrir la terminal de Linux.

2. Instalar el ambiente de conda del archivo "GenAgans.yml". Este paso solo es necesario la primera vez que se vaya a ejecutar.

3. Activar el ambiente de conda "GenAgans" con "conda activate GenAgans".

4. Lanzar el comando: "shiny run --launch-browser app.py". En caso de no estar sobre el directorio en el que se encuentra el "app.py", deberá especificarse la ruta: "shiny run --launch-browser /ruta/a/app.py".

Una vez lanzado el comando debería abrirse automáticamente una pestaña en el navegador con GenAgans.

Si esto no ocurre automáticamente, copie la dirección "http" que aparece en el mensaje de la terminal. Por ejemplo, el caso de aparecer un mensaje como este:

"INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"

Deberá copiar el "http://127.0.0.1:8000" y pegarlo en el navegador para abrir GenAgans.
