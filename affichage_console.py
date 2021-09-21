# -*- coding: utf-8 -*-
"""
Projet de Programmation Scientifique
Groupe : Lucille Caradec et Tom-Hadrian Sy
Theme : Logiciel d'Apprentissage de Langues

Interface console
"""

### Importation des modules
from classes_fonctions import *

### PROGRAMME PRINCIPAL
print(' --- Bienvenue dans l\'application ! --- ')
print(DATE_DU_JOUR,'\n')

#Affichage de tous les utilisateurs enregistrés
liste_users = ListeUsers()
print(liste_users)

terminer = False
while not terminer: 
    
    #Proposition d'ajouter, supprimer ou choisir un utilisateur
    print(' --- Que voulez-vous faire ?')
    print('Pour choisir un utilisateur, tapez 1')
    print('Pour créer un nouvel utilisateur, tapez 2')
    print('Pour supprimer un utilisateur, tapez 3')
    print('Pour quitter l\'application, tapez 4')
    
    choix_action = input('Entrez un chiffre > ')
    while choix_action not in ['1','2','3','4']:
        print('Erreur : la commande rentrée n\'est pas valide')
        choix_action = input('Entrez un chiffre > ')
    
    
    ###Choix d'un utilisateur
    if choix_action == '1':
        
        #S'il n'existe pas encore d'utilisateurs un message d'erreur s'affiche
        if liste_users.isEmpty() : 
            print("\nErreur : Créez d'abord un utilisateur\n")
            
        else :
            repet = True
            while repet :
                choix_id = input('Quel utilisateur voulez-vous choisir '+
                                 '(entrez son identifiant) ? ')
                try :
                    user = liste_users.selectUser(choix_id)
                    repet = False
                except ValueError : 
                    print('Erreur : l\'identifiant rentré est incorrect')
            
            retour = False
            while not retour: 
                
                prenom_nom = str(user.getInfo()[1]) + ' ' + str(user.getInfo()[0])
                print(f'\n --- Choix de l\'utilisateur {prenom_nom} --- \n')
               
                #Affichage de la liste des paquets par défaut
                l_paquets = ListePaquets()
                print(l_paquets)
                 
                #Affichage des paquets de l'utilisateur
                print(user.showPaquets())
                
                #Proposition d'ajouter, supprimer ou choisir un paquet
                print(' --- Que voulez-vous faire ?')
                print('Pour choisir un paquet à réviser, tapez 1')
                print('Pour ajouter un nouveau paquet, tapez 2')
                print('Pour supprimer un paquet, tapez 3')
                print('Pour retourner au menu principal, tapez 4')
                
                choix_action2 = input('Entrez un chiffre > ')
                while choix_action2 not in ['1','2','3','4']:
                    print('Erreur : la commande rentrée n\'est pas valide')
                    choix_action2 = input('Entrez un chiffre > ')
                
                
                #Choix d'un paquet
                if choix_action2 == '1':
                    
                    #Si l'utilisateur n'a pas encore de paquets, un message 
                    #d'erreur s'affiche
                    if user.paquets.empty : 
                        print("\nErreur : l\'utilisateur n\'a pas encore de "+
                              "paquets enregistrés\n")
                    
                    else :
                        repet = True
                        while repet :
                            choix_paq = int(input('Quel paquet voulez-vous '+
                                            'réviser (rentrez son numéro) ? '))
                            
                            try :
                                paq_select = user.selectPaquet(choix_paq)
                                repet = False
                                
                            except ValueError : 
                                print('Erreur : le numéro rentré est incorrect')
                                
                        #Début de la session de révision
                        temps_session = int(input('De combien de temps (min) '+
                                            'disposez-vous pour réviser ? '))
                        reviser(user, paq_select, temps_session, choix_paq)

            
                #Ajout d'un paquet à l'utilisateur, depuis la liste des 
                #paquets par défaut
                if choix_action2 == '2':
                    
                    repet = True
                    while repet :
                        choix_paq = int(input('Quel paquet par défaut '+
                                    'voulez-vous ajouter à l\'utilisateur '+
                                    '(rentrez son numéro) ? '))
                        
                        if str(choix_paq) in user.showPaquets() :
                            print("\nErreur : ce paquet a déjà été importé\n")
                    
                        else :
                            try :
                                paquet, num_paq, nom_paq = l_paquets.selectPaquet(choix_paq)
                                user.addPaquet(paquet,num_paq,nom_paq)
                                repet = False
                            except ValueError : 
                                print('Erreur : le numéro rentré est incorrect')
                        
                    
                #Suppression d'un paquet de l'utilisateur
                if choix_action2 == '3':
                    
                    repet = True
                    while repet :
                        choix_paq = int(input('Quel paquet voulez-vous '+
                                    'supprimer (rentrez son numéro) ? '))
                        try :
                            user.removePaquet(choix_paq)
                            repet = False
                        except ValueError : 
                            print('Erreur : le numéro rentré est incorrect')
                    
                
                #Demander à l'utilisateur s'il veut retourner au menu principal
                if choix_action2 == '4':
                    print('\n(Retour au menu principal)\n')
                    retour = True
                
    
    ###Création d'un nouvel utilisateur
    elif choix_action == '2':
        
        nom = input('Entrez le nom du nouvel utilisateur : ')
        prenom = input('Entrez le prénom du nouvel utilisateur : ')
        newUser=User(nom,prenom)
        liste_users.addUser(newUser)
        print('\nL\'utilisateur a bien été ajouté !\n')
        print(liste_users)
     
        
    ###Suppression d'un utilisateur
    elif choix_action == '3':
        
        repet = True
        while repet :
            id = input('Entrez l\'identifiant de l\'utilisateur à supprimer : ')
            try :
                liste_users.removeUser(id)
                repet = False
            except ValueError : 
                print('Erreur : l\'identifiant rentré est incorrect')
        print('L\'utilisateur a bien été supprimé.\n')
        print(liste_users)
    
    
    ###Demander à l'utilisateur s'il veut sortir de l'application
    elif choix_action == '4':
        terminer = True
        print('\nMerci et à la prochaine !')
   
    
    