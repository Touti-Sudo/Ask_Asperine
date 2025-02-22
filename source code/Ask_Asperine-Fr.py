from flask import Flask, send_from_directory, request, jsonify, render_template
import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')  
import matplotlib.animation as animation
import os
import threading 
import tkinter as tk
from PIL import Image, ImageTk
import time
import webbrowser

if not os.path.exists("static"):
    os.makedirs("static")

app = Flask(__name__)
aspirin_data = {
    "histoire": {
        "description": "📜 L'aspirine a été synthétisée en 1897 par 🧑‍🔬 Félix Hoffmann chez Bayer. Avant cela, 🌿 la salicine, extraite du saule, était utilisée depuis l'Antiquité pour traiter la douleur et la fièvre.",
        "dates_importantes": [
            "🏺 Antiquité : Utilisation de l'écorce de saule pour la douleur et la fièvre.",
            "🧪 1828 : Johann Buchner isole la salicine.",
            "⚗️ 1853 : Charles Frédéric Gerhardt réalise la première synthèse de l'acide acétylsalicylique.",
            "💊 1897 : Félix Hoffmann synthétise l'aspirine moderne chez Bayer."
        ]
    },
    "decouverte": {
        "description": "🔬 L'utilisation médicinale de l'écorce de saule remonte à l'Antiquité. En 1828, Johann Buchner isole la salicine, et en 1897, Félix Hoffmann synthétise l'acide acétylsalicylique, créant l'aspirine moderne.",
        "personnages_cles": [
            "🌿 Hippocrate : Utilisait l'écorce de saule pour soulager la douleur.",
            "🧪 Johann Buchner : A isolé la salicine en 1828.",
            "⚗️ Charles Frédéric Gerhardt : A réalisé la première synthèse de l'acide acétylsalicylique en 1853.",
            "💊 Félix Hoffmann : A synthétisé l'aspirine en 1897."
        ]
    },
    "preparation": {
        "reactifs": ["🧪 Acide salicylique", "⚗️ Anhydride acétique", "🛠️ Acide sulfurique (catalyseur)"],
        "reaction": "⚗️ Acide salicylique + Anhydride acétique → 💊 Acide acétylsalicylique (Aspirine) + 🧴 Acide acétique",
        "etapes": [
            "1️⃣ Mélanger l'acide salicylique avec l'anhydride acétique.",
            "2️⃣ Ajouter quelques gouttes d'acide sulfurique.",
            "3️⃣ Chauffer à 🔥 50-60°C pendant 15 minutes.",
            "4️⃣ Refroidir et ajouter de l'eau froide pour précipiter l'aspirine.",
            "5️⃣ Filtrer et sécher les cristaux obtenus."
        ]
    },
    "synthese_chimique": {
        "reactifs": ["🧪 Acide salicylique", "⚗️ Anhydride acétique", "🛠️ Acide sulfurique (catalyseur)"],
        "reactions": "C7H6O3 + C4H6O3 → C9H8O4 + C2H4O2",
        "reaction": "⚗️ Acide salicylique + Anhydride acétique → 💊 Acide acétylsalicylique (Aspirine) + 🧴 Acide acétique",
        "etapes": [
            "1️⃣ Mélanger l'acide salicylique avec l'anhydride acétique.",
            "2️⃣ Ajouter quelques gouttes d'acide sulfurique.",
            "3️⃣ Chauffer à 🔥 50-60°C pendant 15 minutes.",
            "4️⃣ Refroidir et ajouter de l'eau froide pour précipiter l'aspirine.",
            "5️⃣ Filtrer et sécher les cristaux obtenus."
        ]
    },
    "utilisations_anciennes": [
        "🏺 Antiquité : Infusions d’écorce de saule pour la 🌡️ fièvre et la 🤕 douleur.",
        "📜 -400 av. J.-C. : 🏛️ Hippocrate l’utilise contre les douleurs articulaires.",
        "⏳ Moyen Âge : Utilisée par les guérisseurs et herboristes.",
        "🧪 18e siècle : Edward Stone découvre ses effets et la compare au quinquina."
    ],
    "utilisations_modernes": [
        "💊 Antidouleur : Soulage les maux de tête et douleurs musculaires.",
        "🔥 Anti-inflammatoire : Traitement des rhumatismes et de l'arthrite.",
        "🌡️ Antipyrétique : Réduit la fièvre.",
        "❤️ Anticoagulant : Prévention des AVC et infarctus."
    ],
    "effets_secondaires": [
        "⚠️ Irritations de l'estomac et risque d'ulcères.",
        "🩸 Troubles hémorragiques (fluidification du sang).",
        "🤧 Réactions allergiques possibles.",
        "🚫 Ne pas prendre en cas d'allergie à l'aspirine ou de troubles de la coagulation."
    ],
    "generalites": {
        "description": "💊 L'aspirine, ou acide acétylsalicylique, est un médicament anti-inflammatoire non stéroïdien (AINS) 🦠 qui aide à soulager la douleur 😖, réduire la fièvre 🌡️ et diminuer l'inflammation 🔥. Son principe actif bloque les enzymes qui produisent des substances chimiques appelées prostaglandines, responsables de la douleur et de l'inflammation 🤕.",
        "proprietes": [
            "Antidouleur (analgésique)",
            "Anti-inflammatoire",
            "Antipyrétique (réduit la fièvre)",
            "Anticoagulant (fluidifie le sang)"
        ]
    }
}
def get_aspirin_info(topic):
    return aspirin_data.get(topic, "Je ne trouve pas cette information sur l'aspirine.")

if not os.path.exists("static"):
    os.makedirs("static")

app = Flask(__name__)


def draw_schema():
    try:
        # Crée un schéma avec matplotlib
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 5)
        ax.axis("off")
        
        ax.text(1, 2.5, "Acide salicylique", fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightblue', edgecolor='black'))
        ax.text(5, 2.5, "+ Anhydride acétique", fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightgreen', edgecolor='black'))
        ax.text(9, 2.5, "= Aspirine", fontsize=12, ha='center', va='center', bbox=dict(facecolor='lightcoral', edgecolor='black'))
        
        ax.arrow(2, 2.5, 2, 0, head_width=0.2, head_length=0.3, fc='black', ec='black')
        ax.arrow(6, 2.5, 2, 0, head_width=0.2, head_length=0.3, fc='black', ec='black')
        
        plt.title("Schéma de la Synthèse de l'Aspirine")
        
    
        plt.savefig("static/schema.png")
        plt.close()
        print("Schéma généré et sauvegardé avec succès.")
    except Exception as e:
        print(f"Erreur lors de la génération du schéma : {e}")

def show_schema_tkinter():
    threading.Thread(target=open_tkinter_window, daemon=True).start()

def open_tkinter_window():
    root = tk.Tk()
    root.title("Schéma de la Synthèse de l'Aspirine")

    image = Image.open("static/schema.png")
    image = image.resize((600, 400))
    photo = ImageTk.PhotoImage(image)

    label = tk.Label(root, image=photo)
    label.image = photo
    label.pack()

    close_btn = tk.Button(root, text="Fermer", command=root.destroy)
    close_btn.pack()

    root.mainloop()

def chatbot(question):
    question = question.lower().strip()  

    if any(word in question for word in ["merci", "merci beaucoup", "thanks", "thank you"]):
        return "🤖 Je t'en prie ! N'hésite pas à me poser d'autres questions si tu as besoin d'aide. 😊"

    elif any(word in question for word in ["qui es-tu", "présentation","tu es qui", "présente-toi", "que fais-tu", "comment fonctionnes-tu", "chatbot", "qui t'a créé", "programmé","créateur","anes kada","anes","kada","projet","20/20","bonjour"]):
        info = "🤖 Bonjour ! Je suis Ask_Asperine, une IA non générative (bot) créée par Anes Kada avec Python pour son projet de technologie. Je suis spécialisée dans les informations sur l'aspirine. Pose-moi une question, et je ferai de mon mieux pour te répondre ! 😊"
        return info
    

    elif any(word in question for word in ["effets secondaires","Quels sont ses effets secondaires ", "risques", "danger", "dangereuse", "allergie", "contre-indications", "saignements","risque","saignement","estomac","contre-indication","ulcere","symptome","complication","interdit","enfant","probleme","santé","sante","symptôme"]):
        info2 = get_aspirin_info("effets_secondaires")
        return "\n".join(info2)
    

    elif any(word in question for word in ["découverte", "découvertes","qui la découvert", "découvert","origine","origin","origines","origins","moyen age"]):
        info = get_aspirin_info("decouverte")
        return info["description"]
    

    elif any(word in question for word in ["histoire","qui la créé", "origine", "quand", "qui a inventé", "qui a découvert"]):
        info = get_aspirin_info("histoire")
        return info["description"]
    

    elif any(word in question for word in ["ancienne","anciennes","antiquité", "traditionnelle", "histoire utilisation","traditionnel","plante","moyen","age","naturel","avant"]):
        info = get_aspirin_info("utilisations_anciennes")
        return "\n".join(info)
    
    elif "merci" in question:
        return 
    elif any(word in question for word in ["utilisations modernes","utilisations","positive", "aujourd’hui", "actuelles", "antidouleur", "anti-inflammatoire", "fièvre", "anticoagulant", "AVC", "infarctus", "arthrite", "cardiologie"]):
        info = get_aspirin_info("utilisations_modernes")
        return "\n".join(info)
    

    elif any(word in question for word in ["préparer", "fabriquer", "synthèse", "synthétiser", "réactifs", "réaction chimique", "formule"]):
        info = get_aspirin_info("preparation")
        return f"Reactifs : {', '.join(info['reactifs'])}\nRéaction : {info['reaction']}\nÉtapes :\n" + "\n".join(info["etapes"])
    

    elif any(word in question for word in ["chimique", "synthèse chimique", "synthétisée", "produite"]):
        info = get_aspirin_info("synthese_chimique")
        return f"Reactifs : {', '.join(info['reactifs'])}\nRéactions : {info['reactions']}\nÉtapes :\n" + "\n".join(info["etapes"])
    

    elif any(word in question for word in ["définit l'aspirine", "c'est quoi l'aspirine", "qu'est-ce que l'aspirine", "explique l'aspirine", "fonctionne l'aspirine"]):
        info = get_aspirin_info("generalites")
        return info["description"]
    

    else:
        return "Je ne suis pas sûr de comprendre. Essayez une autre question ! Ou vérifie ton orthographe !"


@app.route("/")
def home():
    return render_template("index.html", message="Bonjour, et Bienvenue dans Ask_Asperine ! Créé par Anes Kada pour son projet de technologie. (svp si vous êtes la prof, donnez-moi 20/20 😆)", time=int(time.time()))

@app.route("/chatbot", methods=["POST"])
def chatbot_api():
    question = request.form.get("question")
    if not question:
        return jsonify({"error": "Veuillez poser une question"})
    
    response = chatbot(question)
    if isinstance(response, (list, dict)):
        response = "\n".join(response) if isinstance(response, list) else str(response)
    return jsonify({"response": response})
@app.route("/static/audio/<filename>")
def get_audio(filename):
    return send_from_directory("static/audio", filename, as_attachment=False)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
url="http://127.0.0.1:5000"
webbrowser.open(url)

if __name__ == "__main__":
    app.run(debug=True)