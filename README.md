# Fitness Tracker Machine Learning Project

## Introduction

Many of the practical issues around carry-on sensors, such as accelerometers, gyroscopes, and GPS receivers, have been resolved over the past ten years. This has made it possible to track and categorize human behavior using data from wearables like smartwatches, and it has led to the development of a developing field of pattern recognition and machine learning research. The strong commercial potential of context-aware software and user interfaces is the reason behind that. Furthermore, several of the major societal issues including sustainability, rehabilitation, health care for the aged, and sustainability can be addressed using activity recognition.

## Experiment Setup

It is possible to use several machine learning algorithms to accelerometer data from free weight exercise and get excellent results, as demonstrated by other publications.
But when it comes to strength training, the process of gathering high-quality statistics has been overlooked. This study attempts to address that by creating an experimental setting that closely resembles actual strength training regimens.
It appears that related works have selected exercises at random. The selection of the particular tasks for the dataset was made without any rationale.

## Project Setup

1. Clone the Gihub Repository:

```sh
git clone https://github.com/debarshee2004/fitness_tracker.git
cd fitness_tracker
```

2. Create a Python environment:

   - Using Conda Environment.

   ```sh
   conda env create -f environment.yml
   conda activate tracking-barbell-exercises
   ```

   - Using Virtual Python Environment.

   ```sh
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Start experimenting the files and the project.

## Conclusion

This was a study about the human movement while doing exercise, and to create a model which can generalize based on Accelerometer and Gyroscope data, from a wrist watch. We tested multiple machine learning algorithms and picked which performed the best and saved it in the [`models`](./models/) folder. Out ML model using Random Forest which was giving accuracy of **99.92%**. The docs are available in [`docs`](./docs/01%20Processing%20the%20Raw%20Data.md) folder you can try to recreate the study using those.

## Licence

This project is under [MIT Licence](./LICENSE), do read the Licence before doing anything.
