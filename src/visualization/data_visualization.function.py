import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

df_file = "../../data/processed/01_data_processed.pkl"


# The main function which is responsible for data visualization.
def data_visualization(df_file):
    """
    Visualize accelerometer and gyroscope data from a processed DataFrame stored in a pickle file.

    This function reads a DataFrame from a pickle file, processes the data, and generates plots for
    each unique combination of 'label' and 'participant' present in the DataFrame. The function saves
    the plots as PNG files in a specified directory.

    Parameters:
    df_file (str): The file path to the pickle file containing the processed DataFrame.

    The DataFrame is expected to have the following columns:
    - 'label': Category label for each data point.
    - 'participant': Identifier for the participant providing the data.
    - 'acc_x', 'acc_y', 'acc_z': Accelerometer data for x, y, and z axes.
    - 'gyr_x', 'gyr_y', 'gyr_z': Gyroscope data for x, y, and z axes.

    Plot details:
    - Two subplots are created for each unique combination of 'label' and 'participant'.
    - The first subplot displays accelerometer data ('acc_x', 'acc_y', 'acc_z').
    - The second subplot displays gyroscope data ('gyr_x', 'gyr_y', 'gyr_z').
    - Legends are added to both subplots.
    - The plots are saved in the '../../report/figures/' directory with filenames formatted as '{Label}_{Participant}.png'.

    The function uses matplotlib for plotting and pandas for data manipulation.

    Example:
    data_visualization('path/to/processed_data.pkl')
    """

    # Load the processed data from a pickle file into a pandas DataFrame
    df = pd.read_pickle(df_file)

    # Adjust plot settings
    # Set the style and figure parameters for matplotlib
    mpl.style.use("seaborn-v0_8-deep")
    mpl.rcParams["figure.figsize"] = (20, 5)  # Set the figure size to 20x5 inches
    mpl.rcParams["figure.dpi"] = 100  # Set the figure resolution to 100 DPI

    # Get the unique labels and participants from the DataFrame
    labels = df["label"].unique()
    participants = df["participant"].unique()

    for label in labels:
        for participant in participants:
            # Filter the DataFrame to include only rows with the current label and participant, then reset the index
            combined_plot_df = (
                df.query(f"label == '{label}'")
                .query(f"participant == '{participant}'")
                .reset_index(drop="True")
            )

            # Check if the filtered DataFrame is not empty
            if len(combined_plot_df) > 0:
                # Create a figure with two subplots (one row, two columns) that share the x-axis
                fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))

                # Plot the 'acc_x', 'acc_y', and 'acc_z' columns of the filtered DataFrame on the first subplot
                combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])

                # Plot the 'gyr_x', 'gyr_y', and 'gyr_z' columns of the filtered DataFrame on the second subplot
                combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

                # Add a legend to the first subplot
                ax[0].legend(
                    loc="upper center",
                    bbox_to_anchor=(0.5, 1.15),
                    ncol=3,
                    fancybox=True,
                    shadow=True,
                )

                # Add a legend to the second subplot
                ax[1].legend(
                    loc="upper center",
                    bbox_to_anchor=(0.5, 1.15),
                    ncol=3,
                    fancybox=True,
                    shadow=True,
                )

                # Set the label for the x-axis of the second subplot
                ax[1].set_xlabel("samples")

                # Save the figure to a file
                plt.savefig(f"../../report/figures/{label.title()}_({participant}).png")
                # Uncomment the following line to display the plot
                # plt.show()


data_visualization(df_file)
