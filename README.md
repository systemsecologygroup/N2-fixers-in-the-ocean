# Overview

### Version: 7.0

This repository was created for 2025 Summer internship at the Systems Ecology Group of the Leibniz Centre for Tropical Marine Research in exploration of predicting the biogeograpgy of different types of nitrogen fixers using environmental data using and by means of machine learning.

The project was further developed and extended during a working student contract in December 2025 - March 2026.

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
- netcdf4

You can find the installation guide for the virtual python environment under [setup_venv.md](./setup_venv.md)

# File structure

All csv files should be stored in the _csv_ folder, and all net CDF files should be put into a _nc_ folder. The exact names of the files can be found in each jupyter notebook. Usually it is the name of the exel file + specific use case. The ones needed to execute the code are already there.

In the main repository folder doc files are contained alongside _.gitignore_ and _README.md_ file. The ignore file makes sure that no dataset files are pushed into the repo as they take a lot of space and no version control is needed for them as the source files are not modifed.

The source files are in _src_ direcotry.

## Doc files
These file inform on repo structure and inner workings. They cover custom functions, classes, global variables and set up for running the code. Also, they discuss how to add more data and what was achieved during the internship.

- [functions.md](./functions.md)
- [setup_venv.md](./setup_venv.md)
- [README.md](./README.md)
- [addinstructions.md](./addinstructions.md)
- [internship_report.pdf](./internship_report.pdf)

## Python files

Notebooks:
- obs\_\*.ipynb: data cleaning code, formating the data into desired format before further analysis and transformations.
- fill_env.ipynb: extrapolating to missing points
- models.ipynb: comparing different models and datasets
- predict.ipynb: predict final data on a given dataset
- visualizations.ipynb: visualizations that complement other files

Other:
- format.py: preprocessing and feature engineering functions
- parula_diy.py: parula colormap as copied from stack overflow
- training.py: functions and classes used for training
- visualize.py: functions for visualizations
- var.py: common variables used in files mostly for training stage

## Other files
- .gitignore: files to not include in version control like intermediate outputs
- libraries.txt: list of libraries used for set up of the venv


## Tree structure of the repo

Tree structure below was obtained by running the command below in the main folder of the repo
```
tree -L 2 --gitignore --dirsfirst
```

```
.
├── csv
│   ├── datasets
│   ├── features
│   ├── filled
│   ├── nifh
│   ├── nifh_di
│   ├── otpn
│   ├── predictions
│   ├── README.md
│   ├── woa23_all_n00mn01.csv
│   ├── woa23_all_o00mn01.csv
│   ├── woa23_all_p00mn01.csv
│   └── woa23_decav_t00mn01.csv
├── model
│   ├── imputer_knn
│   └── transformers
├── nc
│   ├── Fe
│   ├── otpn
│   ├── radiation
│   └── README.md
├── src
│   ├── fill_env.ipynb
│   ├── format.py
│   ├── join_csv.ipynb
│   ├── models.ipynb
│   ├── obs_env.ipynb
│   ├── obs_nifh.ipynb
│   ├── parula_diy.py
│   ├── predict.ipynb
│   ├── training.py
│   ├── var.py
│   ├── visualizations.ipynb
│   └── visualize.py
├── addinstructions.md
├── code_overview.md
├── functions.md
├── internship_report.pdf
├── libraries.txt
├── README.md
└── setup_venv.md

16 directories, 27 files

```

# Set up

If you want to not only view but also run the jupyter notebooks you will need to make sure that all libraries listed above are installed. 

## Step by step guide

Download libraries using the instructions in [setup_venv.md](./setup_venv.md)

# Running the files:

## Running all files:

1.  obs\_\*.ipynb files should be ran in any order
2.  fill\_\*.ipynb files should be executed to fill the missing values in the created datasets, adding columns
3.  join_csv.ipynb file creates joined datasets, viusalizes the analysis of the distributions and transforms the set
4.  models.ipynb training different models to see which performs the best
5.  predict.ipynb predict the results on the inputs and plot them on the map
6. visualizations.ipynb should run at the end

Other python files in src folder contain functions and classes used to make the code work.

```
                  
 obs_nifh obs_env 
    │         │   
    └────┌────┘   
         │        
      fill_env    
         │        
      join_scv    
         │        
    ┌────┘────┐   
    ∨         ∨   
  predict models  
         ∨ 
  visualizations
                  

```

1. obs_env.ipynb & obs_nifh.ipynb
2. fill_env.ipynb
3. join_csv.ipynb
4. models.ipynb & predict.ipynb
5. visualizations.ipynb

# Version history

- 0.1 creation of the repo and the README file
- 1.0 refinements to README, analysis of environmental data in [obs_env.ipynb](./src/obs_env.ipynb) and .gitignore file added. Also, made an overview the the data for bacteria that we aim to later predict.
- 2.0 Joining environmental and bacteria data into a single file. Filling in missing values. Averaged the data in bacterial nifh gene dataset for the same coordinate point. Started conducting exploritory data analysis to make better model performance more likely and possible.
- 3.0 solar data added to model features. Fruther refinements to the data analysis and transformation. Initial model training attempts.
- 4.0 made it possible to easily try out different models and compare results to find the best one. Predicted values for the entire set of environmental data. Comapred models and datasets in plots.
- 5.0 after initial model training, the need for more diverse data was discovered. Added bacterial data from more sources. New versions of the exisitng datasets were tried and more visualizations added in the models file to better compare models and datasets.
- 5.1 Further refinements of the projects code and the model as well as the visualizations. Instructions for adding new data added in [adding new data](./addinstructions.md)
- 6.0 New approach folder added. Significanlty improved code organization and quality as well as trying to improve model performance.
- 7.0 End of the working student project. Results are similar to the paper now. More documentation is added in md files.

# Sources

### Environmental data:

- $O^2$, $N^2$, $P$, Temperature [World Ocean Atlas 2023 Data(National Center for Environmental Information)](https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/)
- Iron data is from a flashdrive
- [ERA5 monthly averaged data on single levels from 1940 to present](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels-monthly-means?tab=overview) 2024 all months

### Diazatrops data:

- [Global oceanic diazotroph database version 2 and elevated estimate of global oceanic N2 fixation](https://essd.copernicus.org/articles/15/3673/2023/essd-15-3673-2023-assets.html)
- [Database of diazotrophs in global ocean: abundance, biomass and nitrogen fixation rates](https://doi.pangaea.de/10.1594/PANGAEA.774851)
- [Data‐Driven Modeling of the Distribution of Diazotrophs in the Global Ocean](https://agupubs.onlinelibrary.wiley.com/doi/pdf/10.1029/2019GL084376)
- [Biological nitrogen fixation detected under Antarctic sea ice (Takuhei Shiozaki et all)](https://www.nature.com/articles/s41561-020-00651-7#MOESM3)
