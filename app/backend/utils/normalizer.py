import pandas as pd
import sys, os

# --- Permitir importar Codigos.Procesamiento ----
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from Code.Procesamiento import preprocess_text

def normalize_text_df(df):
    df_out = pd.DataFrame()
    df_out["normalized_title"] = (
        df["title"] if "title" in df else ["poema_prueba"] * len(df)
    )
    df_out["normalized_content"] = df["content"].apply(preprocess_text)
    return df_out
