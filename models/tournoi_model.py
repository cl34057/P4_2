import json
import os
import datetime
import re

class Tournoi:
    def __init__(self, index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi, joueurs=None):
        self.index = index
        self.nom = nom
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.nb_max_joueurs = nb_max_joueurs
        self.nb_rondes = nb_rondes
        self.type_tournoi = type_tournoi
        self.joueurs = joueurs if joueurs is not None else []
        self.nombre_inscrits = len(self.joueurs)  # Ajout de l'attribut nombre_inscrits


    def ajouter_joueurs(self, joueurs):
        self.joueurs.extend(joueurs)
        self.nombre_inscrits = len(self.joueurs)  # Mettre à jour le nombre d'inscrits

    def supprimer_joueur(self, joueur):
        if joueur in self.joueurs:
            self.joueurs.remove(joueur)
            self.nombre_inscrits = len(self.joueurs)  # Mettre à jour le nombre d'inscrits
            print(f"Le joueur {joueur.nom} a été supprimé du tournoi {self.nom}.")
        else:
            print(f"Le joueur {joueur.nom} n'est pas inscrit dans ce tournoi.")

class TournoiManager:
    MAX_TOURNOIS = 15
    FICHIER_JSON = "data/tournoi.json"

    def __init__(self):
        self.tournois = []
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

    def ajouter_tournoi(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
        if len(self.tournois) < self.MAX_TOURNOIS:
            index = len(self.tournois) + 1  
            nouveau_tournoi = Tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
            self.tournois.append(nouveau_tournoi)
            self.sauvegarder_tournois()
            return True
        else:
            print("Limite de tournois atteinte. Impossible d'ajouter un nouveau tournoi.")
            return False

    def modifier_tournoi(self, index, nom=None, date_debut=None, date_fin=None, nb_max_joueurs=None, nb_rondes=None, type_tournoi=None):
        tournoi = self.tournois[index - 1]
        if nom is not None:
            tournoi.nom = nom
        if date_debut is not None:
            tournoi.date_debut = date_debut
        if date_fin is not None:
            tournoi.date_fin = date_fin
        if nb_max_joueurs is not None:
            tournoi.nb_max_joueurs = nb_max_joueurs
        if nb_rondes is not None:
            tournoi.nb_rondes = nb_rondes
        if type_tournoi is not None:
            tournoi.type_tournoi = type_tournoi
        self.sauvegarder_tournois()
    def supprimer_tournoi(self, index):
        del self.tournois[index - 1]
        self.sauvegarder_tournois()

    def supprimer_joueur_du_tournoi(self, tournoi_index, joueur):
        tournoi = self.tournois[tournoi_index - 1]
        tournoi.supprimer_joueur(joueur)
        tournoi.nombre_inscrits -= 1  # Mettre à jour le nombre d'inscrits
        self.sauvegarder_tournois()

    def ajouter_joueurs_au_tournoi(self, tournoi_index, joueurs):
        tournoi = self.tournois[tournoi_index - 1]
        tournoi.ajouter_joueurs(joueurs)
        tournoi.nombre_inscrits += len(joueurs)  # Mettre à jour le nombre d'inscrits
        self.sauvegarder_tournois()

    def convertir_dict_vers_tournoi(self, data):
        index = data['index']
        nom = data['nom']
        date_debut = datetime.datetime.strptime(data['date_debut'], '%Y-%m-%d').date()
        date_fin = datetime.datetime.strptime(data['date_fin'], '%Y-%m-%d').date()
        nb_max_joueurs = data.get('nb_max_joueurs', 0)
        nb_rondes = data.get('nb_rondes', 0)
        type_tournoi = data.get('type_tournoi', '')
        joueurs = []  # Assurez-vous de récupérer correctement les joueurs depuis les données du fichier JSON
        tournoi = Tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi, joueurs)
        return tournoi

    def convertir_tournoi_vers_dict(self, tournoi):
        joueurs_index = [joueur.index for joueur in tournoi.joueurs]  # Récupérer les index des joueurs
        return {
            'index': tournoi.index,
            'nom': tournoi.nom,
            'date_debut': tournoi.date_debut.isoformat() if isinstance(tournoi.date_debut, datetime.date) else tournoi.date_debut,
            'date_fin': tournoi.date_fin.isoformat() if isinstance(tournoi.date_fin, datetime.date) else tournoi.date_fin,
            'joueurs': joueurs_index,  # Stocker les index des joueurs
            'nombre_inscrits': len(tournoi.joueurs)
    }

