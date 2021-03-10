## Terrain Roughness Classification

This repository contains the original code used for this project, Terrain Roughness Classification for Off-Road Autonomous Vehicles. The original project was developed using Google Drive, and the dataset used in this repository is located on the [Kaggle dataset page](https://www.kaggle.com/magnumresearchgroup/offroad-terrain-dataset-for-autonomous-vehicles).

## Additional Information
This project was developed using Google Drive and Google Colab. The dataset used in this project was also stored in the Google Drive repository. There are a few important distinctions between this Github repository and the Google Drive repository.
1. The Github repository contains only the scripts used in this project and label CSVs.
2. The models, which were in the Google Drive repository, were too large to include in the Github repository. They will either be separately posted to Kaggle or you can email us.
3. The dataset used in this project was in the Google Drive repository but is not included in this repository. It is instead made public on the [Kaggle dataset page](https://www.kaggle.com/magnumresearchgroup/offroad-terrain-dataset-for-autonomous-vehicles).
4. Images used for training the attention region network along with the attention region network's predictions on the images in our dataset were in the Google Drive repository but are not included in this repository. They are posted separately to a [Kaggle dataset page for the attention region images](https://www.kaggle.com/magnumresearchgroup/offroad-terrain-attention-region-images).

Additionally, the Github repository contains a few different organizational and naming conventions than the Google Drive repository. The scripts have not been modified to reflect this new organization so that they remain in their original form. Thus, paths to the dataset, label CSVs, and other items within the repository may not reflect the naming conventions or organizational structure in the Github repository. The changes are listed below.
- `split_within_session` has been renamed to `chronological_split` in folder organization for clarity.
- `/gdrive/My Drive/Labeling` was the location of the Google Drive repository. All occurrences should be changed to this repository.
- The `LabelsCSV` folder was renamed to `Labels` for clarity.
- `Metric1` and `Metric2` were renamed to `TSM1` and `TSM2` in folder organization for consistency with the paper terminology.
- The files within `ValidImages/TSM1` used to be in the `ValidImages` directory. They were moved within a folder for organization.
- The folders within `Model/attention_region` used to be in the `Models` directory. They were moved within a folder for organization.
