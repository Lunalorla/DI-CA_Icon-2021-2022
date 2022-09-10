import pytholog as pl
import pandas as pd

# - DATAFRAME

# Funziona che costruisce il dataframe basato sul dataset steam.csv.
# Aggiunge una nuova colonna 'star', in cui converte i valori del rapporto tra 'negative_ratings' e
# 'positive_ratings' in delle stelle che rappresentanto il voto dato al gioco dagli utenti.
# Converte la colonna 'english' in stringhe.
def build_dataframe():

    # creo il dataframe
    steam_data = pd.read_csv("dataset/steam.csv")

    # creo una nuova colonna 'star', che avrà come valori la percentuale dei 'negative_ratings'
    # in rapporto ai 'positive_ratings'
    steam_data['star'] = (steam_data['negative_ratings'] / steam_data['positive_ratings']) * 100
    # converto 'star' in dei range rappresentati dalle stelle
    # più basso è il valore della percentuale, più alta è la stella
    # [0, 12.5] = 5*;
    # [12.6, 25] = 4*;
    # [25.1, 37.5] = 3*;
    # [37.6, 50] = 2*;
    # [50, inf] = 1*
    steam_data.loc[(steam_data['star'] >= 0) & (steam_data['star'] <= 12.5), ['star']] = 5
    steam_data.loc[(steam_data['star'] > 12.5) & (steam_data['star'] <= 25), ['star']] = 4
    steam_data.loc[(steam_data['star'] > 25) & (steam_data['star'] <= 37.5), ['star']] = 3
    steam_data.loc[(steam_data['star'] > 37.5) & (steam_data['star'] <= 50), ['star']] = 2
    steam_data.loc[(steam_data['star'] > 50), ['star']] = 1
    # converto i valori "0" e "1" di 'english' nelle string "no" e "yes"
    steam_data.loc[(steam_data['english'] == 0), ['english']] = 'no'
    steam_data.loc[(steam_data['english'] == 1), ['english']] = 'yes'

    # creo una copia del dataframe con all'interno solo le colonne d'interesse
    steam_data = steam_data[['name','developer','publisher','english','star','steamspy_tags','price']].copy()

    return steam_data

# - KNOWLEDGE BASE

# Funzione che si occupa di popolare la knowledge base con i dati presi dal dataframe passato in input.
# Crea una lista in cui inizialmente inserisce i dati estratti dal dataframe sottoforma di 'fatti' e 'regole'.
# Questa lista viene poi inserita nella knowledge base creata con pytholog.
def populate_kb(dataframe):
    
    # creo la knowledge base e una lista in cui inserire i dati della kb
    steam_kb = pl.KnowledgeBase('Steam Games')
    kb = []

    # - FATTI

    # fatti riguardanti gli sviluppattori dei giochi
    # developer('name', 'developer')
    data = dataframe[['name', 'developer']].drop_duplicates().to_dict(orient="records")
    for d in data:
        kb.append(f"developer({d['name'].lower()},{d['developer'].lower()})")

    # fatti riguardanti chi ha pubblicato i giochi
    # publisher('name', 'publisher')
    data = dataframe[['name', 'publisher']].drop_duplicates().to_dict(orient="records")
    for d in data:
        kb.append(f"publisher({d['name'].lower()},{d['publisher'].lower()})")

    # fatti riguardanti i prezzi dei giochi
    # prices('name', 'price')
    data = dataframe[['name', 'price']].drop_duplicates().to_dict(orient="records")
    for d in data:
        kb.append(f"prices({d['name'].lower()},{d['price']})")

    # fatti riguardanti i ratings in stelle dei giochi
    # stars('name', 'star')
    data = dataframe[['name', 'star']].drop_duplicates().to_dict(orient="records")
    for d in data:
        kb.append(f"stars({d['name'].lower()},{d['star']})")

    # fatti riguardanti i generi dei giochi
    # genre('name', 'steamspy_tags')
    data = dataframe[['name', 'steamspy_tags']].drop_duplicates().to_dict(orient="records")
    for d in data:
        kb.append(f"genre({d['name'].lower()},{d['steamspy_tags'].lower()})")

    # fatti che ci dicono se un gioco è in inglese o meno
    # has_english('name', 'english')
    data = dataframe[['name', 'english']].drop_duplicates().to_dict(orient="records")
    for d in data:
        kb.append(f"english({d['name'].lower()},{d['english'].lower()})")

    # - REGOLE

    # l'utente può chiedere il costo di un gioco partendo dal nome
    # OPPURE
    # l'utente può chiedere una lista di giochi con un determinato prezzo
    kb.append("has_price(X, Y) :- prices(Y, X)")

    # l'utente può chiedere il rating di un gioco partendo dal nome
    # OPPURE
    # l'utente può chiedere una lista di giochi con un determinato rating
    kb.append("quality(X, Y) :- stars(Y, X)")

    # l'utente può chiedere qual è lo sviluppatore di un gioco
    kb.append("developed_by(X, Y) :- developer(Y, X)")

    # l'utente può chiedere chi ha rilasciato un gioco
    kb.append("released_by(X, Y) :- publisher(Y, X)")

    # l'utente può chiedere il genere di un gioco
    kb.append("is_genre(X, Y) :- genre(Y, X)")

    # l'utente può chiedere se un gioco è in lingua inglese
    kb.append("has_english(X, Y) :- english(Y, X)")

    steam_kb(kb)

    return steam_kb

# - MAIN - INTERAZIONE CON L'UTENTE
def main_kb():

    dataframe = build_dataframe()
    kb = populate_kb(dataframe)

    print("KNOWLEDGE BASE\n")
    print("Benvenuto, qui puoi eseguire ricerche sui giochi e sulle loro caratteristiche")

    while(True):
        print("Ecco le ricerche che puoi eseguire:")
        print("1: ricerche sulle caratteristiche di un gioco")
        print("2: confronti e ricerca di giochi in base ad una caratteristica")
        print("3: verificare delle caratteristiche")
        print("4: esci\n")
        choice1 = input("Quale scegli (inserisci il numero corrispondente alla tua scelta)? ")
        c1 = int(choice1)

        if(c1 == 1):
            while(True):
                game_name = input("Dammi il nome di un gioco: ")
                print("Queste sono le caratteristiche che puoi cercare:")
                print("1) developed_by\n2) released_by\n3) has_price\n4) quality\n5) is_genre\n6) has_english,\n")
                fatto = input("Selezionane una (scrivi il nome dell'operazione da eseguire, tutto in minuscolo e rispettando i trattini): ")
                result = kb.query(pl.Expr(f"{fatto}(What,{game_name})"))
                parola = result[0]['What']
                print('\nil tuo risultato è:', parola)
                risposta = input("\nVuoi eseguire un'altra ricerca o vuoi tornare indietro? indietro = sì, ricerca = no")
                if(risposta == 'sì'):
                    break

        elif(c1 == 2):
            while(True):
                print("Queste sono ricerche che puoi eseguire sulle caratteristiche:\n")
                print("1: lista di giochi di un prezzo")
                print("2: confronto di qualità tra 2 giochi")
                print("3: lista di giochi sviluppati da una casa")
                print("4: lista di giochi rilasciati da una casa")
                print("5: indietro\n")
                choice3 = input("Selezionane una (inserisci il numero corrispondente alla tua scelta): ")
                c3 = int(choice3)

                if(c3 == 1):
                    prezzo = input("Inserisci un prezzo: ")
                    result = kb.query(pl.Expr(f"costo({prezzo},What)"))
                    print("\nEcco la lista di giochi con prezzo ", prezzo, ":\n")
                    result = result[0:100]
                    i = 1
                    for r in result:
                        print(i, ")", r[f"{prezzo}"])
                        i += 1

                # confronto di qualità tra 2 giochi
                elif(c3 == 2):
                    game1 = input("Dimmi il nome del primo gioco: ")
                    game2 = input("DImmi il nome del secondo gioco: ")
                    result = kb.query(pl.Expr(f"quality(What,{game1})"))
                    star1 = result[0]['What']
                    result = kb.query(pl.Expr(f"quality(What,{game2})"))
                    star2 = result[0]['What']
                    if(star1 > star2):
                        print("\nIl gioco migliore è: ", game1)
                    elif(star1 < star2):
                        print("\nIl gioco migliore è: ", game2)
                    elif(star1 == star2):
                        print("\nI due giochi hanno la stessa qualità")

                elif(c3 == 3):
                    sviluppatore = input("Inserisci uno sviluppatore: ")
                    result = kb.query(pl.Expr(f"developed_by({sviluppatore},What)"))
                    print("\nEcco la lista di giochi sviluppati da ", sviluppatore, ":\n")
                    for r in result:
                        print(r['What'])

                elif(c3 == 4):
                    pubblicato = input("Inserisci un publisher: ")
                    result = kb.query(pl.Expr(f"released_by({pubblicato},What)"))
                    print("\nEcco la lista di giochi rilasciati da ", pubblicato, ":\n")
                    for r in result:
                        print(r['What'])

                elif(c3 == 5):
                    break
                    
        elif(c1 == 3):
            while(True):
                print("Questi sono le caratteristiche che puoi verificare:")
                print("1) developer\n2) publisher\n3) prices\n4) stars\n5) genre\n6) english,\n")
                fatto = input("Selezionane una (scrivi il nome dell'operazione da eseguire, tutto in minuscolo): ")
                name = input("Quale gioco vuoi controllare? ")
                char = input("Inserisci un dato corrispondente alla caratteristica scelta: ")
                print(kb.query(pl.Expr(f"{fatto}({name},{char})")))
                risposta = input("Vuoi eseguire un'altra verifica o vuoi tornare indietro? indietro = sì, ricerca = no")
                if(risposta == 'sì'):
                    break

        elif(c1 == 4):
            print("\nArrivederci!")
            break


main_kb()