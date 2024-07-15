# Processing the Raw Data

## Objective

The dataset consists of multiple CSV files of Accelerometer and Gyroscope data of **_time(epoch (ms), time (01:00))_** with respect to movement the **_x-axis, y-axis, z-axis_** for a **_specific test subject_**, **_specific exercise_**, and **_specific set_**. The target is to clear the data and save it.

> If you want the dataset to follow along [Click Here](../data/raw/MetaMotion.zip) and download the **_zip_** file and save it in [`data/raw/MetaMotion`](../data/raw/MetaMotion/) folder.

## Process

#### Step 01:

Extracting the information from the file names and adding them to the data frame. We will first test on one file and then when the process is working correctly we will run a loop over all the files and convert them.

```py
# Read single CSV files for accelerometer and gyroscope data
single_file_acc_name =
"../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Accelerometer_12.500Hz_1.4.4.csv"
single_file_gyr_name =
"../../data/raw/MetaMotion/A-bench-heavy_MetaWear_2019-01-14T14.22.49.165_C42732BE255C_Gyroscope_25.000Hz_1.4.4.csv"
# Load the single accelerometer and gyroscope data files into DataFrames
single_file_acc = pd.read_csv(single_file_acc_name)
single_file_gyr = pd.read_csv(single_file_gyr_name)
```

```py
single_file_acc.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>epoch (ms)</th>
      <th>time (01:00)</th>
      <th>elapsed (s)</th>
      <th>x-axis (g)</th>
      <th>y-axis (g)</th>
      <th>z-axis (g)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1547472169751</td>
      <td>2019-01-14T14:22:49.751</td>
      <td>0.00</td>
      <td>-0.147</td>
      <td>0.702</td>
      <td>-0.276</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1547472169831</td>
      <td>2019-01-14T14:22:49.831</td>
      <td>0.08</td>
      <td>-0.120</td>
      <td>0.710</td>
      <td>-0.360</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1547472169911</td>
      <td>2019-01-14T14:22:49.911</td>
      <td>0.16</td>
      <td>-0.160</td>
      <td>0.768</td>
      <td>-0.392</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1547472169991</td>
      <td>2019-01-14T14:22:49.991</td>
      <td>0.24</td>
      <td>-0.208</td>
      <td>0.817</td>
      <td>-0.379</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1547472170071</td>
      <td>2019-01-14T14:22:50.071</td>
      <td>0.32</td>
      <td>-0.223</td>
      <td>0.839</td>
      <td>-0.403</td>
    </tr>
  </tbody>
</table>
</div>

```py
single_file_gyr.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>epoch (ms)</th>
      <th>time (01:00)</th>
      <th>elapsed (s)</th>
      <th>x-axis (deg/s)</th>
      <th>y-axis (deg/s)</th>
      <th>z-axis (deg/s)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1547472169353</td>
      <td>2019-01-14T14:22:49.353</td>
      <td>0.00</td>
      <td>-2.866</td>
      <td>-0.610</td>
      <td>-5.366</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1547472169393</td>
      <td>2019-01-14T14:22:49.393</td>
      <td>0.04</td>
      <td>-2.500</td>
      <td>-0.610</td>
      <td>-3.963</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1547472169433</td>
      <td>2019-01-14T14:22:49.433</td>
      <td>0.08</td>
      <td>1.707</td>
      <td>-3.902</td>
      <td>1.524</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1547472169473</td>
      <td>2019-01-14T14:22:49.473</td>
      <td>0.12</td>
      <td>2.439</td>
      <td>-4.939</td>
      <td>-4.207</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1547472169513</td>
      <td>2019-01-14T14:22:49.513</td>
      <td>0.16</td>
      <td>7.500</td>
      <td>-6.037</td>
      <td>1.768</td>
    </tr>
  </tbody>
</table>
</div>

From the title of the file we can extract the name of the **_participant_**, **_the label of the exercise_** and the **_category of the exercise_**.

```py
# Extract participant, label, and category from the filename
participant = f.split("-")[0].replace(data_file, "")
label = f.split("-")[1]
category = f.split("-")[2].rstrip("123").rstrip("MetaWear_2019")
```

```py
# Load the first file into a DataFrame
df = pd.read_csv(f)
# Add participant, label, and category columns to the DataFrame
df["participant"] = participant
df["label"] = label
df["category"] = category
```

```py
df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>epoch (ms)</th>
      <th>time (01:00)</th>
      <th>elapsed (s)</th>
      <th>x-axis (deg/s)</th>
      <th>y-axis (deg/s)</th>
      <th>z-axis (deg/s)</th>
      <th>participant</th>
      <th>label</th>
      <th>category</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1547579048841</td>
      <td>2019-01-15T20:04:08.841</td>
      <td>0.00</td>
      <td>1.707</td>
      <td>-2.866</td>
      <td>0.671</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1547579048881</td>
      <td>2019-01-15T20:04:08.881</td>
      <td>0.04</td>
      <td>-0.671</td>
      <td>-2.012</td>
      <td>1.829</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1547579048921</td>
      <td>2019-01-15T20:04:08.921</td>
      <td>0.08</td>
      <td>-9.146</td>
      <td>1.280</td>
      <td>5.061</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1547579048961</td>
      <td>2019-01-15T20:04:08.961</td>
      <td>0.12</td>
      <td>-7.500</td>
      <td>0.427</td>
      <td>2.439</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1547579049001</td>
      <td>2019-01-15T20:04:09.001</td>
      <td>0.16</td>
      <td>1.890</td>
      <td>-2.683</td>
      <td>-2.256</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
    </tr>
  </tbody>
</table>
</div>

After checking that this process can isolate the information we can save it into a data frame.

Now we will do it for all the data of Accelerometer and Gyroscope separately and assign a set to them.

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

```py
acc_df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>epoch (ms)</th>
      <th>time (01:00)</th>
      <th>elapsed (s)</th>
      <th>x-axis (g)</th>
      <th>y-axis (g)</th>
      <th>z-axis (g)</th>
      <th>participant</th>
      <th>label</th>
      <th>category</th>
      <th>set</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1547666786798</td>
      <td>2019-01-16 20:26:26.798</td>
      <td>0.00</td>
      <td>0.067</td>
      <td>-1.000</td>
      <td>-0.108</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1547666786878</td>
      <td>2019-01-16 20:26:26.878</td>
      <td>0.08</td>
      <td>0.072</td>
      <td>-0.998</td>
      <td>-0.210</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1547666786958</td>
      <td>2019-01-16 20:26:26.958</td>
      <td>0.16</td>
      <td>0.113</td>
      <td>-1.034</td>
      <td>-0.213</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1547666787038</td>
      <td>2019-01-16 20:26:27.038</td>
      <td>0.24</td>
      <td>0.094</td>
      <td>-1.012</td>
      <td>-0.180</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1547666787118</td>
      <td>2019-01-16 20:26:27.118</td>
      <td>0.32</td>
      <td>0.071</td>
      <td>-1.031</td>
      <td>-0.209</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

```py
gyr_df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>epoch (ms)</th>
      <th>time (01:00)</th>
      <th>elapsed (s)</th>
      <th>x-axis (deg/s)</th>
      <th>y-axis (deg/s)</th>
      <th>z-axis (deg/s)</th>
      <th>participant</th>
      <th>label</th>
      <th>category</th>
      <th>set</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1547579048841</td>
      <td>2019-01-15T20:04:08.841</td>
      <td>0.00</td>
      <td>1.707</td>
      <td>-2.866</td>
      <td>0.671</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1547579048881</td>
      <td>2019-01-15T20:04:08.881</td>
      <td>0.04</td>
      <td>-0.671</td>
      <td>-2.012</td>
      <td>1.829</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1547579048921</td>
      <td>2019-01-15T20:04:08.921</td>
      <td>0.08</td>
      <td>-9.146</td>
      <td>1.280</td>
      <td>5.061</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1547579048961</td>
      <td>2019-01-15T20:04:08.961</td>
      <td>0.12</td>
      <td>-7.500</td>
      <td>0.427</td>
      <td>2.439</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1547579049001</td>
      <td>2019-01-15T20:04:09.001</td>
      <td>0.16</td>
      <td>1.890</td>
      <td>-2.683</td>
      <td>-2.256</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

#### Step 02:

Handling the time for the dataset and the time interval. We are provided with time in Epochs UTC time and CET winter time, this can cause some disturbance and ineqalitizes for out dataset. So it is a good practice to convert it into a standard using Epoch (computing) timezone.

> **In computing, an epoch is a fixed date and time used as a reference from which a computer measures system time. Most computer systems determine time as a number representing the seconds removed from a particular arbitrary date and time. For instance, Unix and POSIX measure time as the number of seconds that have passed since Thursday 1 January 1970 00:00:00 UT, a point in time known as the Unix epoch. Windows NT systems, up to and including Windows 11 and Windows Server 2022, measure time as the number of 100-nanosecond intervals that have passed since 1 January 1601 00:00:00 UTC, making that point in time the epoch for those systems. Computing epochs are almost always specified as midnight Universal Time on some particular date.**

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

```py
acc_df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x-axis (g)</th>
      <th>y-axis (g)</th>
      <th>z-axis (g)</th>
      <th>participant</th>
      <th>label</th>
      <th>category</th>
      <th>set</th>
    </tr>
    <tr>
      <th>epoch (ms)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-16 19:26:26.798</th>
      <td>0.067</td>
      <td>-1.000</td>
      <td>-0.108</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-16 19:26:26.878</th>
      <td>0.072</td>
      <td>-0.998</td>
      <td>-0.210</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-16 19:26:26.958</th>
      <td>0.113</td>
      <td>-1.034</td>
      <td>-0.213</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-16 19:26:27.038</th>
      <td>0.094</td>
      <td>-1.012</td>
      <td>-0.180</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-16 19:26:27.118</th>
      <td>0.071</td>
      <td>-1.031</td>
      <td>-0.209</td>
      <td>E</td>
      <td>dead</td>
      <td>medium</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

```py
gyr_df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x-axis (deg/s)</th>
      <th>y-axis (deg/s)</th>
      <th>z-axis (deg/s)</th>
      <th>participant</th>
      <th>label</th>
      <th>category</th>
      <th>set</th>
    </tr>
    <tr>
      <th>epoch (ms)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-15 19:04:08.841</th>
      <td>1.707</td>
      <td>-2.866</td>
      <td>0.671</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-15 19:04:08.881</th>
      <td>-0.671</td>
      <td>-2.012</td>
      <td>1.829</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-15 19:04:08.921</th>
      <td>-9.146</td>
      <td>1.280</td>
      <td>5.061</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-15 19:04:08.961</th>
      <td>-7.500</td>
      <td>0.427</td>
      <td>2.439</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
    <tr>
      <th>2019-01-15 19:04:09.001</th>
      <td>1.890</td>
      <td>-2.683</td>
      <td>-2.256</td>
      <td>A</td>
      <td>squat</td>
      <td>heavy</td>
      <td>1</td>
    </tr>
  </tbody>
</table>
</div>

#### Step 03:

Converting the above steps in to a function and running it for all the files of the raw data. This will help us incase of reusablity and also simplify the process.

```py
def reading_data_from_files(files):

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

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acc_x</th>
      <th>acc_y</th>
      <th>acc_z</th>
      <th>gyr_x</th>
      <th>gyr_y</th>
      <th>gyr_z</th>
      <th>participant</th>
      <th>label</th>
      <th>category</th>
      <th>set</th>
    </tr>
    <tr>
      <th>epoch (ms)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-11 15:08:04.950</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-10.671</td>
      <td>-1.524</td>
      <td>5.976</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72.0</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:04.990</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-8.720</td>
      <td>-2.073</td>
      <td>3.171</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72.0</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:05.030</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.488</td>
      <td>-3.537</td>
      <td>-4.146</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72.0</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:05.070</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.244</td>
      <td>-5.854</td>
      <td>3.537</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72.0</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:05.110</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>-0.915</td>
      <td>0.061</td>
      <td>-2.805</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72.0</td>
    </tr>
  </tbody>
</table>
</div>

_The missng values in both the Accelerometer and Gyroscope is due to reading of different frequency of their readings._

> **What is Resampling?**

> **In particular, a set of sufficient conditions is that the rate of convergence of the estimator is known and that the limiting distribution is continuous. In addition, the resample (or subsample) size must tend to infinity together with the sample size but at a smaller rate, so that their ratio converges to zero. While subsampling was originally proposed for the case of independent and identically distributed (iid) data only, the methodology has been extended to cover time series data as well; in this case, one resamples blocks of subsequent data rather than individual data points.**

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

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }

</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>acc_x</th>
      <th>acc_y</th>
      <th>acc_z</th>
      <th>gyr_x</th>
      <th>gyr_y</th>
      <th>gyr_z</th>
      <th>participant</th>
      <th>label</th>
      <th>category</th>
      <th>set</th>
    </tr>
    <tr>
      <th>epoch (ms)</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2019-01-11 15:08:05.200</th>
      <td>0.013500</td>
      <td>0.977000</td>
      <td>-0.071000</td>
      <td>-1.8904</td>
      <td>2.4392</td>
      <td>0.9388</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:05.400</th>
      <td>-0.001500</td>
      <td>0.970500</td>
      <td>-0.079500</td>
      <td>-1.6826</td>
      <td>-0.8904</td>
      <td>2.1708</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:05.600</th>
      <td>0.001333</td>
      <td>0.971667</td>
      <td>-0.064333</td>
      <td>2.5608</td>
      <td>-0.2560</td>
      <td>-1.4146</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:05.800</th>
      <td>-0.024000</td>
      <td>0.957000</td>
      <td>-0.073500</td>
      <td>8.0610</td>
      <td>-4.5244</td>
      <td>-2.0730</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72</td>
    </tr>
    <tr>
      <th>2019-01-11 15:08:06.000</th>
      <td>-0.028000</td>
      <td>0.957667</td>
      <td>-0.115000</td>
      <td>2.4390</td>
      <td>-1.5486</td>
      <td>-3.6098</td>
      <td>B</td>
      <td>bench</td>
      <td>heavy</td>
      <td>72</td>
    </tr>
  </tbody>
</table>
</div>

#### Step 05:

Save the processed data in a pickle file.

> **What is a Pickle file?**

> **A PKL file is a file created by pickle, a Python module that enabless objects to be serialized to files on disk and deserialized back into the program at runtime. It contains a byte stream that represents the objects.**

Source: [https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_pickle](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_pickle.html)

```py
# Export the processed dataset
export_folder_path = "../../data/processed/01_data_processed.pkl"
data_resampling.to_pickle(export_folder_path)
```

## Conclusion

Do refer the code on [`dataprocessing.py`](../src/data/data_processing.py) file for the code and inline documentation of the code. After this process you should have a pickle file which contains the above table. It will help us in the next process of [Data Visualization](./02%20Data%20Visualization%20with%20Matplotlib.md).
