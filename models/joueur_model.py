import json
import os
import datetime
from config import MAX_JOUEURS
class Joueur:
    def __init__(self, index, nom: str, prenom: str, date_naissance: datetime.date, elo: int):
        self.index = index
        self.nom = nom
        self.prenom = prenom
        self.date_naissance = date_naissance
        self.elo = elo

class JoueurManager:
    MAX_JOUEURS = 8
    FICHIER_JSON = "data/joueur.json"

    def __init__(self):
        self.joueurs = []
        self.charger_joueurs()

    def charger_joueurs(self):
        if os.path.exists(self.FICHIER_JSON):
            with open(self.FICHIER_JSON, "r") as file:
                data = json.load(file)
                self.joueurs = [self.convertir_dict_vers_joueur(joueur) for joueur in data]

    def sauvegarder_joueurs(self):
        with open(self.FICHIER_JSON, "w") as file:
            data = [self.convertir_joueur_vers_dict(joueur) for joueur in self.joueurs]
            json.dump(data, file, indent=4)

    def ajouter_joueur(self, nom, prenom, date_naissance, elo):
        if len(self.joueurs) < self.MAX_JOUEURS:
            index = len(self.joueurs) + 1  # Index basé sur la longueur actuelle de la liste des joueurs
            nouveau_joueur = Joueur(index, nom, prenom, date_naissance, elo)
            self.joueurs.append(nouveau_joueur)
            self.sauvegarder_joueurs()
            return True
        else:
            print("Limite de joueurs atteinte. Impossible d'ajouter un nouveau joueur.")
            return False

    def modifier_joueur(self, index, nom, prenom, date_naissance, elo):
        self.joueurs[index - 1].nom = nom
        self.joueurs[index - 1].prenom = prenom
        self.joueurs[index - 1].date_naissance = date_naissance
        self.joueurs[index - 1].elo = elo
        self.sauvegarder_joueurs()

    def supprimer_joueur(self, index):
        del self.joueurs[index - 1]
        # Mettre à jour les index des joueurs suivant le joueur supprimé
        for joueur in self.joueurs[index - 1:]:
            joueur.index -= 1
        self.sauvegarder_joueurs()



    def convertir_joueur_vers_dict(self, joueur):
        return {
            'index': joueur.index,
            'nom': joueur.nom,
            'prenom': joueur.prenom,
            'date_naissance': joueur.date_naissance.isoformat() if isinstance(joueur.date_naissance, datetime.date) else joueur.date_naissance,
            'elo': joueur.elo
        }

    def convertir_dict_vers_joueur(self, data):
        return Joueur(data['index'], data['nom'], data['prenom'], 
                      datetime.datetime.strptime(data['date_naissance'], '%Y-%m-%d').date() if isinstance(data['date_naissance'], str) else data['date_naissance'], 
                      data['elo'])
