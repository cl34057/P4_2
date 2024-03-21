from models.joueur_model import Joueur, JoueurManager
from controllers.joueur_controller import JoueurController
import datetime
from config import MAX_JOUEURS
class JoueurVue:
    def __init__(self):
        self.joueur_controller = JoueurController()

    def afficher_menu(self):
        print("===== Menu Joueur =====")
        print("1. Ajouter un joueur")
        print("2. Modifier un joueur")
        print("3. Supprimer un joueur")
        print("4. Afficher la liste des joueurs")
        print("5. Afficher les détails d'un joueur")
        print("6. Quitter")

    def saisir_joueur(self):
        if len(self.joueur_controller.joueur_manager.joueurs) >= MAX_JOUEURS:
            print("Nombre maximal de joueurs atteint.")
            return None
        while True:
            nom = input("Nom du joueur : ")
            if not nom.isalpha():
                print("Le nom doit contenir uniquement des lettres.")
                continue
            
            prenom = input("Prénom du joueur : ")
            if not prenom.isalpha():
                print("Le prénom doit contenir uniquement des lettres.")
                continue
            
            while True:
                date_naissance = input("Date de naissance du joueur (format YYYY-MM-DD) : ")
                try:
                    datetime.datetime.strptime(date_naissance, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")
                    continue
            
            while True:
                elo = input("Elo du joueur (entre 1000 et 3500) : ")
                if not elo.isdigit():
                    print("Le score Elo doit être un entier.")
                    continue
                elif not 1000 <= int(elo) <= 3500:
                    print("Le score Elo doit être compris entre 1000 et 3500.")
                    continue
                else:
                    break
                    
            # Obtenez l'index du joueur à partir du gestionnaire de joueur
            index = len(self.joueur_controller.joueur_manager.joueurs) + 1
            
            # Créer un objet Joueur avec les informations saisies, y compris l'index
            joueur = Joueur(index, nom, prenom, date_naissance, int(elo))
            return joueur

    def modifier_joueur(self):
        index = self.saisir_index_joueur()
        nom, prenom, date_naissance, elo = self.saisir_joueur_details()
        self.joueur_controller.modifier_joueur(index, nom, prenom, date_naissance, elo)

    def afficher_joueur(self, joueur):
        print("===== Affichage des détails d'un joueur =====")
        print("Nom :", joueur.nom)  # Afficher le nom
        print("Prénom :", joueur.prenom)
        print("Date de naissance :", joueur.date_naissance)
        print("Elo :", joueur.elo)

    def afficher_liste_joueurs(self):
        joueurs = self.joueur_controller.joueur_manager.joueurs
        print("===== Liste des Joueurs =====")
        for joueur in joueurs:
            print(f"Index: {joueurs.index(joueur) + 1}, Nom: {joueur.nom}, Prénom: {joueur.prenom}, Elo: {joueur.elo}")

    def saisir_index_joueur(self):
        while True:
            try:
                index = int(input("Entrez l'index du joueur : "))
                if index < 1 or index > len(self.joueur_controller.joueur_manager.joueurs):
                    print("Index invalide. Veuillez entrer un index valide.")
                    continue
                else:
                    return index
            except ValueError:
                print("Veuillez entrer un nombre entier.")

    def saisir_joueur_details(self):
        while True:
            nom = input("Nouveau nom du joueur : ")
            if not nom.isalpha():
                print("Le nom doit contenir uniquement des lettres.")
                continue
            
            prenom = input("Nouveau prénom du joueur : ")
            if not prenom.isalpha():
                print("Le prénom doit contenir uniquement des lettres.")
                continue
            
            while True:
                date_naissance = input("Nouvelle date de naissance du joueur (format YYYY-MM-DD) : ")
                try:
                    datetime.datetime.strptime(date_naissance, '%Y-%m-%d')
                    break
                except ValueError:
                    print("Format de date invalide. Veuillez entrer la date au format YYYY-MM-DD.")
                    continue
            
            while True:
                elo = input("Nouveau Elo du joueur (entre 1000 et 3500) : ")
                if not elo.isdigit():
                    print("Le score Elo doit être un entier.")
                    continue
                elif not 1000 <= int(elo) <= 3500:
                    print("Le score Elo doit être compris entre 1000 et 3500.")
                    continue
                else:
                    break
                
            return nom, prenom, date_naissance, int(elo)
    def supprimer_joueur(self):
        index = self.saisir_index_joueur()
        self.joueur_controller.supprimer_joueur(index)
        print("Joueur supprimé avec succès.")
    
    def afficher_details_joueur(self):
        index = self.saisir_index_joueur()
        joueur = self.joueur_controller.joueur_manager.joueurs[index - 1]
        self.afficher_joueur(joueur)