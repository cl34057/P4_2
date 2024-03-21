from models.tournoi_model import TournoiManager

class TournoiController:
    def __init__(self):
        self.tournoi_manager = TournoiManager()

    def ajouter_tournoi(self, nom, date_debut, date_fin):
        return self.tournoi_manager.ajouter_tournoi(nom, date_debut, date_fin)

    def modifier_tournoi(self, index, nom, date_debut, date_fin):
        self.tournoi_manager.modifier_tournoi(index, nom, date_debut, date_fin)

    def supprimer_tournoi(self, index):
        self.tournoi_manager.supprimer_tournoi(index)

    def ajouter_joueurs_au_tournoi(self, tournoi_index, joueurs):
        tournoi = self.tournoi_manager.tournois[tournoi_index - 1]
        tournoi.ajouter_joueurs(joueurs)
        self.tournoi_manager.sauvegarder_tournois()
