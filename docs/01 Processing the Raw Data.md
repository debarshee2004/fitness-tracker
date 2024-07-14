# Processing the Raw Data

## Objective

The dataset consists of multiple CSV files of Accelerometer and Gyroscope data of **_time(epoch (ms), time (01:00))_** with respect to movement the **_x-axis, y-axis, z-axis_** for a **_specific test subject_**, **_specific exercise_**, and **_specific set_**. The target is to clear the data and save it.

## Process

#### Step 01:

Extracting the information from the file names and adding them to the data frame. We will first test on one file and then when the process is working correctly we will run a loop over all the files and convert them.

```py
# Read single CSV files for accelerometer and gyroscope data
single_file_acc_name =
"../../data/raw/MetaMotion/A-bench-heavy_MetaWear_
2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
single_file_gyr_name =
"../../data/raw/MetaMotion/A-bench-heavy_MetaWear_
2019-01-14T14.22.49.165_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"

# Load the single accelerometer and gyroscope data files into DataFrames
single_file_acc = pd.read_csv(single_file_acc_name)
single_file_gyr = pd.read_csv(single_file_gyr_name)
```

From the title of the file we can extract the name of the participant, the label of the exercise and the category of the exercise

```py
# Extract participant, label, and category from the filename
participant = f.split("-")[0].replace(data_file, "")
label = f.split("-")[1]
category = f.split("-")[2].rstrip("123").rstrip("MetaWear_2019")
```

After checking that this process can isolate the information we can save it into a data frame.

```py
# Load the first file into a DataFrame
df = pd.read_csv(f)

# Add participant, label, and category columns to the DataFrame
df["participant"] = participant
df["label"] = label
df["category"] = category
```

Now we will do it for all the data of Accelerometer and Gyroscope separately.

```py
# List all CSV files in the specified directory
files = glob("../../data/raw/MetaMotion/*.csv")
file_numbers = len(files)
```

```py
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
```

#### Step 02:

Handling the time for the dataset and the time interval. We are provided with time in Epochs UTC time and CET winter time, this can cause some disturbance and ineqalitizes for out dataset. So it is a good practice to convert it into a standard using Epoch (computing) timezone.

**_In computing, an epoch is a fixed date and time used as a reference from which a computer measures system time. Most computer systems determine time as a number representing the seconds removed from a particular arbitrary date and time. For instance, Unix and POSIX measure time as the number of seconds that have passed since Thursday 1 January 1970 00:00:00 UT, a point in time known as the Unix epoch. Windows NT systems, up to and including Windows 11 and Windows Server 2022, measure time as the number of 100-nanosecond intervals that have passed since 1 January 1601 00:00:00 UTC, making that point in time the epoch for those systems. Computing epochs are almost always specified as midnight Universal Time on some particular date._**

Source: [https://en.wikipedia.org/wiki/Epoch\_(computing)](<https://en.wikipedia.org/wiki/Epoch_(computing)>)

We will first convert the Epoch to UTC timezone and then save it to the index. Then droping the columns which we do not need.

```py
# Set the index of acc_df to datetime based on the "epoch (ms)" column
acc_df.index = pd.to_datetime(acc_df["epoch (ms)"], unit="ms")
# Set the index of gyr_df to datetime based on the "epoch (ms)" column
gyr_df.index = pd.to_datetime(gyr_df["epoch (ms)"], unit="ms")
```

```py
# Remove unnecessary columns from acc_df
del acc_df["epoch (ms)"]
del acc_df["time (01:00)"]
del acc_df["elapsed (s)"]

# Remove unnecessary columns from gyr_df
del gyr_df["epoch (ms)"]
del gyr_df["time (01:00)"]
del gyr_df["elapsed (s)"]
```

#### Step 03:

Converting the above steps in to a function and running it for all the files of the raw data. This will help us incase of reusablity and also simplify the process.

```py
def reading_data_from_files(files):
    """
    Reads accelerometer and gyroscope data from a list of CSV files and processes them
    into two separate DataFrames.

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
        The filename is expected to have a specific format to correctly extract
        participant ID, label, and category.
        The function assumes the presence of 'Accelerometer' or 'Gyroscope' in the
        filenames to classify the data.
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
```

#### Step 04:

Now that we have extracted the features and updated the time index of the Accelerometer and Gyroscope dataframe, it's time to merge the two into one dataframe. Here we experience a problem, the frequency at which the data is taken is different in the case of Accelerometer and Gyroscope.

**Accelerometer: 12.500Hz** <br>
**Gyroscope: 25.000Hz**

To tackle the issue we have to resample the data at a specific frequency.

```py
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
```

**What is Resampling?**

**In particular, a set of sufficient conditions is that the rate of convergence of the estimator is known and that the limiting distribution is continuous. In addition, the resample (or subsample) size must tend to infinity together with the sample size but at a smaller rate, so that their ratio converges to zero. While subsampling was originally proposed for the case of independent and identically distributed (iid) data only, the methodology has been extended to cover time series data as well; in this case, one resamples blocks of subsequent data rather than individual data points.**

Source: [https://en.wikipedia.org/wiki/Resampling\_(statistics)](<https://en.wikipedia.org/wiki/Resampling_(statistics)>)

```py
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
```

```py
# Group data by each day
days = [g for n, g in data_merged.groupby(pd.Grouper(freq="D"))]
# Resample each day's data using the defined rules, drop rows with NaN values,
# and concatenate all resampled data
data_resampling = pd.concat(
    [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
)
```

#### Step 05:

Save the processed data in a pickle file.

**What is a Pickle file?**

**A PKL file is a file created by pickle, a Python module that enabless objects to be serialized to files on disk and deserialized back into the program at runtime. It contains a byte stream that represents the objects.**

Source: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_pickle.html](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_pickle.html)

```py
# Export the processed dataset
export_folder_path = "../../data/processed/01_data_processed.pkl"
data_resampling.to_pickle(export_folder_path)
```
