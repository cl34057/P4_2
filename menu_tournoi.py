from views.tournoi_vue import TournoiVue

def menu_tournoi():
    tournoi_vue = TournoiVue()
    while True:
        tournoi_vue.afficher_menu()
        choix = input("Entrez votre choix : ")

        if choix == "1":
            nom, date_debut, date_fin = tournoi_vue.saisir_tournoi()
            tournoi_vue.tournoi_controller.ajouter_tournoi(nom, date_debut, date_fin)
            print("Tournoi créé avec succès.")
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
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

if __name__ == "__main__":
    menu_tournoi()
