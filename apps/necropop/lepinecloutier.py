
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

#===================================================================================

def telecharger_et_sauvegarder_image(url_image):
        response = requests.get(url_image)
        if response.status_code == 200:
            with open('test_1.jpg', 'wb') as f:
                f.write(response.content)
        return
        # telecharger_et_sauvegarder_image(url_image, requests)

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
        print("\tRetrait des espaces inutiles...\n")
        t5 = t4.strip()
        return t5

def extraire_infos_lepinecloutier(mon_lien):
        # Envoyer une requête pour récupérer le contenu de la page
        response = requests.get(mon_lien)
        response.encoding = "utf-8"
        response.raise_for_status()  # Vérifier si la requête a réussi

        # Parser le contenu HTML de la page
        soup = BeautifulSoup(response.content, "html.parser")
        # soup = BeautifulSoup(response.text, "html.parser")

        print()
        # Récupérer la liste des Ingrediens     FONCTIONNE TRES BIEN
        print("Extraction du texte initiée...\n")
        block_des_infos = soup.find("div", class_="fw-obituary-content")
        les_infos = block_des_infos.text if block_des_infos else "Non_specifie"
        infos = nettoyer_texte(les_infos) 
        print("Affichage du texte après Extraction et Nettoyage...\n")
        #print(infos)
        return infos



    #==================================================================================



