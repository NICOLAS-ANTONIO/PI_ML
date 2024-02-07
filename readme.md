![Imagen Steam](https://areajugones.sport.es/wp-content/uploads/2015/01/Steam-OS-Planet-Steam-Logo-780x440.jpg) 


## Descripción

Este proyecto ofrece una visión comprensiva de los datos relacionados con la plataforma Steam, enfocándose en usuarios, juegos, y reviews. A través de un conjunto de ETLs (Extracción, Transformación, Carga), análisis exploratorio de datos (EDA), funciones personalizadas y un modelo de recomendación, se busca entender mejor las dinámicas de uso, preferencias de los usuarios y patrones de interacción dentro de la plataforma. Con este enfoque se logra una comprensión detallada de los patrones de consumo y preferencias dentro de esta comunidad gaming, ofreciendo insights valiosos tanto para usuarios como para desarrolladores de juegos.

## Proceso

El proyecto se estructura en torno a cuatro etapas principales (ETLs, EDA, Funciones y Modelo de Recomendación), cada uno cumpliendo con objetivos específicos:

### ETLs
- **ETL_users_items**: Procesa datos de usuarios y los juegos que poseen, limpiando y estructurando la información para análisis posterior.
- **ETL_users_reviews**: Enfocado en las reviews dejadas por usuarios, este ETL limpia y prepara los datos para explorar sentimientos y opiniones.
- **ETL_steam_games**: Trabaja con datos de los juegos disponibles en Steam, extrayendo características relevantes para el análisis y la recomendación.

### Análisis Exploratorio de Datos (EDA)
- **EDA**: Examina los datasets resultantes de los ETLs para identificar tendencias, patrones y anomalías, usando visualizaciones y estadísticas descriptivas.

### Funciones Steam
- **Funciones_Steam**: Contiene funciones útiles para manipular y analizar los datos de Steam, apoyando tanto el EDA como el proceso de recomendación.

### Modelo de Recomendación
- **Modelo_Recomendación**: Implementa un modelo para recomendar juegos a usuarios basándose en sus preferencias y comportamientos previos.

### Módulos y Librerias Utilizadas

- **Módulos de la Biblioteca Estándar de Python**:
    - `json`: Módulo para trabajar con datos JSON.
    - `warnings`: Módulo para emitir alertas.
    - `re`: Módulo para trabajar con expresiones regulares.
    - `gc`: Módulo para la gestión del recolector de basura.
    - `ast`: Módulo de la biblioteca estándar de Python para el procesamiento, creación y manipulación del árbol de sintaxis abstracta de Python.

- **Librerías Externas**:
    - `pandas`: Librería para manipulación y análisis de datos.
    - `matplotlib.pyplot`: Librería para crear gráficos y visualizaciones.
    - `seaborn`: Librería basada en matplotlib para visualizaciones estadísticas.
    - `numpy`: Librería para el soporte de vectores y matrices grandes multidimensionales.
    - `textblob`: Librería para procesamiento de texto simplificado y análisis de sentimiento.
    - `sklearn.decomposition.PCA`: Componente de la librería scikit-learn para Análisis de Componentes Principales.
    - `sklearn.metrics.pairwise.cosine_similarity`: Componente de la librería scikit-learn para calcular la similitud coseno entre vectores.
    - `fastapi`: Framework para construir APIs con Python 3.7+.


### Deploy render   
Se pueden revisar los endpoints y el modelo de recomendación desplegados en render en el siguiente link: https://steam-ml-loh5.onrender.com/docs


### Video solicitado
Se puede ver el video explicando brevemente el modelo y probando el deploy aquí: https://drive.google.com/file/d/1I05_P2-7fQ5Lmch__juULZMALHuc7EJv/view?usp=sharing


