# coding=utf-8
# Jeu du BlackJack

# La fonction principale du programme est la fonction jouer_partie(). Elle est appelée en bas du programme et permet de
# jouer une ou plusieurs parties de blackjack.

# Dans ce programme, nous utilisons souvent la methode readline() pour récupérer les saisies de l'utilisateur. Car
# nous avons rencontré des problèmes avec la fonction input lorsque l'on effectuait des tests de vérification de saisie.
# En effet, la fonction input() ne permet pas de saisir une valeur vide. C'est pourquoi nous
# utilisons la methode readline() qui permet de saisir une valeur vide.

# Certaines fonctions sont récursives. Nous avons choisi d'utiliser des fonctions récursives pour éviter de répéter
# des instructions dans le programme.

# Les constantes sont définies en haut du programme, elles représentent les paramètres de la partie. Elles sont
# utilisées dans les fonctions du programme. Vous pouvez les modifier pour modifier les paramètres de la partie (nombre
# de joueurs, mise minimale, mise maximale, solde de départ, etc.).

# Le programme utilise des variables globales. Nous avons choisi d'utiliser des variables globales pour stocker les
# informations sur les joueurs et sur le croupier. Elles sont définies en haut du programme.

# Importation des modules nécessaires
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


def initialisation():
    """
    Initialise toutes les informations de la partie.

    Cette fonction récupère les informations de la partie pour les compléter, notamment le nombre de joueurs, le nom de
    chaque joueur et les informations initiales de chaque joueur. Elle utilise les variables globales `players` et
    'noms_dico'.

    :param:
        None

    :return:
        None
    """

    # On utilise les variables globales `players` et `noms_dico` pour stocker les informations des joueurs
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


def demander_joueur_joue(joueur):
    """
    Demande à un joueur s'il veut jouer le tour.

    :param
        joueur (dict): Un dictionnaire contenant les informations sur le joueur.

    :return:
        bool : True si le joueur désire jouer le tour, False sinon.
    """
    while True:
        # Demander au joueur s'il veut jouer le tour et mettre sa réponse en minuscule
        print(joueur["nom"] + ", voulez-vous jouer le tour ? (o/n)")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()

        # Vérifier si le choix est valide
        if choix == "o":
            # Si le joueur veut jouer le tour, on met à jour son dictionnaire
            joueur["joue"] = True
            return True
        elif choix == "n":
            # Si le joueur ne veut pas jouer le tour, on met à jour son dictionnaire
            joueur["joue"] = False
            return False
        else:
            print("Veuillez saisir 'o' pour 'oui' ou 'n' pour 'non'.")


def miser(joueur):
    """
    Demande à un joueur combien il veut miser et met à jour son dictionnaire si la mise est valide.

    :param:
        joueur (dict): Un dictionnaire contenant les informations d'un joueur.

    :return:
        None

    """
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


def ajouter_carte(cartes):
    """
    Cette fonction prend en paramètre une liste de cartes qui représente la main d'un joueur et ajoute une carte
    aléatoire à cette liste en utilisant la fonction random.choice() de la bibliothèque random.

    :param:
        cartes (list): une liste de cartes représentant la main d'un joueur

    :return:
        None
    """
    cartes.append(random.choice(PILE_DE_CARTES))


def initialiser_le_tour():
    """
    Demande à chaque joueur s'il souhaite jouer le tour et initialise leur mise et leurs cartes.
    Ajoute également deux cartes au croupier.

    :param:
        None

    :return:
        None
    """
    # On ajoute deux cartes au croupier
    main_croupier.append(random.choice(PILE_DE_CARTES))
    main_croupier.append(random.choice(PILE_DE_CARTES))
    for i in range(len(players)):
        nom_dico = noms_dico[i]  # On récupère le nom du joueur dans le dictionnaire
        # On demande au joueur s'il veut jouer le tour
        if demander_joueur_joue(players[nom_dico]):
            # Si le joueur veut jouer le tour, on met à jour le dictionnaire, on lui demande combien il souhaite
            # miser et on lui ajoute deux cartes
            miser(players[nom_dico])
            ajouter_carte(players[nom_dico]["cartes"])
            ajouter_carte(players[nom_dico]["cartes"])  # On ajoute deux cartes à la main du joueur


def is_2d_list(lst):
    """
    Vérifie si une liste est une liste à deux dimensions ou non.

    :param:
        lst (list) : la liste à vérifier

    :return:
        bool : True si la liste est une liste à deux dimensions, False sinon
    """

    # Vérifie si la variable lst est bien de type liste, en utilisant la fonction "isinstance"
    # Si lst n'est pas une liste, retourne False immédiatement
    if not isinstance(lst, list):
        return False

    # Utilise la fonction "any" pour vérifier si au moins un élément de la liste est lui-même une liste
    # Si aucun élément n'est une liste, retourne False
    # Sinon, retourne True, car on a trouvé au moins un élément de type liste dans la liste
    return any(isinstance(elem, list) for elem in lst)


def calculer_valeur_main(cartes):
    """
    Calcule la valeur d'une main de blackjack.

    :param:
        cartes (list): la main du joueur, représentée sous la forme d'une liste de cartes

    :return:
        int : la valeur de la main
    """

    # On teste si la liste est à 1 ou 2 dimensions
    # Le cas de la liste avec 2 dimensions correspond à un joueur qui a fait un split
    if is_2d_list(cartes):
        # Si la liste est à 2 dimensions, on calcule la valeur de chaque main et on retourne la plus proche de 21

        # On crée une liste pour stocker les valeurs de chaque main
        valeurs = []

        # On parcourt chaque main de la liste
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

    # On initialise la valeur de la main à 0
    valeur = 0

    # On parcourt chaque carte de la main
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


def affichage_debut_partie():
    """
    Affiche la première carte du croupier et les cartes des joueurs qui jouent le tour,
    ainsi que leur mise et leur solde.

    :param:
        Aucun paramètre n'est nécessaire.

    :return:
        Aucune valeur n'est renvoyée.
    """
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


def est_blackjack(cartes):
    """
    Détermine si une main est un blackjack.

    :param:
        cartes (list): Liste des cartes contenues dans la main.

    :return:
        bool : True si la main est un blackjack, False sinon.
    """
    # On calcule la valeur totale de la main en appelant la fonction "calculer_valeur_main"
    # qui prend en paramètre la liste de cartes passée en argument.
    valeur_main = calculer_valeur_main(cartes)

    # Si la valeur totale de la main est égale à 21 et qu'il n'y a que 2 cartes dans la main,
    # alors c'est un blackjack, on retourne True.
    if valeur_main == 21 and len(cartes) == 2:
        return True
    else:
        # Sinon, ce n'est pas un blackjack, on retourne False.
        return False


def doubler_mise(joueur):
    """
    Double la mise d'un joueur et retire cette somme de son solde.

    :param:
        joueur (str): Nom du joueur dans le dictionnaire 'players' dont la mise doit être doublée.

    :return:
        bool : True si la mise a été doublée avec succès, False sinon.
    """
    # Si la mise du joueur est inférieure ou égale à son solde,
    # on double sa mise et on la retire de son solde.
    if players[joueur]["mise"] <= players[joueur]["solde"]:
        players[joueur]["mise"] *= 2
        players[joueur]["solde"] -= players[joueur]["mise"]
        return True
    else:
        # Sinon, on affiche un message d'erreur et on ne modifie pas la mise.
        print("Vous ne pouvez pas doubler votre mise car vous n'avez pas assez d'argent.")
        return False


def split(joueur):
    """
    Coupe la main d'un joueur en deux si celui-ci a une paire de cartes identiques.

    :param
        joueur (str): Nom du joueur dans le dictionnaire 'players' dont la main doit être coupée.

    :return:
        bool: True si la main a été coupée avec succès, False sinon.
    """
    # Si les deux premières cartes du joueur sont identiques, on peut se couper.
    if players[joueur]["cartes"][0] == players[joueur]["cartes"][1]:
        # On crée une nouvelle liste de cartes pour le joueur avec 2 sous-listes contenant chacune 1 carte.
        players[joueur]["cartes"] = [players[joueur]["cartes"][0:1], players[joueur]["cartes"][1:2]]
        # On ajoute une carte à chaque sous-liste pour avoir deux mains distinctes.
        ajouter_carte(players[joueur]["cartes"][0])
        ajouter_carte(players[joueur]["cartes"][1])
        return True
    else:
        # Sinon, on affiche un message d'erreur et on ne coupe pas la main.
        print("Vous ne pouvez pas vous couper car vous n'avez pas de paire.")
        return False


def assurer(joueur):
    """
    Permet à un joueur de s'assurer si le croupier à un As visible.

    :param:
        joueur (str) : Nom du joueur dans le dictionnaire 'players' qui souhaite s'assurer.

    :return:
        bool : True si le joueur a choisi de s'assurer, False sinon.
    """
    # Si la première carte du croupier est un As, le joueur peut s'assurer.
    if main_croupier[0] == 'A':
        while True:
            # On demande au joueur le montant de sa mise d'assurance.
            print("Quel est le montant de votre assurance ?")
            assurance_str = sys.stdin.readline().rstrip('\n')
            if not assurance_str.isdigit():
                print("Vous devez saisir un nombre entier.")
                continue
            assurance = int(assurance_str)

            # On vérifie que le joueur à assez d'argent pour assurer sa mise et que sa mise est inférieure à la moitié
            # de sa mise initiale.
            if assurance <= players[joueur]["mise"] / 2 and assurance <= players[joueur]["solde"]:
                # Vu que nous n'afficherons pas les soldes en temps réel, nous pouvons gérer directement les
                # évolutions du solde ici pour simplifier la gestion de la fin de partie.
                # Si la mise est valide, on déduit le montant de l'assurance du solde du joueur.
                players[joueur]["solde"] -= assurance
                # Si le croupier a un blackjack, le joueur gagne le double de sa mise d'assurance.
                if est_blackjack(main_croupier):
                    players[joueur]["solde"] += assurance * 2
                return True
            else:
                print(
                    "Vous ne pouvez pas assurer une mise plus élevée que la moitié de votre mise initiale ou plus "
                    "grande que votre solde.")
    else:
        # Si le croupier n'a pas d'As, le joueur ne peut pas s'assurer.
        print("Vous ne pouvez pas assurer votre mise car le croupier n'a pas d'as.")
        return False


def a_perdu(joueur):
    """
    Détermine si un joueur a perdu en calculant la valeur de sa main et en la comparant à 21.

    :param:
        joueur (str) : Nom du joueur dans le dictionnaire "players".

    :return:
        bool : True si le joueur a perdu, False sinon
    """
    # On calcule la valeur de la main du joueur
    valeur_main = calculer_valeur_main(players[joueur]["cartes"])
    # Si la valeur est supérieure à 21, le joueur a perdu
    if valeur_main > 21:
        return True
    else:
        return False


def demander_action(joueur):
    """
    Demande au joueur quelle action il souhaite effectuer et retourne son choix.

    :param:
        joueur (int): L'identifiant du joueur.

    :return:
        int : Le choix de l'action à effectuer.

    """
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
        # On vérifie que la valeur saisie est un entier
        if not action_str.isdigit():
            print("La valeur saisie n'est pas un entier valide.")
            continue
        action = int(action_str)
        # On vérifie que la valeur saisie est comprise entre 1 et 6
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
        choix = sys.stdin.readline().rstrip('\n')  # On récupère la saisie sans le retour à la ligne
        choix = choix.lower()  # On met la saisie en minuscule
        # On vérifie que la saisie est correcte
        while choix not in ["o", "n"]:
            print("Veuillez saisir 'o' pour 'oui' ou 'n' pour 'non'.")
            choix = sys.stdin.readline().rstrip('\n')
            choix = choix.lower()
        if choix == "o":
            # On ajoute une carte à la main du joueur s'il choisit 'o' (oui)
            ajouter_carte(players[joueur]["cartes"])
        elif choix == "n":
            # On passe au joueur suivant s'il choisit 'n' (non)
            pass
    elif action == 2:
        # double_mise renvoie faux si le joueur n'a pas assez d'argent pour doubler sa mise
        if not doubler_mise(joueur):
            # Si doubler_mise renvoie faux on redemande une action
            demander_action(joueur)
        else:
            # Si le joueur a assez d'argent pour doubler sa mise, on lui ajoute une carte
            ajouter_carte(players[joueur]["cartes"])
            # on affiche sa main
            print("Votre main est maintenant : " + str(players[joueur]["cartes"]))
    elif action == 3:
        # La fonction split() renvoie faux si le joueur n'a pas une paire
        if not split(joueur):
            # Si split renvoie faux on redemande une action
            demander_action(joueur)
    elif action == 4:
        # La fonction assurer() renvoie faux si le joueur ne peut pas assurer sa mise
        if not assurer(joueur):
            # Si assurer renvoie faux on redemande une action
            demander_action(joueur)
    elif action == 5:
        # On met le joueur en mode "ne joue pas" s'il abandonne
        players[joueur]["joue"] = False
        print("Vous avez abandonné la partie.")
    else:
        # On passe au joueur suivant s'il ne veut rien faire
        pass


def est_quelqu_un_en_jeu():
    """
    Vérifie si au moins un joueur est en jeu.

    :param:
        None

    :return:
        bool : True si au moins un joueur est en jeu, False sinon.
    """
    # On parcourt la liste des joueurs
    for joueur in players:
        # Si un joueur est en jeu, on renvoie True
        if players[joueur]["joue"]:
            return True
    # Si aucun joueur n'est en jeu, on renvoie False et on affiche un message
    print("Personne ne joue.")
    return False


def jouer_tour():
    """
    Fonction qui joue un tour de jeu de blackjack.

    :param:
        None

    :return:
        None
    """
    # On initialise le tour
    initialiser_le_tour()

    # Si personne ne joue on arrête la fonction
    if not est_quelqu_un_en_jeu():
        return

    # On affiche les informations au début du tour
    affichage_debut_partie()

    # On effectue les actions de chaque joueur
    for joueur in players:
        # On vérifie si le joueur est toujours en jeu
        if players[joueur]["joue"]:
            # On regarde si le joueur a fait un blackjack
            if est_blackjack(players[joueur]["cartes"]):
                # Si le joueur a un blackjack, on lui annonce
                print("Vous avez fait un blackjack !")
                # On met le joueur en mode "ne joue pas"
                players[joueur]["joue"] = False
                # On met à jour le solde du joueur
                players[joueur]["solde"] += players[joueur]["mise"] * 2.5
            else:
                # Si le joueur n'a pas un blackjack, on lui demande l'action à faire
                demander_action(joueur)
            # On vérifie que le joueur n'a pas perdu
            if a_perdu(joueur):
                # Si le joueur a perdu, on lui annonce
                print("Vous avez perdu !")
                # On met le joueur en mode "ne joue pas"
                players[joueur]["joue"] = False

    # On fait jouer le croupier
    if est_blackjack(main_croupier):
        # Si le croupier a un blackjack, tous les joueurs en jeu perdent
        print("Le croupier a fait un blackjack, tous les joueurs en jeu perdent !")
        return
    else:
        # Tant que la valeur de la main du croupier est inférieure à 17, il doit piocher une carte
        while calculer_valeur_main(main_croupier) < 17:
            ajouter_carte(main_croupier)
        # On annonce que le croupier a fini de jouer
        print("Le croupier a fini de jouer.")
        # On affiche la main du croupier
        print("La main du croupier est : " + str(main_croupier))
        # On vérifie que le croupier n'a pas perdu
        if calculer_valeur_main(main_croupier) > 21:
            # Si le croupier a perdu, on annonce que les joueurs encore en jeu ont gagné
            print("Le croupier a perdu !\nLes joueurs encore en jeu gagnent !")
            # On met à jour le solde des joueurs
            for joueur in players:
                if players[joueur]["joue"]:
                    players[joueur]["solde"] += players[joueur]["mise"] * 2
        else:
            # Si le croupier n'a pas perdu, on compare les mains des joueurs avec celle du croupier
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


def demander_quitter_partie():
    """
    Demande à un joueur s'il souhaite quitter la partie de blackjack.

    :param:
        None

    :return:
        None
    """
    # On demande si quelqu'un veut quitter la partie
    print("Est ce que quelqu'un souhaite quitter la partie ? (o/n)")

    # On lit la réponse du joueur sur l'entrée standard
    choix = sys.stdin.readline().rstrip('\n')
    choix = choix.lower()

    # On s'assure que la réponse est valide (soit "o" pour oui, soit "n" pour non)
    while choix not in ["o", "n"]:
        print("Veuillez saisir 'o' pour 'oui' ou 'n' pour 'non'.")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()

    if choix == "o":
        # Si le joueur veut quitter la partie, on lui demande son nom
        print("Quel est le nom du joueur qui quitte la partie ?")
        nom = sys.stdin.readline().rstrip('\n')
        indice = 0

        # On vérifie que le nom du joueur est bien celui d'un joueur de la partie et on récupère son indice
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
        # Si personne ne veut quitter la partie, on quitte simplement la fonction
        return


def demander_rejoindre_partie():
    """
    Demande si un nouveau joueur veut rejoindre la partie.

    :param:
        None

    :return:
        None
    """
    # On demande à l'utilisateur si un nouveau joueur souhaite rejoindre la partie
    print("Est ce que quelqu'un souhaite rejoindre la partie ? (o/n)")
    choix = sys.stdin.readline().rstrip('\n')
    choix = choix.lower()

    # On boucle jusqu'à ce que l'utilisateur donne une réponse valide
    while choix not in ["o", "n"]:
        print("Veuillez saisir 'o' pour 'oui' or 'n' pour 'non'.")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()

    # Si un nouveau joueur veut rejoindre la partie
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
    # Si personne ne veut rejoindre la partie
    else:
        return


def est_partie_terminee():
    """
    Vérifie si la partie est terminée.

    :param:
        None

    :return:
        True si la partie est terminée, False sinon
    """
    if len(players) == 0:  # si la liste des joueurs est vide
        return True  # on retourne True pour indiquer que la partie est terminée
    else:
        return False  # sinon, la partie n'est pas terminée, on retourne False


def supprimer_joueurs_perdus():
    """
    Supprime les joueurs de la partie qui n'ont plus d'argent.

    :param:
        None

    :return:
        None
    """
    # On parcourt tous les joueurs de la partie
    for joueur in players:
        # Si le solde du joueur est inférieur ou égal à 0, il a perdu
        if players[joueur]["solde"] <= 0:
            # On affiche le nom du joueur qui a perdu
            print(players[joueur]["nom"] + " a perdu car il n'a plus d'argent!")
            # On supprime le joueur de la partie
            del players[joueur]


def demander_rejouer_partie():
    """
    Demande à l'utilisateur s'il souhaite rejouer une partie.

    :param:
        None

    :return:
        True si l'utilisateur souhaite rejouer une partie, False sinon
    """
    # On demande à l'utilisateur s'il souhaite rejouer une partie
    print("Voulez vous rejouer une partie ? (o/n)")
    choix = sys.stdin.readline().rstrip('\n')
    choix = choix.lower()
    # On boucle jusqu'à ce que l'utilisateur donne une réponse valide
    while choix not in ["o", "n"]:
        print("Veuillez saisir 'o' pour 'oui' or 'n' pour 'non'.")
        choix = sys.stdin.readline().rstrip('\n')
        choix = choix.lower()
    if choix == "o":
        # Si l'utilisateur souhaite rejouer une partie, on retourne True
        return True
    else:
        # Si l'utilisateur ne souhaite pas rejouer une partie, on retourne False
        return False


def vider_cartes_joueurs():
    """
    Vide les cartes des joueurs en réinitialisant leur liste de cartes.

    :param:
        None

    :return:
        None
    """
    # On parcourt tous les joueurs de la partie
    for joueur in players:
        # Réinitialisation de la liste des cartes du joueur
        players[joueur]["cartes"] = []


def jouer_partie():
    """
    Joue une partie de blackjack.

    :param:
        None

    :return:
        None
    """
    # On initialise une variable qui indique si on veut rejouer une partie
    do_replay = True
    while do_replay:
        # On initialise le jeu
        initialisation()
        # On joue des tours tant que la partie n'est pas terminée
        while not est_partie_terminee():
            # On vide les cartes des joueurs pour enlever les cartes de la partie précédente
            vider_cartes_joueurs()
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
