import pandas as pd
import numpy as np
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

def main():
    location = pd.read_csv('data/location.csv', usecols=['Country_Region','Lat','Long_']) \
        .rename(columns=({'Country_Region': 'country','Lat': 'latitude','Long_': 'longitude'}))
    train = pd.read_csv('data/cases_train.csv', usecols=['country','latitude','longitude'])
    test = pd.read_csv('data/cases_test.csv', usecols=['country','latitude','longitude'])
    
    continent_map = pd.read_csv('data/countries_continent.csv')
    populations = pd.read_csv('data/population.csv')

    print('\ndatasets imported')
    print('location: {0} rows'.format(len(location)))
    print('train: {0} rows'.format(len(train)))
    print('test: {0} rows\n'.format(len(test)))
    
    agg = pd.concat([location,train,test]).reset_index(drop=True)
    agg[agg['country'] == 'US']['country'] == 'United States'
    agg[agg['country'] == 'Korea, South']['country'] == 'South Korea'
    agg = agg.sort_values('country')
    agg = pd.merge(agg, continent_map, how='left',on='country')

    #  = case_data.merge(location, on=['country','province'], suffixes=('_l','_r')) \
        # .dropna(axis=1)

    # ======================PART 1: BARPLOT======================

    agg_counts = pd.DataFrame(agg.groupby(['continent']).size())
    agg_counts.reset_index(inplace=True)
    agg_counts.columns = ['continent', 'size']
    agg_counts.merge(populations, on='continent')
    print(agg_counts)
    # print(agg_counts)
    # plt.bar(agg_counts['continent'],agg_counts['size'])
    # plt.show()
    return

    # ======================PART 2: WORLD MAP======================

    world = gpd.read_file('data/ne_110m_land/ne_110m_land.shp')
    print(world.columns)

    # Merge data with world geometries based on continent
    world = world.merge(agg_counts, how='left', left_on='continent', right_on='continent')

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(world.pivot_table(index='continent', columns='count'), cmap='YlGnBu', ax=ax, annot=True, fmt=".0f", cbar_kws={'label': 'Value'})
    ax.set_title('Continental Heatmap')
    plt.show()



if __name__ == '__main__':
    main()