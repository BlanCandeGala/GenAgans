# GenAgans
GenAgans es una aplicación que le permitirá realizar el flujo de trabajo de análisis de variantes genéticas en humanos a partir de lecturas pareadas de forma interactiva, intuitiva y personalizada.

GenAgans ha sido probado en Ubuntu-22.04 y Conda 23.9.0.

Para su correcto funcionamiento requiere que los directorios y archivos "comando_css_html2", "comandos_java_html2", "custom_css" y "app.py" se encuentren dentro de un mismo directorio.

Si encontrase algún problema al ejecutarlo, repórtelo, por favor.

---
GenAgans is an application that allows you to perform the genetic variant analysis workflow from paired-end reads in an interactive, intuitive, and customizable way.

GenAgans has been tested on Ubuntu-22.04 and Conda 23.9.0.

For proper execution, the directories and files "comando_css_html2", "comandos_java_html2", "custom_css", and "app.py" must be located in the same directory.

If you encounter any issues while running the application, please report them.

## Intrucciones para ejecutar GenAgans / Instructions to run GenAgans
1. Abrir la terminal de Linux.

2. Instalar el ambiente de conda del archivo "GenAgans.yml" con "conda env create -f GenAgans.yml". Este paso solo es necesario la primera vez que se vaya a ejecutar.

3. Activar el ambiente de conda "GenAgans" con "conda activate GenAgans".

4. Lanzar el comando: "shiny run --launch-browser app.py". En caso de no estar sobre el directorio en el que se encuentra el "app.py", deberá especificarse la ruta: "shiny run --launch-browser /ruta/a/app.py".

Una vez lanzado el comando debería abrirse automáticamente una pestaña en el navegador con GenAgans.

Si esto no ocurre automáticamente, copie la dirección "http" que aparece en el mensaje de la terminal. Por ejemplo, el caso de aparecer un mensaje como este:

"INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)"

Deberá copiar el "http://127.0.0.1:8000" y pegarlo en el navegador para abrir GenAgans.

---
1. Open the Linux terminal

2. Install the Conda environment from the "GenAgans.yml" file using: "conda env create -f GenAgans.yml". This step is only required the first time you run the application.

3. Activate the Conda environment with: "conda activate GenAgans"

4. Launch the application by running the command:
"shiny run --launch-browser app.py"
If you are not inside the directory where "app.py" is located, specify the full path:
"shiny run --launch-browser /path/to/app.py"

Once the command is executed, a new browser tab should automatically open with GenAgans.

If this does not happen automatically, copy the "http" address that appears in the terminal message. For example, if you see the following message:

INFO: Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

You should copy "http://127.0.0.1:8000" and paste it into your browser to open GenAgans.

