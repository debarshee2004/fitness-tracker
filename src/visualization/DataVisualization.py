import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

df_file = "../../data/processed/01_data_processed.pkl"


def data_visualization(df_file) -> None:
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
    """

    df = pd.read_pickle(df_file)

    mpl.style.use("seaborn-v0_8-deep")
    mpl.rcParams["figure.figsize"] = (20, 5)
    mpl.rcParams["figure.dpi"] = 100

    labels = df["label"].unique()
    participants = df["participant"].unique()

    for label in labels:
        for participant in participants:

            combined_plot_df = (
                df.query(f"label == '{label}'")
                .query(f"participant == '{participant}'")
                .reset_index(drop="True")
            )

            if len(combined_plot_df) > 0:
                fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))

                combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])

                combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

                ax[0].legend(
                    loc="upper center",
                    bbox_to_anchor=(0.5, 1.15),
                    ncol=3,
                    fancybox=True,
                    shadow=True,
                )

                ax[1].legend(
                    loc="upper center",
                    bbox_to_anchor=(0.5, 1.15),
                    ncol=3,
                    fancybox=True,
                    shadow=True,
                )

                ax[1].set_xlabel("samples")

                plt.savefig(f"../../report/figures/{label.title()}_({participant}).png")
                # plt.show()


if __name__ == "__main__":
    data_visualization(df_file)
