from ontology import main_ontology
from recommender_system import main_recommender
from knowledge_base import main_kb

def avvio():
    print("BENVENUTO\n")

    while(True):
        print("Scegli una tra le seguenti opzioni:\n\n1) Recommender System\n2) Knowledge Base\n3) Ontologia\n4) Exit\n\nInserisci qui:\t")
        risposta = input()
        if risposta == '1':
            main_recommender()
        elif risposta == '2':
            main_kb()
        elif risposta == '3':
            main_ontology()
        elif risposta == '4':
            print("Arrivederci!")
            break
        else:
            print("Inserisci correttamente il numero")
        
        print("\nVuoi terminare o continuare?\tTermina (si) Continua (no)\n")
        risposta2 = input()
        if risposta2 == 'si':
            print("Arrivederci!")
            break

#if __name__ == '__main__':
avvio()