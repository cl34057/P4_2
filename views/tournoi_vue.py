from controllers.tournoi_controller import TournoiController
from models.joueur_model import Joueur
from models.joueur_model import JoueurManager
import datetime
class TournoiVue:
    def __init__(self):
        self.tournoi_controller = TournoiController()
        self.joueur_manager = JoueurManager()
    def afficher_menu(self):
        print("===== Menu Tournoi =====")
        print("1. Créer un nouveau tournoi")
        print("2. Modifier un tournoi")
        print("3. Supprimer un tournoi")
        print("4. Afficher la liste des tournois")
        print("5. Ajouter joueur du tournoi")
        print("6. Quitter")

    def saisir_tournoi(self):
        while True:
            nom = input("Nom du tournoi : ")
            if not nom.replace(' ', '').isalnum() or not nom.strip():
                print("Le nom du tournoi doit contenir uniquement des caractères alphanumériques et peut contenir des espaces.")
                continue
            date_debut = input("Date de début (format YYYY-MM-DD) : ")
            date_fin = input("Date de fin (format YYYY-MM-DD) : ")
            try:
                date_debut = datetime.datetime.strptime(date_debut, '%Y-%m-%d').date()
                date_fin = datetime.datetime.strptime(date_fin, '%Y-%m-%d').date()
                if date_fin < date_debut:
                    print("La date de fin doit être ultérieure à la date de début.")
                    continue
                return nom, date_debut, date_fin
            except ValueError:
                print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")

    def modifier_tournoi(self):
        index = self.saisir_index_tournoi()
        nom, date_debut, date_fin = self.saisir_tournoi()
        self.tournoi_controller.modifier_tournoi(index, nom, date_debut, date_fin)
        print("Tournoi modifié avec succès.")

    def supprimer_tournoi(self):
        index = self.saisir_index_tournoi()
        self.tournoi_controller.supprimer_tournoi(index)
        print("Tournoi supprimé avec succès.")

    def afficher_liste_tournois(self):
        tournois = self.tournoi_controller.tournoi_manager.tournois
        print("===== Liste des Tournois =====")
        for tournoi in tournois:
            print(f"Index: {tournois.index(tournoi) + 1}, Nom: {tournoi.nom}, Date de début: {tournoi.date_debut}, Date de fin: {tournoi.date_fin}")

    def saisir_index_tournoi(self):
        while True:
            try:
                index = int(input("Entrez l'index du tournoi : "))
                if index < 1 or index > len(self.tournoi_controller.tournoi_manager.tournois):
                    print("Index invalide. Veuillez entrer un index valide.")
                    continue
                else:
                    return index
            except ValueError:
                print("Veuillez entrer un nombre entier.")

    def saisir_joueurs_participants(self, tournoi_index):
        joueurs_disponibles = self.joueur_manager.joueurs
        joueurs_selectionnes = []

        print("===== Sélection des joueurs participants =====")
        while True:
            print("Joueurs disponibles :")
            for joueur in joueurs_disponibles:
                print(f"Index: {joueurs_disponibles.index(joueur) + 1}, Nom: {joueur.nom}, Prénom: {joueur.prenom}, Elo: {joueur.elo}")
            choix = input("Entrez l'index du joueur à ajouter (ou entrez 'terminé' pour terminer) : ")

            if choix.lower() == 'terminé':
                break

            try:
                index_joueur = int(choix)
                if 1 <= index_joueur <= len(joueurs_disponibles):
                    #joueur_choisi = joueurs_disponibles[index_joueur - 1]
                    joueurs_selectionnes.append(choix)
                    joueurs_disponibles.remove(choix)
                else:
                    print("Index invalide. Veuillez entrer un index valide.")
            except ValueError:
                print("Veuillez entrer un nombre entier.")

            continuer = input("Voulez-vous ajouter un autre joueur ? (o/n) : ")
            if continuer.lower() != 'o':
                break

        self.tournoi_controller.ajouter_joueurs_au_tournoi(tournoi_index, joueurs_selectionnes)
        print("Joueurs ajoutés au tournoi avec succès.")