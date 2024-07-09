import pandas as pd
from glob import glob

# Read single CSV files for accelerometer and gyroscope data
single_file_acc_name = "../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
single_file_gyr_name = "../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"

# Load the single accelerometer and gyroscope data files into DataFrames
single_file_acc = pd.read_csv(single_file_acc_name)
single_file_gyr = pd.read_csv(single_file_gyr_name)

# List all CSV files in the specified directory
files = glob("../../data/raw/MetaMotion/*.csv")
file_numbers = len(files)

# Extract features from the filename of the first file
data_file = "../../data/raw/MetaMotion/"
f = files[0]

# Extract participant, label, and category from the filename
participant = f.split("-")[0].replace(data_file, "")
label = f.split("-")[1]
category = f.split("-")[2].rstrip("123").rstrip("MetaWear_2019")

# Load the first file into a DataFrame
df = pd.read_csv(f)

# Add participant, label, and category columns to the DataFrame
df["participant"] = participant
df["label"] = label
df["category"] = category

# Initialize empty DataFrames for accelerometer and gyroscope data
acc_df = pd.DataFrame()
gyr_df = pd.DataFrame()

# Initialize counters for the sets of accelerometer and gyroscope data
acc_set = 1
gyr_set = 1

# Loop through all files and process them
for f in files:

    # Load the current file into a DataFrame
    df = pd.read_csv(f)

    # Extract participant, label, and category from the filename
    participant = f.split("-")[0].replace(data_file, "")
    label = f.split("-")[1]
    category = f.split("-")[2].rstrip("123").rstrip("_MetaWear_2019")

    # Add participant, label, and category columns to the DataFrame
    df["participant"] = participant
    df["label"] = label
    df["category"] = category

    # Check if the file is for accelerometer data
    if "Accelerometer" in f:
        df["set"] = acc_set
        acc_set += 1
        # Concatenate the current DataFrame with the accelerometer DataFrame
        acc_df = pd.concat([acc_df, df])

    # Check if the file is for gyroscope data
    if "Gyroscope" in f:
        df["set"] = gyr_set
        gyr_set += 1
        # Concatenate the current DataFrame with the gyroscope DataFrame
        gyr_df = pd.concat([gyr_df, df])

# acc_df.describe()
# acc_df.info()

# gyr_df.describe()
# gyr_df.info()

# Working with datetimes

# pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
# pd.to_datetime(acc_df["time (01:00)"])
# It is the result of the difference between UTC time and CET winter time.

# Set the index of acc_df to datetime based on the "epoch (ms)" column
acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")

# Set the index of gyr_df to datetime based on the "epoch (ms)" column
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

# Remove unnecessary columns from acc_df
del acc_df["epoch (ms)"]
del acc_df["time (01:00)"]
del acc_df["elapsed (s)"]

# Remove unnecessary columns from gyr_df
del gyr_df["epoch (ms)"]
del gyr_df["time (01:00)"]
del gyr_df["elapsed (s)"]

# Turn into function

files = glob("../../data/raw/MetaMotion/*.csv")
data_file = "../../data/raw/MetaMotion/"


def test_reading_data_from_files(files):
    """
    Reads accelerometer and gyroscope data from a list of CSV files and processes them into two separate DataFrames.

    Args:
        files: (list of str): List of file paths to CSV files containing the data.

    Returns:
        tuple: A tuple containing two DataFrames:
            - acc_df (pd.DataFrame): Processed accelerometer data.
            - gyr_df (pd.DataFrame): Processed gyroscope data.

    The function performs the following steps:
    1. Initializes empty DataFrames for accelerometer (acc_df) and gyroscope (gyr_df) data.
    2. Iterates through each file in the provided list of files.
    3. Reads each file into a DataFrame.
    4. Extracts the participant ID, label, and category from the filename.
    5. Adds the extracted participant ID, label, and category as new columns in the DataFrame.
    6. Determines if the file contains accelerometer or gyroscope data based on the filename.
    7. Adds a 'set' column to distinguish between different sets of accelerometer or gyroscope data.
    8. Concatenates the processed data into the corresponding DataFrame (acc_df or gyr_df).
    9. Converts the 'epoch (ms)' column to a datetime index for both DataFrames.
    10. Removes unnecessary columns ('epoch (ms)', 'time (01:00)', 'elapsed (s)') from both DataFrames.

    Note:
        The filename is expected to have a specific format to correctly extract participant ID, label, and category.
        The function assumes the presence of 'Accelerometer' or 'Gyroscope' in the filenames to classify the data.
    """

    acc_df = pd.DataFrame()
    gyr_df = pd.DataFrame()

    acc_set = 1
    gyr_set = 1

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

    acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
    gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")

    del acc_df["epoch (ms)"]
    del acc_df["time (01:00)"]
    del acc_df["elapsed (s)"]

    del gyr_df["epoch (ms)"]
    del gyr_df["time (01:00)"]
    del gyr_df["elapsed (s)"]

    return acc_df, gyr_df


acc_df, gyr_df = test_reading_data_from_files(files)

# Merging datasets

# Concatenate the first three columns of acc_df with all columns of gyr_df along the columns (axis=1)
data_merged = pd.concat([acc_df.iloc[:, :3], gyr_df], axis=1)

# Rename columns of the merged DataFrame
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

# Resample data (frequency conversion)
# Accelerometer: 12.500Hz
# Gyroscope: 25.000Hz

# Define resampling rules for each column
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

# Apply resampling on a subset of the merged data (first 1000 rows) using a 200ms rule
# data_merged[:1000].resample(rule="200ms").apply(sampling)

# Group data by each day
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]

# Resample each day's data using the defined rules, drop rows with NaN values, and concatenate all resampled data
data_resampling = pd.concat(
    [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
)

# Convert the "set" column to integer type
data_resampling["set"] = data_resampling["set"].astype("int")

# Display info of the resampled data (commented out)
# data_resampling.info()

# Export the processed dataset
export_folder_path = "../../data/processed/01_data_processed.pkl"
data_resampling.to_pickle(export_folder_path)

# A function for the full data_processing process.

files = glob("../../data/raw/MetaMotion/*.csv")
data_file = "../../data/raw/MetaMotion/"


def test_data_processing(files):
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

    acc_df, gyr_df = test_reading_data_from_files(files)

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

    days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]
    data_resampling = pd.concat(
        [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
    )
    data_resampling["set"] = data_resampling["set"].astype("int")

    export_folder_path = "../../data/processed/01_data_processed.pkl"
    data_resampling.to_pickle(export_folder_path)


# Testing the function (This function takes in file path and creates a processed data set).
# test_data_processing(files)
