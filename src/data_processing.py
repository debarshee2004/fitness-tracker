import pandas as pd
from glob import glob

# Read single CSV files for accelerometer and gyroscope data
single_file_acc_name = "../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
single_file_gyr_name = "../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"

# Load the single accelerometer and gyroscope data files into DataFrames
single_file_acc = pd.read_csv(single_file_acc_name)
single_file_gyr = pd.read_csv(single_file_gyr_name)

# List all CSV files in the specified directory
files = glob("../data/raw/MetaMotion/*.csv")
file_numbers = len(files)

# Extract features from the filename of the first file
data_file = "../data/raw/MetaMotion/"
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
    
    # Extract participant, label, and category from the filename
    participant = f.split("-")[0].replace(data_file, "")
    label = f.split("-")[1]
    category = f.split("-")[2].rstrip("123").rstrip("MetaWear_2019")
    
    # Load the current file into a DataFrame
    df = pd.read_csv(f)

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


# Working with datetimes


# Turn into function


# Merging datasets


# Resample data (frequency conversion)

# Accelerometer:    12.500HZ
# Gyroscope:        25.000Hz


# Export dataset