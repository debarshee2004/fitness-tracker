import pandas as pd
from glob import glob

files = glob("../../data/raw/MetaMotion/*.csv")


def data_processing(files) -> None:
    """
    Processes accelerometer and gyroscope data from a list of CSV files, merges them,
    resamples the merged data, and exports the processed data to a pickle file.

    The function performs the following steps:
    1. Reads accelerometer and gyroscope data from the provided files using the `reading_data_from_files` function.
    2. Merges the accelerometer and gyroscope data into a single DataFrame.
    3. Resamples the merged data at 200ms intervals, applying a custom sampling function and dropping any resulting NaN values.
    4. Exports the processed and resampled data to a pickle file.

    Parameters:
    files (list of str): List of file paths to CSV files containing the data.

    Returns:
    None

    The exported DataFrame includes the following columns:
    - acc_x: Accelerometer X-axis data
    - acc_y: Accelerometer Y-axis data
    - acc_z: Accelerometer Z-axis data
    - gyr_x: Gyroscope X-axis data
    - gyr_y: Gyroscope Y-axis data
    - gyr_z: Gyroscope Z-axis data
    - participant: Identifier of the participant
    - label: Label associated with the data
    - category: Category of the data
    - set: Set number indicating the order of the files processed

    The exported DataFrame is saved to the path: "../data/processed/01_data_processed.pkl"
    """

    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

    data_file = "../../data/raw/MetaMotion/"

    for f in files:

        df = pd.read_csv(f)

        participant = f.split("-")[0].replace(data_file, "")
        label = f.split("-")[1]
        category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

        df["participant"] = participant
        df["label"] = label
        df["category"] = category

        if "Accelerometer" in f:
            df["set"] = acc_set
            acc_set += 1
            acc_df = pd.concat([acc_df, df])

        if "Gyroscope" in f:
            df["set"] = gyr_set
            gyr_set += 1
            gyr_df = pd.concat([gyr_df, df])

    key = "epoch (ms)"
    acc_df.index = pd.to_datetime(acc_df[key], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df[key], unit="ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]

    data_merged = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)
    data_merged.columns = [
        "acc_x",
        "acc_y",
        "acc_z",
        "gyr_x",
        "gyr_y",
        "gyr_z",
        "participant",
        "label",
        "category",
        "set",
    ]

    sampling = {
        "acc_x": "mean",
        "acc_y": "mean",
        "acc_z": "mean",
        "gyr_x": "mean",
        "gyr_y": "mean",
        "gyr_z": "mean",
        "participant": "last",
        "label": "last",
        "category": "last",
        "set": "last",
    }

    days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]
    data_resampling = pd.concat(
        [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
    )
    data_resampling["set"] = data_resampling["set"].astype("int")

    export_folder_path = "../../data/processed/01_data_processed.pkl"
    data_resampling.to_pickle(export_folder_path)


if __name__ == "__main__":
    data_processing(files)
