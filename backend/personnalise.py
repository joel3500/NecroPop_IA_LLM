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
#=============================================
import json
#=============================================
# https://www.youtube.com/watch?v=hV1NWnbC-D8  recupérer les donnees d'une paghe HTML
#=============================================

# Dans ce programme, je vais outrepasser cette étape de vérification
# if not os.environ.get("OPENAI_API_KEY"):
# os.environ["OPENAI_API_KEY"] = getpass.getpass("Enter your OpenAI API key: ")
#=============================================

load_dotenv()

#def telecharger_et_sauvegarder_image(url_image):
#    response = requests.get(url_image)
#    #filenmame = url.split("/")[-1]
    #index_point_interrogation = filenmame.find("?")
    #if index_point_interrogation != -1:
    #    filenmame = filenmame[:index_point_interrogation]
#    if response.status_code == 200:
#        with open('test.jpg', 'wb') as f:
#            f.write(response.content)

# telecharger_et_sauvegarder_image(url_image)

recit_1 = "Mon grand-père s'appelle Augustin Adegbenlé (1905-2024).\
           Il laisse dans le deuil ses 3 enfants : David Adégbenlé, Véronique Adégbenlé et Victor Adegbenlé.\
            David Adégbenlé a 3 enfants :  Willfrid Adegbenlé, Terrence Adegbenlé, et Dorice Adegbenlé.\
            Véronique Adégbenlé a 3 enfants : Joel Sandé, Linda manuelle Sandé, et William Joseph Sandé.\
            Victor Adegbenlé a 4 enfants : Odilia meledge Ade, Elie Meledge Ade, Victoria Meledge Ade, et Josia Meledge Ade."
        

recit_2 = ("Mon grand-père s'appelle Augustin Adegbenlé (1905-2024)."
            "Il est L'époux de Ruth Oyénike. "
            "Ensemble ils ont 3 enfants : David Adégbenlé, Véronique Adégbenlé et Victor Adegbenlé."
            "David Adégbenlé est l'époux de Kadiatou. "
            "Ensemble, ils ont enfants :  Willfrid Adegbenlé, Terrence Adegbenlé, et Dorice Adegbenlé."
            "Véronique Adégbenlé est l'épouse de Sandé Oladélé. "
            "Ensemble, ils ont 3 enfants : Joel Sandé, Linda manuelle Sandé, et William Joseph Sandé."
            "Victor Adegbenlé est l'époux de Sonia Burgun. "
            "Ensemble, ils ont 4 enfants : Odilia meledge Ade, Elie Meledge Ade, Victoria Meledge Ade, et Josia Meledge Ade."
        )



prompt_projet = (recit_2 +   
                    ""+
                    "Utilise ces informations pour réaliser un arbre généalogique du meilleur de ton possible."+
                    "Les individus de la même génération (frères, soeurs) doivent figurer approximativement sur la même ligne."+
                    "Paul et Ethye doivent figurer sur la même ligne"+
                    "Micheline sa soeur, doit figurer sur la même ligne que Suzanne"+
                    
                    "Stocke les données de cet arbre dans un fichier JSON que je vais télécharger."+
                    "Affiche l'arbre généalogique.")

#messages = [
#          ( "system", "" ),
#          ( "human", prompt_projet),
#]
#ai_msg = llm.invoke(messages)
#ai_msg
#print(ai_msg.content)