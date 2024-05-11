from views.tournoi_vue import TournoiVue

def menu_tournoi():
    tournoi_vue = TournoiVue()
    while True:
        tournoi_vue.afficher_menu()
        choix = input("Entrez votre choix : ")

        if choix == "1":
            tournoi_info = tournoi_vue.saisir_tournoi()
            if tournoi_info is not None:
                nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi = tournoi_info
                if tournoi_vue.tournoi_controller.ajouter_tournoi(nom, date_debut, date_fin, nb_max_joueurs, nb_rondes, type_tournoi):
                    print("Tournoi créé avec succès.")
                else:
                    print("Échec de la création du tournoi. Veuillez réessayer.")
        elif choix == "2":
            tournoi_vue.modifier_tournoi()
        elif choix == "3":
            tournoi_vue.supprimer_tournoi()
        elif choix == "4":
            tournoi_vue.afficher_liste_tournois()
        elif choix == "5":
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            tournoi_vue.saisir_joueurs_participants(index_tournoi)
        elif choix == "6":
            tournoi_vue.afficher_details_tournoi()
        elif choix == "7":
            index_tournoi = tournoi_vue.saisir_index_tournoi()
            tournoi_vue.supprimer_joueur_tournoi(index_tournoi)
            print("Joueur supprimé du tournoi avec succès.")
        elif choix == "8":
            print("Merci d'avoir utilisé le gestionnaire de tournois. À bientôt !")
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu_tournoi()
