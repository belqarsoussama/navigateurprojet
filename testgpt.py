import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
# Assurez-vous d'avoir installé la bibliothèque requests
import requests

def effectuer_recherche():
    # Obtenez le texte de l'entrée utilisateur
    texte_recherche = entry.get()

    # Effectuez une recherche ou appelez une API ici
    # Dans cet exemple, j'utilise un appel simple à l'API DuckDuckGo (pas d'IA réelle ici)
    url = f"https://api.duckduckgo.com/?q={texte_recherche}&format=json"
    try:
        response = requests.get(url)
        data = response.json()
        # Récupérez la réponse de l'API ou faites quelque chose avec les résultats
        reponse_api = data.get('Abstract', 'Aucun résultat trouvé.')
        # Affichez la réponse dans la zone de texte
        text_box.delete(1.0, tk.END)  # Efface le contenu précédent
        text_box.insert(tk.END, reponse_api)
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

# Créez la fenêtre principale
fenetre = tk.Tk()
fenetre.title("Recherche avec Tkinter et API")

# Créez une étiquette d'instruction
label = tk.Label(fenetre, text="Entrez votre recherche:")
label.pack(pady=10)

# Créez une entrée pour le texte
entry = tk.Entry(fenetre, width=30)
entry.pack(pady=10)

# Créez un bouton pour déclencher la recherche
bouton_recherche = tk.Button(fenetre, text="Rechercher", command=effectuer_recherche)
bouton_recherche.pack(pady=10)

# Créez une zone de texte déroulante pour afficher les résultats
text_box = scrolledtext.ScrolledText(fenetre, width=40, height=10, wrap=tk.WORD)
text_box.pack(pady=10)

# Lancez la boucle principale
fenetre.mainloop()
