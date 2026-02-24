import matplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import seaborn as sns
import pandas as pd
import numpy as np

from var import cordinates_cols


def plotColsOnMap(
        cols,
        df, 
        overlay=None,
        log_range = False, 
        constant = (10**6), 
        cmap="viridis",
        min_lim=None, 
        max_lim=None, 
        transf = (lambda x: x), 
        specific_depth=None,
        colorbar_label = "",
        title="",
        s=5,
        color_steps=None,
    ):
    """
    Plot specified column on a map. Latitude and longitude range should be -180 to 180 and -90 to 90.

    Args:
        cols: list of column names
        df: pandas dataframe
        overlay: pandas dataframe to overlay if not None(default)
        log_range: True/False(defualt False)
        constant: constant by which to mutliply all values(default 10**6)
        cmap: default"viridis"
        min_lim: minimum value to plot (default None) 
        max_lim: maximum value to plot (default None)
        transf = (lambda x: x) transformation function identity by defualt
        specific_depth: specific depth to plot(default is None so all depths)
        colorbar_label: label for the colorbar
        title: title for the plot overall
        s: dot size default is 5
        color_steps: defualt = None, how many steps should the plot colorbar have?

    Returns:
        nothing

    """
    isOverlay = isinstance(overlay, pd.DataFrame)
    max_lim_plot=max_lim
    min_lim_plot=min_lim

    #the index is reset from using lat and lon just in case
    df_reset = df.reset_index()
    dfo_reset = overlay.reset_index() if isOverlay else None

    #the number of rows varies depending on the number of columns to plot and subplots created
    rows = (len(cols)//2) + (len(cols)%2==1)
    fig, axes = plt.subplots(nrows=rows, ncols=2, figsize=(20, rows*4), subplot_kw={"projection": ccrs.PlateCarree()})

    #we plot each column
    axes = axes.flatten()

    for i, col in enumerate(cols):
        ax = axes[i]#subplot

        #COASTLINE GENERATION
        #we want to see the coastlines on the globe and only take not null values
        ax.add_feature(cfeature.COASTLINE)
        valid_data = df_reset[df_reset[col].notna()]
        valid_overlay = dfo_reset[dfo_reset[col].notna()] if isOverlay else None

        #DEPTH, REDUCTION TO 3D->2D
        #the depth when specified limits the depth visualized to a specifc depth
        if specific_depth != None:
            #base layer containing most data
            mask = valid_data["DEPTH (m)"]==specific_depth
            valid_data=valid_data[mask]

            if (isOverlay):
                #overlay layer
                mask = valid_overlay["DEPTH (m)"]==specific_depth
                valid_overlay=valid_overlay[mask]
        else:
            valid_data = valid_data.groupby(by=['LATITUDE', 'LONGITUDE']).mean().reset_index()

            if (isOverlay):
                valid_overlay=valid_overlay.groupby(by=['LATITUDE', 'LONGITUDE']).mean().reset_index()

        #LOG RANGE LIKE THE PAPER
        #this sets the logorithmic scale to be exactly like in the paper instead of default
        norm = None        
        if log_range:
            norm = matplotlib.colors.LogNorm(vmin=1e3, vmax=1e11)

        # PLOTTING DATA
        plotted_data=transf(((valid_data[col])*constant))

        #STEPPED COLOR BAR
        #the color steps mean that we need to specify the max 
        if color_steps != None:
            data_cols = list(set(valid_data.columns)-set(cordinates_cols))

            #set the limit for the colorbar
            color_max=None
            if max_lim==None:
                color_max=plotted_data.max()
            else:
                color_max=max_lim
                max_lim_plot=None

            #set the min limit
            color_min=None
            if min_lim==None:
                color_min=plotted_data.min()
            else:
                color_min=min_lim
                min_lim_plot=None

            #now we can create a boundary between them
            bounds = np.linspace(start=color_min, stop=color_max, endpoint=True, num=color_steps+1)
            norm=mpl.colors.BoundaryNorm(bounds, plt.get_cmap(cmap).N)
            
        #MAIN SCATTER PLOT
        #scatter plot is created
        sc = ax.scatter(
            valid_data["LONGITUDE"],
            valid_data["LATITUDE"],
            c=plotted_data,#data is multiplied by a constant and transformed
            cmap=cmap,
            s=s,
            transform=ccrs.PlateCarree(),
            norm=norm,
            vmin=min_lim_plot,
            vmax=max_lim_plot,
            zorder=1
        )

        #OVERLAY PLOT IF NEEDED
        if (isOverlay):
            sc_over = ax.scatter(
                valid_overlay["LONGITUDE"],
                valid_overlay["LATITUDE"],
                c=transf(((valid_overlay[col])*constant)),#data is multiplied by a constant and transformed
                cmap=cmap,
                s=4*s,
                transform=ccrs.PlateCarree(),
                norm=norm,
                vmin=min_lim_plot,
                vmax=max_lim_plot,
                zorder=2,
                edgecolors="black",
                linewidth=0.5
            )

        #we want to see the entire globe and not just the values 
        ax.set_xlim(-180,180)
        ax.set_ylim(-90,90)        

        plt.colorbar(sc, ax=ax, label=colorbar_label)
        ax.set_title(col)
    
    plt.suptitle(title)
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

def plotCorMatr(cols, df, cmap="vlag"):
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
    sns.heatmap(mtrx, cmap=cmap, annot=True)

    plt.show()

    return mtrx

def errorScorePlot(scores, error_fun, y_axis, title, color, y_columns):
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 20))
    axes = axes.flatten()

    for i, feature in enumerate(y_columns):
        #simplify notation
        ax=axes[i]
        
        ##we plot a single feature
        subset = scores[scores['feature'] == feature]

        #the barplot is made
        sns.barplot(
            data=subset,
            x='dataset name',
            y=error_fun,
            hue='model',
            palette=color,
            ax=ax
        )

        ax.set_title('Comparison of models and scalers on feature: {0}'.format(feature))
        ax.set_ylabel(y_axis)

        ax.tick_params(axis='x', rotation=45)
        ax.legend(title='Model')

    plt.tight_layout()
    fig.suptitle(title,fontsize=16)
    fig.subplots_adjust(top=0.95)
    plt.show()