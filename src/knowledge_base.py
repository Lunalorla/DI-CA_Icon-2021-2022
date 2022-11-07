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
    steam_data = steam_data[['name','developer','publisher','english','star','steamspy_tags','price','average_playtime','genres']].copy()

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

    # l'utente può passare 2 giochi diversi per confrontarne la qualità
    kb.append("quality_check(X, Y, T, Z) :- stars(X, T), stars(Y, Z)")

    steam_kb(kb)

    return steam_kb

def liking_prob(dataframe):

    liking_kb = pl.KnowledgeBase('Liking Probability')
    kb = []

    # chiedo di darmi il nome di un gioco che è piaciuto all'utente e di un gioco di cui vuole sapere la liking probability
    Gioco_Piaciuto = input("Insrisci il nome del gioco che ti è piaciuto: ").lower()
    genere = input("Dimmi il genere del gioco: ").lower()
    tempo_gioco = input("e il tempo di gioco medio: ")
    tempo_gioco = int(tempo_gioco)
    # aggiungo i fatti riguardanti questo gioco
    kb.append(f"is_genre({Gioco_Piaciuto}, {genere}")
    kb.append(f"avg_playtime({Gioco_Piaciuto}, %s" % tempo_gioco)
    kb.append(f"liked_game(utente, {Gioco_Piaciuto}")

    Gioco_Nuovo = input("\nInserisci il nome di un gioco di cui vuoi calcolare la probabilità che ti piaccia: ").lower()
    genere_n = input("Dimmi il genere del gioco: ").lower()
    tempo_gioco_n = input("e il tempo di gioco medio: ")
    tempo_gioco_n = int(tempo_gioco_n)
    # aggiungo i fatti riguardanti questo gioco
    kb.append(f"is_genre({Gioco_Nuovo}, {genere_n}")
    kb.append(f"avg_playtime({Gioco_Nuovo}, %s" % tempo_gioco_n)

    # chiedo di sapere quante ora l'utente lavora in un giorno
    Orario = input("\nQuante ore lavori/studi al giorno? ")
    Orario = int(Orario)
    # fatto che associa l'utente e le sue ore di lavorio giornaliere
    kb.append(f"has_work(utente, %s)" % Orario)
    # regola che calcola lo stress dell'utente
    kb.append(f"stress(utente, Prob) :- Prob is %s" % Orario)

    # aggiungo i fatti che associano un genere al genere stesso, potendo dare la conferma che due generi siano uguali
    data = dataframe['genres']
    result = list(set(data))
    i = 0
    while(i < len(result)):
        kb.append(f"same_genre({result[i].lower()},{result[i].lower()}")
        i += 1

    # l'utente può chiedere l'avg_playtime di un gioco
    kb.append("has_avg_playtime(X, Y) :- avg_playtime(X, Y)")

    # regola che fa la differenza tra l’avg_playtime del gioco che già piace all’utente e del gioco nuovo.
    # kb.append(f"avg_playtime_comp({Gioco_Piaciuto}, {Gioco_Nuovo}, Y) :- liked_game(utente, Gioco_Piaciuto), has_avg_playtime({Gioco_Piaciuto}, Avg1), has_avg_playtime({Gioco_Nuovo}, Avg2), Y is Avg1 - Avg2")
    kb.append(f"avg_playtime_comp(Gioco1, Gioco2, Y) :- liked_game(utente, Gioco1), has_avg_playtime(Gioco1, Avg1), has_avg_playtime(Gioco2, Avg2), Y is Avg1 - Avg2")

    # Regola che controlla se due giochi hanno lo stesso genere
    kb.append(f"has_same_genre(Gioco1, Gioco2) :- is_genre(Gioco1, X), is_genre(Gioco2, Y), same_genre(X, Y)")

    liking_kb(kb)

    # PLAYTIME SIMILARITY

    # faccio la query per potermi salvare il valore di Y
    result = liking_kb.query(pl.Expr(f"avg_playtime_comp({Gioco_Piaciuto}, {Gioco_Nuovo}, What)"))
    Playtime_Similarity = result[0]['What']

    Playtime_Similarity = assign_range(Playtime_Similarity)

    # GENRE SIMILARITY

    result = liking_kb.query(pl.Expr(f"has_same_genre({Gioco_Piaciuto}, {Gioco_Nuovo})"))
    bool = result[0]
    Genre_Similarity = 0
    if(bool == 'Yes'):
        Genre_Similarity = 2.5
    elif(bool == 'No'):
        Genre_Similarity = -2.5

    Compatibility = Playtime_Similarity + Genre_Similarity

    # aggiungo la regola che calcola la probabilità che il gioco nuovo possa piacere all'utente
    # Regola che calcola la probabilità che il nuovo gioco possa piacere all'utente
    kb.append(f"to_like(utente, %s, Prob) :- stress(utente, P1), Prob is P1 + %s" % (Compatibility, Compatibility))

    liking_kb(kb)

    result = liking_kb.query(pl.Expr(f"to_like(utente, {Compatibility}, What)"))
    p = result[0][f"{Compatibility}"]

    if(p > 100):
        p = 100
    elif(p < 0):
        p = 0

    print("\nLa probabilità che", Gioco_Nuovo, "ti possa piacere è:", p, "%")

def assign_range(num):

    num = int(num)

    if((abs(num) >= 0) & (abs(num) <= 100)):
        i = 100
    elif((abs(num) > 100) & (abs(num) <= 250)):
        i = 90
    elif((abs(num) > 250) & (abs(num) <= 500)):
        i = 80
    elif((abs(num) > 500) & (abs(num) <= 750)):
        i = 70
    elif((abs(num) > 750) & (abs(num) <= 1000)):
        i = 60
    elif((abs(num) > 1000) & (abs(num) <= 1250)):
        i = 50
    elif((abs(num) > 1250) & (abs(num) <= 1500)):
        i = 40
    elif((abs(num) > 1500) & (abs(num) <= 1750)):
        i = 30
    elif((abs(num) > 1750) & (abs(num) <= 2000)):
        i = 20
    elif((abs(num) > 2000) & (abs(num) <= 2500)):
        i = 20
    elif((abs(num) > 2500) & (abs(num) <= 10000)):
        i = 10
    elif(abs(num) > 10000):
        i = 0

    return i

# - MAIN - INTERAZIONE CON L'UTENTE
def main_kb():

    dataframe = build_dataframe()
    kb = populate_kb(dataframe)

    print("\nKNOWLEDGE BASE\n")
    print("Benvenuto, qui puoi eseguire ricerche sui giochi e sulle loro caratteristiche")

    while(True):
        print("Ecco le ricerche che puoi eseguire:")
        print("1) Ricerche sulle caratteristiche di un gioco")
        print("2) Confronti e ricerca di giochi in base ad una caratteristica")
        print("3) Verificare delle caratteristiche")
        print("4) Vedere con quale probabilità ti possa piacere un nuovo gioco")
        print("5) Exit Knowledge Base\n")
        choice1 = input("Quale scegli (inserisci il numero corrispondente alla tua scelta)? ")
        c1 = int(choice1)

        if(c1 == 1):
            while(True):
                game_name = input("Dammi il nome di un gioco: ").lower()
                print("Queste sono le caratteristiche che puoi cercare:")
                print("1) Chi lo ha sviluppato")
                print("2) Chi lo ha distribuito")
                print("3) Quanto costa")
                print("4) Quante stelle ha (su una scala da 1 a 5)")
                print("5) Di che genere è")
                print("6) Se è disponibile in lingua inlgese")
                choice2 = input("Selezionane una: ")
                c2 = int(choice2)

                if(c2 == 1):
                    result = kb.query(pl.Expr(f"developed_by(What,{game_name})"))
                    parola = result[0]['What']
                    print("\n", game_name, "è stato sviluppato da:", parola)

                elif(c2 == 2):
                    result = kb.query(pl.Expr(f"released_by(What,{game_name})"))
                    parola = result[0]['What']
                    print("\n", game_name, "è stato rilasciato da:", parola)

                elif(c2 == 3):
                    result = kb.query(pl.Expr(f"has_price(What,{game_name})"))
                    parola = result[0]['What']
                    print("\n", game_name, "costa:", parola)

                elif(c2 == 4):
                    result = kb.query(pl.Expr(f"quality(What,{game_name})"))
                    parola = result[0]['What']
                    print("\n", game_name, "ha:", parola, "stelle")

                elif(c2 == 5):
                    result = kb.query(pl.Expr(f"is_genre(What,{game_name})"))
                    parola = result[0]['What']
                    print("\nIl genere di", game_name, "è:", parola)

                elif(c2 == 6):
                    result = kb.query(pl.Expr(f"has_english(What,{game_name})"))
                    parola = result[0]['What']
                    if (parola == 'yes'):
                        print("\n", game_name, "è disponibile in lingua inglese")
                    elif (parola == 'no'):
                        print("\n", game_name, "non è disponibile in lingua inglese")
                
                risposta = input("\nVuoi eseguire un'altra ricerca o vuoi tornare indietro?\tIndietro (sì), Continua (no)")
                if(risposta == 'sì'):
                    break
                elif(risposta == 'si'):
                    break
                elif(risposta == 's'):
                    break

        elif(c1 == 2):
            print("Queste sono ricerche che puoi eseguire sulle caratteristiche:")
            while(True):
                print("1) Lista di giochi di un prezzo")
                print("2) Confronto di qualità tra 2 giochi")
                print("3) Indietro\n")
                choice3 = input("Selezionane una (inserisci il numero corrispondente alla tua scelta): ")
                c3 = int(choice3)

                if(c3 == 1):
                    prezzo = input("Inserisci un prezzo: ")
                    result = kb.query(pl.Expr(f"has_price({prezzo},What)"))
                    print("\nEcco la lista dei primi 100 giochi con prezzo ", prezzo, ":\n")
                    result = result[0:100]
                    i = 1
                    for r in result:
                        print(i, ")", r[f"{prezzo}"])
                        i += 1
                    print("\nPuoi selezionare una nuova ricerca:")

                # confronto di qualità tra 2 giochi
                elif(c3 == 2):
                    game1 = input("Dimmi il nome del primo gioco: ")
                    game2 = input("DImmi il nome del secondo gioco: ")
                    result = kb.query(pl.Expr(f"quality_check({game1}, {game2}, X, Y"))
                    star1 = result[0]['X']
                    star2 = result[0]['Y']
                    if(star1 > star2):
                        print("\nIl gioco migliore è: ", game1, ", perché la qualità di", game1, "è", star1, "è la qualità di", game2, "è", star2)
                    elif(star1 < star2):
                        print("\nIl gioco migliore è: ", game2, ", perché la qualità di", game2, "è", star2, "è la qualità di", game1, "è", star1)
                    elif(star1 == star2):
                        print("\nI due giochi hanno la stessa qualità, perché la qualità di", game1, "è", star1, ", e la qualità di", game2, "è", star2)
                    print("\nPuoi selezionare una nuova ricerca:")

                elif(c3 == 3):
                    break
                    
        elif(c1 == 3):
            while(True):
                print("Questi sono le caratteristiche che puoi verificare:")
                print("1) developer\n2) publisher\n3) prices\n4) stars\n5) genre\n6) english\n")
                fatto = input("Selezionane una (scrivi il nome dell'operazione da eseguire, tutto in minuscolo): ").lower()
                name = input("Quale gioco vuoi controllare? ").lower()
                char = input("Inserisci un dato corrispondente alla caratteristica scelta: ").lower()
                print(kb.query(pl.Expr(f"{fatto}({name},{char})")))
                risposta = input("Vuoi eseguire un'altra verifica o vuoi tornare indietro?\tIndietro (sì), Continua (no)")
                if(risposta == 'sì'):
                    break
                elif(risposta == 'si'):
                    break
                elif(risposta == 's'):
                    break

        elif(c1 == 4):
            while(True):
                liking_prob(dataframe)
                risposta = input("Vuoi controllare un'altra probabilità o vuoi tornare indietro?\tIndietro (sì), Continua (no)")
                if(risposta == 'sì'):
                    break
                elif(risposta == 'si'):
                    break
                elif(risposta == 's'):
                    break

        elif(c1 == 5):
            break