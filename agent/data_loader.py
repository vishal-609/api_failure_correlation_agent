import pandas as pd

def load_data(file_path):
    # Reads the CSV file and converts it into a pandas DataFrame (a 2D table of data)
    df = pd.read_csv(file_path)
    
    # Returns the loaded data so other parts of the script can use it
    return df