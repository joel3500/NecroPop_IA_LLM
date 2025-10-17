
#=== env = environnement ===========================================================
import getpass
from dotenv import load_dotenv
import os
load_dotenv()                                # Téléchargement de la structure contenant ma clé
key =  os.getenv("OPENAI_API_KEY_2")         # ma clé provient de mon os. env me permet de ne PAS écrire ma clé dans ce fichier

#=== importation des librairies permettant de scrapper les données des sites =======
import requests
from bs4 import BeautifulSoup
import json

# page Le Necrologue
# https://www.lenecrologue.com/necrologie/province/quebec/

def nettoyer_texte(t):
    print("Nettoyage du texte en cours...\n")
    print("\tRetrait des anticlash de retour à la ligne...\n")
    t1 = t.replace("\n", "")
    print("\tRetrait des balises de type <p>...\n")
    t2 = t.replace("<p>", "")
    print("\tRetrait des balises de type </p>...\n")
    t3 = t2.replace("</p>", "")
    print("\tRetrait des balises de type <br/>...\n")
    t4 = t3.replace("<br/>", "")
    print("\tRetrait des balises de type <br />...\n")
    t5 = t4.replace("<br />", "")
    print("\tRetrait des espaces inutiles...\n")
    t6 = t5.strip()
    return t6


def extraire_infos_jjcardinal(mon_lien):
    # Envoyer une requête pour récupérer le contenu de la page
    response = requests.get(mon_lien)
    response.encoding = "utf-8"
    response.raise_for_status()  # Vérifier si la requête a réussi
    # Parser le contenu HTML de la page
    soup = BeautifulSoup(response.content, "html.parser")
    # soup = BeautifulSoup(response.text, "html.parser")
    # Fonction pour extraire les données du defunt
    recette = {}
    print()
    # Récupérer la liste des Ingrediens     FONCTIONNE TRES BIEN
    print("Extraction du texte initiée...\n")
    block_des_infos = soup.find("section", class_="post_content")
    les_infos = block_des_infos.text if block_des_infos else "Non_specifie"
    infos = nettoyer_texte(les_infos) 
    print("Affichage du texte après Extraction et Nettoyage...\n")
    print(infos)
    return infos

    
    

   