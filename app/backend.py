import pandas as pd
import numpy as np
import pickle
import yaml
import os

with open("app_config.yaml", "r") as f:
    config = yaml.safe_load(f)


class Extract:
    def __init__(self):
        self.df = pd.read_excel(config['data'])

    def extract_make(self):
        return self.df['MAKE'].unique()

    def extract_model(self, make):
         return self.df[self.df['MAKE']==make]['MODEL'].unique()
    
    def extract_transmission(self, model):
        return self.df[self.df['MODEL']==model]['TRANSMISSION'].unique()

    def extract_fuel(self, model, transmission):
        return self.df[(self.df['MODEL']==model) & (self.df['TRANSMISSION']==transmission)]['FUEL'].unique()
    
    def extract_engine_cylinder(self, make, transmission):
        return (self.df[(self.df['MAKE']==make) & (self.df['TRANSMISSION']==transmission)]['ENGINE SIZE'].unique(),
                self.df[(self.df['MAKE']==make) & (self.df['TRANSMISSION']==transmission)]['CYLINDERS'].unique())


class Prediction(Extract):
    def __init__(self):
        super().__init__()
        self.model = pickle.load(open(config['model'], 'rb'))

    def column_config_loader(self, path=config['column_enc'], file_list=os.listdir(config['column_enc'])):
        all_column_configs = {} # Initializing empty disctionary
        keys = [i.split('_')[0] for i in file_list]

        for key, file in zip(keys, file_list):
                with open(path+file, "r") as f:
                        all_column_configs[key] = yaml.safe_load(f)
        return all_column_configs
    
    def encode_model(self, col, x):
        all_column_configs = self.column_config_loader()
        if x in (all_column_configs[col.lower()].keys()):
            return all_column_configs[col.lower()][x]
        else:
            return all_column_configs['global']['global_mean']

    def predict(self, engine_size, cylinders_no, fuel_consumption, make, transmission, fuel, model):
        user_df = pd.DataFrame({
             'ENGINE SIZE': engine_size,
             'CYLINDERS': cylinders_no,
             'TRANSMISSION': transmission,
             'FUEL': fuel,
             'FUEL CONSUMPTION': fuel_consumption,
             'MAKE': make,
             'MODEL': model

        }, index=[0])
        print(user_df)
        # encoding categorical inputs
        cat_col = ['TRANSMISSION', 'FUEL', 'MAKE', 'MODEL']
        for col in cat_col:
             user_df[col] = user_df[col].apply(lambda x: self.encode_model(col, x))
        print(user_df)

        result = round(self.model.predict(user_df)[0], 0)
        print(result)

        return result



if __name__ == "__main__":
    extract = Prediction()
    extract.predict(engine_size=1.5, cylinders_no=4, fuel_consumption=10.5,
                    make='ACURA', transmission='A4', fuel='X', model='3.2TL')

# np.array('A4').reshape(1, -1)
# np.array('X').reshape(1, -1)