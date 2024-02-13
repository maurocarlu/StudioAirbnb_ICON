import os
import pandas as pd
import numpy as np
from datetime import datetime

class AirbnbDatasetPreprocessing:
    def __init__(self, original_file_path, output_directory):
        self.original_file_path = original_file_path
        self.output_directory = output_directory
        self.data = None

    def load_data(self):
        # Carico il file CSV in un DataFrame pandas
        try:
            self.data = pd.read_csv(self.original_file_path, low_memory=False)
            print("Caricamento dati completato.")
        except FileNotFoundError:
            print(f"Errore: File non trovato - {self.original_file_path}")
        except Exception as e:
            print(f"Errore durante il caricamento dei dati: {str(e)}")

    def clean_data(self):
        if self.data is not None:
            # Rimuovo colonne non necessarie
            columns_to_drop = ['country', 'NAME', 'country code', 'license',
                               'host name', 'house_rules']

            self.data = self.data.drop(columns=columns_to_drop)
            self.data.drop_duplicates(inplace=True)

            # Rimuovo simbolo "$" e converto la colonna 'price' in numerica
            self.data['price'] = self.data['price'].replace('[\$,]', '', regex=True)
            self.data['price'] = pd.to_numeric(self.data['price'], errors='coerce')
            # Rimuovo simbolo "$" e converto la colonna 'service fee' in numerica
            self.data['service fee'] = self.data['service fee'].replace('[\$,]', '', regex=True)
            self.data['service fee'] = pd.to_numeric(self.data['service fee'], errors='coerce')

            # Sostituisco i valori non numerici con la media della colonna 'price'
            self.data['price'].fillna(self.data['price'].mean(), inplace=True)
            # Sostituisco i valori non numerici con la media della colonna 'service fee'
            self.data['service fee'].fillna(self.data['service fee'].mean(), inplace=True)

            # Converto la colonna 'construction year' in tipo int
            self.data['Construction year'] = self.data['Construction year'].astype('Int64')
            # Converto la colonna 'minimum nights' in tipo int
            self.data['minimum nights'] = self.data['minimum nights'].astype('Int64')

            # Converto last review da object a data
            self.data['last review'] = pd.to_datetime(self.data['last review'])
            mean_date = self.data['last review'].mean().date()
            self.data['last review'] = self.data['last review'].astype('datetime64[ns]')
            self.data['last review'].fillna(pd.to_datetime(mean_date),inplace=True)

            # Converto room type da object a string
            self.data['room type'] = self.data['room type'].astype(str)

            # Se la colonna è minore di 0 la pongo a positivo e se è maggiore di 365 la pongo a 365
            self.data['availability 365'] = np.where(self.data['availability 365'] < 0, self.data['availability 365'] * -1,self.data['availability 365'])
            self.data['availability 365'] = np.where(self.data['availability 365'] > 365, 365, self.data['availability 365'])

            # Se la colonna è minore di 0 la pongo a positivo e se è maggiore di 365 la pongo a 365 e se è NaN la pongo a 1
            self.data['minimum nights'] = self.data['minimum nights'].mask(self.data['minimum nights'] < 0,self.data['minimum nights'] * -1)
            self.data['minimum nights'] = self.data['minimum nights'].mask(self.data['minimum nights'] > 365, 365)
            self.data['minimum nights'].fillna(1, inplace=True)

            # Correggo l'outlier della colonna 'neighbourhood group'
            self.data['neighbourhood group'] = self.data['neighbourhood group'].replace('brookln', 'Brooklyn')

            # Mi occupo della gestione delle colonne con valori null
            self.data['host_identity_verified'] = self.data['host_identity_verified'].fillna('unconfirmed')
            self.data['calculated host listings count'] = self.data.groupby('host id')['calculated host listings count'].transform(lambda x: x.fillna(x.count()))

            # Droppo le righe che hanno le seguenti colonne null, in quanto la moda non è affidabile in questo caso
            self.data = self.data.dropna(subset=['neighbourhood group', 'neighbourhood'])
            self.data = self.data.dropna(subset=['lat', 'long'])
            self.data = self.data.dropna(subset=['instant_bookable'])

            # Sostituisco i valori null di 'cancellation_policy' con la moda
            modal_value = self.data['cancellation_policy'].mode()[0]
            self.data['cancellation_policy'].fillna(modal_value, inplace=True)

            # Sostituisco i valori null di 'Construction year' con la media del quartiere corrispondente
            construction_year_mean = self.data.groupby('neighbourhood group')['Construction year'].mean()
            self.data['Construction year'] = self.data.apply(lambda row: construction_year_mean[row['neighbourhood group']]
            if pd.isnull(row['Construction year'])
            else row['Construction year'], axis=1)
            self.data['Construction year'] = self.data['Construction year'].astype(int)

            self.data['number of reviews'].fillna(self.data['number of reviews'].median(), inplace=True)
            self.data['reviews per month'].fillna(self.data['reviews per month'].median(), inplace=True)
            self.data['availability 365'].fillna(self.data['availability 365'].median(), inplace=True)
            self.data['review rate number'].fillna(self.data['review rate number'].mean(), inplace=True)

            # Per evitare inconsistenza, se la cella number of reviews è 0, pongo anche reviews per month a 0
            self.data.loc[self.data['number of reviews'] == 0, 'reviews per month'] = 0

            # Correggo le date impostate a giorni nel futuro
            today = datetime.now().date()
            self.data['last review'] = self.data['last review'].apply(lambda x: today if pd.notna(x) and x.date() > today else x)
            self.data['last review'] = pd.to_datetime(self.data['last review'])
            mean_date = self.data['last review'].mean().date()
            self.data['last review'].fillna(mean_date, inplace=True)
            self.data['last review'] = pd.to_datetime(self.data['last review'])

            print("Dati puliti.")

    def save_processed_data(self):
        # Verifica se la directory di output esiste, altrimenti creala
        output_path = os.path.join(self.output_directory, 'Post_PreProcessing')
        os.makedirs(output_path, exist_ok=True)

        # Salva il DataFrame processato in un nuovo file CSV
        if self.data is not None:
            try:
                output_file_path = os.path.join(output_path, 'file_preprocessato.csv')
                self.data.to_csv(output_file_path, index=False)
                print(f"Dati processati salvati in {output_file_path}.")
            except Exception as e:
                print(f"Errore durante il salvataggio dei dati processati: {str(e)}")



original_file_path = '../dataset/Originali/Airbnb_Open_Data.csv'
output_directory = '../dataset'
preprocessor = AirbnbDatasetPreprocessing(original_file_path, output_directory)
preprocessor.load_data()
preprocessor.clean_data()
preprocessor.save_processed_data()

