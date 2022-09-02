import numpy as np
import pandas as pd
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel

#funzione che gestisce la comunicazione con l'utente, chiedendo di inserire le caratteristiche del gioco su cui vuole che venga fatta la recomendation
def get_info():
    #prendo gli input dall'utente
    print("GET RECOMMENDED\n\nBenvenuto, digita le caratteristiche del gioco su cui vuoi che si avvii la raccomandazione\n")

    nome = input("Inserisci il nome:\n")
    developer = input("Inserisci lo sviluppatore:\n")
    publisher = input("Inserisci la casa pubblicatrice:\n")
    platforms = input("Inserisci le piattaforme:\t (ricorda tra una parola e l'altra di mettere il simbolo ';' )\n")
    genres = input("Inserisci il genere:\t (ricorda tra una parola e l'altra di mettere il simbolo ';' )\n")

    #creo un dataframe temporaneo contenente i dati messi dall'utente
    users_data = pd.DataFrame({'name': nome, 'developer': developer,'publisher': publisher,'platforms': platforms,'genres': genres}, index=[0])

    return users_data

#funzione che legge il dataset iniziale, lo riduce, controlla se il gioco inserito dall'utente sia già presente o meno, se non lo è lo aggiunge,
#vettorizza il dataset aggiornato, calcola la similarità del coseno, trova i 5 giochi più simili a quello indicato dall'utente, basandosi sulla sua posizione
#nel dataframe utilizzando l'indice ottenuto
def recommend_games(filename, users_data):

    steam_data = pd.read_csv(filename)
    steam_data['positivity_quote'] = steam_data['positive_ratings'] // steam_data['negative_ratings']
    steam_data['genres'] = steam_data['steamspy_tags']
    steam_data = steam_data[['name','release_date','developer','publisher','platforms','genres','positivity_quote', 'average_playtime','owners','price']].copy()

    #controllo se l'elemento dato dall'utente si trova già nel dataset o meno, se non si trova, lo aggiungo all'inizio/fine. Mi salvo l'indice di cosa ha chiesto l'utente in ogni caso
    control = 0

    for name in steam_data['name']:
        if users_data['name'][0] != name:
            index = 0
            control = 1
        else:
            index = steam_data.index[steam_data['name'] == name].values[0] #invece di Zelda metterai il gioco dato da input che si trova nel dataset
            control = 0
            break

    if control == 1:
        steam_data = pd.concat([users_data,steam_data], ignore_index=True) #per metterlo alla fine scambia l'ordine dei dataframe

    steam_data['all_content'] = steam_data['name'] + ';' + steam_data['developer'] + ';' + steam_data['publisher'] + ';' + steam_data['platforms'] + ';' + steam_data['genres'] #definisci le categorie che vuoi usare e uniscile in una, per poter applicare il tf-idf
    
    tfidf_matrix = vectorize_data(steam_data)
    cosine_similarity = linear_kernel(tfidf_matrix, tfidf_matrix) #costruzione della similarità del coseno da applicare poi alla matrice creata

    indices = pd.Series(steam_data['name'].index)

    id = indices[index]
    # Get the pairwise similarity scores of all books compared that book,
    # sorting them and getting top 5
    similarity_scores = list(enumerate(cosine_similarity[id]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:6]
    
    #Get the books index
    games_index = [i[0] for i in similarity_scores]
    
    #Return the top 5 most similar games using integer-location based indexing (iloc)
    result = steam_data[['name','price','developer','genres']].iloc[games_index]  #metti tutte le categorie che ti interessano per far uscire il risultato
    return result

#funzione che prende il dataframe ridotto e aggiornato e lo vettorizza per crearsi una matrice tfidf
def vectorize_data(steam_data):

    vectorizer = TfidfVectorizer(analyzer='word')
    tfidf_matrix = vectorizer.fit_transform(steam_data['all_content'])
    return tfidf_matrix

#funzione main che gestisce il flusso del programma per la recommendation e che stampa alla fine il risultato avuto
def main():
    users_data = get_info()

    print("Questo è il videogioco che hai inserito:\n")
    print(users_data.head())
    # risposta = input("\nE' corretto?:\t")

    # if risposta == "no" or "n" or "o":
    #     users_data = get_info()
    # else:
    #     result = recommend_games('dataset/steam.csv', users_data)

    result = recommend_games('dataset/steam.csv', users_data)

    print("Ecco a te i 5 giochi più simili a quello proposto:\n\n", result)

main()
