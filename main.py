from fastapi import FastAPI, HTTPException
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import cosine_similarity
import gc  # Para la gestión de la memoria

app = FastAPI()
# Redirigir de la raíz a /docs
@app.get("/", include_in_schema=False)
async def root_redirect():
    return RedirectResponse(url='/docs')

# Cargar los archivos parquet 
archivos_parquet = {
    'df_ur': 'DataSet/clean_df_ur.parquet',
    'df_ui': 'DataSet/definitivo_df_ui.parquet',
    'df_sg': 'DataSet/definitivo_df_sg.parquet'
}

# Optimización: Funciones para cargar DataFrames
def cargar_dataframe(nombre):
    try:
        if nombre in archivos_parquet:
            return pd.read_parquet(archivos_parquet[nombre])
        else:
            raise ValueError(f"No existe un archivo parquet para {nombre}")
    except FileNotFoundError as e:
        raise ValueError(f"El archivo para {nombre} no se encontró: {e}")

class RecomendacionManager:
    def __init__(self):
        self.game_features_reduced = None

    def cargar_y_preparar_datos(self):
        if self.game_features_reduced is None:
            df_ui = cargar_dataframe('df_ui')
            df_sg = cargar_dataframe('df_sg')
            combined_df = pd.merge(df_ui[['item_id', 'playtime_forever_log']], df_sg[['id', 'price']], left_on='item_id', right_on='id')
            game_features = combined_df[['playtime_forever_log', 'price']].astype({'playtime_forever_log': 'float32', 'price': 'float32'})
            pca = PCA(n_components=2)
            self.game_features_reduced = pca.fit_transform(game_features)
        return self.game_features_reduced

# Instancia de la clase RecomendacionManager
recomendacion_manager = RecomendacionManager()

@app.get("/recomendacion-juego/{game_id}")
async def get_recomendacion_juego(game_id: int, top_n: int = 5):
    try:
        game_features_reduced = recomendacion_manager.cargar_y_preparar_datos()
        df_ui = cargar_dataframe('df_ui')
        if game_id not in range(len(game_features_reduced)):
            raise ValueError("ID de juego no válido")
        return recomendacion_juego(game_id, game_features_reduced, df_ui, top_n)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def recomendacion_juego(game_id, game_features_reduced, df_ui, top_n=5):
    game_vector = game_features_reduced[game_id:game_id+1]
    cosine_similarities = cosine_similarity(game_vector, game_features_reduced)
    similar_games_indices = cosine_similarities.argsort()[0][-top_n-1:-1][::-1]
    similar_games_indices = [i for i in similar_games_indices if i != game_id]
    recommended_games = df_ui.loc[similar_games_indices, 'item_name']
    return recommended_games[:top_n].tolist()

# Funciones
@app.get("/developer/{desarrollador}")
async def get_developer_analysis(desarrollador: str):
    try:
        df_sg = cargar_dataframe('df_sg')
        resultado = developer(desarrollador, df_sg)
        gc.collect()  # Limpieza de memoria después de cada ejecución pesada
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def developer(desarrollador, df_sg):
    # Filtrar el DataFrame para incluir solo los juegos del desarrollador especificado
    df_dev = df_sg[df_sg['developer'].str.contains(desarrollador, case=False, na=False)]

    # Agrupar por año de lanzamiento
    grouped = df_dev.groupby('release_year').agg(
        Cantidad_de_Items=('id', 'count'),  # Contar la cantidad de juegos por año
        Contenido_Free=('price', lambda x: (x == 0).sum())  # Contar juegos gratuitos
    )

    # Calcular el porcentaje de contenido gratuito
    grouped['Porcentaje_Contenido_Free'] = (grouped['Contenido_Free'] / grouped['Cantidad_de_Items']) * 100

    # Formatear el DataFrame para la presentación de resultados
    grouped = grouped.reset_index()
    grouped = grouped.rename(columns={'release_year': 'Año'})
    grouped['Porcentaje_Contenido_Free'] = grouped['Porcentaje_Contenido_Free'].apply(lambda x: f'{x:.2f}%')

    # Optimización de tipos de datos para reducir el uso de memoria
    grouped['Año'] = grouped['Año'].astype('category')
    grouped['Porcentaje_Contenido_Free'] = grouped['Porcentaje_Contenido_Free'].astype('string')

    return grouped[['Año', 'Cantidad_de_Items', 'Porcentaje_Contenido_Free']].to_dict(orient='records')

@app.get("/userdata/{user_id}")
async def get_userdata(user_id: str):
    try:
        # Cargar los DataFrames necesarios 
        df_ui = cargar_dataframe('df_ui')
        df_sg = cargar_dataframe('df_sg')
        df_ur = cargar_dataframe('df_ur')
        
        resultado = userdata(user_id, df_ui, df_sg, df_ur)
        gc.collect()  # Sugerir la liberación de memoria no utilizada
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def userdata(user_id, df_ui, df_sg, df_ur):
    # Filtrar df_ui para el usuario especificado
    user_items = df_ui[df_ui['user_id'] == user_id]
    
    # Optimizar el uso de memoria convirtiendo los IDs a categorías 
    if user_items['item_id'].dtype != 'category':
        user_items['item_id'] = user_items['item_id'].astype('category')
    
    # Obtener los precios de los juegos que el usuario posee, utilizando df_sg
    precios_juegos = df_sg[df_sg['id'].isin(user_items['item_id'])]

    # Calcular el total de dinero gastado
    total_gastado = precios_juegos['price'].sum()

    # Calcular el porcentaje de recomendación
    user_reviews = df_ur[df_ur['user_id'] == user_id]
    if len(user_reviews) > 0:
        porcentaje_recomendacion = (user_reviews['recommend'].sum() / len(user_reviews)) * 100
    else:
        porcentaje_recomendacion = 0

    # Calcular la cantidad total de items
    cantidad_items = user_items['item_id'].nunique()

    # Preparar y retornar el resultado
    resultado = {
        "Usuario": user_id,
        "Dinero gastado": f"{total_gastado:.2f} USD",
        "% de recomendación": f"{porcentaje_recomendacion:.2f}%",
        "cantidad de items": cantidad_items
    }

    return resultado


@app.get("/user-for-genre/{genero}")
async def get_user_for_genre(genero: str):
    try:
        df_sg = cargar_dataframe('df_sg')
        df_ui = cargar_dataframe('df_ui')
        
        resultado = UserForGenre(genero, df_ui, df_sg)
        gc.collect()  # Sugerir la liberación de memoria no utilizada
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def UserForGenre(genero, df_ui, df_sg):
    # Filtrar df_sg para juegos del género especificado
    juegos_genero = df_sg[df_sg['genres'].str.contains(genero, case=False, na=False)]

    # Unir df_ui con juegos_genero para obtener las horas jugadas en ese género por usuario
    horas_por_usuario = pd.merge(df_ui, juegos_genero, left_on='item_id', right_on='id')

    # Agrupar por usuario y sumar las horas jugadas totales
    total_horas_usuario = horas_por_usuario.groupby('user_id')['playtime_forever'].sum()

    # Encontrar el usuario con más horas jugadas
    usuario_max_horas = total_horas_usuario.idxmax()

    # Agrupar por año de lanzamiento y sumar las horas jugadas
    horas_por_año = horas_por_usuario.groupby('release_year')['playtime_forever'].sum().reset_index()
    horas_por_año = horas_por_año.rename(columns={'playtime_forever': 'Horas', 'release_year': 'Año'})

    # Convertir las horas acumuladas por año en una lista de diccionarios
    horas_lista = horas_por_año.to_dict('records')

    # Preparar y retornar el resultado
    resultado = {
        "Usuario con más horas jugadas para Género " + genero: usuario_max_horas,
        "Horas jugadas": horas_lista
    }

    return resultado


@app.get("/best-developer/{anio}")
async def get_best_developer_year(anio: int):
    try:
        df_ur = cargar_dataframe('df_ur')
        df_sg = cargar_dataframe('df_sg')
        
        resultado = best_developer_year(anio, df_ur, df_sg)
        gc.collect()  # Sugerir la liberación de memoria no utilizada
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def best_developer_year(anio, df_ur, df_sg):
    # Filtrar df_ur para obtener solo las recomendaciones del año dado
    recomendaciones_anio = df_ur[(df_ur['posted_year'] == anio) & (df_ur['recommend'])]

    # Unir df_ur filtrado con df_sg para obtener información del desarrollador
    recomendaciones_desarrollador = pd.merge(recomendaciones_anio, df_sg, left_on='item_id', right_on='id')

    # Contar las recomendaciones por desarrollador
    conteo_recomendaciones = recomendaciones_desarrollador.groupby('developer')['user_id'].count().sort_values(ascending=False)

    # Obtener el top 3 de desarrolladores
    top_3_desarrolladores = conteo_recomendaciones.head(3).index.tolist()

    # Preparar y retornar el resultado 
    resultado = [{"Puesto " + str(i+1): dev} for i, dev in enumerate(top_3_desarrolladores)]

    return resultado



@app.get("/developer-reviews-analysis/{desarrolladora}")
async def get_developer_reviews_analysis(desarrolladora: str):
    try:
        df_ur = cargar_dataframe('df_ur')
        df_sg = cargar_dataframe('df_sg')
        
        resultado = developer_reviews_analysis(desarrolladora, df_ur, df_sg)
        gc.collect()  # Sugerir la liberación de memoria no utilizada
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def developer_reviews_analysis(desarrolladora, df_ur, df_sg):
    try:
        # Filtrar df_sg primero para reducir la cantidad de datos a unir
        df_sg_desarrollador = df_sg[df_sg['developer'].str.contains(desarrolladora, case=False, na=False)]
        reseñas_desarrollador = pd.merge(df_ur, df_sg_desarrollador, left_on='item_id', right_on='id')

        conteo_positivas = int((reseñas_desarrollador['sentiment_analysis'] == 2).sum())
        conteo_negativas = int((reseñas_desarrollador['sentiment_analysis'] == 0).sum())

        resultado = {
            desarrolladora: {
                'Negative': conteo_negativas,
                'Positive': conteo_positivas
            }
        }
        return resultado
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))