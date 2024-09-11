import pandas as pd, numpy as np, os
from numpy import dot
from numpy.linalg import norm
from fastembed import TextEmbedding

model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

def cosine_similarity(a, b):
    try:
        result = dot(a, b) / (norm(a) * norm(b))
        if np.isnan(result) or np.isinf(result):
            return 0.0  # Return 0 similarity if the result is NaN or inf
        return result
    except Exception as e:
        print(e)
        return 0.0  # Return 0 similarity in case of an exception

    
def get_embeddings(query:str):
    try:
        return list(model.embed(['hello']))[0]
    
    except Exception as e:
        print(e)
        return np.nan

df = pd.read_parquet("Diet_recommendation_vectorized_only_str_and_embeddings.parquet")

def recommend(query:str, data_path:str = "Diet_recommendation_vectorized_only_str_and_embeddings.parquet", threshold:float = 0.7, n: int=5):
    try:
        print(query)
        df = pd.read_parquet(data_path).copy()

        query_embed = list(model.embed([query]))[0]

        df['cos_sim'] = df['embedding_fast'].apply(lambda x: cosine_similarity(x, query_embed))

        # Filter out any NaN or inf values from the 'cos_sim' column
        df = df[np.isfinite(df['cos_sim'])]

        if df['cos_sim'].max() >= threshold:
            df_temp = df.drop('embedding_fast', axis=1).sort_values(by='cos_sim', ascending=False, kind='mergesort').head(n).reset_index().drop('index', axis=1)

            z = {}
            for i in range(len(df_temp)):
                z[df_temp['full_str'][i]] = np.float64(df_temp['cos_sim'][i])

            print(z)
            
            return z
        else:
            return 'No significant matches'
        
    except Exception as e:
        print(e)
        return 'An error occurred'

