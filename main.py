# coding=utf-8
# Jeu du BlackJack

# Dans ce programme, nous utilisons souvent la methode readline() pour récupérer les saisies de l'utilisateur. Car
# nous avons rencontré des problèmes avec la fonction input lorsque l'on effectuait des tests de vérification de saisie

import random
import sys

# Informations sur la partie
SOLDE_DEPART = 1000  # Solde de départ par défaut
NB_MAX_JOUEURS = 7  # Nombre maximum de joueurs
MISE_MAX = 300  # Mise maximale par joueur
MISE_MIN = 5  # Mise minimale par joueur
PILE_DE_CARTES = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']  # Le jeu de cartes

# Variables globales
noms_dico = []  # Les noms des joueurs dans le dictionnaire seront stockés dans cette liste
players = {}  # Les informations sur les joueurs seront stockées dans ce dictionnaire.
main_croupier = []  # Les cartes du croupier seront stockées dans cette liste.


# Initialiser toutes les informations de la partie
def initialisation():
    # On récupère les informations de la partie pour les compléter
    global players
    global noms_dico

    # Demander le nombre de joueurs
    while True:
        print("Combien de joueurs vont jouer (maximum " + str(NB_MAX_JOUEURS) + ") ?")
        saisie = sys.stdin.readline().rstrip('\n')
        if saisie == "":
            print("Vous n'avez rien saisi. Veuillez réessayer.")
            continue
        if not saisie.isdigit():
            print("La valeur saisie doit être un entier. Veuillez réessayer.")
            continue
        nb_joueurs = int(saisie)
        if nb_joueurs in range(1, NB_MAX_JOUEURS + 1):
            break
        else:
            print("Veuillez entrer un nombre entier entre 1 et " + str(NB_MAX_JOUEURS) + ".")

    # Demander les informations pour chaque joueur
    for i in range(nb_joueurs):
        # Demander le nom pour chaque joueur
        print("Joueur " + str(i + 1) + ", veuillez saisir votre nom :")
        # Ici, nous utilisons la methode readline pour éviter de saisir le nom du joueur entre guillemets. La méthode
        # rstrip('\n') permet de supprimer le caractère de retour à la ligne qui est inclus dans la saisie effectuée
        # avec sys.stdin.readline().
        nom = sys.stdin.readline().rstrip('\n')

        nom_dico = "joueur" + str(i + 1)  # On définit le mot clef utilisé dans le dictionnaire
        # On ajoute les informations sur le joueur dans le dictionnaire
        players[nom_dico] = {"nom": nom, "solde": SOLDE_DEPART, "mise": 0, "cartes": [], "joue": False}
        # On ajoute le nom du joueur dans la liste
        noms_dico.append(nom_dico)


# Demander à un joueur s'il veut jouer le tour
def demander_joueur_joue(joueur):
    while True:
        # Demander au joueur s'il veut jouer le tour et mettre sa réponse en minuscule
        print(joueur["nom"] + ", voulez-vous jouer le tour ? (o/n)")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()
        if choix == "o":
            return True
        elif choix == "n":
            return False
        else:
            print("Veuillez saisir 'o' pour 'oui' ou 'n' pour 'non'.")


def miser(joueur):
    while True:
        # Demander au joueur combien il veut miser et vérifier que la mise est valide
        print(joueur["nom"] + ", combien voulez-vous miser ? (minimum : " + str(MISE_MIN) + ", maximum : " + str(
            MISE_MAX) + ".)")
        mise_str = sys.stdin.readline().rstrip('\n')  # Récupérer la saisie de l'utilisateur sans le caractère de
        # retour à la ligne
        if not mise_str.isdigit():  # Tester si la saisie est un nombre entier
            print("Veuillez saisir un nombre entier.")
            continue
        mise = int(mise_str)  # Convertir la saisie en un entier
        if not (MISE_MIN <= mise <= MISE_MAX):  # Vérifier que la mise est comprise entre les valeurs MISE_MIN et
            # MISE_MAX
            print("Veuillez saisir un nombre entier entre " + str(MISE_MIN) + " et " + str(MISE_MAX) + ".")
            continue
        if mise > joueur["solde"]:  # Vérifier que le joueur a assez d'argent pour miser cette somme
            print("Vous ne pouvez pas miser plus que votre solde actuel de " + str(joueur["solde"]) + ".")
            continue
        # Si la mise est valide, on met à jour le dictionnaire du joueur avec la mise choisie et on sort de la boucle
        # while
        joueur["mise"] = mise
        joueur["solde"] -= mise
        break


# Ajouter une carte aléatoire à la main d'un joueur
def ajouter_carte(cartes):
    # On ajoute une carte aléatoire à la main du joueur
    cartes.append(random.choice(PILE_DE_CARTES))


# Demander à chaque joueur s'il veut jouer le tour
def initialiser_le_tour():
    # On ajoute deux cartes au croupier
    main_croupier.append(random.choice(PILE_DE_CARTES))
    main_croupier.append(random.choice(PILE_DE_CARTES))
    for i in range(len(players)):
        nom_dico = noms_dico[i]  # On récupère le nom du joueur dans le dictionnaire
        # On demande au joueur s'il veut jouer le tour
        if demander_joueur_joue(players[nom_dico]):
            # Si le joueur veut jouer le tour, on met à jour le dictionnaire, on lui demande combien il souhaite
            # miser et on lui ajoute deux cartes
            players[nom_dico]["joue"] = True
            miser(players[nom_dico])
            ajouter_carte(players[nom_dico]["cartes"])
            ajouter_carte(players[nom_dico]["cartes"])


# Tester si une liste est à 1 ou 2 dimensions
def is_2d_list(lst):
    return isinstance(lst, list) and any(isinstance(elem, list) for elem in lst)


# Calculer la valeur de la main d'un joueur
def calculer_valeur_main(cartes):
    # On teste si la liste est à 1 ou 2 dimensions
    # Le cas de la liste avec 2 dimensions correspond à un joueur qui a fait un split
    if is_2d_list(cartes):
        # Si la liste est à 2 dimensions, on calcule la valeur de chaque main et on retourne la plus proche de 21
        valeurs = []
        for main in cartes:
            # On calcule la valeur de chaque main en appelant récursivement la fonction calculer_valeur_main
            valeurs.append(calculer_valeur_main(main))
        # On retourne la plus grande valeur de la liste si celle-ci ne dépasse pas 21, sinon on retourne la plus
        # petite. Nous n'avons pas besoins de tester que la petite main est aussi inférieure ou égale à 21,
        # car la défaite du joueur sera gérée dans une autre fonction. Ici ce test est fait pour éviter de stopper un
        # joueur qui aurait pu continuer avec sa deuxième main.
        if max(valeurs) > 21:
            return min(valeurs)
        return max(valeurs)
    # Si la liste est à une dimension, cela signifie que le joueur n'a qu'une seule main
    valeur = 0
    for carte in cartes:
        # Si la carte est une figure, elle vaut 10 points
        if carte in ['J', 'Q', 'K']:
            valeur += 10
        # Si la carte est un as, elle peut valoir 1 ou 11 points en fonction de la main
        elif carte == 'A':
            if valeur + 11 > 21:
                valeur += 1
            else:
                valeur += 11
        # Si la carte est une carte numérique, elle vaut sa propre valeur en points
        else:
            valeur += int(carte)
    # On retourne la valeur de la main
    return valeur


# Affichage de début de partie
def affichage_debut_partie():
    # Afficher la première carte du croupier
    print("La première carte du croupier est : " + main_croupier[0])
    # Afficher les cartes de tous les joueurs qui jouent le tour
    print("Les cartes des joueurs sont :")
    for i in range(len(players)):
        nom_dico = noms_dico[i]  # On récupère le nom du joueur dans le dictionnaire
        if players[nom_dico]["joue"]:
            # Si le joueur joue le tour, on affiche ses cartes, sa mise et son solde
            print(players[nom_dico]["nom"] + " : " + str(players[nom_dico]["cartes"]) + " | Mise : " +
                  str(players[nom_dico]["mise"]) + " | Solde : " + str(players[nom_dico]["solde"]))


# Determiner si une main est un blackjack
def est_blackjack(cartes):
    if calculer_valeur_main(cartes) == 21 and len(cartes) == 2:
        return True
    else:
        return False


# Doubler la mise d'un joueur
def doubler_mise(joueur):
    if players[joueur]["mise"] <= players[joueur]["solde"]:
        players[joueur]["mise"] *= 2
        players[joueur]["solde"] -= players[joueur]["mise"]
        return True
    else:
        print("Vous ne pouvez pas doubler votre mise car vous n'avez pas assez d'argent.")
        return False


# Si on a une paire, on peut se couper
def split(joueur):
    if players[joueur]["cartes"][0] == players[joueur]["cartes"][1]:
        # Cartes devient une liste à 2 dimensions avec 1 carte dans chaque sous-liste
        players[joueur]["cartes"] = [players[joueur]["cartes"][0:1], players[joueur]["cartes"][1:2]]
        # On ajoute une carte à chaque main
        ajouter_carte(players[joueur]["cartes"][0])
        ajouter_carte(players[joueur]["cartes"][1])
        return True
    else:
        print("Vous ne pouvez pas vous couper car vous n'avez pas de paire.")
        return False


# Assurer la mise si le croupier possède un as
def assurer(joueur):
    if main_croupier[0] == 'A':
        # On demande au joueur le montant de sa mise "assurance"
        while True:
            # Demande au joueur combien il veut assurer sa mise
            print("Quel est le montant de votre assurance ?")
            assurance_str = sys.stdin.readline().rstrip('\n')
            if not assurance_str.isdigit():
                print("Vous devez saisir un nombre entier.")
                continue
            assurance = int(assurance_str)

            # Vérifie que le joueur à assez d'argent pour assurer sa mise
            if assurance <= players[joueur]["mise"] / 2 and assurance <= players[joueur]["solde"]:
                # Vu que nous n'afficherons pas les soldes en temps réel, nous pouvons gérer directement les
                # évolutions du solde ici pour simplifier la gestion de la fin de partie.
                players[joueur]["solde"] -= assurance
                if est_blackjack(main_croupier):
                    players[joueur]["solde"] += assurance * 2
                return True
            else:
                print(
                    "Vous ne pouvez pas assurer une mise plus élevée que la moitié de votre mise initiale ou plus "
                    "grande que votre solde.")
    else:
        print("Vous ne pouvez pas assurer votre mise car le croupier n'a pas d'as.")
        return False


# Determiner si un joueur a perdu
def a_perdu(joueur):
    if calculer_valeur_main(players[joueur]["cartes"]) > 21:
        return True
    else:
        return False


# On demande au joueur ce qu'il compte faire
def demander_action(joueur):
    # On demande au joueur ce qu'il compte faire et on vérifie que la valeur saisie est correcte
    print(str(players[joueur]["nom"]) + ", que voulez-vous faire ?")
    print("1 - Piocher une/plusieurs carte(s)")
    print("2 - Doubler votre mise")
    print("3 - Split (si vous avez une paire)")
    print("4 - Assurer (si le croupier a un as)")
    print("5 - Abandonner")
    print("6 - Ne rien faire")
    action = 0
    while True:
        print("Saisissez le numéro de l'action que vous voulez effectuer :")
        action_str = sys.stdin.readline().rstrip('\n')
        if not action_str.isdigit():
            print("La valeur saisie n'est pas un entier valide.")
            continue
        action = int(action_str)
        if not (1 <= action <= 6):
            print("La valeur saisie doit être entre 1 et 6.")
            continue
        break

    # On effectue l'action demandée
    if action == 1:
        ajouter_carte(players[joueur]["cartes"])
        # on lui demande s'il veut encore tirer une carte jusqu'à ce qu'il ne veuille plus
        # on affiche sa main
        print("Votre main est maintenant : " + str(players[joueur]["cartes"]))
        # Si le joueur a perdu, on ne lui demande pas s'il veut piocher une carte
        if a_perdu(joueur):
            return
        print("Voulez-vous encore piocher une carte ? (o/n)")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()
        while choix not in ["o", "n"]:
            print("Veuillez saisir 'o' pour 'oui' ou 'n' pour 'non'.")
            choix = sys.stdin.readline().rstrip('\n')
            choix = choix.lower()
        if choix == "o":
            ajouter_carte(players[joueur]["cartes"])
        elif choix == "n":
            pass
    elif action == 2:
        # Si doubler_mise renvoie faux on redemande une action
        if not doubler_mise(joueur):
            demander_action(joueur)
        else:
            # On ajoute une carte à la main du joueur
            ajouter_carte(players[joueur]["cartes"])
            # on affiche sa main
            print("Votre main est maintenant : " + str(players[joueur]["cartes"]))
    elif action == 3:
        # Si split renvoie faux on redemande une action
        if not split(joueur):
            demander_action(joueur)
    elif action == 4:
        # Si assurer renvoie faux on redemande une action
        if not assurer(joueur):
            demander_action(joueur)
    elif action == 5:
        # On met le joueur en mode "ne joue pas"
        players[joueur]["joue"] = False
        print("Vous avez abandonné la partie.")
    else:
        pass


# Jouer un tour de jeu
def jouer_tour():
    # On initialise le tour
    initialiser_le_tour()
    # On affiche les infos au début du tour
    affichage_debut_partie()
    # On effectue les actions de chaque joueur
    for joueur in players:
        # On vérifie que le joueur est encore en jeu
        if players[joueur]["joue"]:
            # On regarde si le joueur a fait un blackjack
            if est_blackjack(players[joueur]["cartes"]):
                print("Vous avez fait un blackjack !")
                # On met le joueur en mode "ne joue pas"
                players[joueur]["joue"] = False
                # On met à jour le solde du joueur
                players[joueur]["solde"] += players[joueur]["mise"] * 2.5
            else:
                # On demande au joueur ce qu'il veut faire
                demander_action(joueur)
            # On vérifie que le joueur n'a pas perdu
            if a_perdu(joueur):
                print("Vous avez perdu !")
                # On met le joueur en mode "ne joue pas"
                players[joueur]["joue"] = False
    # On fait jouer le croupier
    if est_blackjack(main_croupier):
        print("Le croupier a fait un blackjack, tous les joueurs en jeu perdent!")
        return
    else:
        while calculer_valeur_main(main_croupier) < 17:
            ajouter_carte(main_croupier)
        print("Le croupier a fini de jouer.")
        print("La main du croupier est : " + str(main_croupier))
        # On vérifie que le croupier n'a pas perdu
        if calculer_valeur_main(main_croupier) > 21:
            print("Le croupier a perdu !\nLes joueurs encore en jeu gagnent !")
            # On met à jour le solde des joueurs
            for joueur in players:
                if players[joueur]["joue"]:
                    players[joueur]["solde"] += players[joueur]["mise"] * 2
        else:
            # On compare les mains des joueurs avec celle du croupier
            print("Le croupier obtient " + str(calculer_valeur_main(main_croupier)) + " points.")
            for joueur in players:
                if players[joueur]["joue"]:
                    print(players[joueur]["nom"] + ", vous obtenez " + str(
                        calculer_valeur_main(players[joueur]["cartes"])) + " points.")
                    if calculer_valeur_main(players[joueur]["cartes"]) > calculer_valeur_main(main_croupier):
                        print("Vous avez gagné " + str(players[joueur]["mise"] * 2) + " euros !")
                        # On met à jour le solde du joueur
                        players[joueur]["solde"] += players[joueur]["mise"] * 2
                    elif calculer_valeur_main(players[joueur]["cartes"]) == calculer_valeur_main(main_croupier):
                        print("Vous avez fait égalité !")
                        # On met à jour le solde du joueur
                        players[joueur]["solde"] += players[joueur]["mise"]
                    else:
                        print("Vous avez perdu !")


# Demander si un joueur veut quitter la partie
def demander_quitter_partie():
    print("Est ce que quelqu'un souhaite quitter la partie ? (o/n)")
    choix = sys.stdin.readline().rstrip('\n')
    choix = choix.lower()
    while choix not in ["o", "n"]:
        print("Veuillez saisir 'o' pour 'oui' ou 'n' pour 'non'.")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()
    if choix == "o":
        # On demande le nom du joueur qui quitte la partie
        print("Quel est le nom du joueur qui quitte la partie ?")
        nom = sys.stdin.readline().rstrip('\n')
        indice = 0
        # On vérifie que le joueur est bien celui d'un joueur de la partie et on récupère son indice
        while nom != players[noms_dico[indice]]["nom"]:
            print("Ce joueur n'est pas dans la partie.")
            print("Quel est le nom du joueur qui quitte la partie ?")
            nom = sys.stdin.readline().rstrip('\n')
            indice += 1
        # On supprime le joueur de la partie
        print(players[noms_dico[indice]]["nom"] + " a quitté la partie.")
        del players[noms_dico[indice]]
        del noms_dico[indice]
        # On demande si un autre joueur veut quitter la partie
        demander_quitter_partie()
    elif choix == "n":
        return


# Demander si un nouveau joueur veut rejoindre la partie
def demander_rejoindre_partie():
    print("Est ce que quelqu'un souhaite rejoindre la partie ? (o/n)")
    choix = sys.stdin.readline().rstrip('\n')
    choix = choix.lower()
    while choix not in ["o", "n"]:
        print("Veuillez saisir 'o' pour 'oui' or 'n' pour 'non'.")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()
    if choix == "o":
        # On demande le nom du joueur qui rejoint la partie
        print("Quel est le nom du joueur qui rejoint la partie ?")
        nom = sys.stdin.readline().rstrip('\n')
        # On ajoute le joueur à la partie
        print(nom + " a rejoint la partie.")
        nom_dico = "joueur" + str(len(players) + 1)
        players[nom_dico] = {"nom": nom, "solde": SOLDE_DEPART, "mise": 0, "cartes": [], "joue": False}
        noms_dico.append(nom_dico)
        # On demande si un autre joueur veut rejoindre la partie
        demander_rejoindre_partie()
    else:
        return


# Tester si la partie est terminée
def est_partie_terminee():
    # On teste si la partie est terminée
    if len(players) == 0:
        return True
    else:
        return False


# Supprimer les joueurs qui ont perdu
def supprimer_joueurs_perdus():
    # On supprime les joueurs qui ont perdu
    for joueur in players:
        if players[joueur]["solde"] <= 0:
            print(players[joueur]["nom"] + " a perdu car il n'a plus d'argent!")
            del players[joueur]


# Demander si on veut rejouer une partie
def demander_rejouer_partie():
    print("Voulez vous rejouer une partie ? (o/n)")
    choix = sys.stdin.readline().rstrip('\n')
    choix = choix.lower()
    while choix not in ["o", "n"]:
        print("Veuillez saisir 'o' pour 'oui' or 'n' pour 'non'.")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()
    if choix == "o":
        return True
    else:
        return False


# Jouer une partie
def jouer_partie():
    do_replay = True
    while do_replay:
        # On initialise le jeu
        initialisation()
        # On joue des tours tant que la partie n'est pas terminée
        while not est_partie_terminee():
            # On joue un tour
            jouer_tour()
            # On demande si un joueur veut quitter la partie
            demander_quitter_partie()
            # On demande si un joueur veut rejoindre la partie
            demander_rejoindre_partie()
            # On supprime les joueurs qui ont perdu
            supprimer_joueurs_perdus()
        # On demande si on veut rejouer une partie
        print ("La partie est terminée.")
        do_replay = demander_rejouer_partie()


# Lancement du jeu
jouer_partie()

"""
⢀⡴⠑⡄⠀⠀⠀⠀⠀⠀⠀⣀⣀⣤⣤⣤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠸⡇⠀⠿⡀⠀⠀⠀⣀⡴⢿⣿⣿⣿⣿⣿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠑⢄⣠⠾⠁⣀⣄⡈⠙⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⢀⡀⠁⠀⠀⠈⠙⠛⠂⠈⣿⣿⣿⣿⣿⠿⡿⢿⣆⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⢀⡾⣁⣀⠀⠴⠂⠙⣗⡀⠀⢻⣿⣿⠭⢤⣴⣦⣤⣹⠀⠀⠀⢀⢴⣶⣆ 
⠀⠀⢀⣾⣿⣿⣿⣷⣮⣽⣾⣿⣥⣴⣿⣿⡿⢂⠔⢚⡿⢿⣿⣦⣴⣾⠁⠸⣼⡿ 
⠀⢀⡞⠁⠙⠻⠿⠟⠉⠀⠛⢹⣿⣿⣿⣿⣿⣌⢤⣼⣿⣾⣿⡟⠉⠀⠀⠀⠀⠀ 
⠀⣾⣷⣶⠇⠀⠀⣤⣄⣀⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
⠀⠉⠈⠉⠀⠀⢦⡈⢻⣿⣿⣿⣶⣶⣶⣶⣤⣽⡹⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠉⠲⣽⡻⢿⣿⣿⣿⣿⣿⣿⣷⣜⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣷⣶⣮⣭⣽⣿⣿⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⣀⣀⣈⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⠿⠿⠿⠛⠉
"""

"""
    ,--._
    `.   `.                      ,-.
      `.`. `.                  ,'   )
        \`:  \               ,'    /
         \`:  ),.         ,-' ,   /
         ( :  |:::.    ,-' ,'   ,'
         `.;: |::::  ,' ,:'  ,-'
         ,^-. `,--.-/ ,'  _,'
        (__        ^ ( _,'
      __((o\   __   ,-'
    ,',-.     ((o)  /
  ,','   `.    `-- (
  |'      ,`        \
  |     ,:' `        |
 (  `--      :-.     |
 `,.__       ,-,'   ;
 (_/  `,__,-' /   ,'
 |\`--|_/,' ,' _,'
 \_^--^,',-' -'(
 (_`--','       `-.
  ;;;;'       ::::.`------.
    ,::       `::::  `:.   `.
   ,:::`       :::::   `::.  \
  ;:::::       `::::     `::  \
  |:::::        `::'      `:   ;
  |:::::.        ;'        ;   |
  |:::::;                   )  |
  |::::::        ,   `::'   |  \
  |::::::.       ;.   :'    ;   ::.
  |::::,::        :.  :   ,;:   |::
  ;:::;`"::     ,:::  |,-' `:   |::,
  /;::|    `--;""';'  |     :. (`";'
  \   ;           ;   |     ::  `,
   ;  |           |  ,:;     |  :
   |  ;           |  |:;     |  |
   |  |           |  |:      |  |
   |  |           |  ;:      |  |
  /___|          /____|     ,:__|
 /    /          /    |     /    )
 `---'          '----'      `---'
"""
