import pickle
import pandas as pd
import numpy as np

def test(x1, x2, x3, x4):

    model = pickle.load(open('flask-server\model.pickle','rb'))
    dataset = pd.read_csv('flask-server\Bengaluru_House_Data.csv')

    dataset.drop(['area_type','society','availability','balcony'], axis='columns', inplace=True)


    dataset.dropna(inplace=True)


    dataset['bhk'] = dataset['size'].apply(lambda x: float(x.split(' ')[0]))

    def is_float(x):
        try:
            float(x)
        except :
            return False
        return True


    def convert_sqft_to_num(x):
        tokens = x.split('-')
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1]))/2
        try:
            return float(x)
        except:
            return None

    dataset['total_sqft'] = dataset['total_sqft'].apply(convert_sqft_to_num)

    dataset['price_per_sqft'] = dataset['price']*100000/dataset['total_sqft']



    dataset['location'] = dataset['location'].apply(lambda x: x.strip())

    location_stats = dataset.groupby('location')['location'].agg('count').sort_values(ascending=False)

    location_stats_less_than_10 = location_stats[location_stats <= 10]

    dataset['location'] = dataset['location'].apply(lambda x: 'other' if x in location_stats_less_than_10 else x)

    dataset = dataset[~(dataset['total_sqft'] / dataset['bhk'] < 300)]

    def remove_pps_outliers(df):
        df_out = pd.DataFrame()
        for key, subdf in df.groupby('location'):
            mean = np.mean(subdf['price_per_sqft'])
            std = np.std(subdf['price_per_sqft'])
            reduced_df = subdf[(subdf['price_per_sqft'] > (mean - std)) & (subdf['price_per_sqft'] <= (mean + std))]
            df_out = pd.concat([df_out, reduced_df], ignore_index=True)
        return df_out

    dataset = remove_pps_outliers(dataset)

    def remove_bhk_outliers(df):
        exclude_indices = np.array([])
        for location, location_df in df.groupby('location'):
            bhk_stats = {}
            for bhk, bhk_df in location_df.groupby('bhk'):
                bhk_stats[bhk] = {
                        'mean': np.mean(bhk_df['price_per_sqft']),
                        'std': np.std(bhk_df['price_per_sqft']),
                        'count': bhk_df.shape[0]
                    }
            for bhk, bhk_df in location_df.groupby('bhk'):
                stats = bhk_stats.get(bhk-1)
                if stats and stats['count'] > 5:
                    exclude_indices = np.append(exclude_indices, bhk_df[bhk_df['price_per_sqft'] < (stats['mean'])].index.values)
        return df.drop(exclude_indices, axis='index')
            
    dataset = remove_bhk_outliers(dataset)

    dataset = dataset[dataset['bath'] < dataset['bhk'] + 2]


    ### after removing outliers, dropping unwanted features
    dataset.drop(['size','price_per_sqft'], axis='columns', inplace=True)


    ## one hot encoding the 'location' column
    dummies = pd.get_dummies(dataset['location'])


    dataset = pd.concat([dataset,dummies.drop('other', axis='columns')], axis='columns')
    dataset.drop('location', axis=1, inplace=True)


    X = dataset.drop(['price'],axis= 'columns')


    ## evaluating the model
    def predict_price(location,sqft,bath,bhk):
        loc_index = np.where(X.columns == location)[0][0]
        
        x = np.zeros(len(X.columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk 
        if loc_index >= 0:
            x[loc_index] = 1
        return model.predict([x])[0]

    print(x1)
    print(x2)
    print(x3)
    print(x4)
    
    res = predict_price(x1,x2,x3,x4)
    res = round(res/100, 2)
    
    return res

