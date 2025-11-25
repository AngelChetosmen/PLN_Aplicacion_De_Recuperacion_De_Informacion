
# PLN: Aplicación de Recuperación de Información

> [!NOTE]
> El proyecto **PLN: Aplicación de Recuperación de Información** ha sido desarrollado por:
> - J.A, Vega Reyes (autor de este repositorio)

Este proyecto fue desarrollado como práctica en la materia de **Procesamiento de Lenguaje Natural (PLN)** & **Machine Learning (ML)** en la **Escuela Superior de Cómputo** del **Instituto Politécnico Nacional**, Unidad Zacatenco, Ciudad de México.

---

> [!IMPORTANT]
> Este sistema está implementado en **Python**, ejecutándose con una interfaz gráfica hecha en **Tkinter** y utilizando librerías para análisis NLP como **NLTK**.
> Además, se cuenta con una interfaz web desplegada para su consulta y prueba directa:
> ```url
> [https://pln-aplicacion-de-recuperacion-de.onrender.com](https://pln-aplicacion-de-recuperacion-de.onrender.com)
>

También puedes descargar el corpus para pruebas:
* Desde la rama principal (default) del repositorio.
* Desde la rama `VOmega` donde se incluyen mejoras en el contenido para evaluación del modelo.

📌 El usuario puede ejecutar el sistema con su propio corpus siguiendo las instrucciones más adelante.

## 📌 Descripción del Proyecto

El proyecto Recuperación de Información tiene como objetivo procesar texto y realizar análisis semántico mediante un **modelo estadístico** que permite consultar términos y visualizar resultados relevantes dentro del corpus.

Incluye:
* ✔ **Normalización** del lenguaje
* ✔ **Eliminación de stopwords**
* ✔ **Modelado para recuperación de información**
* ✔ **Interfaz gráfica** para interacción del usuario

## 🧩 Estructura del Proyecto

El repositorio contiene scripts, recursos y módulos utilizados en la aplicación:

| Archivo / Carpeta | Descripción |
| :--- | :--- |
| `Procesamiento.py` | Módulo para limpiar y normalizar el corpus |
| `Main.py` | Ejecución principal de la interfaz de la aplicación |
| `corpus/` | Carpeta que contiene corpus crudos y normalizados |
| `requirements.txt` | Dependencias necesarias para ejecución |
| `README.md` | Documento guía del proyecto (este archivo) |

## ⚙️ Funcionalidades Principales

### Procesamiento de Texto
* Tokenización
* Lematización
* Stopwords en español mediante NLTK

### Modelado y Recuperación de Información
* Se analiza el corpus para recuperar términos relevantes
* Se muestran métricas de búsqueda basadas en coincidencias

### Interfaz de Usuario
* Formulario para cargar corpus propio
* Selección de métodos de análisis
* Visualización de resultados del modelo

## 📌 Requisitos

* **Python 3.8** o superior
* Librerías necesarias (instalación automática con):
    ```bash
    pip install -r requirements.txt
    ```
* NLTK y recursos en español descargados desde el mismo script

## 🚀 Instalación y Ejecución

### 1️⃣ Clonar el Repositorio
```bash
git clone [https://github.com/AngelChetosmen/PLN_Aplicacion_De_Recuperacion_De_Informacion.git](https://github.com/AngelChetosmen/PLN_Aplicacion_De_Recuperacion_De_Informacion.git)
````

### 2️⃣ Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar la Aplicación

```bash
python app.py 
#irse hasta la ruta donde se encuentra para una mejor ejecución de prueba, sino visualizar mejor desde la liga. 
```

## 🧪 Pasos Generales de Uso

> [\!TIP]
> Puedes realizar todo el proceso desde la misma aplicación, sin necesidad de manipular archivos externos.

1.  **Procesar el corpus crudo a corpus normalizado**.
2.  Ir a la sección de **Procesamiento**.
3.  Ejecutar la **normalización** desde el script.
4.  **Seleccionar el tipo de análisis**.
5.  **Visualizar los resultados**:
      * El modelo de recuperación mostrará la información según la consulta ingresada.

> [\!CAUTION]
> Si el corpus no se encuentra en el formato soportado o sin normalización, es probable que la aplicación no arroje resultados correctos.
> Se recomienda siempre ejecutar el proceso de limpieza primero.

## 🌐 Demostración en Línea

Puedes probar una versión web accesible desde:

`https://pln-aplicacion-de-recuperacion-de.onrender.com`

> [\!WARNING]
> El despliegue web puede tardar algunos segundos en cargar debido a limitaciones del hosting seleccionado.

## 📜 Licencia

Este proyecto está licenciado bajo **MIT** y **EUVA** (consultar la Politicas de EUVA en el repositorio general o perfil de GitHub del autor).

Consulta el archivo `LICENSE` para más información.
Cabe aclarar que el repositorio fue creado con fines educativos. Sin embargo, consultar las Politicas Oficiales de EUVA que se encuentran en el repositorio general para no tener problemas de plagio y duplicidad de trabajos.

El uso del corpus, modelo y código es totalmente permitido siempre y cuando se **cite el origen del proyecto. Recuerda, es para fines educativos, EUVA se deslinda de toda acción que perjudique a terceros por datos obtenidos desde los repositorios**.

-----

Gracias por revisar y utilizar esta herramienta. ¡Disfruta explorando el mundo del PLN\! 😄