from glob import glob
from data import DataProcessing as dpf
from visualization import DataVisualization as dvf

# FIXME: The function are working indivisualy but are not working while called from the main function.
def main() -> None:
    files_name = "../../data/raw/MetaMotion/*.csv"
    df_file = "../../data/processed/01_data_processed.pkl"
    dpf.data_processing(files_name, df_file)
    dvf.data_visualization(df_file)
    
if __name__ == "__main__":
    main()