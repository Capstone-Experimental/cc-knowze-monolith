from google.cloud import storage
import csv
from io import BytesIO, TextIOWrapper
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from joblib import load, dump
from sklearn.feature_extraction.text import TfidfVectorizer
from util.credentials import credentials

def load_csv_from_gcs(bucket_name, file_path):
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)

    with blob.open("r") as file:
        df = pd.read_csv(file)
    return df

def load_model_from_gcs(bucket_name, model_file_path):
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.get_bucket(bucket_name)
    blob_model = bucket.blob(model_file_path)

    local_model_path = 'model/recom-v1.pkl'
    blob_model.download_to_filename(local_model_path)

    cosine_sim_loaded = load(local_model_path)
    return cosine_sim_loaded

def retrain_model_and_upload(bucket_name, csv_file_path, model_file_path):
    df = load_csv_from_gcs(bucket_name, csv_file_path)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['shortdesc'])
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    local_model_path = 'model/recom-v1.pkl'
    dump(cosine_sim, local_model_path)

    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket(bucket_name)
    blob_model = bucket.blob(model_file_path)
    blob_model.upload_from_filename(local_model_path)

    return cosine_sim

def append_data_to_csv_in_gcs(bucket_name, file_path, prompt, type_activity, theme_activity, desc):
    storage_client = storage.Client(credentials=credentials)

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(file_path)

    with blob.open("r") as file:
        lines = file.readlines()
        lines.append(f'{prompt},{theme_activity},{type_activity},{desc}\n')

    with blob.open("w") as file:
        file.writelines(lines)

def get_recommendations(prompt):
    df = load_csv_from_gcs('go-mono', 'csv/data_recom.csv')
    cosine_sim = load_model_from_gcs('go-mono', 'model/recom-v1.pkl')

    indices = pd.Series(df.index, index=df['prompt']).drop_duplicates()

    idx = indices[prompt]

    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:6]

    course_indices = [i[0] for i in sim_scores]

    return df['prompt'].iloc[course_indices]
