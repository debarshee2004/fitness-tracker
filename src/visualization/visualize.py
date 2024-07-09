import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# Load the processed data from a pickle file into a pandas DataFrame
df_file = "../../data/processed/01_data_processed.pkl"
df = pd.read_pickle(df_file)

# Filter the DataFrame to include only rows where the 'set' column is equal to 1
set_df = df[df["set"] == 1]

# Visualize the time frame and the number of samples for a given set
# Plot the 'acc_x' column of the filtered DataFrame
plt.plot(set_df["acc_x"])
# Plot the 'acc_x' column of the filtered DataFrame with the index reset
plt.plot(set_df["acc_x"].reset_index(drop="True"))

# Plot all exercises for each label of the DataFrame
# Loop through each unique label in the 'label' column of the DataFrame
for label in df["label"].unique():
    # Filter the DataFrame to include only rows with the current label
    subset = df[df["label"] == label]
    # Create a new figure and axis for each label
    fig, ax = plt.subplots()
    # Plot the 'acc_x' column of the filtered subset with the index reset
    plt.plot(subset["acc_x"].reset_index(drop="True"), label=label)
    plt.legend()
    plt.show()

# Plotting the first 100 data points to see the difference more clearly
# Loop through each unique label in the 'label' column of the DataFrame
for label in df["label"].unique():
    # Filter the DataFrame to include only rows with the current label
    subset = df[df["label"] == label]
    # Create a new figure and axis for each label
    fig, ax = plt.subplots()
    # Plot the first 100 rows of the 'acc_x' column of the filtered subset with the index reset
    plt.plot(subset[:100]["acc_x"].reset_index(drop="True"), label=label)
    plt.legend()
    plt.show()

# Adjust plot settings
# Set the style and figure parameters for matplotlib
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20, 5)  # Set the figure size to 20x5 inches
mpl.rcParams["figure.dpi"] = 100  # Set the figure resolution to 100 DPI

# Compare medium vs. heavy sets

category_df = df.query("label == 'squat'").query("participant == 'A'").reset_index()

fig, ax = plt.subplots()
category_df.groupby(["category"])["acc_x"].plot()
ax.set_xlabel("samples")
ax.set_ylabel("acc_x")
plt.legend()
plt.show()

# Compare participants

participant_df = df.query("label == 'squat'").sort_values("participant").reset_index()

fig, ax = plt.subplots()
participant_df.groupby(["participant"])["acc_x"].plot()
ax.set_xlabel("samples")
ax.set_ylabel("acc_x")
plt.legend()
plt.show()

# Plot multiple axis

label = "squat"
participant = "A"

all_axis_df = df.query(f"label == '{label}'")

# Create a loop to plot all combinations per sensor


# Combine plots in one figure


# Loop over all combinations and export for both sensors
