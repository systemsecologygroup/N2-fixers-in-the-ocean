# Overview

### Version: 3.0

This repository was created for 2025 Summer internship at the Systems Ecology Group of the Leibniz Centre for Tropical Marine Research in exploration of predicting the biogeograpgy of different types of nitrogen fixers using environmental data using and by means of machine learning.

# Requirements

- Python
- Jupyter notebooks

## Libraries:

It should be noted that some of these libraries themselves have dependencies that should be installed to run the code.

- numpy
- pandas
- xarray
- cartopy
- matplotlib
- sklearn
- seaborn
- joblib (for saving the model and the imputer objects)

# File structure

All csv files should be stored in the _csv_ folder, and all net CDF files should be put into a _nc_ folder. The exact names of the files can be found in each jupyter notebook. Usually it is the name of the exel file + specific use case.

In the main repository folder all jupyter notebook files are contained alongside _.gitignore_ and _README.md_ file. The ignore file makes sure that no dataset files are pushed into the repo as they take a lot of space and no version control is needed for them as the source files are not modifed.

### Python files

- obs\_\*.ipynb - contains data cleaning code, formating the data into desired format before further analysis and transformations.

```
.
├── csv
│   ├── features
│   ├── filled
│   └── *.csv
├── fill_env.ipynb
├── fill_nifh.ipynb
├── join_csv.ipynb
├── model
│   └── imputer_knn
├── nc
│   ├── Fe
│   └── *.nc
├── obs_diazotr.ipynb
├── obs_env.ipynb
├── obs_nifh.ipynb
├── obs_nifh_nc.ipynb
└── README.md
```

# Set up

If you want to not only view but also run the jupyter notebooks you will need to make sure that all libraries listed above are installed. Then download all the datasets used for the project from the sources listed below and put different file types in corresponding folders according to the file structure of the repo.

### Running the files:

#### Running all files:

1.  obs\_\*.ipynb files should be ran in any order
2.  fill\_\*.ipynb files should be executed to fill the missing values in the created datasets and average the points
3.  join_csv.ipynb file creates joined datasets, viusalizes the analysis of the distributions and transforms the set

#### Running only necessary files to create the model

# Version history

- 0.1 creation of the repo and the README file
- 1.0 refinements to README, analysis of environmental data in [obs_env.ipynb](./obs_env.ipynb) and .gitignore file added. Also, made an overview the the data for bacteria that we aim to later predict.
- 2.0 Joining environmental and bacteria data into a single file. Filling in missing values. Averaged the data in bacterial nifh gene dataset for the same coordinate point. Started conducting exploritory data analysis to make better model performance more likely and possible.
- 3.0

# Sources

### Environmental data:

- [World Ocean Atlas 2023 Data(National Center for Environmental Information)](https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/)
- Iron data

### Diazatrops data:

- [Global oceanic diazotroph database version 2 and elevated estimate of global oceanic N2 fixation](https://essd.copernicus.org/articles/15/3673/2023/essd-15-3673-2023-assets.html)
- [Database of diazotrophs in global ocean: abundance, biomass and nitrogen fixation rates](https://doi.pangaea.de/10.1594/PANGAEA.774851)
