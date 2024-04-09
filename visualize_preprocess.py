import pandas as pd
import numpy as np
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    
    # import datasets
    location = pd.read_csv('data/location.csv', usecols=lambda x: x not in ['Lat', 'Long_']) \
        .rename(columns=({'Province_State': 'province', 'Country_Region': 'country'}))
    train = pd.read_csv('data/cases_train.csv', usecols=lambda x: x not in ['latitude', 'longitude'])
    test = pd.read_csv('data/cases_test.csv', usecols=lambda x: x not in ['latitude', 'longitude'])
    continent_map = pd.read_csv('data/countries_continent.csv')

    # import geo data for heatmap and population info
    world = gpd.read_file('data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')[['ADMIN', 'CONTINENT', 'POP_EST', 'geometry']]
    world.columns = ['country', 'continent', 'population', 'geometry']
    world[world['country'] == 'United States']['country'] == 'United States of America'

    print('\ndatasets imported')
    print('location: {0} rows'.format(len(location)))
    print('train: {0} rows'.format(len(train)))
    print('test: {0} rows\n'.format(len(test)))

    # ===================== DATA PREPROCESSING ====================
    # Handle the missing values. 
    # Join both location and case data on both country and province together as a primary key and add an ‘Expected_Mortality_Rate’ to the cases dataset. 
    # Find out what is the best strategy for dealing with missing values and mention and explain your choice in the report.
    
    #colourcode 
    # confirmed cases/population
    #scrap cases
    agg = location.merge(train, on=['country','province'], how = 'left', suffixes=('_l','_r'))
    agg.dropna(axis=1)
    # agg = pd.concat([location,train]).reset_index(drop=True)
    agg[agg['country'] == 'US']['country'] == 'United States'
    agg[agg['country'] == 'Korea, South']['country'] == 'South Korea'
    agg = agg.sort_values('country')
    agg = pd.merge(agg, continent_map, how='left',on='country')
    print(agg.columns)
    


    # ======================
    # First, you have to visualize the data. 
    # Create a bar plot of data availability based on continents. 
    # Are there any anomalies? How do they compare to the continents’ overall populations? 
    # Use a color spectrum for different proportions; for example, the bars for the continents with a higher data availability should be redder and bluer otherwise. 
    # Create a colored heatmap of the world, concerning the percentage of available data on the countries' populations. An example of this is life expectancy based on countries. 
    # Note that you have to use both the location and cases csv files and combine them. Report all the plots and your interpretation of them.

    # ======================PART 1: BARPLOT======================

    agg_counts = pd.DataFrame(agg.groupby(['continent']).size())
    agg_counts.reset_index(inplace=True)
    print(agg_counts.columns)
    agg_counts.columns = ['continent', 'size']
    colours = plt.cm.RdBu(np.linspace(0,1,len(agg_counts['continent'])))
    plt.bar(agg_counts['continent'],agg_counts['size'], color = colours)
    plt.show()
    ### how well countries represented, plot ratio #cases in country/population
    # cases can be seen as subset of location, we can omit combining for 

    # ======================PART 2: WORLD MAP=====================

    ### plot availability of data/population

    #add column 'geometry'
    fig, ax = plt.subplots(figsize=(10, 8))
    

    # Merge data with world geometries based on geometry
    world = world.merge(agg, how='left', left_on='country', right_on='country')
    print(world.columns)
    world['res'] = (world['Confirmed'] + world['Deaths'] + world['Active'] + world['Recovered'])/world['population']
    world.plot(column = 'res', cmap='YlGnBu', kind = 'geo', ax=ax, legend = True)
    plt.show()
    return

    



    
def debug_old():
    ### debug for all cols in world
    # world_deb = gpd.read_file('data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
    # pd.set_option('display.max_columns', None)
    # print(world_deb.head())

    # location = pd.read_csv('data/location.csv', usecols=['Country_Region','Lat','Long_']) \
    #     .rename(columns=({'Country_Region': 'country','Lat': 'latitude','Long_': 'longitude'}))
    # train = pd.read_csv('data/cases_train.csv', usecols=['country','latitude','longitude'])
    # test = pd.read_csv('data/cases_test.csv', usecols=['country','latitude','longitude'])

    # Plotting heatmap
    fig, ax = plt.subplots(figsize=(10, 6))
    #agg_geo = gpd.GeoDataFrame(agg, geometry=gpd.points_from_xy(agg['longitude'], agg['latitude']))
   # world_pivot = agg_geo.pivot_table('latitude','longitude', columns='continent')
    #sns.heatmap(world_pivot, cmap='YlGnBu', ax=ax, annot=True, fmt=".0f", cbar_kws={'label': 'Value'})
    # sns.heatmap(world.pivot_table(index='continent', columns='count'), cmap='YlGnBu', ax=ax, annot=True, fmt=".0f", cbar_kws={'label': 'Value'})
    ax.set_title('Continental Heatmap')
    plt.show()


if __name__ == '__main__':
    main()