from models.joueur_model import JoueurManager
from config import MAX_JOUEURS

class JoueurController:
    def __init__(self):
        self.joueur_manager = JoueurManager()

    def ajouter_joueur(self, nom, prenom, date_naissance, elo):
         if len(self.joueur_manager.joueurs) < MAX_JOUEURS:
            index = len(self.joueur_manager.joueurs) + 1  # Index basé sur la longueur actuelle de la liste des joueurs
            self.joueur_manager.ajouter_joueur( nom, prenom, date_naissance, elo)
            print("Joueur ajouté avec succès.")
        
         else:
            print("Limite de joueurs atteinte. Impossible d'ajouter un nouveau joueur.")

    def modifier_joueur(self, index, nom, prenom, date_naissance, elo):
        self.joueur_manager.modifier_joueur(index, nom, prenom, date_naissance, elo)
        print("Joueur modifié avec succès.")

    def supprimer_joueur(self, index):
        self.joueur_manager.supprimer_joueur(index)
        print("Joueur supprimé avec succès.")
