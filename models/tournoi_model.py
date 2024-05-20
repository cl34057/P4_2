import json
import os
import random
from typing import List
from models.joueur_model import Joueur
import datetime


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
        self.tours = []  # Liste pour stocker les tours
        self.nb_tours = 0  # Initialisation de l'attribut pour compter le nombre de tours


    def generer_donnees_json(self):
        # Générer les données à sauvegarder dans le fichier JSON
        data = {
            "nom": self.nom,
            "date_debut": str(self.date_debut),
            "date_fin": str(self.date_fin),
            "nombre_joueurs_inscrits": self.nombre_inscrits,
            "nombre_rondes": self.nb_rondes,
            "rondes": [ronde.__dict__ for ronde in self.tours]
        }
        return data

    def creer_fichier_json(self):
        # Créer un fichier JSON pour le tournoi et y sauvegarder les données
        filename = f"data/tournaments/{self.nom}.json"
        with open(filename, "w") as file:
            data = self.generer_donnees_json()
            json.dump(data, file, indent=4)
            
    def mise_a_jour_fichier_json(self):
        # Implémentez la logique pour générer et mettre à jour les fichiers JSON pour chaque tournoi
        if not os.path.exists("data/tournaments"):
            os.makedirs("data/tournaments")
        self.creer_fichier_json()
            
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
    def charger_joueurs(self):
        # Charger les joueurs depuis le fichier JSON
        filepath = f"data/tournaments/{self.nom}_joueurs.json"
        if os.path.exists(filepath):
            with open(filepath, "r") as file:
                self.joueurs = json.load(file)
    def sauvegarder_joueurs(self):
        # Sauvegarde les joueurs dans le fichier JSON à chaque modification
        filepath = f"data/tournaments/{self.nom}_joueurs.json"
        with open(filepath, "w") as file:
            json.dump(self.joueurs, file, indent=4)
    def creer_tour(self):
        """
        Crée un nouveau tour et l'ajoute à la liste des tours du tournoi.
        """
        if self.date_fin < datetime.datetime.now().date():
            print("Impossible de créer un nouveau tour. Le tournoi est terminé.")
            return
        
        if len(self.tours) >= self.nb_rondes:
            print("Impossible de créer un nouveau tour. Le nombre maximum de tours est atteint.")
            return

        # Initialisation de l'attribut pour compter le nombre de tours
        self.nb_tours = len(self.tours)
        
        # Créer un nouveau tour et l'ajouter à la liste des tours du tournoi
        tour = Tour(self.nb_tours + 1, datetime.datetime.now(), "en cours")
        self.tours.append(tour)
        self.nb_tours += 1
        
        # Générer et mettre à jour les fichiers JSON pour chaque tournoi avec les informations appropriées
        self.mise_a_jour_fichier_json()

  
class Tour:
    def __init__(self, numero, date, statut):
        """
        Initialise un objet Tour avec son numéro, sa date et son statut.

        Args:
            numero (int): Le numéro du tour.
            date (datetime): La date du tour.
            statut (str): Le statut du tour.

        Attributes:
            numero (int): Le numéro du tour.
            date (datetime): La date du tour.
            statut (str): Le statut du tour.
            matchs (list): Liste des matchs du tour.
            rondes (list): Liste des rondes du tour.
            nb_tours (int): Nombre total de tours dans le tournoi.
        """
        self.numero = numero
        self.date = date
        self.statut = statut
        self.matchs = []  # Liste pour stocker les matchs
        self.rondes = []  # Initialisation de l'attribut pour stocker les rondes
        self.joueurs: List[Joueur] = []  # Spécifiez le type de joueurs comme une liste de Joueur
    
    def appariement_tour(self):
        """
        Effectue l'appariement des joueurs pour le tour en cours.
        """
        # Vérifier s'il y a assez de joueurs pour créer des paires
            # Initialisation de l'attribut pour stocker les rondes
        self.rondes = []
            # Vérifier s'il y a assez de joueurs pour créer des paires
        if len(self.joueurs) < 2:
                print("Nombre insuffisant de joueurs pour créer des paires.")
                return
            # Mélanger aléatoirement la liste des joueurs au début du premier tour
        if len(self.rondes) == 0:
                random.shuffle(self.joueurs)
            
            # Trier les joueurs en fonction de leur nombre total de points dans le tournoi
        self.joueurs.sort(key=lambda joueur: joueur.points_total, reverse=True)

            # Créer des paires en associant les joueurs dans l'ordre
        pairs = []
        for i in range(0, len(self.joueurs), 2):
                if i + 1 < len(self.joueurs):
                    pairs.append((self.joueurs[i], self.joueurs[i + 1]))

            # Vérifier les paires précédentes pour éviter les matchs identiques
        if len(self.rondes) > 0:
                paires_precedentes = {(match["joueur_blanc"], match["joueur_noir"]) for ronde in self.rondes for match in ronde["matchs"]}
                pairs = [(blanc, noir) for blanc, noir in pairs if (blanc, noir) not in paires_precedentes]

            # Créer une ronde avec les paires
        ronde = {
                "numero": len(self.rondes) + 1,
                "matchs": []
        }

        for pair in pairs:
                match = {
                    "joueur_blanc": pair[0],
                    "joueur_noir": pair[1],
                    "resultat": ""
                }
                ronde["matchs"].append(match)

            # Ajouter la ronde à la liste des rondes du tournoi
        self.rondes.append(ronde)


    
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
        joueurs_index = data.get('joueurs', [])  # Récupérer les index des joueurs
        joueurs = self.charger_joueurs_par_index(joueurs_index)  # Charger les joueurs associés à leurs index
        tournoi = Tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi, joueurs)
        return tournoi
    
    def charger_joueurs_par_index(self, joueurs_index):
        joueurs = []
        joueur_trouve = False  # Variable pour suivre si un joueur a été trouvé

        # Charger les joueurs associés à leurs index à partir du fichier JSON des joueurs
        if os.path.exists("data/joueur.json"):
            with open("data/joueur.json", "r") as file:
                all_players = json.load(file)
                for index in joueurs_index:
                    joueur_trouve = False  # Réinitialiser la variable pour chaque itération
                    for player_data in all_players:
                        if player_data['index'] == index:
                            try:
                                # Convertir la date de naissance en objet datetime
                                date_naissance = datetime.datetime.strptime(player_data['date_naissance'], '%Y-%m-%d').date()
                            except ValueError:
                                print(f"La date de naissance pour le joueur avec l'index {index} n'est pas au bon format.")
                                continue  # Passer à l'itération suivante si le format de date est incorrect
                                
                            joueur = Joueur(
                                index=index,
                                nom=player_data['nom'],
                                prenom=player_data['prenom'],
                                date_naissance=date_naissance,
                                elo=player_data['elo']
                            )
                            joueurs.append(joueur)
                            joueur_trouve = True  # Définir la variable à True si le joueur est trouvé
                            break  # Sortir de la boucle interne une fois que le joueur est trouvé
                    if not joueur_trouve:
                        print(f"Les données pour le joueur avec l'index {index} n'ont pas été trouvées.")
        else:
            print("Le fichier des joueurs n'existe pas.")

        return joueurs

        
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
    def trouver_tournoi_par_index(self, index):
        for tournoi in self.tournois:
            if tournoi.index == index:
                return tournoi
        return None