import pandas as pd
import numpy as np
import pickle
import yaml
import os
from pathlib import Path

# Project root
root_path = Path(__file__).resolve().parent.parent

# Load config
config_path = root_path / "app" / "app_config.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Resolve all paths
data_path = root_path / config['data']
model_path = root_path / config['model']
column_enc_path = root_path / config['column_enc']


class Extract:
    def __init__(self):
        self.df = pd.read_excel(data_path)

    def extract_make(self):
        return self.df['MAKE'].unique()

    def extract_model(self, make):
        return self.df[self.df['MAKE'] == make]['MODEL'].unique()

    def extract_transmission(self, model):
        return self.df[self.df['MODEL'] == model]['TRANSMISSION'].unique()

    def extract_fuel(self, model, transmission):
        return self.df[
            (self.df['MODEL'] == model) &
            (self.df['TRANSMISSION'] == transmission)
        ]['FUEL'].unique()

    def extract_engine_cylinder(self, make, transmission):
        df_filtered = self.df[
            (self.df['MAKE'] == make) &
            (self.df['TRANSMISSION'] == transmission)
        ]
        return (
            df_filtered['ENGINE SIZE'].unique(),
            df_filtered['CYLINDERS'].unique()
        )


class Prediction(Extract):
    def __init__(self):
        super().__init__()
        self.model = pickle.load(open(model_path, 'rb'))

    def column_config_loader(self):
        all_column_configs = {}

        file_list = os.listdir(column_enc_path)
        keys = [i.split('_')[0] for i in file_list]

        for key, file in zip(keys, file_list):
            with open(column_enc_path / file, "r") as f:
                all_column_configs[key] = yaml.safe_load(f)

        return all_column_configs

    def encode_model(self, col, x):
        all_column_configs = self.column_config_loader()

        if x in all_column_configs[col.lower()]:
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

        # Encode categorical columns
        cat_col = ['TRANSMISSION', 'FUEL', 'MAKE', 'MODEL']
        for col in cat_col:
            user_df[col] = user_df[col].apply(lambda x: self.encode_model(col, x))

        result = round(self.model.predict(user_df)[0], 0)
        return result


if __name__ == "__main__":
    extract = Prediction()
    print(
        extract.predict(
            engine_size=1.5,
            cylinders_no=4,
            fuel_consumption=10.5,
            make='ACURA',
            transmission='A4',
            fuel='X',
            model='3.2TL'
        )
    )