
## Descripción

Este proyecto ofrece una visión comprensiva de los datos relacionados con la plataforma Steam, enfocándose en usuarios, juegos, y reviews. A través de un conjunto de ETLs (Extracción, Transformación, Carga), análisis exploratorio de datos (EDA), funciones personalizadas y un modelo de recomendación, se busca entender mejor las dinámicas de uso, preferencias de los usuarios y patrones de interacción dentro de Steam. Con este enfoque se logra una comprensión detallada de los patrones de consumo y preferencias dentro de la platagorma Steam, ofreciendo insights valiosos tanto para usuarios como para desarrolladores de juegos.

## Proceso

El proyecto se estructura en torno a cuatro etapas principales (ETLs, EDA, Funciones y Modelo de Recomendación), cada uno cumpliendo con objetivos específicos:

### ETLs
- **ETL_users_items.py**: Procesa datos de usuarios y los juegos que poseen, limpiando y estructurando la información para análisis posterior.
- **ETL_users_reviews.py**: Enfocado en las reviews dejadas por usuarios, este ETL limpia y prepara los datos para explorar sentimientos y opiniones.
- **ETL_steam_games.py**: Trabaja con datos de los juegos disponibles en Steam, extrayendo características relevantes para el análisis y la recomendación.

### Análisis Exploratorio de Datos (EDA)
- **EDA.py**: Examina los datasets resultantes de los ETLs para identificar tendencias, patrones y anomalías, usando visualizaciones y estadísticas descriptivas.

### Funciones Steam
- **Funciones_Steam.py**: Contiene funciones útiles para manipular y analizar los datos de Steam, apoyando tanto el EDA como el proceso de recomendación.

### Modelo de Recomendación
- **Modelo_Recomendación.py**: Implementa un modelo para recomendar juegos a usuarios basándose en sus preferencias y comportamientos previos.

## Librerías Utilizadas

- Pandas
- Matplotlib
- Seaborn
- NumPy
- Sklearn
- Warnings
- PyArrow 



