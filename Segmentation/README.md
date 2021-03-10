## Segmentation

This folder contains the three versions of the segmentation network which we trained to add an attention region to the images. The models themselves are too large to include in the Github repository, but they will either be posted to Kaggle or you can email us.

The `Predictions` folder contains the script used to add the attention region to each of the 7,061 images valid for TSM 2. `overlay_images.csv` contains the images scores for attention region validation. The attention region labeling CSV in the `Labels` folder is filtered to only contain images scoring a 0 or 1 in attention region validation.

The images with the attention region added are included in the Kaggle dataset.