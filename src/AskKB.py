from pyswip import Prolog

def main():
    prolog = Prolog()
    prolog.consult('KB.pl')

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
            for soln in results:
                print(soln["ID"])  # Stampa l'ID di ogni soluzione

        repeat = int(input("\n\nVuoi ripetere la query?\n1) Si\n2) No\n"))
        if repeat == 2:
            break
        else:
            print("\n\n\n\n")

if __name__ == "__main__":
    main()