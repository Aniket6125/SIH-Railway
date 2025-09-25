# utils/data_loader.py
import pandas as pd
import os

def load_csv(uploaded_file=None, default_path=None):
    """
    Load timetable CSV. If no uploaded file, load default CSV.
    """
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    elif default_path and os.path.exists(default_path):
        df = pd.read_csv(default_path)
    else:
        raise FileNotFoundError("No timetable CSV found.")

    return df


def save_to_csv(df, path):
    """
    Save dataframe to CSV.
    """
    df.to_csv(path, index=False)
    return path
