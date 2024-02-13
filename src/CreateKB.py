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

        columns_to_drop = ['reviews per month','neighbourhood group','availability 365','host id','lat','long','instant_bookable','last review','calculated host listings count','service fee']
        df = df.drop(columns=columns_to_drop)

        columns_to_string = ['neighbourhood','host_identity_verified','room type']
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
            for index, row in df.iterrows():
                f.write(f"room_type({row['id']}, '{row['room type']}').\n")
            for index, row in df.iterrows():
                f.write(f"host_identity_verified({row['id']}, '{row['host_identity_verified']}').\n")


            quartieri_centrali = ["Kensington", "Midtown", "Harlem", "Murray Hill", "Hells Kitchen",
                         "Upper West Side", "Chinatown", "West Village", "Chelsea", "SoHo",
                         "East Village", "Lower East Side", "Kips Bay", "Greenwich Village",
                         "Little Italy", "Tribeca", "Financial District", "Flatiron District"]

            for quartiere in quartieri_centrali:
                f.write(f"posizione_centrale('{quartiere}').\n")

            quartieri_periferici = ["Clinton Hill", "East Harlem", "Bedford-Stuyvesant", "Upper East Side",
                         "South Slope", "Bushwick", "Flatbush", "Fort Greene",
                         "Prospect-Lefferts Gardens", "Long Island City", "Williamsburg",
                         "Greenpoint", "Park Slope", "Brooklyn Heights", "Gowanus",
                         "Washington Heights", "Flatlands", "Cobble Hill", "Flushing", "DUMBO"]

            for quartiere in quartieri_periferici:
                f.write(f"quartieri_periferici('{quartiere}').\n")

            f.write(f"cancellazione_stretta('strict').\n")
            f.write(f"cancellazione_media('moderate').\n")
            f.write(f"cancellazione_flessibile('flexible').\n")

            # REGOLE

            #TASK 1 Regole per la ricerca di tutti gli airbnb che corrispondono a determinate caratteristiche

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

            # TASK 2: Regole per trovare l'airbnb con score maggiore date le preferenze dell'utente

            f.write("""
            has_reviews(AirbnbId, ReviewScore) :-
                number_of_reviews(AirbnbId, NumberOfReviews),
                (   NumberOfReviews >= 0, NumberOfReviews =< 256 -> ReviewScore = 5;
                    NumberOfReviews > 256, NumberOfReviews =< 512 -> ReviewScore = 10;
                    NumberOfReviews > 512, NumberOfReviews =< 768 -> ReviewScore = 15;
                    NumberOfReviews > 768, NumberOfReviews =< 1024 -> ReviewScore = 20
                ).
            """)

            f.write("""
            user_pref_score(AirbnbId, PrefRoomType, PrefCancellationPolicy, PrefPriceMax, BonusScore) :-
                room_type(AirbnbId, RoomType),
                cancellation_policy(AirbnbId, CancellationPolicy),
                price(AirbnbId, Price),
                (RoomType == PrefRoomType -> ScoreRoomType is 15 ; ScoreRoomType is 0),
                (CancellationPolicy == PrefCancellationPolicy -> ScoreCancellationPolicy is 8 ; ScoreCancellationPolicy is 0),
                (Price =< PrefPriceMax -> ScorePrice is 5 ; ScorePrice is 0),
                BonusScore is ScoreRoomType + ScoreCancellationPolicy + ScorePrice.
            """)

            f.write("""
            price_index(AirbnbId, PriceIndex) :-
                price(AirbnbId, Price),
                (
                    (Price >= 50, Price =< 100 -> PriceIndex is 15);
                    (Price > 100, Price =< 300 -> PriceIndex is 10);
                    (Price > 300, Price =< 500 -> PriceIndex is 5);
                    (Price > 500, Price =< 700 -> PriceIndex is 3);
                    (Price > 700, Price =< 900 -> PriceIndex is 2);
                    (Price > 900, Price =< 1200 -> PriceIndex is 1)
                ).
            """)

            f.write("""
            room_type_score(AirbnbId, RoomTypeScore) :-
                room_type(AirbnbId, RoomType),
                ( RoomType = 'Entire home/apt' -> RoomTypeScore = 15;
                  RoomType = 'Private room' -> RoomTypeScore = 5;
                  RoomType = 'Shared room' -> RoomTypeScore = 0;
                  RoomType = 'Hotel room' -> RoomTypeScore = 10
                ).
            """)

            f.write("""
            cancellation_policy_score(AirbnbId, CancellationPolicyScore) :-
                cancellation_policy(AirbnbId, CancellationPolicy),
                ( CancellationPolicy = 'flexible' -> CancellationPolicyScore = 10;
                  CancellationPolicyScore = 5
                ).
            """)

            f.write("""
            host_identity_verified_score(AirbnbId, HostIdentityVerifiedScore) :-
                host_identity_verified(AirbnbId, HostIdentityVerified),
                ( HostIdentityVerified = 'true' -> HostIdentityVerifiedScore = 5;
                  HostIdentityVerifiedScore = 0
                ).
            """)

            f.write("""
            overall_score(AirbnbId, OverallScore) :-
                price_index(AirbnbId, PriceIndex),
                has_reviews(AirbnbId, ReviewScore),
                room_type_score(AirbnbId, RoomTypeScore),
                cancellation_policy_score(AirbnbId, CancellationPolicyScore),
                host_identity_verified_score(AirbnbId, HostIdentityVerifiedScore),
                OverallScore is PriceIndex + ReviewScore + RoomTypeScore + CancellationPolicyScore + HostIdentityVerifiedScore.
            """)

            f.write("""
            final_score(AirbnbId, PrefRoomType, PrefCancellationPolicy, PrefPriceMax, FinalScore) :-
                overall_score(AirbnbId, OverallScore),
                user_pref_score(AirbnbId, PrefRoomType, PrefCancellationPolicy, PrefPriceMax, BonusScore),
                FinalScore is OverallScore + BonusScore.
            """)

            f.write("""
            highest_review_score([AirbnbId], PrefRoomType, PrefCancellationPolicy, PrefPriceMax, AirbnbId) :-
                final_score(AirbnbId, PrefRoomType, PrefCancellationPolicy, PrefPriceMax, _).
            """)

            f.write("""
            highest_review_score([AirbnbId1, AirbnbId2 | Rest], PrefRoomType, PrefCancellationPolicy, PrefPriceMax,
                                 HighestReviewScoreAirbnbId) :-
                final_score(AirbnbId1, PrefRoomType, PrefCancellationPolicy, PrefPriceMax, FinalScore1),
                final_score(AirbnbId2, PrefRoomType, PrefCancellationPolicy, PrefPriceMax, FinalScore2),
                ( FinalScore1 >= FinalScore2 ->
                  highest_review_score([AirbnbId1 | Rest], PrefRoomType, PrefCancellationPolicy, PrefPriceMax, HighestReviewScoreAirbnbId);
                  highest_review_score([AirbnbId2 | Rest], PrefRoomType, PrefCancellationPolicy, PrefPriceMax,
                                       HighestReviewScoreAirbnbId)
                ).
            """)


kb = CreateKB()
kb.createKnowledgeBase()