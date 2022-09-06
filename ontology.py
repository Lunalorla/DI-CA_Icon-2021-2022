from owlready2 import *

print("\nBENVENUTO NELLA STEAM-ONTOLOGY\n")
while(True):
    print("Seleziona cosa vorresti esplorare:\n\n1) Visualizzazione Classi\n\n2) Visualizzazione proprietà d'oggetto\n\n3) Visualizzazione proprietà dei dati\n\n4) Visualizzazione query d'esempio\n")

    risposta_menù = input("Inserisci qui la tua scelta:\t")

    ontology = get_ontology('dataset/Steam-Ontology.owl').load()

    if risposta_menù == '1':
        print("\nClassi presenti nell'ontologia:\n")
        print(list(ontology.classes()))

        while(True):
            print("\nVorresti esplorare meglio qualche classe in particolare?\n\n1)Agent\n2)Game\n3)Developer\n4)Genre\n5)Platform\n6)Publisher\n7)Costumer\n8)Shop\n")
            risposta_class = input("Inserisci qui la tua scelta:\t")

            if risposta_class == '1':
                print("\nLista di Agenti presenti:\n")
                agents = ontology.search(is_a = ontology.Agent)
                print(agents)
            elif risposta_class == '2':
                print("\nLista dei Giochi presenti:\n")
                games = ontology.search(is_a = ontology.Game)
                print(games)
            elif risposta_class == '3':
                print("\nLista degli Sviluppatori presenti:\n")
                developers = ontology.search(is_a = ontology.Developer)
                print(developers)
            elif risposta_class == '4':
                print("\nLista delle Categorie presenti:\n")
                genres = ontology.search(is_a = ontology.Genre)
                print(genres)
            elif risposta_class == '5':
                print("\nLista delle Piattaforme presenti:\n")
                platforms = ontology.search(is_a = ontology.Platform)
                print(platforms)
            elif risposta_class == '6':
                print("\nLista delle Case Pubblicatrici presenti:\n")
                publishers = ontology.search(is_a = ontology.Publisher)
                print(publishers)
            elif risposta_class == '7':
                print("\nLista dei Clienti presenti:\n")
                costumers = ontology.search(is_a = ontology.Costumer)
                print(costumers)
            elif risposta_class == '8':
                print("\nLista dei Negozi presenti:\n")
                shops = ontology.search(is_a = ontology.Shop)
                print(shops)
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
        print("\nLista di Giochi che presentano la categoria 'Classic':\n")
        games = ontology.search(is_a = ontology.Game, has_genre = ontology.search(is_a = ontology.Classic))
        print(games, "\n")
        print("\nLista di Giochi che presentano lo sviluppatore 'Valve':\n")
        games = ontology.search(is_a = ontology.Game, has_developer = ontology.search(is_a = ontology.Valve))
        print(games, "\n")
        print("\nLista di Giochi che presentano la piattaforma 'Windows':\n")
        games = ontology.search(is_a = ontology.Game, has_platform = ontology.search(is_a = ontology.Windows))
        print(games, "\n")
    
    # print("\nVorresti terminare o continuare?\tTermina (si) Continua (no)")
    # risp = input("\n")
    # if risp == 'si':
    #     print("\nArrivederci")
    #     break
