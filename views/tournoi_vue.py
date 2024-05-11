import datetime
import re
from controllers.tournoi_controller import TournoiController
from models.joueur_model import JoueurManager

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
        print("5. Ajouter un joueur au tournoi")
        print("6. Afficher les détails d'un tournoi")
        print("7. Supprimer un joueur du tournoi")
        print("8. Quitter")

    def saisir_tournoi(self):
        while True:
            nom = input("Nom du tournoi : ")
            if not re.match("^[a-zA-Z0-9 ]+$", nom):
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
                nb_max_joueurs = int(input("Nombre maximal de joueurs : "))
                nb_rondes = int(input("Nombre de rondes : "))
                type_tournoi = input("Type de tournoi : ")
                return nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi
            except ValueError:
                print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")

    def modifier_tournoi(self):
        index = self.saisir_index_tournoi()
        nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi = self.saisir_tournoi()
        self.tournoi_controller.modifier_tournoi(index, nom, date_debut, date_fin)

    def supprimer_tournoi(self):
        index = self.saisir_index_tournoi()
        self.tournoi_controller.supprimer_tournoi(index)

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
        tournoi = self.tournoi_controller.tournoi_manager.tournois[tournoi_index - 1]
        joueurs_deja_inscrits = tournoi.joueurs
        joueurs_disponibles = [joueur for joueur in self.joueur_manager.joueurs if joueur not in joueurs_deja_inscrits]
        joueurs_selectionnes = []

        print("===== Gestion des joueurs participants =====")
        while True:
            print("1. Ajouter un joueur")
            print("2. Supprimer un joueur inscrit")
            print("3. Terminer")
            choix = input("Entrez votre choix : ")

            if choix == '1':
                print("===== Sélection des joueurs à ajouter =====")
                for i, joueur in enumerate(joueurs_disponibles, 1):
                    print(f"{i}. Nom: {joueur.nom}, Prénom: {joueur.prenom}, Elo: {joueur.elo}")
                index = input("Entrez l'index du joueur à ajouter (ou 'terminer' pour quitter) : ")
                if index.lower() == 'terminer':
                        break
                try:
                    index = int(index)
                    if 1 <= index <= len(joueurs_disponibles):
                        joueur_choisi = joueurs_disponibles.pop(index - 1)
                        joueurs_selectionnes.append(joueur_choisi)
                        print(f"Le joueur {joueur_choisi.nom} a été ajouté au tournoi.")
                    else:
                        print("Index invalide.")
                except ValueError:
                    print("Veuillez entrer un nombre valide.")
            elif choix == '2':
                print("===== Suppression des joueurs inscrits =====")
                for i, joueur in enumerate(joueurs_deja_inscrits, 1):
                    print(f"{i}. Nom: {joueur.nom}, Prénom: {joueur.prenom}, Elo: {joueur.elo}")
                index = input("Entrez l'index du joueur à supprimer (ou 'terminer' pour quitter) : ")
                if index.lower() == 'terminer':
                    break
                try:
                    index = int(index)
                    if 1 <= index <= len(joueurs_deja_inscrits):
                        joueur_supprime = joueurs_deja_inscrits.pop(index - 1)
                        print(f"Le joueur {joueur_supprime.nom} a été supprimé du tournoi.")
                    else:
                        print("Index invalide.")
                except ValueError:
                    print("Veuillez entrer un nombre valide.")
            elif choix == '3':
                break
            else:
                print("Choix invalide. Veuillez réessayer.")

        # Enregistrer les joueurs sélectionnés dans la base de données
            self.tournoi_controller.ajouter_joueurs_au_tournoi(tournoi_index, joueurs_selectionnes)

    def afficher_details_tournoi(self):
        index_tournoi = self.saisir_index_tournoi()
        tournoi = self.tournoi_controller.tournoi_manager.tournois[index_tournoi - 1]
        
        print("===== Détails du Tournoi =====")
        print(f"Nom du tournoi: {tournoi.nom}")
        print(f"Date de début: {tournoi.date_debut}")
        print(f"Date de fin: {tournoi.date_fin}")
        print(f"Nombre maximum de joueurs: {tournoi.nb_max_joueurs}")
        print(f"Nombre de rondes: {tournoi.nb_rondes}")
        print(f"Type de tournoi: {tournoi.type_tournoi}")
        print("Liste des joueurs inscrits:")
        for joueur in tournoi.joueurs:
            print(joueur.nom, joueur.prenom)  # Affichez les noms et prénoms des joueurs

    def supprimer_joueur_tournoi(self, tournoi_index):
    # Récupérer le tournoi à partir du gestionnaire de tournoi en utilisant l'index fourni en paramètre
        tournoi = self.tournoi_controller.tournoi_manager.tournois[tournoi_index - 1]
        
        # Récupérer la liste des joueurs inscrits dans le tournoi
        joueurs_inscrits = tournoi.joueurs
        
        # Vérifier si la liste des joueurs est vide
        if not joueurs_inscrits:
            print("Aucun joueur inscrit dans ce tournoi.")
            return

        # Afficher la liste des joueurs inscrits dans le tournoi
        print("Liste des joueurs inscrits au tournoi : ")
        for i, joueur in enumerate(joueurs_inscrits, 1):
            print(f"{i}. {joueur.nom} {joueur.prenom}")

        while True:
            try:
                joueur_index = int(input("Entrez l'index du joueur à supprimer : "))
                if 1 <= joueur_index <= len(joueurs_inscrits):
                    joueur = joueurs_inscrits[joueur_index - 1]
                    self.tournoi_controller.supprimer_joueur_du_tournoi(tournoi_index, joueur)
                    print("Joueur supprimé du tournoi avec succès.")
                    break
                else:
                    print("Index du joueur invalide. Veuillez entrer un index valide.")
            except ValueError:
                print("Veuillez entrer un nombre entier.")






if __name__ == "__main__":
    tournoi_vue = TournoiVue()
    tournoi_vue.menu_tournoi()
