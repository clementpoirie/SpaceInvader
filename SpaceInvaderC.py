###################################################################################################################################################
#                                                          Header
###################################################################################################################################################

"""
Ce programme permet via tkinter de jouer à une version du jeu Space Invader
Auteur : Adrien Lapalus , Poirié clément
Il a été réalisé le 18/12/2020
A faire : 
- fenetre informative sur le x disparaisse dès qu'on appuye sur x
- Créer des zones de protection


Lien du git : https://github.com/clementpoirie/SpaceInvader.git
"""

###################################################################################################################################################
#                                                      Modules importés
###################################################################################################################################################
from random import uniform
from tkinter import Tk, Label, Button, Canvas
from tkinter import  PhotoImage , ALL ,Menu , Toplevel , DISABLED 
from time import sleep

###################################################################################################################################################
#                                                          Classes
###################################################################################################################################################
#class interface graphique gérant toute la fenêtre principale
class CInterface :
    def __init__ (self,vie,score,image):
        self.vie = str(vie)
        self.score = str(score)
        self.FichierGif_Fond = image
        self.CreerFenetre()
        self.CreerToile(self.FichierGif_Fond)
        self.CreerChamps(self.vie,self.score)
        self.CreerBoutons()
        self.CreerMenu()

    #création de la fenêtre
    def CreerFenetre(self):
        "Creation de la fenetre"
        self.Fenetre = Tk()
        self.Fenetre.title("space invader")
        self.Fenetre.attributes('-fullscreen', True)

        self.etatFenetre = False
        self.Fenetre.bind("<F11>", self.Remise_PleineEcran) #event permettant la remise en pleine écran
        self.Fenetre.bind("<Escape>", self.Arreter_PleinEcran) #event permettant l'arrêt du pleine écran

        # Le fichier .gif de l'image de fond est dans le répertoire "Gif_Autres", au même niveau que ce programme

       
    #permet la remise en pleine écran
    def Remise_PleineEcran(self, event):
        self.etatFenetre = not self.etatFenetre
        self.Fenetre.attributes("-fullscreen", self.etatFenetre)

    #event permettant l'arrêt du pleine écran
    def Arreter_PleinEcran(self, event):
        self.etatFenetre = False
        self.Fenetre.attributes("-fullscreen", self.etatFenetre)

    #création du canvas de jeu
    def CreerToile(self,FichierGif_Fond):
        self.ImageFond = PhotoImage(file=FichierGif_Fond)

        self.LargeurFenetre = self.ImageFond.width()
        self.HauteurFenetre = self.ImageFond.height()
        "Creation de la Toile (Canevas)"
        self.Toile = Canvas(self.Fenetre, width= 1350, height= 850, background='white')
        self.Toile.grid(row=1, column=0 , columnspan = 3 , rowspan = 4 )
        
        self.Fond = self.Toile.create_image(0, 0, image=self.ImageFond, anchor='nw')
        self.Toile.update()

    #création des Label 
    def CreerChamps(self,vie,score):
        "Creation des champs"
        self.Score = Label(self.Fenetre, text="Score :" + score, font='Arial 10', fg='black',anchor='w', borderwidth=0 , padx = 20)
        self.Score.grid(row=0, column=0, sticky='nw')

        self.Vie = Label(self.Fenetre, text="Vie : " + vie, font='Arial 10', fg='black',anchor='w', borderwidth=0)
        self.Vie.grid(row=0, column=2, sticky='nw')

    # change l'image du background du canvas 
    def ChangerImage(self,FichierGif_Fond):   
        self.ImageFond = PhotoImage(file=FichierGif_Fond)
        self.Toile.itemconfigure(self.Fond, image = self.ImageFond ) 
    
    # création des boutons
    def CreerBoutons(self):
        self.Btn_Quitter = Button(self.Fenetre, text ='Quitter', width=15, command= self.Fenetre.destroy)#self.Fenetre.destroy)
        self.Btn_Quitter.grid(row=3, column=4, sticky='e', padx=15)

        self.Btn_Recommencer = Button(self.Fenetre, text ='Nouvelle partie', width=15,command= lambda : [genererFenetreX() , creationEnnemie(self.Toile, 1)])
        self.Btn_Recommencer.grid(row=2, column=4, sticky='e', padx=15)

    # création du menu
    def CreerMenu(self):
        menuBar = Menu(self.Fenetre )
        
        menuFile = Menu(menuBar, tearoff=0 , bg = '#2A2C2B' , fg = 'white' , activebackground='#004c99', activeborderwidth = 0.3)
        menuFile.add_command(label="Nouvelle partie", command= lambda : creationEnnemie(self.Toile , self.Btn_Recommencer ))
        menuFile.add_command(label="Aide" , command = genererFenetreAide)
        menuFile.add_command(label="Difficulté" , command = genererFenetreDifficulte)
        menuFile.add_command(label="à propos" , command = genererFenetrePropos)

        menuFile.add_separator() #créé une séparation visuelle

        menuFile.add_command(label="Quitter", command= self.Fenetre.destroy)
        menuBar.add_cascade( label="Menu", menu=menuFile)

        self.Fenetre.config(menu = menuBar) 

    # permet de fermer la fenetre principale permet d'être appelé hors de la classe et fermer l'objet "fenetre principale"
    def fermerFenetre(self):
        self.Fenetre.destroy()

    #permet d'appeler mainloop hors de la class 
    def Mainloop(self):
        self.Fenetre.mainloop()

class Ennemie:
    def __init__(self, canvas, ennemie,X,Y):
        self.Pcanvas=canvas
        self.Pfilename = PhotoImage(file="Data/Chasseur_Tie.png")
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
                self.YMAX = self.Getcoord()[1]+40
            elif self.Getcoord()[0] <= 5 and self.limite == 0:
                self.direction = 0
                self.limite = 1
                self.X = 1
                self.YMAX = self.Getcoord()[1]+40   
            elif abs(self.Getcoord()[1] - self.YMAX) > 0 and self.limite == 1:
                self.Pcanvas.move(self.Pimage, 0, 40)
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
    def actu(self):
        self.Pcanvas.update()

class Camis:
    def __init__(self , canvas ):
        self.Pcanvas=canvas
        self.Pfilename = PhotoImage(file="Data/X-wing_2.png")
        self.Pimage = self.Pcanvas.create_image(675,750, image=self.Pfilename)
        #self.vaisseau = Canvas(self.Pcanvas, width = 20 , height = 20 , background = 'white') 
        #self.Fond = self.vaisseau.create_image(0, 0, image=self.ImageFond, anchor='nw')
        #self.vaisseau.place(x = 1350 / 2 , y = 850 - 100)
    def mouvementG(self,event):
        coord = self.Getcoord()
        Xj = coord[0]
        if Xj >= 5:
            self.Pcanvas.move(self.Pimage, -10, 0)
        else :
            self.Pcanvas.move(self.Pimage, 2, 0)  

    def mouvementD (self,event):
        coord = self.Getcoord()
        Xj = coord[0]
        if Xj <= 1325:
            self.Pcanvas.move(self.Pimage, 10, 0) 
        else :
            self.Pcanvas.move(self.Pimage, -2, 0)   

    def Getcoord(self):
        # fonction pour récuperer les coordonnées du joueur
        return self.Pcanvas.coords(self.Pimage)    
    def TirJoueur(self,event):
        coord = self.Getcoord()
        Xj = coord[0]
        Yj = coord[1]
        listeTir.append(Tir(fenetre.Toile,"Data/Tir_Vert.png",0,Xj,Yj))
    def actu(self):
        self.Pcanvas.update()

###################################################################################################################################################
#                                                          FONCTIONS
###################################################################################################################################################

def creationEnnemie(Toile,niveau):
    global Amis
    Amis = Camis(Toile)
    global listeEN
    listeEN = []
    global listeTir
    listeTir = []
    global ChanceTir
    NbrEnnemies,ChanceTir = Niveau(niveau)
   
    Toile.update()
    X = 25
    Y = 25
    for  i in range(NbrEnnemies):
        if X < 1300 :
            listeEN.append(Ennemie(Toile,1,X,Y))
            X=X + 100
        else:
            Y = Y + 100
            X = 25
            listeEN.append(Ennemie(Toile,1,X,Y)) 


def Niveau(niveau):
    if niveau == 1 :
        fenetre.ChangerImage("Data/StarWars.png")
        return 15,0.05
    if niveau == 2 :
        fenetre.ChangerImage("Data/StarWars2.png")
        return 20,0.1
    if niveau == 3 :
        fenetre.ChangerImage("Data/StarWars3.png")
        return 25,0.5
    if niveau == 4 :
        fenetre.ChangerImage("Data/StarWars4.png")
        return 30,1
    if niveau == 5 :
        fenetre.ChangerImage("Data/StarWars5.png")
        return 35,1.5

#créé la fenetre recommencer
def genererFenetreRecommencer(defaite):
    fenetreRecommencer = Toplevel()
    fenetreRecommencer.overrideredirect(1)
    fenetreRecommencer.title("Recommencer")
    fenetreRecommencer.geometry("500x500+500+200")

    #condition d'affichage suivant le dénoument de la partie  
    if defaite == True :
        etatFinJeu = Label(fenetreRecommencer , text = 'DEFAITE' , font=("Courier", 40)  )   
    else:
        etatFinJeu = Label(fenetreRecommencer , text = 'VICTOIRE' , font=("Courier", 40)  )

    boutonQuitter = Button(fenetreRecommencer , text = "Quitter le jeu", command = fenetre.fermerFenetre)
    boutonRejouer = Button(fenetreRecommencer , text = "Recommencer", command = lambda : [creationEnnemie(fenetre.Toile,1), fenetreRecommencer.destroy()])
    boutonNiveau = Button(fenetreRecommencer , text = "Choix du niveau", command = lambda : [fenetreRecommencer.destroy(), genererFenetreDifficulte()])
    #placement des widgets
    etatFinJeu.place(x = 115 , y = 110 )
    boutonRejouer.place(x = 50 , y = 350)
    boutonNiveau.place (x = 200 , y = 350)
    boutonQuitter.place(x = 350 , y = 350 , width = 100 )

#créé la fenetre d'aide
def genererFenetreAide():
    fenetreAide = Toplevel()
    fenetreAide.overrideredirect(1)
    fenetreAide.title("aide")
    fenetreAide.geometry('500x500+500+200')

    label1 = Label(fenetreAide , text ="Les touches :" , font=("Courier", 15))
    toucheX = Label(fenetreAide , text ="La touche x permet de démarrer la partie")
    toucheESP = Label(fenetreAide , text ="La touche w permet de tirer")
    toucheFleche = Label(fenetreAide , text ="Les touches flèches permettent de se déplacer")
    label2 = Label(fenetreAide , text ="Le but :" , font=("Courier", 15))
    leBut = Label(fenetreAide , text ="Le but du jeu est de tuer tous les vaisseaux ennemies sans perdre toutes ses vies")
    bonJeu = Label(fenetreAide , text ="Amusez-vous bien" , font=("Courier", 15))
    boutonQuitter = Button(fenetreAide , text = "quitter", command = fenetreAide.destroy)
    #placement des widgets
    label1.place(x = 25 , y = 50)
    toucheX.place(x = 25 , y = 75 )
    toucheESP.place(x = 25 , y = 100)
    toucheFleche.place(x = 25 , y = 125)
    label2.place(x = 25 , y = 200 )
    leBut.place(x = 25 , y = 225)
    bonJeu.place(x = 150 , y = 285)

    boutonQuitter.place(x = 25 , y = 350 , width = 450)

#créé la fenetre à propos
def genererFenetrePropos():
    fenetrePropos = Toplevel()
    fenetrePropos.overrideredirect(1)
    fenetrePropos.title("à propos")
    fenetrePropos.geometry('500x270+500+200')

    label1 = Label(fenetrePropos , text ="Qui sommes nous ? " , font=("Courier", 15))
    paragraphe1 = Label(fenetrePropos , text ="Nous sommes deux étudiants de CPE Lyon nous avons réalisé ce jeu pour que les fans ")
    paragraphe2 = Label(fenetrePropos , text ="de star wars puissent enfin jouer au space invader")
    
    label2 = Label(fenetrePropos , text ="Le meilleur score réalisé est : " + lectureBestscore() , font=("Courier", 15))
    boutonQuitter = Button(fenetrePropos , text = "quitter", command = fenetrePropos.destroy)
    #placement des widgets
    label1.place(x = 25 , y = 50)
    paragraphe1.place(x = 25 , y = 85 )
    paragraphe2.place(x = 25 , y = 100)
    label2.place(x = 25 , y = 150 )
    boutonQuitter.place(x = 25 , y = 230 , width = 450)


#création la fenetre d'information du début
def genererFenetreX():
    fenetreAide = Toplevel()
    fenetreAide.overrideredirect(1)
    fenetreAide.title("à propos")
    fenetreAide.geometry('500x100+500+200')

    label1 = Label(fenetreAide , text ="appuyez sur x quand vous êtes prêt" , font=("Courier", 15))
    boutonQuitter = Button(fenetreAide , text = "quitter", command = fenetreAide.destroy)
    label1.place(x = 25 , y = 25)
    boutonQuitter.place(x=25 , y = 60 , width = 450)


#création la fenetre d'information de difficulté
def genererFenetreDifficulte():
    fenetreDifficulte = Toplevel()
    fenetreDifficulte.overrideredirect(1)
    fenetreDifficulte.title("Difficulté")
    fenetreDifficulte.geometry('500x500+500+200')
    
    labelTitre = Label(fenetreDifficulte , text = "choisissez le niveau de difficulté :" , font=("Courier", 13) ,  padx = 30 , pady = 15)
    
    boutonNiv1 = Button(fenetreDifficulte , text = "Facile", bg = 'blue', fg = 'white', command = lambda : creationEnnemie(fenetre.Toile,1))
    boutonNiv2 = Button(fenetreDifficulte , text = "moyen", bg = 'green' ,fg = 'white', command = lambda : creationEnnemie(fenetre.Toile,2))
    boutonNiv3 = Button(fenetreDifficulte , text = "difficile", bg = 'red' ,fg = 'white', command = lambda : creationEnnemie(fenetre.Toile,3))
    boutonNiv4 = Button(fenetreDifficulte , text = "mortel", bg = 'purple' ,fg = 'white',command = lambda : creationEnnemie(fenetre.Toile,4))
    boutonNiv5 = Button(fenetreDifficulte , text = "hardcore",bg = 'black' ,fg = 'white', command = lambda : creationEnnemie(fenetre.Toile,5))
    boutonQuitter = Button(fenetreDifficulte , text = "Jouer", command = fenetreDifficulte.destroy)
    
    labelTitre.place(x = 25 , y = 150)
    boutonNiv1.place(x = 50 , y = 250)
    boutonNiv2.place(x = 125 , y = 250)
    boutonNiv3.place(x = 200 , y = 250)
    boutonNiv4.place(x = 275 , y = 250)
    boutonNiv5.place(x = 350 , y = 250)
    boutonQuitter.place(x = 25 , y = 350 , width = 450)

    
def VictoireDefaite(vie , condition):
    vc = []
    perdu = 0
    if condition ==0:
        for i in range(len(listeEN)):
            coord = listeEN[i].Getcoord() 
            Ye = coord[1]
            if Ye > 850 :
                perdu = 1
        if vie == 0 or perdu == 1 :
            Reinitialisation()
            condition = 1
            vc.append(0)
            vc.append(condition)
            genererFenetreRecommencer(True)
        elif listeEN == [] : 
            condition = 1
            Reinitialisation()
            vc.append(0)
            vc.append(condition)
            genererFenetreRecommencer(False)
        else:
            vc.append(1)
            vc.append(condition)

    return vc

def Collision(listeTir,vie,score,bestscore):
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
                if abs(Xe - Xt) <= 25 and abs(Ye - Yt) <= 25 :
                    score += 10
                    modifBestscore(bestscore , score)
                    indiceEnnemie.append(listeEN[t])
                    indiceTir.append(listeTir[i])
        elif listeTir[i].direction == 1 : #Si le tir provient d'un ennemie 
            if  abs(Xj - Xt) <= 25 and abs(Yj - Yt) <= 25:
                vie -=1
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
    fenetre.CreerChamps(str(vie),str(score))            
    return vie,score



def Partie(vie,score,condition):
    var = VictoireDefaite(vie , condition)
    victoiredefaite = 1
    victoiredefaite = var[0]
    condition = var[1]
    meilleurScore = lectureBestscore()
    meilleurScore_int = float(meilleurScore)
    if victoiredefaite == 1:

        fenetre.Fenetre.bind('<Left>',Amis.mouvementG)
        fenetre.Fenetre.bind('<Right>',Amis.mouvementD)
        fenetre.Fenetre.bind('w',Amis.TirJoueur)



        for i in range(len(listeEN)):
            listeEN[i].actu()
            R = uniform(0,100)
            if R <= ChanceTir :
                coord = listeEN[i].Getcoord()
                Xe = coord[0]
                Ye = coord[1]
                listeTir.append(Tir(fenetre.Toile,"Data/Tir_Rouge.png",1,Xe,Ye))
        if listeTir != []:
            vie,score = Collision(listeTir,vie,score,meilleurScore_int)
            for i in range(len(listeTir)):
                listeTir[i].Direction()
    fenetre.Fenetre.after(10,lambda : Partie(vie,score,condition)) 
    VictoireDefaite(vie ,condition)       


def Debut_Partie(event):
   
    fenetre.Btn_Recommencer.config(state = DISABLED) #désactive le bouton nouvelle partie
    vie = 3
    condition = 0
    victoiredefaite = 1
    for i in range(len(listeEN)):
        listeEN[i].Mouvement()      
   
    fenetre.Fenetre.after(10,lambda : Partie(vie,score,condition)) 

#permet de lire le fichier texte score.txt et de retourner ce qu'il y a dedans
def lectureBestscore():
    fichier = open("score.txt",'r') #'r' = read 
    meilleurScore = fichier.read()
    fichier.close
    return meilleurScore 


#permet de modifier le fichier texte score.txt
def modifBestscore(ancien , nouveau):
    if nouveau > ancien:
        meilleurScore = str(nouveau) 
        fichierScore = open("score.txt" , "w") #'w' = write 
        fichierScore.writelines(meilleurScore)
        fichierScore.close


def Reinitialisation():
    for i in range(len(listeTir)):
        listeTir[i].Pcanvas.delete(listeTir[i].Pimage)
    Amis.Pcanvas.delete(Amis.Pimage)       


###################################################################################################################################################
#                                                            Main
###################################################################################################################################################
#variable globale
vie = 3 
score = 0

#instance de l'objet fenetre principale
fenetre = CInterface(vie,score,'data/StarWars.png')
# lance la partie lorsqu'on appuye sur x
fenetre.Fenetre.bind('x',Debut_Partie)

fenetre.Mainloop()