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
    #world[world['country'] == 'United States of America']['country'] == 'United States'
    world['country'] = world['country'].replace('United States of America', 'United States')

    location.dropna(axis=1)
    #location[location['country'] == 'US']['country'] == 'United States'
    location['country'] = location['country'].replace('US', 'United States')
    #location[location['country'] == 'Korea, South']['country'] == 'South Korea'
    location['country'] = location['country'].replace('Korea, South', 'South Korea')
    location = location.sort_values('country')

    print('\ndatasets imported')
    print('location: {0} rows'.format(len(location)))
    print('train: {0} rows'.format(len(train)))
    print('test: {0} rows\n'.format(len(test)))


    # ======================
    # First, you have to visualize the data. 
    # Create a bar plot of data availability based on continents. 
    # Are there any anomalies? How do they compare to the continents’ overall populations? 
    # Use a color spectrum for different proportions; for example, the bars for the continents with a higher data availability should be redder and bluer otherwise. 
    # Create a colored heatmap of the world, concerning the percentage of available data on the countries' populations.
    # Note that you have to use both the location and cases csv files and combine them. Report all the plots and your interpretation of them.

    # ======================PART 1: BARPLOT======================

    world_loc = world.merge(location, how='right', left_on='country', right_on='country')
    world_loc_confirmed = world_loc.groupby('country')['Confirmed'].sum().reset_index()
    print(world_loc_confirmed.columns)
    print(world_loc_confirmed.head(10))

    world_loc_population = world_loc.groupby('country')['population'].max().reset_index()
    world_loc_population = world_loc_population.dropna(axis = 0)
    print(world_loc_population.columns)
    print(world_loc_population.head(10))

    world_loc_confirmed = world_loc_confirmed.merge(world_loc_population, on = ['country'])
    world_loc_confirmed = world_loc_confirmed.merge(continent_map, on = ['country'])

    print(world_loc_confirmed.columns)
    print(world_loc_confirmed.head(10))

    world_loc_confirmed['res'] = (world_loc_confirmed['Confirmed']/world_loc_confirmed['population']*100)

    print(world_loc_confirmed.columns)
    print(world_loc_confirmed.head(10))

    cmap = plt.get_cmap('bwr')
    plt.bar(world_loc_confirmed['continent'], world_loc_confirmed['res'], color = cmap(world_loc_confirmed['res']/max(world_loc_confirmed['res'])))
    plt.show()
    plt.bar(world_loc_confirmed['continent'], world_loc_confirmed['population'])
    plt.show()

    # ======================PART 2: WORLD MAP=====================

    fig, ax = plt.subplots(figsize=(10, 10))
    world_loc = world_loc.merge(world_loc_confirmed, on = 'country')
    world_loc.plot(column = 'res', cmap='YlGnBu', kind = 'geo', ax=ax, legend = True)
    plt.show()

    return



    world_loc_confirmed = world_loc_confirmed.merge(world_loc, on = ['country'])
    world_loc_confirmed['res'] = (world_loc_confirmed['Confirmed']/world_loc_confirmed['population']*100)
    print(world_loc_confirmed.columns)
    print(world_loc_confirmed.head(10))
    world_loc_confirmed = world_loc_confirmed.merge(continent_map, how='left',on='country')
    print(world_loc_confirmed.columns)
    print(world_loc_confirmed.head(10))

    world_loc_confirmed['res'].replace(np.inf, np.nan, inplace=True)
    world_loc_confirmed.dropna(subset=['res'], inplace=True)

    world_loc_counts = world_loc_confirmed.groupby('continent')['res'].sum().reset_index()
    world_loc_pop = world_loc_confirmed.groupby('continent')['population'].sum().reset_index()
    world_loc_counts = world_loc_counts.merge(world_loc_pop, on = ['continent'])
    print(world_loc_counts.head(10))

    cmap = plt.get_cmap('bwr')
    plt.bar(world_loc_counts['continent'], world_loc_counts['res'], color = cmap(world_loc_counts['res'] / max(world_loc_counts['res'])))
    plt.show()
    plt.bar(world_loc_counts['continent'], world_loc_counts['population'])
    plt.show()

    return


    world_loc_counts = world_loc.groupby('continent')['res'].sum().reset_index()
    #world_loc_counts.reset_index(inplace=True)
    print(world_loc_counts.columns)
    world_loc_pop = world_loc.groupby('continent')['population'].sum().reset_index()
    world_loc_counts = world_loc_counts.merge(world_loc_pop, on = ['continent'])
    print(world_loc_counts.columns)
    #world_loc_counts.columns = ['continent', 'size', 'population']
    print(world_loc_counts.head(7))


    fig, ax = plt.subplots(figsize=(10, 8))
    world_loc.plot(column = 'res', cmap='YlGnBu', kind = 'geo', ax=ax, legend = True)
    plt.show()
    return



    # ===================== DATA PREPROCESSING ====================
    # Handle the missing values. 
    # Join both location and case data on both country and province together as a primary key and add an ‘Expected_Mortality_Rate’ to the cases dataset. 
    # Find out what is the best strategy for dealing with missing values and mention and explain your choice in the report.
    
    location.dropna(axis=1)
    train.dropna(axis=1)
    # Join both location and case data on both country and province together as a primary key
    agg = train.merge(location, on=['country','province'], how = 'left')
    # agg = pd.concat([train,location]).reset_index(drop=True)
    # Handle the missing values. 
    agg.dropna(axis=1)
    agg[agg['country'] == 'US']['country'] == 'United States'
    agg[agg['country'] == 'Korea, South']['country'] == 'South Korea'
    agg = agg.sort_values('country')



    agg['Expected_Mortality_Rate'] = (agg['Confirmed']/world[world['country'] == agg['country']]['population'])
    agg = agg.merge(continent_map, how='left',on='country')
    print(agg.columns)
    print(agg.head(10))
    return
    


    # ======================
    # First, you have to visualize the data. 
    # Create a bar plot of data availability based on continents. 
    # Are there any anomalies? How do they compare to the continents’ overall populations? 
    # Use a color spectrum for different proportions; for example, the bars for the continents with a higher data availability should be redder and bluer otherwise. 
    # Create a colored heatmap of the world, concerning the percentage of available data on the countries' populations. An example of this is life expectancy based on countries. 
    # Note that you have to use both the location and cases csv files and combine them. Report all the plots and your interpretation of them.

    # ======================PART 1: BARPLOT======================

    #colourcode 
    # confirmed cases/population
    #scrap cases

    agg_counts = pd.DataFrame(agg.groupby(['continent']).size())
    agg_counts.reset_index(inplace=True)
    print(agg_counts.columns)
    agg_counts.columns = ['continent', 'size']
    colours = plt.cm.RdBu(np.linspace(0,1,len(agg_counts['continent'])))
    plt.bar(agg_counts['continent'],agg_counts['size'], color = colours)
    plt.show()
    return
    ### how well countries represented, plot ratio #cases in country/population
    # cases can be seen as subset of location, we can omit combining for 

    # ======================PART 2: WORLD MAP=====================

    ### plot availability of data/population

    

    # Merge data with world geometries based on geometry
    world = world.merge(agg, how='left', left_on='country', right_on='country')
    print(world.columns)
    world['res'] = (world['Confirmed']/world['population'])
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