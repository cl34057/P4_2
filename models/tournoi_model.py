import json
import os
import datetime
from config import MAX_TOURNOIS

class Tournoi:
    def __init__(self, index, nom, date_debut, date_fin):
        self.index = index
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.joueurs = []
    def ajouter_joueurs(self, joueurs):
        self.joueurs.extend(joueurs)
class TournoiManager:
    MAX_TOURNOIS = 5
    FICHIER_JSON = "data/tournoi.json"

    def __init__(self):
        self.tournois = []
        self.joueurs = []
        self.charger_tournois()

    def charger_tournois(self):
        if os.path.exists(self.FICHIER_JSON):
            with open(self.FICHIER_JSON, "r") as file:
                data = json.load(file)
                self.tournois = [self.convertir_dict_vers_tournoi(tournoi) for tournoi in data]

    def sauvegarder_tournois(self):
        with open(self.FICHIER_JSON, "w") as file:
            data = [self.convertir_tournoi_vers_dict(tournoi) for tournoi in self.tournois]
            json.dump(data, file, indent=4)

    def ajouter_tournoi(self, nom, date_debut, date_fin):
        if len(self.tournois) < self.MAX_TOURNOIS:
            index = len(self.tournois) + 1  
            nouveau_tournoi = Tournoi(index, nom, date_debut, date_fin)
            self.tournois.append(nouveau_tournoi)
            self.sauvegarder_tournois()
            return True
        else:
            print("Limite de tournois atteinte. Impossible d'ajouter un nouveau tournoi.")
            return False

    def modifier_tournoi(self, index, nom, date_debut, date_fin):
        self.tournois[index - 1].nom = nom
        self.tournois[index - 1].date_debut = date_debut
        self.tournois[index - 1].date_fin = date_fin
        self.sauvegarder_tournois()

    def supprimer_tournoi(self, index):
        del self.tournois[index - 1]
        for tournoi in self.tournois[index - 1:]:
            tournoi.index -= 1
        self.sauvegarder_tournois()

    def ajouter_joueurs_au_tournoi(self, tournoi_index, joueurs):
        tournoi = self.tournois[tournoi_index - 1]
        for joueur in joueurs:
            if self.verifier_chevauchement_dates(joueur, tournoi):
                print(f"Impossible pour le joueur {joueur.nom} de participer au tournoi {tournoi.nom}. Les périodes se chevauchent.")
            else:
                 tournoi.joueurs.append(joueur)
        self.sauvegarder_tournois()  # Déplacement de l'indentation

    def verifier_chevauchement_dates(self, joueur, tournoi):
        for tournoi_existant in self.tournois:
            if tournoi_existant != tournoi and joueur in tournoi_existant.joueurs:
                if tournoi_existant.date_debut <= tournoi.date_fin and tournoi_existant.date_fin >= tournoi.date_debut:
                    return True
        return False
    def convertir_tournoi_vers_dict(self, tournoi):
        return {
            'index': tournoi.index,
            'nom': tournoi.nom,
            'date_debut': tournoi.date_debut.isoformat() if isinstance(tournoi.date_debut, datetime.date) else tournoi.date_debut,
            'date_fin': tournoi.date_fin.isoformat() if isinstance(tournoi.date_fin, datetime.date) else tournoi.date_fin,
            'joueurs': [joueur.index for joueur in tournoi.joueurs]
        }
    
    def convertir_dict_vers_tournoi(self, data):
        tournoi = Tournoi(data['index'], data['nom'],
                          datetime.datetime.strptime(data['date_debut'], '%Y-%m-%d').date(),
                          datetime.datetime.strptime(data['date_fin'], '%Y-%m-%d').date())
        return tournoi
    def convertir_tournoi_vers_dict(self, tournoi):
        joueurs_noms = [joueur.nom for joueur in tournoi.joueurs]
        nombre_inscrits = len(tournoi.joueurs)
        
        return {
            'index': tournoi.index,
            'nom': tournoi.nom,
            'date_debut': tournoi.date_debut.isoformat() if isinstance(tournoi.date_debut, datetime.date) else tournoi.date_debut,
            'date_fin': tournoi.date_fin.isoformat() if isinstance(tournoi.date_fin, datetime.date) else tournoi.date_fin,
            'joueurs': joueurs_noms,
            'nombre_inscrits': nombre_inscrits
        }