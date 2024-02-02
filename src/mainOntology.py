from owlready2 import *

def main_ontology():
    print("\nBenvenuto nell'ontologia\n")
    while(True):
        print("Seleziona cosa vorresti esplorare:\n\n1) Visualizzazione Classi\n2) Visualizzazione proprietà d'oggetto\n3) Visualizzazione proprietà dei dati\n4) Visualizzazione query d'esempio\n5) Esci dall' Ontologia\n")

        risposta_menù = input("Inserisci qui la tua scelta:\t")

        ontology = get_ontology('ontology.owl').load()

        if risposta_menù == '1':
            print("\nClassi presenti nell'ontologia:\n")
            print(list(ontology.classes()))

            while(True):
                print("\nVorresti esplorare meglio qualche classe in particolare?\n\n1) Alloggio\n2) Città\n3) Proprietario\n4) Provider\n5) Quartiere\n")
                risposta_class = input("Inserisci qui la tua scelta:\t")

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



                else:
                    print("\nInserisci il numero correttamente tra quelli presentati")

                print("\nVorresti tornare indietro o continuare?\tIndietro (si) Continua (no)")
                risp = input("\n")
                if risp == 'si':
                    break

        elif risposta_menù == '2':
            print("\nProprietà d'oggetto presenti nell'ontologia:\n")
            print(list(ontology.object_properties()), "\n")
        elif risposta_menù == '3':
            print("\nProprietà dei dati presenti nell'ontologia:\n")
            print(list(ontology.data_properties()), "\n")
        elif risposta_menù == '4':
            print("\nQuery d'esempio:")
            print("\n-Lista di alloggi che presentano il proprietario 'mauro_carlucci':\n")
            alloggio = ontology.search(is_a = ontology.Alloggio, is_owned = ontology.search_one(username="maurocarlu"))
            print(alloggio, "\n")
        elif risposta_menù == '5':
            break

if __name__ == "__main__":
    main_ontology()