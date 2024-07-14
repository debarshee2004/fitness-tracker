import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from DataTransformation import LowPassFilter, PrincipalComponentAnalysis
from TemporalAbstraction import NumericalAbstraction
from FrequencyAbstraction import FourierTransformation

# Load data

df_file = "../../data/processed/02_outliers_removed_chauvenets.pkl"
df = pd.read_pickle(df_file)

predictor_columns = list(df.columns[:6])

plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (20, 5)
plt.rcParams["figure.dpi"] = 100
plt.rcParams["lines.linewidth"] = 2

# Dealing with missing values (imputation)

for col in predictor_columns:
    df[col] = df[col].interpolate()

df.info()

# Calculating set duration

duration = df[df["set"] == 1].index[-1] - df[df["set"] == 1].index[0]
duration.seconds

for s in df["set"].unique():
    start = df[df["set"] == s].index[0]
    stop = df[df["set"] == s].index[-1]
    duration = stop - start
    df.loc[(df["set"] == s), "duration"] = duration.seconds

df.groupby(["category"])["duration"].mean()
df.groupby(["category"])["duration"].unique()

# Butterworth lowpass filter

df_lowpass = df.copy()
LowPass = LowPassFilter()

sampling_frequency = 1000 / 200
cutoff_frequency = 1.2

df_lowpass = LowPass.low_pass_filter(
    data_table=df_lowpass,
    col="acc_y",
    sampling_frequency=sampling_frequency,
    cutoff_frequency=cutoff_frequency,
    order=5,
    phase_shift=True,
)

subset = df_lowpass[df_lowpass["set"] == 45]
print(subset["label"][0])

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
ax[0].plot(subset["acc_y"].reset_index(drop=True), label="raw data")
ax[1].plot(subset["acc_y_lowpass"].reset_index(drop=True), label="butterworth filter")
ax[0].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)
ax[1].legend(loc="upper center", bbox_to_anchor=(0.5, 1.15), fancybox=True, shadow=True)

df_lowpass = df.copy()

for col in predictor_columns:
    df_lowpass = LowPass.low_pass_filter(
        data_table=df_lowpass,
        col=col,
        sampling_frequency=sampling_frequency,
        cutoff_frequency=cutoff_frequency,
        order=5,
        phase_shift=True,
    )
    df_lowpass[col] = df_lowpass[col + "_lowpass"]
    del df_lowpass[col + "_lowpass"]

# Principal component analysis PCA

df_pca = df_lowpass.copy()
PCA = PrincipalComponentAnalysis()

pca_values = PCA.determine_pc_explained_variance(
    data_table=df_pca, cols=predictor_columns
)

plt.figure(figsize=(10, 10))
plt.plot(range(1, len(predictor_columns) + 1), pca_values)
plt.xlabel("principal component number")
plt.ylabel("explained variance")
plt.show()

df_pca = PCA.apply_pca(data_table=df_pca, cols=predictor_columns, number_comp=3)

subset = df_pca[df_pca["set"] == 35]
subset[["pca_1", "pca_2", "pca_3"]].plot()

# Sum of squares attributes

df_squared = df_pca.copy()

acc_r = df_squared["acc_x"] ** 2 + df_squared["acc_y"] ** 2 + df_squared["acc_z"] ** 2
gyr_r = df_squared["gyr_x"] ** 2 + df_squared["gyr_y"] ** 2 + df_squared["gyr_z"] ** 2

df_squared["acc_r"] = np.sqrt(acc_r)
df_squared["gyr_r"] = np.sqrt(gyr_r)

subset = df_squared[df_squared["set"] == 14]
subset[["acc_r", "gyr_r"]].plot(subplots=True)

# Temporal abstraction

df_temporal = df_squared.copy()
NumAbs = NumericalAbstraction()

predictor_columns = predictor_columns + ["acc_r", "gyr_r"]
window_size = int(1000 / 200)

for col in predictor_columns:
    df_temporal = NumAbs.abstract_numerical(
        data_table=df_temporal,
        cols=[col],
        window_size=window_size,
        aggregation_function="mean",
    )
    df_temporal = NumAbs.abstract_numerical(
        data_table=df_temporal,
        cols=[col],
        window_size=window_size,
        aggregation_function="std",
    )

df_temporal.columns

df_temporal_list = []
for sets in df_temporal["set"].unique():
    subset = df_temporal[df_temporal["set"] == sets].copy()
    for col in predictor_columns:
        subset = NumAbs.abstract_numerical(
            data_table=subset,
            cols=[col],
            window_size=window_size,
            aggregation_function="mean",
        )
        subset = NumAbs.abstract_numerical(
            data_table=subset,
            cols=[col],
            window_size=window_size,
            aggregation_function="std",
        )
    df_temporal_list.append(subset)

df_temporal_list = pd.concat(df_temporal_list)
df_temporal_list.info()

subset[["acc_y", "acc_y_temp_mean_ws_5", "acc_y_temp_std_ws_5"]].plot()
subset[["gyr_y", "gyr_y_temp_mean_ws_5", "gyr_y_temp_std_ws_5"]].plot()

# Frequency features

df_freq = df_temporal.copy().reset_index()
freqAbs = FourierTransformation()

sampling_frequency = int(1000 / 200)
window_size = int(2800 / 200)

df_freq = freqAbs.abstract_frequency(
    data_table=df_freq,
    cols=["acc_y"],
    window_size=window_size,
    sampling_rate=sampling_frequency,
)

df_freq.columns

subset = df_freq[df_freq["set"] == 15]
subset[["acc_y"]].plot()
subset[
    [
        "acc_y_max_freq",
        "acc_y_freq_weighted",
        "acc_y_pse",
        "acc_y_freq_1.429_Hz_ws_14",
        "acc_y_freq_2.5_Hz_ws_14",
    ]
].plot()

df_freq_list = []
for sets in df_freq["set"].unique():
    print(f"Applicating Fourier transformations to set {sets}")
    subset = df_freq[df_freq["set"] == sets].reset_index(drop=True).copy()
    subset = freqAbs.abstract_frequency(
        data_table=subset,
        cols=predictor_columns,
        window_size=window_size,
        sampling_rate=sampling_frequency,
    )
    df_freq_list.append(subset)

df_freq = pd.concat(df_freq_list).set_index("epoch (ms)", drop=True)

# Dealing with overlapping windows

df_freq = df_freq.dropna()
df_freq.info()

df_freq = df_freq.iloc[::2]

# Clustering

df_cluster = df_freq.copy()

cluster_columns = ["acc_x", "acc_y", "acc_z"]
k_values = range(2, 10)
inertias = []

for k in k_values:
    subset = df_cluster[cluster_columns]
    kmeans = KMeans(n_clusters=k, n_init=20, random_state=0)
    cluster_labels = kmeans.fit_predict(subset)
    inertias.append(kmeans.inertia_)

plt.figure(figsize=(10, 10))
plt.plot(k_values, inertias)
plt.xlabel("x")
plt.ylabel("Sum of squared distance")
plt.show()

kmeans = KMeans(n_clusters=5, n_init=20, random_state=0)
subset = df_cluster[cluster_columns]
df_cluster["cluster"] = kmeans.fit_predict(subset)

fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(projection="3d")
for c in df_cluster["cluster"].unique():
    subset = df_cluster[df_cluster["cluster"] == c]
    ax.scatter(subset["acc_x"], subset["acc_y"], subset["acc_z"], label=c)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
plt.legend()
plt.show()

fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(projection="3d")
for l in df_cluster["label"].unique():
    subset = df_cluster[df_cluster["label"] == l]
    ax.scatter(subset["acc_x"], subset["acc_y"], subset["acc_z"], label=l)
ax.set_xlabel("X-axis")
ax.set_ylabel("Y-axis")
ax.set_zlabel("Z-axis")
plt.legend()
plt.show()

# Export dataset
df_cluster.to_pickle("../../data/final/03_data_feature.pkl")
