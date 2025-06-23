# Overview

### Version: 0.1

This repository was created for 2025 Summer internship at Leibniz Centre for Tropical Marine Research in exploration of predicting the bio geograpgy of different types of nitrogen fixers using environmental data using machine learning.

# Requirements

- Python
- Jupyter notebooks

## Libraries:

It should be noted that some of these libraries themselves have dependencies that should be installed to run the code.

- numpy
- pandas
- xarray
- matplotlib

# File structure

```
.
├── csv
│   └── *.csv
├── nc
│   └── *.nc
├── obs_env.ipynb
└── README.md
```

# Set up

If you want to not only view but also run the jupyter notebooks you will need to make sure that all libraries listed above are installed. Then download all the datasets used for the project from the sources listed below and put different file types in corresponding folders according to the file structure of the repo.

# Version history

- 0.1 creation of the repo and the README file
- 1.0 refinements to README, analysis of environmental data in [obs_env.ipynb](./obs_env.ipynb) and .gitignore file added

# Sources

### Environmental data:

- [World Ocean Atlas 2023 Data(National Center for Environmental Information)](https://www.ncei.noaa.gov/access/world-ocean-atlas-2023/)

### Diazatrops data:

- [Global oceanic diazotroph database version 2 and elevated estimate of global oceanic N2 fixation](https://essd.copernicus.org/articles/15/3673/2023/essd-15-3673-2023-assets.html)
- [Database of diazotrophs in global ocean: abundance, biomass and nitrogen fixation rates](https://doi.pangaea.de/10.1594/PANGAEA.774851)
