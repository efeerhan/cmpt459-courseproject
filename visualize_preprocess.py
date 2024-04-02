import pandas as pd
import numpy as np
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    # location = pd.read_csv('data/location.csv', usecols=['Country_Region','Lat','Long_']) \
    #     .rename(columns=({'Country_Region': 'country','Lat': 'latitude','Long_': 'longitude'}))
    # train = pd.read_csv('data/cases_train.csv', usecols=['country','latitude','longitude'])
    # test = pd.read_csv('data/cases_test.csv', usecols=['country','latitude','longitude'])

    location = pd.read_csv('data/location.csv') \
        .rename(columns=({'Country_Region': 'country','Lat': 'latitude','Long_': 'longitude'}))
    train = pd.read_csv('data/cases_train.csv')
    test = pd.read_csv('data/cases_test.csv')
    
    continent_map = pd.read_csv('data/countries_continent.csv')

    print('\ndatasets imported')
    print('location: {0} rows'.format(len(location)))
    print('train: {0} rows'.format(len(train)))
    print('test: {0} rows\n'.format(len(test)))
    
    agg = pd.concat([location,train,test]).reset_index(drop=True)
    agg[agg['country'] == 'US']['country'] == 'United States'
    agg[agg['country'] == 'Korea, South']['country'] == 'South Korea'
    agg = agg.sort_values('country')
    agg = pd.merge(agg, continent_map, how='left',on='country')
    print(agg.columns)


    # ===================== DATA PREPROCESSING ====================

    # data_merge = train.merge(location, on=['country','province'], suffixes=('_l','_r'))
    # data_merge.dropna(axis=1)

    # ======================PART 1: BARPLOT======================

    agg_counts = pd.DataFrame(agg.groupby(['continent']).size())
    agg_counts.reset_index(inplace=True)
    print(agg_counts.columns)
    agg_counts.columns = ['continent', 'size']
    colours = plt.cm.RdBu(np.linspace(0,1,len(agg_counts['size'])))
    plt.bar(agg_counts['continent'],agg_counts['size'], color = colours)
    plt.show()

    # ======================PART 2: WORLD MAP======================

    # source https://www.relataly.com/visualize-covid-19-data-on-a-geographic-heat-maps/291/

    ### debug for all cols in world
    # world_deb = gpd.read_file('data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')
    # pd.set_option('display.max_columns', None)
    # print(world_deb.head())

    world = gpd.read_file('data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')[['ADMIN', 'CONTINENT', 'POP_EST', 'geometry']]
    world.columns = ['country', 'continent', 'population', 'geometry']
    world[world['country'] == 'United States of America']['country'] == 'United States'
    #world.plot(figsize=(10, 6), edgecolor='white', linewidth=1, color='lightblue')

    ### plot availability of data/population

    #add column 'geometry'
    fig, ax = plt.subplots(figsize=(10, 8))
    agg_geo = gpd.GeoDataFrame(agg, geometry=gpd.points_from_xy(agg['longitude'], agg['latitude']))

    # Merge data with world geometries based on geometry
    world = world.merge(agg, how='left', left_on='country', right_on='country')
    print(world.columns)
    world['res'] = (world['Confirmed'] + world['Deaths'] + world['Active'] + world['Recovered'])/world['population']
    world.plot(column = 'res', cmap='YlGnBu', kind = 'geo', ax=ax, legend = True)
    plt.show()
    return

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    world_pivot = agg_geo.pivot_table('latitude','longitude', columns='continent')
    sns.heatmap(world_pivot, cmap='YlGnBu', ax=ax, annot=True, fmt=".0f", cbar_kws={'label': 'Value'})
    # sns.heatmap(world.pivot_table(index='continent', columns='count'), cmap='YlGnBu', ax=ax, annot=True, fmt=".0f", cbar_kws={'label': 'Value'})
    ax.set_title('Continental Heatmap')
    plt.show()



if __name__ == '__main__':
    main()