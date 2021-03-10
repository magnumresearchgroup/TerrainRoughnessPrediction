## Model
This folder contains the code for the roughness classification models trained. The models themselves were too large to put in the Github repository. They will either be uploaded to a Kaggle dataset, or you can email us.

The scripts to train the models in this folder are as follows.

`random_split`
- v8: Models trained with TSM 1, original groups, random split.
- v9: Models trained with TSM 1, k = 2 groups, random split.
- v10: Models trained with TSM 1, k = 3 groups, random split.
- v11: Models trained with TSM 1, k = 4 groups, random split.
- v12: Models trained with TSM 2, original groups, random split.
- v13: Models trained with TSM 2, k = 2 groups, random split.
- v14: Models trained with TSM 2, k = 3 groups, random split.
- v15: Models trained with TSM 2, k = 4 groups, random split.

`chronological_split`
- v16: Models trained with TSM 2, k = 2 groups, chronological split.
- v17: Models trained with TSM 2, k = 4 groups, chronological split.

`attention_region`
- v18: Models trained with TSM 2, k = 2 groups with original images, images with a dark attention region, and images with a light attention region.
- v19: Models trained with TSM 2, k = 4 groups with original images, images with a dark attention region, and images with a light attention region.