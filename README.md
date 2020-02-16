# ember-alerts
TreeHacks 2020 Project with Isaac Perper, Wilbur Li, Ethan Goldfarb, Michael Karachewski

[Here](https://devpost.com/software/ember-alerts-tmzrv4) is the DevPost for the project.

## Getting Started / User guide

All services should be run in the Google Cloud environment.

### To train model
Open [fire_predictor.ipynb](https://drive.google.com/open?id=1Ool26DrdAiplirfD-5psWM-KouQQ86zr) in Drive folder 
Run code blocks 1-3.

### To predict with model
Run block 4. 

## File Details

The important files in this repo include:

`utilities/darksky.py`: Takes rows of (lon,lat,date) inputs from a CSV and calls DarkSky Weather API several times for each entry to output 13 weather features and other fields to a CSV.

`model/fire_predictor.ipynb`: Loads rows of training points from aggregate_features.gsheet (a Google Cloud Colab functionality), slicing into train and test datasets; trains and tests a Tensorflow model

`pullDayData.js`: Google Earth Engine Script for exporting CSV of (lon,lat,visibility) for fire events in our region for any specified day. 
File location: https://code.earthengine.google.com/1b11bc26a21390d60a70e23b81b87fa8

`aggregate_features.gsheet`: Store for all of our training data, where we have 1384 1-labeled points, and 3061 0-labeled points. Each point has an ID, day, lon, lat, and 13 features. The labels correspond to whether there was a fire at that location. The features are used in the model.

