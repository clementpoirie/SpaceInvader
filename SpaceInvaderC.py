###################################################################################################################################################
#                                                          Header
###################################################################################################################################################

"""
Ce programme permet via tkinter de jouer à une version du jeu Space Invader
Auteur : Adrien Lapalus , Poirié clément
Il a été réalisé le 18/12/2020
A faire : 

Lien du git : https://github.com/clementpoirie/SpaceInvader.git
"""

###################################################################################################################################################
#                                                      Modules importés
###################################################################################################################################################
from random import uniform
from tkinter import Tk, Label, Button, Canvas
from tkinter import  PhotoImage , ALL ,Menu , Toplevel , DISABLED


###################################################################################################################################################
#                                                          Classes
###################################################################################################################################################

class CInterface :
    def __init__ (self):
        self.CreerFenetre()
        self.CreerToile()
        self.CreerChamps()
        self.CreerBoutons()
        self.createMenuBar()

    def CreerFenetre(self):
        "Creation de la fenetre"
        self.Fenetre = Tk()
        self.Fenetre.title("space invader")
        self.Fenetre.attributes('-fullscreen', True)

        self.etatFenetre = False
        self.Fenetre.bind("<F11>", self.Remise_PleineEcran)
        self.Fenetre.bind("<Escape>", self.Arreter_PleinEcran)

        # Le fichier .gif de l'image de fond est dans le répertoire "Gif_Autres", au même niveau que ce programme
        self.FichierGif_Fond = "Data/StarWars.png"
        self.FichierPng_Vaisseau = "Data/Chasseur_Tie.png"

        self.ImageFond = PhotoImage(file=self.FichierGif_Fond)
        self.ImageVaisseau = PhotoImage(file=self.FichierPng_Vaisseau)

        self.LargeurFenetre = self.ImageFond.width()
        self.HauteurFenetre = self.ImageFond.height()

    def Remise_PleineEcran(self, event):
        self.etatFenetre = not self.etatFenetre
        self.Fenetre.attributes("-fullscreen", self.etatFenetre)

    def Arreter_PleinEcran(self, event):
        self.etatFenetre = False
        self.Fenetre.attributes("-fullscreen", self.etatFenetre)

    def CreerToile(self):
        "Creation de la Toile (Canevas)"
        self.Toile = Canvas(self.Fenetre, width= 1350, height= 850, background='white')
        self.Toile.grid(row=1, column=0 , columnspan = 3 , rowspan = 4 )
        self.Toile.delete(ALL)
        self.Fond = self.Toile.create_image(0, 0, image=self.ImageFond, anchor='nw')


    def CreerChamps(self ,):
        "Creation des champs"
        self.Score = Label(self.Fenetre, text="Score :" + '100', font='Arial 10', fg='black',anchor='w', borderwidth=0 , padx = 20)
        self.Score.grid(row=0, column=0, sticky='nw')

        self.Vie = Label(self.Fenetre, text="Vie : " + str(Vie), font='Arial 10', fg='black',anchor='w', borderwidth=0)
        self.Vie.grid(row=0, column=2, sticky='nw')

    def actuChamps(self):
        self.Vie.update()
        self.Score.update()
        
    
    def CreerBoutons(self):
        self.Btn_Quitter = Button(self.Fenetre, text ='Quitter', width=15, command= genererFenetreRecommencer)#self.Fenetre.destroy)
        self.Btn_Quitter.grid(row=3, column=4, sticky='e', padx=15)

        self.Btn_Recommencer = Button(self.Fenetre, text ='Nouvelle partie', width=15,command= lambda : creationEnnemie(self.Toile, self.Btn_Recommencer))
        self.Btn_Recommencer.grid(row=2, column=4, sticky='e', padx=15)

    def createMenuBar(self):
        menuBar = Menu(self.Fenetre )
        
        menuFile = Menu(menuBar, tearoff=0 , bg = '#2A2C2B' , fg = 'white' , activebackground='#004c99', activeborderwidth = 0.3)
        menuFile.add_command(label="Nouvelle partie", command= lambda : creationEnnemie(self.Toile , self.Btn_Recommencer ))
        menuFile.add_command(label="Aide" , command = genererFenetreAide)
        menuFile.add_command(label="Difficulté" , command = genererFenetreDifficulte)

        menuFile.add_separator()

        menuFile.add_command(label="Quitter", command= self.Fenetre.destroy)
        menuBar.add_cascade( label="Menu", menu=menuFile)

        self.Fenetre.config(menu = menuBar) 

    def Mainloop(self):
        self.Fenetre.mainloop()

class Ennemie:
    def __init__(self, canvas, ennemie,X,Y):
        self.Pcanvas=canvas
        self.Pfilename = PhotoImage(file="Data/X-wing_2.png")
        self.X = X
        self.Y = Y
        self.Pimage = self.Pcanvas.create_image(self.X,self.Y, image=self.Pfilename)
        self.direction = 0
        self.limite = 0
        self.YMAX = 0
        self.ennemie = ennemie
    def Mouvement(self):
        #Fonction permmettant le déplacement du vaisseau ennemie
        #Méthode : Si le vaisseau se trouve dans la fenêtre, il se déplace soit à gauche soit à droite suivant la valeur de direction
        #Ensuite si le vaiseau s'apprête à sortir de l'écran on initialise une valeur limite à 1 pour qu'il ne rentre plus dans le premier if
        #puis on initalise une autre valeur qui servira de limite quant au déplacement du vaisseau vers le bas; cette dernière valeur récupère la coordonnée
        #en Y du vaisseau puis lui rajoute une certaine valeur, par la suit cette valeur sera comparée avec la prochaine coordonnée du vaisseau.
        #Si la différence est égale à 0, on repasse la valeur limite à 0 puis on recommence le déplacement avec la direction changée
        if self.Getcoord()[1] < 850 :
            if self.Getcoord()[0] > 5 and self.Getcoord()[0] < 1345 and self.limite == 0 : #légerement inférieur a la taille du canavs
                self.Direction()
            elif self.Getcoord()[0] >= 1345 and self.limite == 0:
                self.direction = 1
                self.limite = 1
                self.X = 99
                self.YMAX = self.Getcoord()[1]+20
            elif self.Getcoord()[0] <= 5 and self.limite == 0:
                self.direction = 0
                self.limite = 1
                self.X = 1
                self.YMAX = self.Getcoord()[1]+20    
            elif abs(self.Getcoord()[1] - self.YMAX) > 0 and self.limite == 1:
                self.Pcanvas.move(self.Pimage, 0, 20)
            elif abs(self.Getcoord()[1] - self.YMAX) <= 0 and self.limite == 1:
                self.limite = 0
                self.Direction()         
    def actu(self):
        self.Pcanvas.update()
        fenetre.Fenetre.after(10,self.Mouvement)
    def Getcoord(self):
        # fonction pour récuperer les coordonnées du Vaisseau
        return self.Pcanvas.coords(self.Pimage)

    def Direction(self):
        if self.direction == 0:
            self.Pcanvas.move(self.Pimage, 10, 0)
        elif self.direction == 1:
            self.Pcanvas.move(self.Pimage, -10, 0)

class Tir():
    def __init__(self,canvas,Tir,direction,X,Y):
        self.Pcanvas = canvas
        self.Pfilename = PhotoImage(file=Tir)
        self.X = X
        self.Y = Y
        self.Pimage = self.Pcanvas.create_image(self.X,self.Y, image=self.Pfilename)
        self.direction = direction
    
    def Direction(self):
        #Fonction permettant de déplacer le tir vers le haut ou vers le bas suivant qui tir
        #vers le haut pour le joueur (direction = 0) et vers le bas pour les ennemies (direction = 1)
        if self.direction == 0 :
             self.Pcanvas.move(self.Pimage, 0, -10)
        elif self.direction == 1:
            self.Pcanvas.move(self.Pimage, 0, 10)
    def Getcoord(self):
        # fonction pour récuperer les coordonnées du Tir
        return self.Pcanvas.coords(self.Pimage)    


class Camis:
    def __init__(self , canvas ):
        self.Pcanvas=canvas
        self.Pfilename = PhotoImage(file="Data/X-wing_2.png")
        self.Pimage = self.Pcanvas.create_image(675,750, image=self.Pfilename)
        #self.vaisseau = Canvas(self.Pcanvas, width = 20 , height = 20 , background = 'white') 
        #self.Fond = self.vaisseau.create_image(0, 0, image=self.ImageFond, anchor='nw')
        #self.vaisseau.place(x = 1350 / 2 , y = 850 - 100)
    def mouvementG(self,event):
        self.Pcanvas.move(self.Pimage, -10, 0)

    def mouvementD (self,event):
        self.Pcanvas.move(self.Pimage, 10, 0)          
    def Getcoord(self):
        # fonction pour récuperer les coordonnées du joueur
        return self.Pcanvas.coords(self.Pimage)    
    def TirJoueur(self,event):
        coord = self.Getcoord()
        Xj = coord[0]
        Yj = coord[1]
        listeTir.append(Tir(fenetre.Toile,"Data/Tir_Rouge.png",0,Xj,Yj))


###################################################################################################################################################
#                                                          FONCTIONS
###################################################################################################################################################

def creationEnnemie(Toile , Bouton ):
    Bouton.config(state = DISABLED)
    global Amis
    Amis = Camis(Toile)
    global listeEN
    listeEN = []
    global listeTir
    listeTir = []
    X = 25
    Y = 25
    for  i in range(25):
        if X < 1300 :
            listeEN.append(Ennemie(Toile,1,X,Y))
            X=X + 100
        else:
            Y = Y + 100
            X = 25
            listeEN.append(Ennemie(Toile,1,X,Y)) 
    return listeEN 




def genererFenetreRecommencer(defaite):
    fenetreRecommencer = Toplevel()
    fenetreRecommencer.overrideredirect(1)
    fenetreRecommencer.title("Recommencer")
    fenetreRecommencer.geometry("500x500+500+200")
       
    if defaite == True :
        etatFinJeu = Label(fenetreRecommencer , text = 'DEFAITE' , font=("Courier", 40)  )   
    else:
        etatFinJeu = Label(fenetreRecommencer , text = 'VICTOIRE' , font=("Courier", 40)  )

    boutonQuitter = Button(fenetreRecommencer , text = "Quitter", command = fenetreRecommencer.destroy)
    boutonRejouer = Button(fenetreRecommencer , text = "Recommencer", command = fenetreRecommencer.destroy)
    boutonNiveau = Button(fenetreRecommencer , text = "Choix du niveau", command = genererFenetreDifficulte)
    etatFinJeu.place(x = 115 , y = 110 )
    boutonRejouer.place(x = 50 , y = 350)
    boutonNiveau.place (x = 200 , y = 350)
    boutonQuitter.place(x = 350 , y = 350 , width = 100 )


def genererFenetreAide():
    fenetreAide = Toplevel()
    fenetreAide.overrideredirect(1)
    fenetreAide.title("aide")
    fenetreAide.geometry('500x500+500+200')

    label1 = Label(fenetreAide , text ="Les touches :" , font=("Courier", 15))
    toucheX = Label(fenetreAide , text ="La touche x permet de démarrer une nouvelle partie")
    toucheESP = Label(fenetreAide , text ="La touche espace permet de tirer")
    toucheFleche = Label(fenetreAide , text ="Les touches flèches permettent de se déplacer")
    label2 = Label(fenetreAide , text ="Le but :" , font=("Courier", 15))
    leBut = Label(fenetreAide , text ="Le but du jeu est de tuer tous les vaisseaux ennemies sans perdre toutes ses vies")
    bonJeu = Label(fenetreAide , text ="Amusez-vous bien" , font=("Courier", 15))
    boutonQuitter = Button(fenetreAide , text = "quitter", command = fenetreAide.destroy)
    
    label1.place(x = 25 , y = 50)
    toucheX.place(x = 25 , y = 75 )
    toucheESP.place(x = 25 , y = 100)
    toucheFleche.place(x = 25 , y = 125)
    label2.place(x = 25 , y = 200 )
    leBut.place(x = 25 , y = 225)
    bonJeu.place(x = 150 , y = 285)

    boutonQuitter.place(x = 25 , y = 350 , width = 450)

def genererFenetreDifficulte():
    fenetreDifficulte = Toplevel()
    fenetreDifficulte.overrideredirect(1)
    fenetreDifficulte.title("Difficulté")
    fenetreDifficulte.geometry('500x500+500+200')
    
    labelTitre = Label(fenetreDifficulte , text = "choisissez le niveau de difficulté :" , font=("Courier", 13) ,  padx = 30 , pady = 15)
    
    boutonNiv1 = Button(fenetreDifficulte , text = "Facile", bg = 'blue', fg = 'white', command = fenetreDifficulte.destroy)
    boutonNiv2 = Button(fenetreDifficulte , text = "moyen", bg = 'green' ,fg = 'white', command = fenetreDifficulte.destroy)
    boutonNiv3 = Button(fenetreDifficulte , text = "difficile", bg = 'red' ,fg = 'white', command = fenetreDifficulte.destroy)
    boutonNiv4 = Button(fenetreDifficulte , text = "mortel", bg = 'purple' ,fg = 'white',command = fenetreDifficulte.destroy)
    boutonNiv5 = Button(fenetreDifficulte , text = "hardcore",bg = 'black' ,fg = 'white', command = fenetreDifficulte.destroy)
    boutonQuitter = Button(fenetreDifficulte , text = "quitter", command = fenetreDifficulte.destroy)
    
    labelTitre.place(x = 25 , y = 150)
    boutonNiv1.place(x = 50 , y = 250)
    boutonNiv2.place(x = 125 , y = 250)
    boutonNiv3.place(x = 200 , y = 250)
    boutonNiv4.place(x = 275 , y = 250)
    boutonNiv5.place(x = 350 , y = 250)
    boutonQuitter.place(x = 25 , y = 350 , width = 450)


def VictoireDefaite(vie , condition):
    vc = []
    if condition ==0:

        if vie == 0 :
            print("Défaite")
            condition = 1
            vc.append(0)
            vc.append(condition)
            return vc
        elif listeEN == [] :
            print("Victoire") 
            condition = 1
            vc.append(0)
            vc.append(condition)
            return vc
        else:
            vc.append(1)
            vc.append(condition)
            return vc

def Collision(listeTir,vie):
    coord = Amis.Getcoord()
    Xj = coord[0]
    Yj = coord[1]
    indiceTir = []
    indiceEnnemie = []
    print(vie)
    for i in range(len(listeTir)):
        coord = listeTir[i].Getcoord()
        Xt = coord[0]
        Yt = coord[1]
        if listeTir[i].direction == 0 : #Si le tir provient du joueur
            for t in range(len(listeEN)):
                coord = listeEN[t].Getcoord()
                Xe = coord[0]
                Ye = coord[1]
                if abs(Xe - Xt) <= 25 and abs(Ye - Yt) <= 25:
                    indiceEnnemie.append(listeEN[t])
                    indiceTir.append(listeTir[i])
        elif listeTir[i].direction == 1 : #Si le tir provient d'un ennemie 
            if  abs(Xj - Xt) <= 25 and abs(Yj - Yt) <= 25:
                vie -=1
                fenetre.Vie.config(text = "Vie : " + str(Vie))
                indiceTir.append(listeTir[i])
        if Yt < 0 or Yt > 1350 :
            indiceTir.append(listeTir[i])
    if indiceTir != []:
        for Tir in indiceTir :
            if Tir in listeTir:          
                listeTir.remove(Tir)  
    if indiceEnnemie != []:
        for Ennemie in indiceEnnemie :      
            if Ennemie in listeEN:
                listeEN.remove(Ennemie) 
    return vie

def Partie(vie , condition):
    var = VictoireDefaite(vie , condition)
    victoiredefaite = 1
    victoiredefaite = var[0]
    condition = var[1]
    if victoiredefaite == 1:

        fenetre.Fenetre.bind('<Left>',Amis.mouvementG)
        fenetre.Fenetre.bind('<Right>',Amis.mouvementD)
        fenetre.Fenetre.bind('w',Amis.TirJoueur)

        
        for i in range(len(listeEN)):
            listeEN[i].actu()  
            R = uniform(0,100)
            if R <= 5 :
                coord = listeEN[i].Getcoord()
                Xe = coord[0]
                Ye = coord[1]
                listeTir.append(Tir(fenetre.Toile,"Data/Tir_Rouge.png",1,Xe,Ye))
        if listeTir != []:
            vie = Collision(listeTir,vie)
            for i in range(len(listeTir)):
                listeTir[i].Direction()
    fenetre.Fenetre.after(10,lambda : Partie(vie , condition)) 
        


def Debut_Partie(event):
    vie = 3
    condition = 0
    for i in range(len(listeEN)):
        listeEN[i].Mouvement()      
   
    fenetre.Fenetre.after(10,lambda : Partie(vie , condition))    
  

                    
###################################################################################################################################################
#                                                            Main
###################################################################################################################################################
global Vie
Vie = 3
fenetre = CInterface()
fenetre.Fenetre.bind('x',Debut_Partie)

fenetre.Mainloop()