
from __future__ import annotations

import os
import io
import base64
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any
import graphviz


from .generation_arbre import creer_arbre_genealogique
from .llm_client import extract_family_json

# Import des scrapers existants (inchangés)
from .lenecrologue import *
from .lepinecloutier import *
from .mesaieux import *
from .necroquebec import *

main = Flask(__name__, 
             template_folder="templates", 
             static_folder="static")

CORS(main)

#===========================================================================================#
#     Dossier pour les sorties générées : C'est dans ce dossier que seront stockés          #
#                                         - les fichiers .JSON ainsi que                    #
#                                         - les fichiers arbres.png                         #
#===========================================================================================#  

OUTPUT_FOLDER = os.path.join(main.root_path, "static", "output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def _ensure_graphviz_on_path():
    import os, shutil
    if shutil.which("dot"):
        return
    for c in (r"C:\Program Files\Graphviz\bin", r"C:\Program Files (x86)\Graphviz2.38\bin",
              rf"{os.environ.get('LOCALAPPDATA', '')}\Programs\Graphviz\bin"):
        if c and os.path.isdir(c):
            os.environ["PATH"] = c + os.pathsep + os.environ.get("PATH", "")
            if shutil.which("dot"):
                return
    raise RuntimeError("Graphviz 'dot' introuvable. Installe Graphviz et ajoute \\Graphviz\\bin au PATH.")

_ensure_graphviz_on_path()

def creer_image_from_json(fichier_json: str) -> str:
    """Génère l'image PNG (base64) à partir du JSON conformément à generation_arbre.py"""
    dot = creer_arbre_genealogique(fichier_json)
    dot.format = "png"
    image_data = dot.pipe()
    return base64.b64encode(image_data).decode("utf-8")


def traitement_llm(infos: str) -> str:
    """Appelle l'IA moderne pour obtenir un JSON structuré."""
    return extract_family_json(infos)


@main.get("/healthz")
def healthz():
    return {"status":"ok"}, 200


@main.route("/")
def apercu_video():
    return render_template("apercu_video.html")


@main.route("/page_de_presentation")
def page_de_presentation():
    return render_template("index.html")


@main.route("/traitement_lenecrologue", methods=["GET", "POST"])
def traitement_lenecrologue():
    if request.method == "POST":
        #mon_lien = request.form["url_defunt"]
        #infos = extraire_infos_jjcardinal(mon_lien)
        #fichier_json = traitement_llm(infos)
        #image_b64 = creer_image_from_json(fichier_json)
        return render_template(
            "traitement_lenecrologue.html"#,
            #fichier_json=fichier_json,
            #image_arbre=image_b64,
        )
    return render_template("traitement_lenecrologue.html")


@main.route("/traitement_lepinecloutier", methods=["GET", "POST"])
def traitement_lepinecloutier():
    if request.method == "POST":
        #mon_lien = request.form["url_defunt"]
        #infos = extraire_infos_lepinecloutier(mon_lien)
        #fichier_json = traitement_llm(infos)
        #image_b64 = creer_image_from_json(fichier_json)
        return render_template(
            "traitement_lepinecloutier.html"#,
            #fichier_json=fichier_json,
            #image_arbre=image_b64,
        )
    return render_template("traitement_lepinecloutier.html")


@main.route("/traitement_mesaieux", methods=["GET", "POST"])
def traitement_mesaieux():
    if request.method == "POST":
        #mon_lien = request.form["url_defunt"]
        #infos = extraire_infos_mesaieux(mon_lien)
        #fichier_json = traitement_llm(infos)
        #image_b64 = creer_image_from_json(fichier_json)
        return render_template(
            "traitement_mesaieux.html"#,
            #fichier_json=fichier_json,
            #image_arbre=image_b64,
        )
    return render_template("traitement_mesaieux.html")


@main.route("/traitement_necroquebec", methods=["GET", "POST"])
def traitement_necroquebec():
    if request.method == "POST":
        #mon_lien = request.form["url_defunt"]
        #infos = extraire_infos_necroquebec(mon_lien)
        #fichier_json = traitement_llm(infos)
        #image_b64 = creer_image_from_json(fichier_json)
        return render_template(
            "traitement_necroquebec.html"#,
            #fichier_json=fichier_json,
            #image_arbre=image_b64,
        )
    return render_template("traitement_necroquebec.html")


@main.route("/traitement_personnalise", methods=["GET", "POST"])
def traitement_personnalise():
    if request.method == "POST":
        # texte = request.form.get("texte_personnalise","").strip()
        # if not texte:
        #    return render_template("traitement_personnalise.html", fichier_json="", image_arbre="")
        texte = request.form["texte_personnalise"]
        fichier_json = traitement_llm(texte)
        image_b64 = creer_image_from_json(fichier_json)

        return render_template(
            "traitement_personnalise.html",
            fichier_json=fichier_json,
            image_arbre=image_b64,
        )
    return render_template("traitement_personnalise.html")


@main.route('/download_json')
def download_json():
    # Récupérer les données de la session ou les passer comme paramètre
    data = request.args.get('data')
    
    # Créer un fichier JSON en mémoire
    json_file = io.BytesIO()
    json_file.write(json.dumps(data, indent=4).encode('utf-8'))
    json_file.seek(0)
    
    return send_file(json_file, 
                     mimetype='application/json', 
                     as_attachment=True, 
                     download_name='fichier_json_defunt.json')

@main.route('/download_arbre')
def download_arbre():

    data = request.args.get('data') 
    print(data)
    print(type(data))
    #arbre = creer_arbre_genealogique(data)
    try:
        # Créer l'arbre généalogique
        dot = creer_arbre_genealogique(data)
        
        # Créer un objet BytesIO pour stocker l'image
        image_stream = io.BytesIO()
        
        # Rendre le graphe en format PNG et le sauvegarder dans image_stream
        dot.format = 'png'
        image_data = dot.pipe()
        image_stream.write(image_data)
        
        # Remettre le curseur au début du stream
        image_stream.seek(0)
        
        # Envoyer le fichier au client
        return send_file(
            image_stream,
            mimetype='image/png',
            as_attachment=True,
            download_name='arbre_genealogique.png'
        )
    except Exception as e:
        return str(e), 500

#----------------------------------------------------------------------------------#

if __name__ == "__main__":
    main.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
