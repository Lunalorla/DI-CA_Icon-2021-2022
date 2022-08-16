# DI-CA_Icon-2021-2022
Progetto Icon dell'anno 2021-2022.

TO DO LIST RECOMMENDER SYSTEM:

1) come aggiungere un nuovo elemento a un Dataframe (deve avere tutte le categorie, ma alcune potrebbero essere vuote, problema?)

2) ordine esecuzione:

	-prendiamo in input un gioco che piace all'utente con tutte le categorie che richiediamo (decidere se deve inserirle per forza o può anche non farlo)
	-controlliamo se l'elemento si trova già nel dataframe, altrimenti inserirlo
		-salvarsi l'indice dell'elemento appena aggiunto (probabilmente sarà un'aggiunta alla fine)
		-oppure salvarsi l'indice dell'elemento che si sta cercando se lo si trova già all'interno
	-creare la tf-idf matrix, basandosi sulle categorie che vogliamo includere
		-per le categorie su cui basare la creazione della tf-idf, unirle prima in un'unica categoria (vedi file web)
	-calcola la similarità del coseno sulla stessa matrice (2 volte)
	-applica la funzione che calcola i top n giochi raccomandati (vedi file web)
		-(far vedere la differenza di punteggi di similarità, tra i risultati proposti)
