# -*- coding: utf-8 -*-
"""
Projet de Programmation Scientifique
Groupe : Lucille Caradec et Tom-Hadrian Sy
Theme : Logiciel d'Apprentissage de Langues

Graphical User Interface (GUI)
"""

### Importation des modules
from classes_fonctions import *
import tkinter as tk
from tkinter import messagebox

### PROGRAMME PRINCIPAL

class MainApp(object):
    '''classe principale : menu principal de l'application, gestion des 
    utilisateurs, des options, des statistiques'''
    
    def __init__(self, master):
        '''constructeur : écran principal'''
        
        self.master = master
        
        #importation de la liste d'utilisateurs
        liste_users = ListeUsers()
        
        #Définition du menu principal
        self.menubar = tk.Menu(self.master)
        
        #Onglet gestion des utilisateurs
        self.menu_user = tk.Menu(self.menubar, tearoff=0)
        self.menu_user.add_command(label="Choisir un utilisateur et réviser", 
                              command = lambda: self.switch('revise',
                                                            [liste_users]))
        
        self.menu_user.add_command(label="Créer un utilisateur",
                              command = lambda: self.switch('create',
                                                            [liste_users]))
        
        self.menu_user.add_command(label="Supprimer un utilisateur",
                              command = lambda: self.switch('remove',
                                                            [liste_users]))

        self.menubar.add_cascade(label="Gérer les utilisateurs", 
                                 menu=self.menu_user)
      
        self.master.config(menu=self.menubar)
        
        #affichage de l'écran d'accueil
        self.bienvenue = tk.Label(self.master, 
                           text = '--- Bienvenue dans l\'application ! ---\n' +
                           str(DATE_DU_JOUR) +
                           '\nVeuillez vous connecter' +
                           '\n\n\n' + str(liste_users))
    
        self.bienvenue.place(relx =0.3)

    
    def all_children(self) :
        '''renvoie la liste de tous les widgets présents au sein d'un parent'''
        _list = self.master.winfo_children()

        for item in _list :
            if item.winfo_children() :
                _list.extend(item.winfo_children())
        return _list
    
    
    def clear_widgets(self) :
        ''' efface tous les widgets de la fenêtre '''
        widget_list = self.all_children()
        for item in widget_list:
            item.place_forget()
            item.grid_forget()
            item.pack_forget()
        
    
    def switch(self, action, L_param = []):
        '''permet de switch entre les différentes options du menu principal'''
        
        #fermeture des anciens widgets
        self.clear_widgets()
        
        #exécution de la nouvelle action demandée
        if action == 'revise':
            self.chooseUser(L_param[0], action)
            
        elif action == 'create':
            self.createUser(L_param[0])
            
        elif action == 'remove':
            self.chooseUser(L_param[0], action)
            
        elif action == 'main':
            MainApp.__init__(self,self.master)
            
        elif action == 'user_app':
            UserApp(self.master,L_param[0])
            
    
    def chooseUser(self, liste_users, action):
        '''affichage de l'écran de choix d'un utilisateur'''

        #S'il n'existe pas encore d'utilisateurs un message d'erreur s'affiche
        if liste_users.isEmpty() : 
            messagebox.showerror("Erreur", 
                                 "Il n'existe encore aucun utilisateur enregistré.")
            #retour à l'écran d'accueil
            self.switch('main')
   
        else :
        
            #constitution du widget liste d'utilisateurs
            L_users, L_id = liste_users.getList()
            self.liste = tk.Listbox(self.master,justify='center')
            for i in range(len(L_users)):
                self.liste.insert(i, L_users[i])
            
            self.avant_liste = tk.Label(self.master, 
                                        text = 'Choisir un utilisateur :')
            self.avant_liste.pack(side='top')
            self.liste.pack(side='top')
            self.liste.bind('<ButtonRelease-1>', 
                            lambda x: self.chosenUser(liste_users, 
                                                    L_users, 
                                                    L_id, 
                                                    action))
        
                     
    def chosenUser(self, liste_users, L_users, L_id, action):
        '''traitement de la demande après le choix d'un utilisateur'''
        
        #obtention de l'utilisateur sélectionné dans la liste
        i = self.liste.curselection()
        self.liste.activate(i)
        choix = self.liste.get(i)
        index_choix = L_users.index(choix)
        
        #choix d'action sur cet utilisateur
        if action == 'revise':
            user = liste_users.selectUser(L_id[index_choix])
            self.switch('user_app',[user])

        if action == 'remove':
            choice = messagebox.askquestion("Yes/No", 
                                              "Voulez-vous vraiment supprimer l'utilisateur ?" +
                                              " Ses données seront perdues.", icon='warning')
            if choice == 'yes' :
                liste_users.removeUser(L_id[index_choix])
                
                #retour à l'écran d'accueil
                self.switch('main')
            
        
    def createUser(self, liste_users):
        '''création d'un nouvel utilisateur'''
        
        #définition des widgets
        self.label_prenom = tk.Label(self.master, text = 'Entrez le nom : ')
        self.label_nom = tk.Label(self.master, text = 'Entrez le prénom : ')
        ''' note : la confusion nom/prenom est voulue, sinon il y avait des 
        problemes de continuite entre l'affichage graphique et l'affichage console
        '''    
        
        self.entry_prenom = tk.Entry(self.master)
        self.entry_nom = tk.Entry(self.master)
        self.bouton_confirmer = tk.Button(self.master, 
                                 text = 'Confirmer la saisie',
                                 bg = 'light green',
                                 command = lambda: self.getText(liste_users))

        #affichage sous forme de grid
        self.bouton_confirmer.grid(row=2, column=1, padx=5, pady=5)
        self.entry_prenom.grid(row=0, column=1, padx=5, pady=5)
        self.entry_nom.grid(row=1, column=1, padx=5, pady=5)
        self.label_prenom.grid(row=0, column=0, padx=5, pady=5)
        self.label_nom.grid(row=1, column=0, padx=5, pady=5)
        

    def getText(self, liste_users):
        '''récupère le texte rentré par l'utilisateur dans les champs et ajoute l'utilisateur'''
        
        #récupération du texte dans les champs
        prenom = self.entry_prenom.get()
        nom = self.entry_nom.get()
        
        #ajout du nouvel utilisateur
        newUser=User(nom,prenom)
        liste_users.addUser(newUser)
        messagebox.showinfo("Info","L\'utilisateur a bien été ajouté !")
        
        #retour à l'écran d'accueil
        self.switch('main')
        
         
class UserApp(MainApp):
    '''classe orientée vers la gestion des paquets de l'utilisateur choisi'''
    
    def __init__(self, master, user):
        '''constructeur'''
        self.master = master
        self.user = user
        
        #importation des paquet par défaut
        self.l_paquets = ListePaquets()
        
        #Définition du menu principal
        self.menubar = tk.Menu(self.master)
        
        #Onglet gestion des utilisateurs
        self.menu_user = tk.Menu(self.menubar, tearoff=0)
        self.menu_user.add_command(label="Choisir un paquet et réviser", 
                              command = lambda: self.switch2('revise'))
        
        self.menu_user.add_command(label="Importer un paquet",
                              command = lambda: self.switch2('import'))
        
        self.menu_user.add_command(label="Supprimer un paquet",
                              command = lambda: self.switch2('remove'))

        self.menubar.add_cascade(label="Gérer les paquets", 
                                 menu=self.menu_user)
        
        self.menubar.add_command(label="Retour", 
                              command = lambda: self.switch('main'))

        
        self.master.config(menu=self.menubar)
        
        #affichage de l'écran d'accueil
        self.prenom, self.nom = self.user.getInfo()[1], self.user.getInfo()[0]
        self.affich_paquets = tk.Label(self.master, 
                           text = '--- Vous avez choisi l\'utilisateur ' +
                           f'{self.prenom} {self.nom} ---\n\n' +
                           self.user.showPaquets() + '\n\n' +
                           str(self.l_paquets))
    
        self.affich_paquets.place(relx =0.075)
    
    
    def switch2(self, action, L_param = []):
        '''permet de switch entre les différentes options du menu'''
        
        #fermeture des anciens widgets
        self.clear_widgets()
        
        #exécution de la nouvelle action demandée
        if action in ['revise', 'import', 'remove']:
            self.choosePaquet(action)

        elif action == 'main':
            self.__init__(self.master,self.user)
            
        elif action == 'start_session':
            # self.back = tk.Menu(self.master)
            # self.back.add_command(label="Retour",
            #                   command = self.switch('main'))
            # self.master.config(menu=self.back)            
            Session(self.master,L_param[0],L_param[1],L_param[2])
            
            
    def choosePaquet(self, action):
        '''affichage de l'écran de choix d'un paquet'''

        #S'il n'existe pas encore de paquets un message d'erreur s'affiche
        if self.user.paquets.empty and action in ['revise','remove']: 
            messagebox.showerror("Erreur", 
                                 "Il n'existe encore aucun paquet importé.")
            #retour à l'écran d'accueil
            self.switch2('main')
   
        else :
        
            #constitution du widget liste de paquets
            #si action = revise ou remove, on s'intéresse à la liste des paquets 
            #de l'utilisateur
            if action in ['revise','remove']:
                L_num, L_nom = self.user.getList()
                
            #si action = import, on s'intéresse à la liste des paquets par défaut
            else:
                L_num, L_nom = self.l_paquets.getList()
            
            self.liste = tk.Listbox(self.master,justify='center', width=50)
            for i in range(len(L_num)):
                self.liste.insert(i, "Paquet " 
                                  + str(L_num[i]) 
                                  + ' : ' 
                                  + str(L_nom[i]))
            
            
            self.avant_liste = tk.Label(self.master, text = 'Choisir un paquet')
            self.avant_liste.pack(side='top')
            self.liste.pack(side='top',fill='both',expand=True)
            self.liste.bind('<ButtonRelease-1>', 
                            lambda x: self.chosenPaquet(action, L_num))
        
    
    def chosenPaquet(self, action, L_num):
        '''traitement de la demande après le choix d'un paquet'''
        
        #obtention de l'utilisateur sélectionné dans la liste
        i = self.liste.curselection()
        self.liste.activate(i)
        choix = self.liste.get(i)
        
        for c in choix:
            if c in str(L_num) and c!=' ':
                index_choix = int(c)
                break
           
        #choix d'action sur cet utilisateur
        if action == 'revise':
            paq_select = self.user.selectPaquet(index_choix)

            self.switch2('start_session', [self.user, paq_select, index_choix])

        if action == 'remove':
            choice = messagebox.askquestion("Yes/No", 
                                              "Voulez-vous vraiment supprimer le paquet ?",
                                              icon='warning')
            if choice == 'yes' :
                self.user.removePaquet(index_choix)

                #retour à l'écran d'accueil
                self.switch2('main')
            
        if action == 'import':
            
            if str(index_choix) in self.user.showPaquets():
                messagebox.showerror("Erreur", 
                                 "Ce paquet a déjà été importé.")
            else:
                paquet, num_paq, nom_paq = self.l_paquets.selectPaquet(index_choix)
                self.user.addPaquet(paquet,num_paq,nom_paq)
                messagebox.showinfo("Info","Le paquet a bien été importé !")
            
                #retour à l'écran d'accueil
                self.switch2('main')
            

class Session(UserApp):
    
    def __init__(self, master, user, paq_select, idPaquet):
        ''' constructeur : menu d'introduction à la session '''
        
        self.master = master
        self.user = user
        self.paq_select = paq_select
        self.idPaquet = idPaquet
        
        self.intro = tk.Label(self.master, 
                           text = '\n ---Début de la session de révision --- \n\n' +
                           'Vous allez d\'abord voir le mot dans la langue d\'apprentissage.\n' +
                              'Pour voir la traduction en français, appuyer sur la touche '+
                              'Enter.\nBon apprentissage!\n')
        
        self.label_entry_temps = tk.Label(self.master)
        self.label_temps = tk.Label(self.label_entry_temps,
                                          text = 'Durée de la session (en minutes): ')
        self.entry_temps = tk.Entry(self.label_entry_temps, width=5)
        
        self.bouton_confirmer = tk.Button(self.master, 
                                 text = 'Commencer !',
                                 bg = 'light green',
                                 command = self.startSession)
        
        self.intro.pack(side = 'top')
        self.label_entry_temps.pack(side = 'top')
        self.label_temps.pack(side = 'left')
        self.entry_temps.pack(side = 'left')
        self.entry_temps.pack(side = 'top')
        self.bouton_confirmer.pack(side = 'top', pady = 20)

        
    def startSession(self):
        '''classe gérant l'affichage de la session de révision '''
        
        #vérification que le temps de session rentré est bien conforme
        try :
            temps_session= int(self.entry_temps.get())
            if temps_session <= 0 :
                raise ValueError
                
        except ValueError :
            messagebox.showerror("Erreur", 
                                 "Veuillez entrer une durée valide.")
        
        else:
            #fermeture des anciens widgets
            self.clear_widgets()
            emptymenu=tk.Menu(self.master)
            self.master.config(menu=emptymenu)
            
            # Definition de la repartition de la session
            
            # évalue l'expression contenu dans le string -> creation du dico
            if type(self.user.getInfo()[2])== dict :
                parametres = self.user.getInfo()[2]
            else :
                parametres = eval(self.user.getInfo()[2])
            
            #calcul du nombre de mots en fonction du temps
            nb_mots = round(temps_session * 60 / 15) 
            
            l_mots = listeRevision(self.paq_select, nb_mots, parametres)
              
            #Debut de la session
            i=0
            arret = False
            len_l_mots = len(l_mots)
            while len(l_mots) != 0:
                
                #reset de l'index à 0
                tmp = l_mots.sample(1).reset_index(drop=True) 
                
                score = self.displayWords(tmp['Langue_apprentissage'][0],
                                  tmp['Francais'][0],len_l_mots,i)
                
                #si l'utilisateur veut arrêter la session (score == 4)
                if score == 4 :
                    arret = True
                    l_mots = []
                    
                else:
                    
                    #fermeture des anciens widgets
                    self.clear_widgets()
                    
                    #Si le score est non nul l'utilisateur ne reverra pas 
                    #ce mot dans la session
                    #(Si le score vaut 0, le mot est conservé dans la liste 
                    #de mots)
                    if score != 0:
                        
                        pos = l_mots['Langue_apprentissage'].tolist().index(tmp['Langue_apprentissage'][0])
                        l_mots = l_mots.drop(l_mots.index[[pos]], axis=0)
                        #on retire le mot de la liste du jour
                        self.user.changerScore(self.idPaquet, score, tmp)
                        #on change le score dans l'objet User
                        
                        i += 1
                    
            #à la fin de la session de revision, on enregistre les progrès de
            #l'utilisateur
            self.user.savePaquets()
            
            #message de fécilitations si la session a été terminée jusqu'au bout
            if not arret:
                messagebox.showinfo("Félicitations","Session terminée !")

            #retour à l'écran d'accueil
            self.switch('main')
        
    
    def displayWords(self, mot1, mot2, len_l_mots, i):
        ''' classe gérant l'affichage des mots '''
        
        self.score = tk.IntVar()
    
        self.compteur = tk.Label(self.master, 
                       text = f'\n {i+1} / {len_l_mots} ',
                       borderwidth=2, relief="groove")
                       
        self.bouton_quitter = tk.Button(self.master,
                                 text = 'Quitter la session',
                                 command = lambda: self.update_score(4))

        self.label_mot1 = tk.Label(self.master,
                                   text = f'Mot proposé : {mot1} ')
        
        self.bouton_reponse = tk.Button(self.master, 
                                 text = 'Révéler la traduction',
                                 command = self.revealWidgets)
        
        self.label_mot2 = tk.Label(self.master,
                                   text = f'Sa traduction est : {mot2} ')
        self.label_scores = tk.Label(self.master,
                                     text = "Comment évaluez-vous votre " 
                                     "connaissance du mot ? \n")
        
        self.container = tk.LabelFrame(self.master, text = 'Réponse')

        self.score0 = tk.Button(self.container, 
                                 text = 'Mauvaise',
                                 bg = "red",
                                 command = lambda: self.update_score(0))
        self.score1 = tk.Button(self.container, 
                                 text = 'Moyenne',
                                 bg = "orange",
                                 command = lambda: self.update_score(1))
        self.score2 = tk.Button(self.container, 
                                 text = 'Bonne',
                                 bg = "yellow",
                                 command = lambda: self.update_score(2))
        self.score3 = tk.Button(self.container, 
                                 text = 'Très bonne',
                                 bg = "light green",
                                 command = lambda: self.update_score(3))
        
        self.master.columnconfigure(index=2 ,weight=5)
        self.master.rowconfigure(index=6 ,weight=5)

        self.compteur.grid(row=1, column=1, padx=5, pady=5)
        self.label_mot1.grid(row=2, column=2, padx=5, pady=30)
        self.bouton_reponse.grid(row=3, column=2, padx=5, pady=30)
        self.bouton_quitter.grid(row=7, column=3, padx=5, pady=30)

        #attente de la variable self.score, determinée par le choix de
        #l'utilisateur
        self.master.wait_variable(self.score)
        
        return self.score.get()
        
    
    def update_score(self, value):
        ''' mise à jour du score '''
        
        #si l'utilisateur a cliqué sur le bouton arreter
        if value == 4 :
            choice = messagebox.askquestion("Yes/No", 
                                              "Voulez-vous vraiment quitter"+
                                              " la session en cours ?",
                                              icon='warning')
            if choice == 'yes' :
                self.score.set(value)
        else:
            self.score.set(value)
        
    
    def revealWidgets(self):
        ''' classe affichant la traduction du mot et le choix du score '''
        
        #suppression du bouton "réveler la réponse"
        self.bouton_reponse.grid_forget()
        
        self.label_mot2.grid(row=4, column=2, padx=5, pady=5)
        self.label_scores.grid(row=5, column=2, padx=5, pady=5)
        self.container.grid(row=6, column=2, padx=5, pady=30)
        self.score0.grid(row=0, column=1, padx=5, pady=10)
        self.score1.grid(row=0, column=2, padx=5, pady=10)
        self.score2.grid(row=0, column=3, padx=5, pady=10)
        self.score3.grid(row=0, column=4, padx=5, pady=10)
   
    
 
#Création de la fenêtre
root = tk.Tk()
root.title("Révisons les langues avec Lucille et Tom !")

#Paramétrage graphique de la fenêtre
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2)-200
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2)-200
root.geometry('500x500+'+str(positionRight)+'+'+str(positionDown))
root.resizable(0, 0)

#exécution de l'application
app = MainApp(root)

root.mainloop()




