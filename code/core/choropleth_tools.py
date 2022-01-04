"""
created: 2022-01-03
author: JER
this script is useful for making choropleth plots.
"""
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable


def plot_county_data(LOCATION_COUNTS_DF):

    # specify the shape file to use for county boundaries
    IN_SHAPE_FILE_NAME = 'tl_2021_us_county.shp'
    IN_SHAPE_FILE_PATH = '../../data/shapefiles/tl_2021_us_county/'

    # set chloropleth column and colors
    CHLOROPLETH_COL = 'counts'
    MIN_COLOR_COUNT = 1  # counts that will be colored by min color of cmap
    MAX_COLOR_COUNT = 'automatic'  # counts that will be colored by max color of cmap
    COLOR_MAP = mpl.cm.OrRd  # choose a perceptually uniform colormap

    # set some kwds for the locations with missing data
    MISSING_KWDS = {'color': (0.85, 0.85, 0.85, 1.0), 'label': 'missing values'}

    # use geopandas to read in a shapefile for US county borders
    US_COUNTIES_GDF = gpd.read_file(IN_SHAPE_FILE_PATH + IN_SHAPE_FILE_NAME)
    # print(US_COUNTIES_GDF.columns.to_list())
    # print(US_COUNTIES_GDF['CLASSFP'])
    US_COUNTIES_GDF['identifier'] = (US_COUNTIES_GDF['STATEFP'].astype(str)
                                     + '_'
                                     + US_COUNTIES_GDF['NAME'].astype(str))

    US_COUNTIES_GDF.set_index('identifier', inplace=True)
    US_COUNTIES_GDF.sort_index(inplace=True)
    US_COUNTIES_GDF['counts'] = LOCATION_COUNTS_DF['count']

    # set the maximum value for the color scale
    if MAX_COLOR_COUNT == 'automatic':
        if US_COUNTIES_GDF['counts'].max() < 10:
            MAX_COLOR_COUNT = 10
        else:
            MAX_COLOR_COUNT = US_COUNTIES_GDF['counts'].max()

    # change the name of the "geometry" column to something more informative
    US_COUNTIES_GDF = US_COUNTIES_GDF.rename(columns={'geometry': 'county_borders'})

    # set the column to be used as the 'geometry' column
    US_COUNTIES_GDF = US_COUNTIES_GDF.set_geometry('county_borders')

    # initialize a figure
    fig_01, CONTINENTAL_AX = plt.subplots(1, 1, figsize=(4, 4), dpi=300)

    # set the boundaries for each axis
    CONTINENTAL_AX.set_xlim(-126, -65)
    CONTINENTAL_AX.set_ylim(23, 51)

    # make a list of all of the figure axes to plot on
    AXES_LIST = [CONTINENTAL_AX]  # , AK_ax, HI_ax, PR_ax]

    # make a layered map plot
    for axis in AXES_LIST:
        axis.set_aspect('equal')  # set the aspect ratio
        '''
        # mask the states with 0 cases (NOT NaN) with white (if there are any)
        if not true_zeros_gdf.empty:
            true_zeros_gdf.plot(ax=axis, color='w', zorder=1)
        '''
        # add layer for county borders
        US_COUNTIES_GDF.boundary.plot(ax=axis, zorder=2, linewidth=0.3,
                                      color=(0.0, 0.0, 0.0, 1.0))
        '''
        # add a layer of points
        if PLOT_POINTS:
            points_gdf.plot(ax=axis, zorder=3, marker='o',
                            markersize=2, linewidth=0.25,
                            facecolor=(0.5, 0.5, 0.5, 0.0), edgecolor='k')
        '''
        # add chloropleth layers
        if axis == CONTINENTAL_AX:
            # hide the axis ticks (lat and lon numbers are not critical here)
            axis.tick_params(left=False, labelleft=False,
                             bottom=False, labelbottom=False)
            '''
            # include the time frame dates as a label for the x axis
            axis.set_xlabel(str(START_DAY.date())
                            + ' to '
                            + str(END_DAY.date()),
                            fontsize=6, color='k')
            '''
            axis.xaxis.set_label_position('top')

            # remove the frame
            axis.spines['top'].set_visible(False)
            axis.spines['right'].set_visible(False)
            axis.spines['bottom'].set_visible(False)
            axis.spines['left'].set_visible(False)

            # plot chloropleth on bottom layer
            US_COUNTIES_GDF.plot(ax=axis, zorder=0, column='counts',
                                cmap=COLOR_MAP,
                                vmin=MIN_COLOR_COUNT, vmax=MAX_COLOR_COUNT,
                                missing_kwds=MISSING_KWDS)

        else:
            axis.axis('off')  # remove entire box around inset axes
            # plot chloropleth on bottom layer
            us_states_gdf.plot(ax=axis, zorder=0, column='counts',
                               cmap=COLOR_MAP,
                               vmin=MIN_COLOR_COUNT, vmax=MAX_COLOR_COUNT,
                               legend=False, missing_kwds=MISSING_KWDS)
    plt.show()
    return fig_01


test_data = list(zip(['WI', 'CA', 'LA', 'LA', 'KY', 'MD', 'KY'],
                      ['55', '06', '22', '22', '21', '24', '21'],
                      ['Monroe', 'San Bernandino', 'Grant', 'Orleans', 'Kenton', 'Baltimore City', 'Boone'],
                      [0, 1, 2, 3, 4, 5, 6]))
test_df = pd.DataFrame(data=test_data, columns=['state_name', 'state_FIPS', 'county_name', 'count'])
test_df['identifier'] = (test_df['state_FIPS'].astype(str)
                         + '_'
                         + test_df['county_name'].astype(str))
test_df.set_index('identifier', inplace=True)
test_df.sort_index(inplace=True)
print(test_df)

test_fig = plot_county_data(test_df)

# test_fig.show()

# TROUBLESHOOTING SPACE
