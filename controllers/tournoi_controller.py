from models.tournoi_model import TournoiManager

class TournoiController:
    def __init__(self):
        self.tournoi_manager = TournoiManager()

    def ajouter_tournoi(self, nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
        return self.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi)

    def modifier_tournoi(self, index, nom, date_debut, date_fin):
        self.tournoi_manager.modifier_tournoi(index, nom, date_debut, date_fin)

    def supprimer_tournoi(self, index):
        self.tournoi_manager.supprimer_tournoi(index)

    def ajouter_joueurs_au_tournoi(self, tournoi_index, joueurs):
        if 1 <= tournoi_index <= len(self.tournoi_manager.tournois):
            tournoi = self.tournoi_manager.tournois[tournoi_index - 1]
            joueurs_inscrits = tournoi.joueurs
            joueurs_a_ajouter = [joueur for joueur in joueurs if joueur not in joueurs_inscrits]
            tournoi.ajouter_joueurs(joueurs_a_ajouter)
            self.tournoi_manager.sauvegarder_tournois()
        else:
            print("Index de tournoi invalide.")

    def supprimer_joueur_du_tournoi(self, tournoi_index, joueur):
        self.tournoi_manager.supprimer_joueur_du_tournoi(tournoi_index, joueur)
