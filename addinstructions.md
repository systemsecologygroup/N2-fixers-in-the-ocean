# How to add new bacterial and environmental data to the project
## Environmental data

### Expected format of data:
This is in what state the data is saved at the end of ***obs_env.ipynb*** file before further modifications.

| column    | LATITUDE             | LONGITUDE            | O2    | T     | N     | P     | Fe    | solar |
| --------- | -------------------- | -------------------- | ----- | ----- | ----- | ----- | ----- | ----- |
| data type | integer -180 to +180 | integer -180 to +180 | float | float | float | float | float | float |
## Bacterial data

This section is more crutial as additional NifH data is more likely and more important. The main modifications to be done are in the ***obs_nifh.ipynb*** file.

### Expected format of data:
PAY ATTENTION TO DATA TYPE AND COLUMN NAMES!

| column    | LATITUDE             | LONGITUDE            | Trichodesmium nifH Gene (x106 copies m-3) | UCYN-A nifH Gene (x106 copies m-3) | UCYN-B nifH Gene (x106 copies m-3) |
| --------- | -------------------- | -------------------- | ----------------------------------------- | ---------------------------------- | ---------------------------------- |
| data type | integer -180 to +180 | integer -180 to +180 | float from 0 to 1.9e8                     | float from 0 to 99700              | float from 0 to 898000             |

The data is expected to be in this format by the end of the file. There are functions to make it easier to convert but on case by case basis more or less effort might be requires.

**Specific things to pay attention to**
1. Column names
2. Range of coordinates! Can be checked via *dataframe.describe()* command
3. Missing/Nan values and empty rows especially in landmasses
4. Column types
5. Depth column in the original dataset and how its named.
6. Unnecessary columns

### How to process data
Examples of this can be found in corresponding files

1. open the csv file as pandas dataframe
2. (recommended: use describe and info in order to get an overview of the data)
3. Rename columns if needed, but can be done later on for data columns
4. use *removeRed* to remove columns that are not needed. If you want to supply it with *keepers* list add the corresponding names to it.
5. *objToNum* to convert all object columns to a number value
6. (rename if needed column to ""DEPTH (m)") use *filterDepth* to remove deeper values than needed
7. use *removeEmptyRows* in order to remove rows that might be empty after the modifications
8. round the coordinates using *roundCoord*

After that the data is ready to be joined together with other datasets at the end of the file. In section **combining all of them into 1** add the object to the list where *combined_df* is created.

If a new column is added, that did not exist before you will need to add it to column lists at the beginning of following files(pipeline wise).

## After adding to obs_ files
Make sure to rerun the files in order described in README file.


