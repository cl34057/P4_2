from models.tournoi_model import TournoiManager
class TournoiController:
    def __init__(self):
        self.tournoi_manager = TournoiManager()
     # Méthode pour ajouter un tournoi
    def ajouter_tournoi(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
        return self.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)
    # Méthode pour modifier un tournoi
    def modifier_tournoi(self, index, nom=None, date_debut=None, date_fin=None, nb_max_joueurs=None, nb_rondes=None, type_tournoi=None):
        self.tournoi_manager.modifier_tournoi(index, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)

    # Méthode pour supprimer un tournoi
    def supprimer_tournoi(self, index):
        self.tournoi_manager.supprimer_tournoi(index)
     # Méthode pour ajouter des joueurs à un tournoi
    def ajouter_joueurs_au_tournoi(self, tournoi_index, joueurs):
        if 1 <= tournoi_index <= len(self.tournoi_manager.tournois):
            tournoi = self.tournoi_manager.tournois[tournoi_index - 1]
            joueurs_inscrits = tournoi.joueurs
            joueurs_a_ajouter = [joueur for joueur in joueurs if joueur not in joueurs_inscrits]
            tournoi.ajouter_joueurs(joueurs_a_ajouter)
            self.tournoi_manager.sauvegarder_tournois()
        else:
            print("Index de tournoi invalide.")
    # Méthode pour supprimer un joueur du tournoi
    def supprimer_joueur_du_tournoi(self, tournoi_index, joueur):
        self.tournoi_manager.supprimer_joueur_du_tournoi(tournoi_index, joueur)
    # Méthode pour créer un nouveau tour
    def creer_tour(self, index_tournoi):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        tournoi.creer_tour()
        tournoi.sauvegarder_joueurs()  # Sauvegarde après la création du tour
    # Méthode pour effectuer l'appariement des tours
    def appariement_tour(self, index_tournoi):
        tournoi = self.tournoi_manager.trouver_tournoi_par_index(index_tournoi)
        tournoi.appariement_tour()
        tournoi.sauvegarder_joueurs()  # Sauvegarde après l'appariement du tour