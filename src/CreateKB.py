import csv
from pyswip import Prolog
import pandas as pd

def clean_string(s):
    return s.replace("'", "").encode('ascii', 'ignore').decode()

class CreateKB:
    def createKnowledgeBase(self):
        prolog = Prolog()
        # Leggi il file CSV
        df = pd.read_csv('../dataset/Post_PreProcessing/file_preprocessato.csv')

        columns_to_drop = ['reviews per month','neighbourhood group','room type','availability 365','host id','host_identity_verified','lat','long','instant_bookable','last review','calculated host listings count','service fee']
        df = df.drop(columns=columns_to_drop)

        columns_to_string = ['neighbourhood']
        df[columns_to_string] = df[columns_to_string].apply(lambda x: x.apply(clean_string))
        df['neighbourhood'] = df['neighbourhood'].replace("Hell's Kitchen", "Hells Kitchen")
        df['neighbourhood'] = df['neighbourhood'].replace("Bull's Head", "Bulls Head")
        df['neighbourhood'] = df['neighbourhood'].replace("Prince's Bay", "Princes Bay")

        # Crea un file Prolog con tutti i fatti
        with open('KB.pl', 'w') as f:
            for index, row in df.iterrows():
                f.write(f"neighbourhood({row['id']}, '{row['neighbourhood']}').\n")
            for index, row in df.iterrows():
                f.write(f"price({row['id']}, {row['price']}).\n")
            for index, row in df.iterrows():
                f.write(f"minimum_nights({row['id']}, {row['minimum nights']}).\n")
            for index, row in df.iterrows():
                f.write(f"number_of_reviews({row['id']}, {row['number of reviews']}).\n")
            for index, row in df.iterrows():
                f.write(f"review_rate_number({row['id']}, {row['review rate number']}).\n")
            for index, row in df.iterrows():
                f.write(f"cancellation_policy({row['id']}, '{row['cancellation_policy']}').\n")

            quartieri_centrali = ["Kensington", "Midtown", "Harlem", "Murray Hill", "Hells Kitchen",
                         "Upper West Side", "Chinatown", "West Village", "Chelsea", "SoHo",
                         "East Village", "Lower East Side", "Kips Bay", "Greenwich Village",
                         "Little Italy", "Tribeca", "Financial District", "Flatiron District"]

            for quartiere in quartieri_centrali:
                f.write(f"posizione_centrale('{quartiere}').\n")

            quartieri = ["Clinton Hill", "East Harlem", "Bedford-Stuyvesant", "Upper East Side",
                         "South Slope", "Bushwick", "Flatbush", "Fort Greene",
                         "Prospect-Lefferts Gardens", "Long Island City", "Williamsburg",
                         "Greenpoint", "Park Slope", "Brooklyn Heights", "Gowanus",
                         "Washington Heights", "Flatlands", "Cobble Hill", "Flushing", "DUMBO"]

            for quartiere in quartieri:
                f.write(f"quartieri_periferici('{quartiere}').\n")

            f.write(f"cancellazione_stretta('strict').\n")
            f.write(f"cancellazione_media('moderate').\n")
            f.write(f"cancellazione_flessibile('flexible').\n")

            # REGOLE

            # Regole che prendono in considerazione solo il PREZZO
            f.write("prezzo_economico(ID) :- price(ID, Price), Price < 100.\n")
            f.write("prezzo_medio(ID) :- price(ID, Price), Price >= 100, Price =< 600.\n")
            f.write("prezzo_costoso(ID) :- price(ID, Price), Price > 600.\n")

            # Regole che prendono in considerazione solo il REVIEW RATE
            f.write("ottima_recensione(ID) :- review_rate_number(ID, Voto), Voto >= 4.\n")

            # Regole che prendono in considerazione PREZZO E REVIEW RATE
            f.write("economico_e_ben_recensito(ID) :- prezzo_economico(ID), ottima_recensione(ID).\n")
            f.write("economico_e_mal_recensito(ID) :- prezzo_economico(ID), not(ottima_recensione(ID)).\n")
            f.write("medio_e_ben_recensito(ID) :- prezzo_medio(ID), ottima_recensione(ID).\n")
            f.write("medio_e_mal_recensito(ID) :- prezzo_medio(ID), not(ottima_recensione(ID)).\n")
            f.write("costoso_e_ben_recensito(ID) :- prezzo_costoso(ID) , ottima_recensione(ID).\n")
            f.write("costoso_e_mal_recensito(ID) :- prezzo_costoso(ID) , not(ottima_recensione(ID)).\n")

            # Regole che prendono in considerazione PREZZO, REVIEW RATE E POSIZIONE
            f.write("economico_ben_recensito_centrale(ID) :- economico_e_ben_recensito(ID), neighbourhood(ID, Quartiere), posizione_centrale(Quartiere).\n")
            f.write("economico_ben_recensito_periferico(ID) :- economico_e_ben_recensito(ID), neighbourhood(ID, Quartiere), quartieri_periferici(Quartiere).\n")
            f.write("economico_mal_recensito_centrale(ID) :- economico_e_mal_recensito(ID), neighbourhood(ID, Quartiere), posizione_centrale(Quartiere).\n")
            f.write("economico_mal_recensito_periferico(ID) :- economico_e_mal_recensito(ID), neighbourhood(ID, Quartiere), quartieri_periferici(Quartiere).\n")

            f.write("costoso_ben_recensito_centrale(ID) :- costoso_e_ben_recensito(ID), neighbourhood(ID, Quartiere), posizione_centrale(Quartiere).\n")
            f.write("costoso_mal_recensito_periferico(ID) :- costoso_e_mal_recensito(ID), neighbourhood(ID, Quartiere), quartieri_periferici(Quartiere).\n")
            f.write("costoso_ben_recensito_periferico(ID) :- costoso_e_ben_recensito(ID), neighbourhood(ID, Quartiere), quartieri_periferici(Quartiere).\n")
            f.write("costoso_mal_recensito_centrale(ID) :- costoso_e_mal_recensito(ID), neighbourhood(ID, Quartiere), posizione_centrale(Quartiere).\n")

            f.write("medio_ben_recensito_centrale(ID) :- medio_e_ben_recensito(ID), neighbourhood(ID, Quartiere), posizione_centrale(Quartiere).\n")
            f.write("medio_mal_recensito_periferico(ID) :- medio_e_mal_recensito(ID), neighbourhood(ID, Quartiere), quartieri_periferici(Quartiere).\n")
            f.write("medio_mal_recensito_centrale(ID) :- medio_e_mal_recensito(ID), neighbourhood(ID, Quartiere), posizione_centrale(Quartiere).\n")
            f.write("medio_ben_recensito_periferico(ID) :- medio_e_ben_recensito(ID), neighbourhood(ID, Quartiere), quartieri_periferici(Quartiere).\n")

            # Regole che prendono in considerazione PREZZO, REVIEW RATE, POSIZIONE E POLITICA DI CANCELLAZIONE
            f.write("economico_ben_recensito_centrale_stretto(ID) :- economico_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("economico_ben_recensito_centrale_media(ID) :- economico_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("economico_ben_recensito_centrale_flessibile(ID) :- economico_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("economico_ben_recensito_periferico_stretto(ID) :- economico_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("economico_ben_recensito_periferico_media(ID) :- economico_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("economico_ben_recensito_periferico_flessibile(ID) :- economico_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("economico_mal_recensito_centrale_stretto(ID) :- economico_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("economico_mal_recensito_centrale_media(ID) :- economico_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("economico_mal_recensito_centrale_flessibile(ID) :- economico_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("economico_mal_recensito_periferico_stretto(ID) :- economico_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("economico_mal_recensito_periferico_media(ID) :- economico_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("economico_mal_recensito_periferico_flessibile(ID) :- economico_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("costoso_ben_recensito_centrale_stretto(ID) :- costoso_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("costoso_ben_recensito_centrale_media(ID) :- costoso_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("costoso_ben_recensito_centrale_flessibile(ID) :- costoso_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("costoso_ben_recensito_periferico_stretto(ID) :- costoso_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("costoso_ben_recensito_periferico_media(ID) :- costoso_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("costoso_ben_recensito_periferico_flessibile(ID) :- costoso_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("costoso_mal_recensito_centrale_stretto(ID) :- costoso_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("costoso_mal_recensito_centrale_media(ID) :- costoso_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("costoso_mal_recensito_centrale_flessibile(ID) :- costoso_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("costoso_mal_recensito_periferico_stretto(ID) :- costoso_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("costoso_mal_recensito_periferico_media(ID) :- costoso_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("costoso_mal_recensito_periferico_flessibile(ID) :- costoso_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("medio_ben_recensito_centrale_stretto(ID) :- medio_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("medio_ben_recensito_centrale_media(ID) :- medio_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("medio_ben_recensito_centrale_flessibile(ID) :- medio_ben_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("medio_ben_recensito_periferico_stretto(ID) :- medio_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("medio_ben_recensito_periferico_media(ID) :- medio_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("medio_ben_recensito_periferico_flessibile(ID) :- medio_ben_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("medio_mal_recensito_centrale_stretto(ID) :- medio_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("medio_mal_recensito_centrale_media(ID) :- medio_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("medio_mal_recensito_centrale_flessibile(ID) :- medio_mal_recensito_centrale(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            f.write("medio_mal_recensito_periferico_stretto(ID) :- medio_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_stretta(Politica).\n")
            f.write("medio_mal_recensito_periferico_media(ID) :- medio_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_media(Politica).\n")
            f.write("medio_mal_recensito_periferico_flessibile(ID) :- medio_mal_recensito_periferico(ID), cancellation_policy(ID, Politica), cancellazione_flessibile(Politica).\n")

            #Regole finali che prendono in considerazione: PREZZO - POSIZIONE - REVIEW RATE - CANCELLAZIONE - MINIMUM NIGHTS
            f.write("economico_ben_recensito_centrale_stretto_notti(ID, Notti) :- economico_ben_recensito_centrale_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_ben_recensito_centrale_media_notti(ID, Notti) :- economico_ben_recensito_centrale_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_ben_recensito_centrale_flessibile_notti(ID, Notti) :- economico_ben_recensito_centrale_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("economico_ben_recensito_periferico_stretto_notti(ID, Notti) :- economico_ben_recensito_periferico_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_ben_recensito_periferico_media_notti(ID, Notti) :- economico_ben_recensito_periferico_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_ben_recensito_periferico_flessibile_notti(ID, Notti) :- economico_ben_recensito_periferico_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("economico_mal_recensito_periferico_stretto_notti(ID, Notti) :- economico_mal_recensito_periferico_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_mal_recensito_periferico_media_notti(ID, Notti) :- economico_mal_recensito_periferico_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_mal_recensito_periferico_flessibile_notti(ID, Notti) :- economico_mal_recensito_periferico_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("economico_mal_recensito_centrale_stretto_notti(ID, Notti) :- economico_mal_recensito_centrale_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_mal_recensito_centrale_media_notti(ID, Notti) :- economico_mal_recensito_centrale_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("economico_mal_recensito_centrale_flessibile_notti(ID, Notti) :- economico_mal_recensito_centrale_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("costoso_ben_recensito_centrale_stretto_notti(ID, Notti) :- costoso_ben_recensito_centrale_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_ben_recensito_centrale_media_notti(ID, Notti) :- costoso_ben_recensito_centrale_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_ben_recensito_centrale_flessibile_notti(ID, Notti) :- costoso_ben_recensito_centrale_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("costoso_ben_recensito_periferico_stretto_notti(ID, Notti) :- costoso_ben_recensito_periferico_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_ben_recensito_periferico_media_notti(ID, Notti) :- costoso_ben_recensito_periferico_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_ben_recensito_periferico_flessibile_notti(ID, Notti) :- costoso_ben_recensito_periferico_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("costoso_mal_recensito_periferico_stretto_notti(ID, Notti) :- costoso_mal_recensito_periferico_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_mal_recensito_periferico_media_notti(ID, Notti) :- costoso_mal_recensito_periferico_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_mal_recensito_periferico_flessibile_notti(ID, Notti) :- costoso_mal_recensito_periferico_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("costoso_mal_recensito_centrale_stretto_notti(ID, Notti) :- costoso_mal_recensito_centrale_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_mal_recensito_centrale_media_notti(ID, Notti) :- costoso_mal_recensito_centrale_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("costoso_mal_recensito_centrale_flessibile_notti(ID, Notti) :- costoso_mal_recensito_centrale_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("medio_ben_recensito_centrale_stretto_notti(ID, Notti) :- medio_ben_recensito_centrale_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_ben_recensito_centrale_media_notti(ID, Notti) :- medio_ben_recensito_centrale_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_ben_recensito_centrale_flessibile_notti(ID, Notti) :- medio_ben_recensito_centrale_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("medio_ben_recensito_periferico_stretto_notti(ID, Notti) :- medio_ben_recensito_periferico_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_ben_recensito_periferico_media_notti(ID, Notti) :- medio_ben_recensito_periferico_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_ben_recensito_periferico_flessibile_notti(ID, Notti) :- medio_ben_recensito_periferico_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("medio_mal_recensito_periferico_stretto_notti(ID, Notti) :- medio_mal_recensito_periferico_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_mal_recensito_periferico_media_notti(ID, Notti) :- medio_mal_recensito_periferico_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_mal_recensito_periferico_flessibile_notti(ID, Notti) :- medio_mal_recensito_periferico_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

            f.write("medio_mal_recensito_centrale_stretto_notti(ID, Notti) :- medio_mal_recensito_centrale_stretto(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_mal_recensito_centrale_media_notti(ID, Notti) :- medio_mal_recensito_centrale_media(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")
            f.write("medio_mal_recensito_centrale_flessibile_notti(ID, Notti) :- medio_mal_recensito_centrale_flessibile(ID), minimum_nights(ID, MinNotti), MinNotti =< Notti.\n")

# Crea un'istanza della classe KnowledgeBase e chiama il metodo createKnowledgeBase
kb = CreateKB()
kb.createKnowledgeBase()