#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Projet de Programmation Scientifique
Groupe : Lucille Caradec et Tom-Hadrian Sy
Theme : Logiciel d'Apprentissage de Langues

Fonctions et classes
"""

# Importation des modules
import pandas as pd
import datetime
import os


### Définition des variables globales ###
DATE_DU_JOUR = datetime.date.today()

#Pourcentages des mots de score 0,1,2,3 constituant la liste de révision
PARAMETRES_DEFAUT = {'Mots_niv0': 40,
                     'Mots_niv1': 30,
                     'Mots_niv2': 20,
                     'Mots_niv3': 10, }

# Etablissement du chemin
os.chdir(os.path.abspath(os.getcwd())+'/data/')


### DEFINITION DES CLASSES ###

class ListePaquets(object):
    '''
    La classe ListePaquets gere tous les paquets par défaut de l'application
    '''

    # Definition du constructeur
    def __init__(self):
        '''
        Initialisation de l'objet
        '''
        
        #importation du fichier
        fich = pd.read_excel("Voc_par_defaut.xlsx")
        self.liste = fich

    # Definition des methodes
    def __str__(self):
        '''
        Permet d'imprimer la liste des Paquets

        Returns
        -------
        text : string
            Contient une description de la liste
        '''
        text = "Paquets par défaut : \n"
        numPaquet = self.liste["NumPaquet"].unique()
        nomPaquet = self.liste["NomPaquet"].unique()

        for i in range(len(numPaquet)):
            text += "Paquet " + \
                str(numPaquet[i]) + " || " + nomPaquet[i] + '\n'

        return(text)

    def getList(self):
        '''
        Retourne les données des paquets par défaut sous forme de listes 
        Méthode seulement utilisée pour l'affichage GUI

        Return
        ----------
        L_num : liste des numeros des paquets (str)
        L_nom : listes des noms des paquets (str)
        '''
        L_num = list(self.liste["NumPaquet"].unique())
        L_nom = list(self.liste["NomPaquet"].unique())

        return(L_num, L_nom)

    def selectPaquet(self, idPaquet):
        '''
        Permet de selectionner un paquet a partir de la liste des paquets par 
        defaut

        Parameters
        ----------
        idPaquet : int
            Identifiant du paquet dans la base de données

        Returns
        -------
        paq : dataframe
            Un dataframe contenant une liste de mots dans la langue
            d'apprentissage et leur traduction en francais
        idPaquet : int
            Identifiant du paquet dans la base de données
        NomPaquet : string
            Nom du paquet (ex : 100 mots en Espagnol)

        '''
        paq = self.liste.loc[
            self.liste['NumPaquet'] == idPaquet,
            ['Langue_apprentissage', 'Francais']]
        NomPaquet = self.liste.loc[
            self.liste['NumPaquet'] == idPaquet, 'NomPaquet'].unique()
        if paq.empty:
            raise ValueError
        return(paq, idPaquet, NomPaquet[0])


class ListeUsers(object):
    '''
    La classe ListeUsers gere tous les utilisateurs de l'application'
    '''

    # Definition du constructeur
    def __init__(self):
        '''
        Initialiser ListeUsers
        '''
        try:
            self.df_users = pd.read_excel("Users.xlsx")

        except FileNotFoundError:
            header = pd.DataFrame(
                columns=["id", "Nom", "Prénom", "Paramètres"])

            header.to_excel("Users.xlsx", index=False)
            self.df_users = pd.read_excel("Users.xlsx")

    # Definition des methodes

    def __str__(self):
        '''
        Afficher la liste des utilisateurs et leurs identifiants

        Returns
        -------
        text : string
            Variable qui contient les informations à afficher

        '''
        if self.df_users.empty:
            return('Il n\'existe pas encore d\'utilisateurs\n')
        else:
            text = '---Affichage des utilisateurs---\n'
            for i in range(len(self.df_users)):
                text += f"\nIdentifiant : {self.df_users['id'][i]}"
                text += f"\nPrénom : {self.df_users['Prénom'][i]}"
                text += f"\nNom : {self.df_users['Nom'][i]}\n-----------"
            return(text)

    def isEmpty(self):
        '''
        Retourne un booléen qui détermine si la liste des utilisateurs est 
        vide, ou non
        '''
        return(self.df_users.empty)

    def getList(self):
        '''
        Retourne les données des utilisateurs sous forme de listes 
        Méthode seulement utilisée pour l'affichage GUI

        Return
        ----------
        L_users : liste des données des utilisateurs (str)
        L_id : listes des identifiants
        '''
        L_users, L_id = [], []
        for i in range(len(self.df_users)):
            string = f'{self.df_users["Prénom"][i]} {self.df_users["Nom"][i]}'
            L_users.append(string)
            L_id.append(self.df_users["id"][i])
        return(L_users, L_id)

    def addUser(self, new_User):
        '''
        Ajout d'un nouvel utilisateur et sauvegarde dans la base de données.

        Parameters
        ----------
        new_User : objet de la classe User

        '''
        ide = create_new_id(self.df_users)
        nom, prenom, parametres, paquets = new_User.getInfo()
        self.df_users = self.df_users.append({'id': ide,
                                              "Nom": nom,
                                              "Prénom": prenom,
                                              "Paramètres": parametres},
                                             ignore_index=True)
        self.save()

    def removeUser(self, idUser):
        '''
        Suppression d'un utilisateur dans la base de données

        Parameters
        ----------
        idUser : string
            Identifiant de l'utilisateur dans la base de données
        '''
        pos = self.df_users["id"].tolist().index(idUser)

        # suppression de l'excel
        prenom = self.df_users['Prénom'][pos]
        os.remove(prenom+'.xlsx')

        # suppression des données de l'utilisateur dans le dataframe
        self.df_users = self.df_users.drop(self.df_users.index[[pos]], axis=0)
        
        self.df_users = self.df_users.reset_index(drop=True)
        # fait que l'index du dataframe commence à 0 
        
        self.save()

    def save(self):
        '''
        Permet de sauvegarder la base de données dans un excel.

        '''
        self.df_users.to_excel('Users.xlsx', index=False)

    def selectUser(self, idUser):
        '''
        Crée un objet User a partir de la selection d'un identifiant

        Parameters
        ----------
        idUser : string
            Identifiant de l'utilisateur dans la base de données.

        Returns
        -------
        User : un objet de la classe User

        '''
        pos = self.df_users["id"].tolist().index(idUser)
        nom = self.df_users.loc[pos, 'Nom']
        prenom = self.df_users.loc[pos, 'Prénom']

        parametres = self.df_users.loc[pos,
                                       'Paramètres']

        return(User(nom, prenom, parametres))


class User(object):
    '''
    La classe User gere toutes les informations relatives a l'apprentissage
    d'un utilisateur dans l'application. 
    '''

    # Definition du constructeur
    def __init__(self, nom, prenom, parametres=PARAMETRES_DEFAUT):
        '''
        Initialiser l'objet User

        Parameters
        ----------
        nom : string
            Nom de famille de l'utilisateur.
        prenom : string
            Prenom de l'utilisateur.
        parametres : dataframe, optional
            Contient les paramètres d'apprentissage : nombre de mots de score
            0, 1, 2 et 3 à montrer à chaque session d'apprentissage.
            The default is PARAMETRES_DEFAUT.
        '''

        self.nom = nom
        self.prenom = prenom
        self.parametres = parametres

        # Charger les paquets et le progres de l'utilisateur, enregistre dans
        # un xlsx a son nom
        try:
            self.paquets = pd.read_excel(prenom+'.xlsx')
            # l'argument paquet contient les listes de vocabulaire et les progres
            # effectues par l'utilisateur

        except FileNotFoundError:
            # lorsqu'un nouvel utilisateur est créé, son fichier est créé aussi
            header = pd.DataFrame(columns=["Langue_apprentissage", "Francais",
                                           "NumPaquet", "NomPaquet", 
                                           "Score", "Date"])
            chemin = prenom + '.xlsx'
            header.to_excel(chemin, index=False)
            self.paquets = pd.read_excel(chemin)

   # Definition des methodes

    def getInfo(self):
        '''
        Renvoie les informations de l'utilisateur
        '''
        return(self.nom, self.prenom, self.parametres, self.paquets)

    def showPaquets(self):
        '''
        Montrer les paquets de l'utilisateur

        Returns
        -------
        text : string
            Contient la description des paquets de l'utilisateur
        '''
        if self.paquets.empty:
            text = 'Cet utilisateur n\'a pas encore de paquets enregistrés.\n'
            return(text)
        else:
            text = f"Listes de vocabulaire de {self.prenom} {self.nom}\n"
            numPaquet = self.paquets["NumPaquet"].unique()
            nomPaquet = self.paquets["NomPaquet"].unique()

            for i in range(len(numPaquet)):
                text += f"Paquet {numPaquet[i]} || {nomPaquet[i]}\n"
            return(text)

    def getList(self):
        '''
        Retourne les données des paquets de l'utilisateur sous forme de listes 
        Méthode seulement utilisée pour l'affichage GUI

        Return
        ----------
        L_num : liste des numeros des paquets (str)
        L_nom : listes des noms des paquets (str)
        '''
        L_num = list(self.paquets["NumPaquet"].unique())
        L_nom = list(self.paquets["NomPaquet"].unique())

        return(L_num, L_nom)

    def selectPaquet(self, idPaquet):
        '''
        Sélectionne un paquet pour la session d'apprentissage

        Parameters
        ----------
        idPaquet : int
            Identifiant du paquet dans la base de données de l'utilisateur.

        Returns
        -------
        paq : dataframe
            Un dataframe contenant un liste de mots dans la Langue d'apprentissage
            et leur traduction en français, ainsi que leur Score et la date de 
            la dernière session sur ce paquet

        '''
        paq = self.paquets.loc[
            self.paquets['NumPaquet'] == idPaquet,
            ['Langue_apprentissage', 'Francais', 'Score', 'Date']]

        if paq.empty:
            raise ValueError
        return(paq)

    def addPaquet(self, paquet, numPaquet, nomPaquet):
        '''
        Ajouter un paquet à la liste des paquets de l'utilisateur

        Parameters
        ----------
        paquet : dataframe
            Un paquet de l'ensemble des paquets par défaut, qui contient les 
            mots dans la langue d'apprentissage et leur traduction en français.
        numPaquet : int
            Le numéro d'identifiant du Paquet.
        nomPaquet : string
            Le nom du paquet dans la base de données.
        '''

        paquet = paquet.reset_index(drop=True)
        # fait que l'index de paquet commence à 0 ; sinon l'index du subset est
        # hérité du dataframe d'origine

        # on cree un nouveau dataframe qui respecte le format de self.paquets
        paq = pd.DataFrame({
            'Langue_apprentissage': paquet['Langue_apprentissage'],
            'Francais': paquet['Francais'],
            'NumPaquet': pd.Series([numPaquet] * len(paquet['Francais'])),
            'NomPaquet': pd.Series([nomPaquet] * len(paquet['Francais'])),
            'Score': [0] * len(paquet['Francais']),
            # on initialise le score a 0, ce qui signifie que l'utilisateur n'a
            # jamais vu le mot
            'Date': pd.Series([pd.Timestamp(DATE_DU_JOUR)] * len(paquet['Francais']))
        })

        # on ajoute le nouveau paquet à la liste de paquets de l'utilisateur
        self.paquets = pd.concat([self.paquets, paq])
        # on sauvegarde le nouveau paquet
        self.savePaquets()

    def removePaquet(self, numPaquet):
        '''
        Supprimer un paquet de la liste de l'utilisateur

        Parameters
        ----------
        numPaquet : int
            L'identifiant du paquet.
        '''
        indexNames = self.paquets[self.paquets['NumPaquet'] == numPaquet].index
        self.paquets.drop(indexNames, inplace=True)
        self.savePaquets()

    def changerScore(self, idPaquet, score, mots):
        '''
        Changer le score sur un mot

        Parameters
        ----------
        idPaquet : int
            Identifiant du paquet de l'User
        score : int
            Score attribué par l'utilisateur
        mots : dataframe
            DF contenant le mot dans la langue d'apprentissage et en français
        '''

        ligneMot = self.paquets[(self.paquets['NumPaquet'] == idPaquet) &
                                (self.paquets['Langue_apprentissage'] ==
                                 mots['Langue_apprentissage'][0])]
        indexMot = ligneMot.index
        self.paquets.loc[indexMot, 'Score'] = score
        self.paquets.loc[indexMot, 'Date'] = DATE_DU_JOUR

    def savePaquets(self):
        '''
        Permet de sauvegarder les progres de l'utilisateur
        '''
        self.paquets = self.paquets.reset_index(drop=True)
        # fait que l'index de paquet commence à 0 ; sinon l'index du subset est
        # hérité du dataframe d'origine
        chemin = self.prenom + '.xlsx'
        self.paquets.to_excel(chemin, index=False)


### DEFINITION DES FONCTIONS ###

def create_new_id(df):
    '''
    La fonction create_new_id permet de creer un identifiant d'utilisateur
    en évitant les redondances.
    
    Parameters
    ----------
    df : dataframe : le tableau d'utilisateurs'
    Returns
    -------
    Un nouvel identifiant, qui n'est pas déjà utilisé par un utilisateur
    '''
    if df.empty:
        return 'U1'
    else:
        L = []
        for ide in df["id"]:
            L.append(int(ide[1:]))
            # on stocke dans la liste L tous les numeros d'utilisateurs
            # ide[1:] permet le slicing de "UX" pour récupérer uniquement le
            # numéro d'utilisateur
        return 'U'+str(max(L)+1)

def reviser(User, paq, temps, idPaquet):
    '''
    La fonction reviser permet de faire réviser l'utilisateur, c'est a dire lui
    présenter les mots un a un et noter sa connaissance du mot.

    Parameters
    ----------
    User : objet de la classe User
        Utilisateur de la session active
    paq : dataframe
        Le paquet ayant été sélectionné pour révision
    idPaquet : int
        Identifiant d'un des paquets associés à User
    temps : int
        Temps de révision demandé par l'User, en minutes
    '''

    # Definition de la repartition de la session
    if type(User.getInfo()[2])== dict :
        parametres = User.getInfo()[2]
    else :
        parametres = eval(User.getInfo()[2])
    # évalue l'expression contenu dans le string -> creation du dico

    # calcul du nombre de mots en fonction du temps
    nb_mots = round(temps * 60 / 15)

    l_mots = listeRevision(paq, nb_mots, parametres)

    # Debut de la session

    print('\n ---Début de la session de révision --- \n')
    print('Vous allez d\'abord voir le mot dans la langue d\'apprentissage. ' +
          'Pour voir la traduction en français, appuyer sur la touche ' +
          'Enter.\nBon apprentissage!\n')

    len_l_mots = len(l_mots)
    i = 0
    while len(l_mots) != 0:

        print(f'\n {i+1} / {len_l_mots}')

        tmp = l_mots.sample(1).reset_index(drop=True)  # reset de l'index à 0

        score = montrerMots(tmp['Langue_apprentissage'][0],
                            tmp['Francais'][0])

        # Si le score est non nul l'utilisateur ne reverra pas ce mot dans
        # la session
        # (Si le score vaut 0, le mot est conservé dans la liste de mots)
        if score != 0:

            pos = l_mots['Langue_apprentissage'].tolist().index(
                tmp['Langue_apprentissage'][0])
            l_mots = l_mots.drop(l_mots.index[[pos]], axis=0)
            # on retire le mot de la liste du jour
            User.changerScore(idPaquet, score, tmp)
            # on change le score dans l'objet User

            i += 1

    # à la fin de la session de revision, on enregistre les progrès de
    # l'utilisateur
    User.savePaquets()

    print('\n--- Fin de la session --- \n')

def listeRevision(paq, nb_mots, parametres):
    '''
    Permet de creer une liste de mots à réviser

    Parameters
    ----------
    paq : dataframe
        Un paquet de mots extrait de la base de données de l'utilisateur.
        Contient les colonnes Langue_apprentissage, Francais, Score et Date
    nb_mots : int
        Nombre de mots total que doit contenir la liste
    parametres : Dictionnaire
        Proportion de mots en % a présenter à l'utilisateur en fonction du score
    Returns
    -------
    l_mots : dataframe
        Une liste de mots dans la langue d'apprentissage et leur traduction en 
        Francais.
    '''
    
    #plafonnement du maximum du nombre de mots à réviser au nombre de mots
    #effectivement présents dans le paquet
    nb_mots = min(nb_mots, len(paq['Langue_apprentissage']))
    
    
    #initialisation de la liste de mots à réviser
    l_mots = pd.DataFrame(columns=["Langue_apprentissage", "Francais"])

    # Mots de niveau 0 : jamais vus par l'utilisateur
    niv0 = paq.loc[paq['Score'] == 0, ['Langue_apprentissage', 'Francais']]

    l_mots = l_mots.append(niv0.sample(
        min(int(nb_mots * parametres['Mots_niv0']/100),len(niv0))))
    
    # Mots de niveau 1 : mauvaise connaissance, revus en priorité,
    # sélectionnés si ils ont été vus il y a 2 jours ou plus
    niv1 = paq.loc[(paq['Score'] == 1) &
                   (paq['Date'] >= pd.Timestamp(
                       DATE_DU_JOUR - datetime.timedelta(days=1))),
                   ['Langue_apprentissage', 'Francais']]

    if not niv1.empty:
        l_mots = l_mots.append(niv1.sample(
            min(int(nb_mots * parametres['Mots_niv1']/100),len(niv1))))

    # Mots de niveau 2 : connaissance moyenne, sélectionnés si ils ont été
    # vus il y a 2 jours ou plus
    niv2 = paq.loc[(paq['Score'] == 2) &
                   (paq['Date'] >= pd.Timestamp(
                       DATE_DU_JOUR - datetime.timedelta(days=2))),
                   ['Langue_apprentissage', 'Francais']]

    if not niv2.empty:
        l_mots = l_mots.append(niv2.sample(
            min(int(nb_mots * parametres['Mots_niv2']/100),len(niv2))))

    # Mots de niveau 3 : bonne connaissance, sélectionnés si ils ont été vus il
    # y a 4 jours ou plus
    niv3 = paq.loc[(paq['Score'] == 3) &
                   (paq['Date'] >= pd.Timestamp(
                       DATE_DU_JOUR - datetime.timedelta(days=4))),
                   ['Langue_apprentissage', 'Francais']]

    if not niv3.empty:
        l_mots = l_mots.append(niv3.sample(
            min(int(nb_mots * parametres['Mots_niv3']/100),len(niv3))))
        
    # S'il n'existe pas encore de mots classés niveau 1, 2, 3 (première
    # utilisation de l'application), la liste est completée de mots de niv0
    if len(l_mots) < nb_mots:
        diff = nb_mots - len(l_mots)
        l_mots = l_mots.append(niv0.sample(diff))
        
    return(l_mots)

def montrerMots(mot1, mot2):
    '''
    La fonction montrerMots permet de montrer deux mots a faire reviser.

    Parameters
    ----------
    mot1 : string
        Mot dans la langue d'apprentissage
    mot2 : string
        Mot en français

    Returns
    -------
    score : int
        Le score que l'utilisateur s'attribue sur sa connaissance du mot
            0 : mauvaise
            1 : moyenne
            2 : bonne
            3 : très bonne
    '''

    input(f'Mot proposé : {mot1} \n(Pressez Enter pour révéler sa traduction)')
    # mettre une fonction input permet d'attendre un retour de l'utilisateur
    # avant de continuer
    print(f'\n >> Traduction : {mot2}')

    score = input("\n--- Quelle est votre connaissance du mot?\n"
                      "0 : Mauvaise - je veux revoir le mot dans la session "
                      "d'aujourd'hui\n"
                      "1 : Moyenne - je veux revoir ce mot dans la prochaine" 
                      "session\n"
                      "2 : Bonne - je veux revoir ce mot dans une semaine\n"
                      "3 : Très bonne - je n'ai pas besoin de revoir ce mot\n\n"
                      "Entrez un chiffre > ")

    while score not in ['0', '1', '2', '3']:
        score = input("Veuillez entrer une valeur correcte (0,1,2,3) : ")

    return(int(score))
