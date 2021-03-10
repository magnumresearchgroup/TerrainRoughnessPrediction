## Path Detection Classifier

This folder contains the CSV with the images used for training. We do not include the Path Detection Classifier itself, as it contains images with sensitive information (i.e. other bikers, license plates).

`Predictions` contains the script used to predict whether images were valid under visual validation. It contains the CSV with the Path Detection Classifier's original predictions, as well as the two CSVs with the manual validated categories after each round of manual validation. The final image categories are in `validated_image_categories_2.csv`.