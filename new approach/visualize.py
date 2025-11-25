import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns

def plotColsOnMap(cols,df, log_range = False, constant = (10**6), cmap="viridis",min_lim=None, max_lim=None, transf = (lambda x: x)):
    """
    Plot specified column on a map. Latitude and longitude range should be -180 to 180 and -90 to 90.

    Args:
        cols: list of column names
        df: pandas dataframe
        log_range: True/False(defualt False)
        constant: constant by which to mutliply all values(default 10**6)

    Returns:
        nothing

    """
    #the index is reset from using lat and lon just in case
    df_reset = df.reset_index()

    #the number of rows varies depending on the number of columns to plot
    rows = (len(cols)//2) + (len(cols)%2==1)

    #a set of subplots is created
    fig, axes = plt.subplots(nrows=rows, ncols=2, figsize=(20, rows*4), subplot_kw={"projection": ccrs.PlateCarree()})

    #we plot each column
    axes = axes.flatten()
    for i, col in enumerate(cols):
        ax = axes[i]#subplot

        #we want to see the coastlines on the globe and only take not null values
        ax.add_feature(cfeature.COASTLINE)
        valid_data = df_reset[df_reset[col].notna()]

        #this sets the logorithmic scale to be exactly like in the paper instead of default
        norm = matplotlib.colors.LogNorm(vmin=1e3, vmax=1e11)
        if(not log_range):
            norm = None

        #scatter plot is created
        sc = ax.scatter(
            valid_data["LONGITUDE"],
            valid_data["LATITUDE"],
            c=transf(valid_data[col]*constant),#data is multiplied by a constant
            cmap=cmap,
            s=5,
            transform=ccrs.PlateCarree(),
            norm=norm,
            vmin=min_lim,
            vmax=max_lim
        )

        #we want to see the entire globe and not just the values 
        ax.set_xlim(-180,180)
        ax.set_ylim(-90,90)

        plt.colorbar(sc, ax=ax, label="nifH Gene (copies m-3)")
        ax.set_title(col.replace("x106 ",""))

    plt.tight_layout()
    plt.show()

def histCols(cols,df, transf = (lambda x: x), suptitle=""):
    """
    Plot specified columns of a dataframe as a histogram

    Args:
        cols: list of column names
        df: pandas dataframe
        transf: (default (lambda x: x))
        suptitle: suptitle text

    Returns:
        nothing
    """
    #the index is reset from using lat and lon just in case
    df_reset = df.reset_index()

    #the number of rows varies depending on the number of columns to plot
    rows = (len(cols)//2) + (len(cols)%2==1)

    #a set of subplots is created
    fig, axes = plt.subplots(nrows=rows, ncols=2, figsize=(20, rows*4))

    #we plot each column
    axes = axes.flatten()
    for i, col in enumerate(cols):
        ax = axes[i]#subplot

        valid_data = df_reset[df_reset[col].notna()]
        transf(valid_data[col]).hist(bins=50, ax=ax)

        ax.set_title(col)
    if(len(suptitle)>0):
        plt.suptitle(suptitle, fontsize=16)

    plt.tight_layout()
    plt.show()

def plotCorMatr(cols, df):
    """
    Creates a display of the correlation matrix of specified columns

    Args:
        cols: list of column names
        df: pandas dataframe

    Returns:
        nothing
    """
    #we create the matrix
    mtrx = df[cols].corr()
    #a heatmap is created to show the results
    sns.heatmap(mtrx, cmap="YlGnBu", annot=True)

    plt.show()

    return mtrx