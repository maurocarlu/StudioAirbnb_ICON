from owlready2 import *

def main_ontology():
    print("\nBenvenuto nell'ontologia\n")
    while(True):
        print("Seleziona cosa vorresti esplorare:\n1) Visualizzazione Classi\n2) Visualizzazione proprietà d'oggetto\n3) Visualizzazione proprietà dei dati\n4) Esegui query\n5) Esci dall' Ontologia\n")

        risposta_menù = input("Inserisci qui la tua scelta: ")

        ontology = get_ontology('ontology.owl').load()

        if risposta_menù == '1':
            print("\nClassi presenti nell'ontologia:\n")
            print(list(ontology.classes()))

            while(True):
                print("\nVorresti esplorare meglio qualche classe in particolare?\n\n1) Alloggio\n2) Città\n"
                    "3) Proprietario\n4) Provider\n5) Quartiere\n6) Prenotazione\n7) Cliente\n8) Pagamento\n")

                risposta_class = input("Inserisci qui la tua scelta: ")

                if risposta_class == '1':
                    print("\nLista degli alloggi presenti:\n")
                    alloggio = ontology.search(is_a = ontology.Alloggio)
                    print(alloggio)
                elif risposta_class == '2':
                    print("\nLista delle città presenti:\n")
                    citta = ontology.search(is_a = ontology.Città)
                    print(citta)
                elif risposta_class == '3':
                    print("\nLista dei proprietari presenti:\n")
                    proprietario = ontology.search(is_a = ontology.Proprietario)
                    print(proprietario)
                elif risposta_class == '4':
                    print("\nLista dei provider presenti:\n")
                    provider = ontology.search(is_a = ontology.Provider)
                    print(provider)
                elif risposta_class == '5':
                    print("\nLista dei quartieri presenti:\n")
                    quartiere = ontology.search(is_a = ontology.Quartiere)
                    print(quartiere)
                elif risposta_class == '6':
                    print("\nLista delle prenotazioni presenti:\n")
                    prenotazione = ontology.search(is_a = ontology.Prenotazione)
                    print(prenotazione)
                elif risposta_class == '7':
                    print("\nLista dei clienti presenti:\n")
                    cliente = ontology.search(is_a = ontology.Cliente)
                    print(cliente)
                elif risposta_class == '8':
                    print("\nLista dei pagamenti presenti:\n")
                    pagamento = ontology.search(is_a = ontology.Pagamento)
                    print(pagamento)
                else:
                    print("\nInserisci il numero correttamente tra quelli presentati")

                risp = input("\nVuoi esaminare un'altra classe? (y/n): ")
                if risp == 'n' or risp == 'N':
                    break

        elif risposta_menù == '2':
            print("\nProprietà d'oggetto presenti nell'ontologia:\n")
            print(list(ontology.object_properties()), "\n")
        elif risposta_menù == '3':
            print("\nProprietà dei dati presenti nell'ontologia:\n")
            print(list(ontology.data_properties()), "\n")
        elif risposta_menù == '4':
            while True:
                print("1) Lista di alloggi che presentano il proprietario 'mauro_carlucci\n"
                      "2) Lista di alloggi pubblicati su 'AirBnB'\n"
                      "3) Prenotazioni effettuate da Marco Blu\n"
                      "4) Torna indietro\n")
                scelta = input("inserisci la tua scelta: ")
                if scelta == '1':
                    alloggio = ontology.search(is_a=ontology.Alloggio,is_owned=ontology.search_one(username="maurocarlu"))
                    print(alloggio, "\n")
                elif scelta == '2':
                    alloggio = ontology.search(is_a=ontology.Alloggio,is_situated=ontology.search(is_a=ontology.New_York))
                    print(alloggio, "\n")
                elif scelta == '3':
                    prenotazione = ontology.search(is_a=ontology.Prenotazione,submitted_by=ontology.search_one(username="marcoblu"))
                    print(prenotazione, "\n")
                elif scelta == '4':
                    break
                else:
                    print("Scelta non valida. Inserisci un numero tra 1 e 4.")

        elif risposta_menù == '5':
            break

if __name__ == "__main__":
    main_ontology()