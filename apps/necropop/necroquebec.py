
#===================================================================================================#
#   Nom du Programme               : Prompt Ingineering Avancé                                      #
#   Auteur                         : ...                                                     #
#                                  :                                                                #
#   Date de création               : inconnue                                                      # 
#   Date de dernièere modification : 18 Novembre 2024                                               #  
#   But du programme               : Ce programme a pour but de faire du Prompt Ingineering Avancé: #
#                                    à partir d'une API, nous allons exploiter les ressources       #
#                                    d'une IA, en utilisant les services des llms.                  #
#                                    Ce code sera réalisé par l'importation de                      #
#                                    la Bibliotheque LangChain.                                     #
#===================================================================================================#
import getpass
from dotenv import load_dotenv
import os
#===============================
import requests
from bs4 import BeautifulSoup
import json
#===============================
# https://www.youtube.com/watch?v=hV1NWnbC-D8  recupérer les donnees d'une page HTML
#===============================

#import cgi
#form = cgi.FieldStorage()
#url = form.getvalue("url")
#print(url)

# Dans ce programme, je vais outrepasser cette étape de vérification
# if not os.environ.get("OPENAI_API_KEY"):
   # os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")

load_dotenv()

# URL d'un defunt spécifique sur Cuisine Libre
url_1 = "https://necrologie.quebec/laval/claude-brunet/"

# voir ligne 578 à 588 pour toutes informtions à scrapper
url_image = "https://jjcardinal.ca/wp-content/uploads/2024/11/600ARichard-Hughes-photo.webp"

def telecharger_et_sauvegarder_image(url_image):
    response = requests.get(url_image)
    if response.status_code == 200:
        with open('test_2.jpg', 'wb') as f:
            f.write(response.content)

# telecharger_et_sauvegarder_image(url_image)

def nettoyer_texte(t):
    print("Nettoyage du texte en cours...\n")
    print("\tRetrait des anticlash de retour à la ligne...\n")
    t1 = t.replace("\n", "")
    print("\tRetrait des balises de type <p>...\n")
    t2 = t.replace("<p>", "")
    print("\tRetrait des balises de type </p>...\n")
    t3 = t2.replace("</p>", "")
    print("\tRetrait des balises de type <br/>...\n")
    t4 = t3.replace("<br>", "")
    print("\tRetrait des espaces inutiles...\n")
    t5 = t4.strip()
    return t5

# page Le Necrologue
# https://www.lenecrologue.com/necrologie/province/quebec/

def extraire_infos_necroquebec(url_1):
    # Envoyer une requête pour récupérer le contenu de la page
    response = requests.get(url_1)
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
    block_des_infos = soup.find("div", class_="entry-content")
    les_infos = block_des_infos.text if block_des_infos else "Non_specifie"
    infos = nettoyer_texte(les_infos) 
    print("Affichage du texte après Extraction et Nettoyage...\n")
    print(infos)

    return infos


