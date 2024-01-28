from pyswip import Prolog

def main():
    prolog = Prolog()
    prolog.consult('KB.pl')

    while True:
        choice = int(input("Scegliere quale funzione eseguire:\n1) Trova gli airbnb date determinate caratteristiche\n"
                           "2) Dati i gusti dell'utente, trova l'airbnb col punteggio migliore\n3) Esci\n"))
        if choice == 1:
            query_airbnb(prolog)
        elif choice == 2:
            ask_user_preferences_and_query(prolog)
        elif choice == 3:
            exit(0)
        else:
            print("Input non valido. Utilizzare solo 1 o 2 o 3.")


def query_airbnb(prolog):
    while True:
        tipo = None
        recensione = None
        posizione = None
        politica = None

        while tipo is None:
            tipo_input = int(input("Inserisci la fascia di prezzo che preferisci per l'airbnb\n1) Economico\n2) Medio\n3) Costoso\n"))
            if tipo_input == 1:
                tipo = "economico"
            elif tipo_input == 2:
                tipo = "medio"
            elif tipo_input == 3:
                tipo = "costoso"
            else:
                print("Input non valido. Utilizzare solo 1, 2 o 3.")

        while recensione is None:
            recensione_input = int(input("Vuoi che gli airbnb mostrati abbiano buone o cattive recensioni ?\n1) Ben recensito\n2) Mal recensito\n"))
            if recensione_input == 1:
                recensione = "ben_recensito"
            elif recensione_input == 2:
                recensione = "mal_recensito"
            else:
                print("Input non valido. Utilizzare solo 1 o 2.")

        while posizione is None:
            posizione_input = int(input("Vuoi che l'airbnb sia in una posizione centrale o periferica ? \n1) centrale\n2) periferico\n"))
            if posizione_input == 1:
                posizione = "centrale"
            elif posizione_input == 2:
                posizione = "periferico"
            else:
                print("Input non valido. Utilizzare solo 1 o 2.")

        while politica is None:
            politica_input = int(input("Quale tipo di politica di cancellazione deve avere l'airbnb ?\n1) stretta\n2) media\n3) flessibile\n"))
            if politica_input == 1:
                politica = "stretto"
            elif politica_input == 2:
                politica = "media"
            elif politica_input == 3:
                politica = "flessibile"
            else:
                print("Input non valido. Utilizzare solo 1, 2 o 3.")

        flag = False
        notti = None
        while not flag:
            notti = int(input("Inserisci il numero di notti che vuoi soggiornare:\n"))
            if 0 <= notti <= 365:
                flag = True
            else:
                print("Input non valido. Utilizzare solo valori compresi tra 0 e 365.")

        query = f"{tipo}_{recensione}_{posizione}_{politica}_notti(ID, {notti})"

        results = list(prolog.query(query))

        if len(results) == 0:
            print("Con questi filtri non vi sono risultati.")
        else:
            print("Gli id degli airbnb che rispettano i filtri sono:")
            for soln in results:
                print(soln["ID"])

        repeat = int(input("Vuoi ripetere la query?\n1) Si\n2) No\n"))
        if repeat == 2:
            break
        else:
            print("\n")


from pyswip import Prolog

def ask_user_preferences_and_query(prolog):
    pref_room_type = None
    pref_cancellation_policy = None
    pref_price_max = None
    while pref_room_type is None:
        scelta1 = int(input(
            "Quale tipo di stanza preferisci?\n1) Stanza privata\n2) Intero appartamento/casa\n3) Stanza condivisa\n4) Stanza di hotel\n"))
        if scelta1 == 1:
            pref_room_type = "Private Room"
        elif scelta1 == 2:
            pref_room_type = "Entire home/apt"
        elif scelta1 == 3:
            pref_room_type = "Shared room"
        elif scelta1 == 4:
            pref_room_type = "Hotel room"
        else:
            print("Input non valido. Utilizzare solo 1, 2, 3 o 4.")

    while pref_cancellation_policy is None:
        scelta2 = int(input(
            "Quale tipo di politica di cancellazione deve avere l'airbnb ?\n1) stretta\n2) moderata\n3) flessibile\n"))
        if scelta2 == 1:
            pref_cancellation_policy = "strict"
        elif scelta2 == 2:
            pref_cancellation_policy = "moderate"
        elif scelta2 == 3:
            pref_cancellation_policy = "flexible"
        else:
            print("Input non valido. Utilizzare solo 1, 2 o 3.")

    while pref_price_max is None:
        try:
            user_input = int(input("Inserisci il prezzo massimo che vorresti pagare (Tra 50 e 1200): "))
            if 50 <= user_input <= 1200:
                pref_price_max = user_input
            else:
                print("Input non valido, inserisci un numero tra 50 e 1200.")
        except ValueError:
            print("Input non valido, inserisci un numero tra 50 e 1200.")

    # Get all Airbnb IDs from the Prolog knowledge base
    airbnb_ids = [soln["AirbnbId"] for soln in prolog.query("price(AirbnbId, _)")]

    # Query the highest_review_score rule
    highest_review_score = list(prolog.query(f"highest_review_score({airbnb_ids}, '{pref_room_type}', '{pref_cancellation_policy}', {pref_price_max}, HighestReviewScoreAirbnbId)"))

    # Get the Airbnb ID with the highest final score
    highest_review_score_id = highest_review_score[0]['HighestReviewScoreAirbnbId']

    # Query all the facts related to this Airbnb ID
    airbnb_facts = list(prolog.query(f"price({highest_review_score_id}, Price), "
                                     f"neighbourhood({highest_review_score_id}, Neighbourhood), "
                                     f"minimum_nights({highest_review_score_id}, MinNights), "
                                     f"number_of_reviews({highest_review_score_id}, NumReviews), "
                                     f"review_rate_number({highest_review_score_id}, ReviewRate), "
                                     f"cancellation_policy({highest_review_score_id}, CancellationPolicy), "
                                     f"room_type({highest_review_score_id}, RoomType), "
                                     f"host_identity_verified({highest_review_score_id}, HostIdentityVerified)"))

    # Print the Airbnb ID with the highest final score
    print(f"The Airbnb with the highest final score is: {highest_review_score_id}")

    # Print all the facts related to this Airbnb ID
    for fact in airbnb_facts:
        print(f"Price: {fact['Price']}")
        print(f"Neighbourhood: {fact['Neighbourhood']}")
        print(f"Minimum Nights: {fact['MinNights']}")
        print(f"Number of Reviews: {fact['NumReviews']}")
        print(f"Review Rate: {fact['ReviewRate']}")
        print(f"Cancellation Policy: {fact['CancellationPolicy']}")
        print(f"Room Type: {fact['RoomType']}")
        print(f"Host Identity Verified: {fact['HostIdentityVerified']}")

    print("\n")



if __name__ == "__main__":
    main()