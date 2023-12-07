import os
import pandas as pd


class AirbnbDatasetPreprocessing:
    def __init__(self, original_file_path, output_directory):
        self.original_file_path = original_file_path
        self.output_directory = output_directory
        self.data = None

    def load_data(self):
        # Carica il file CSV in un DataFrame pandas
        try:
            self.data = pd.read_csv(self.original_file_path)
            print("Caricamento dati completato.")
        except FileNotFoundError:
            print(f"Errore: File non trovato - {self.original_file_path}")
        except Exception as e:
            print(f"Errore durante il caricamento dei dati: {str(e)}")

    def clean_data(self):
        # Esempio di operazioni di pre-processing: rimozione di colonne non necessarie e gestione di valori mancanti
        if self.data is not None:
            # Rimuovi colonne non necessarie
            columns_to_drop = ['country', 'NAME', 'country code', 'license',
                               'host name', 'house_rules']

            self.data = self.data.drop(columns=columns_to_drop)

            # Rimuovi simbolo "$" e converti la colonna 'price' in numerica
            self.data['price'] = self.data['price'].replace('[\$,]', '', regex=True)
            self.data['price'] = pd.to_numeric(self.data['price'], errors='coerce')
            # Rimuovi simbolo "$" e converti la colonna 'service fee' in numerica
            self.data['service fee'] = self.data['service fee'].replace('[\$,]', '', regex=True)
            self.data['service fee'] = pd.to_numeric(self.data['service fee'], errors='coerce')

            # Sostituisci i valori non numerici con la media della colonna 'price'
            self.data['price'].fillna(self.data['price'].mean(), inplace=True)
            # Sostituisci i valori non numerici con la media della colonna 'service fee'
            self.data['service fee'].fillna(self.data['service fee'].mean(), inplace=True)

            # Converti la colonna 'construction year' in tipo int
            self.data['Construction year'] = self.data['Construction year'].astype('Int64')
            # Converti la colonna 'minimum nights' in tipo int
            self.data['minimum nights'] = self.data['minimum nights'].astype('Int64')


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


# Esempio di utilizzo
original_file_path = '../dataset/Originali/Airbnb_Open_Data.csv'
output_directory = '../dataset'
preprocessor = AirbnbDatasetPreprocessing(original_file_path, output_directory)
preprocessor.load_data()
preprocessor.clean_data()
preprocessor.save_processed_data()

