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
from tkinter import Tk, Label, Button, Canvas, PhotoImage , ALL ,Menu , Toplevel 

from time import sleep

###################################################################################################################################################
#                                                          Classes
###################################################################################################################################################

class CInterface:
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
        self.FichierPng_Vaisseau = "Data/X-wing_2.png"

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

        
    def CreerChamps(self):
        "Creation des champs"
        self.Score = Label(self.Fenetre, text="Score :" + '100', font='Arial 10', fg='black',anchor='w', borderwidth=0)
        self.Score.grid(row=0, column=0, sticky='nw')

        self.Vie = Label(self.Fenetre, text="Vie : :" + '3', font='Arial 10', fg='black',anchor='w', borderwidth=0)
        self.Vie.grid(row=0, column=2, sticky='nw')
    
    def CreerBoutons(self):
        self.Btn_Quitter = Button(self.Fenetre, text ='Quitter', width=15, command= self.Fenetre.destroy)
        self.Btn_Quitter.grid(row=3, column=4, sticky='e', padx=15)

        self.Btn_Recommencer = Button(self.Fenetre, text ='Nouvelle partie', width=15,command= lambda : nouvelle_partie(self.Toile))
        self.Btn_Recommencer.grid(row=2, column=4, sticky='e', padx=15)

       

    def createMenuBar(self):
        menuBar = Menu(self.Fenetre )
        
        menuFile = Menu(menuBar, tearoff=0 , bg = '#2A2C2B' , fg = 'white' , activebackground='#004c99', activeborderwidth = 0.3)
        menuFile.add_command(label="Nouvelle partie", command= lambda : nouvelle_partie(self.Toile))
        menuFile.add_command(label="Aide" , command = genererFenetreAide)
        menuFile.add_command(label="Difficulté")

        menuFile.add_separator()

        menuFile.add_command(label="Quitter", command= self.Fenetre.destroy)
        menuBar.add_cascade( label="Menu", menu=menuFile)

        self.Fenetre.config(menu = menuBar) 


    def Mainloop(self):
        self.Fenetre.mainloop()


def genererFenetreAide():
    fenetreAide = Toplevel()
    fenetreAide.title("aide")

    label1 = Label(fenetreAide , text ="Les touches :")
    toucheX = Label(fenetreAide , text ="La touche x permet de démarrer une nouvelle partie")
    toucheESP = Label(fenetreAide , text ="La touche espace permet de tirer")
    toucheFleche = Label(fenetreAide , text ="Les touches flèches permettent de se déplacer")
    label2 = Label(fenetreAide , text ="Le but :")
    leBut = Label(fenetreAide , text ="Le but du jeu est de tuer tous les vaisseau ennemie sans perdre toutes ses vie")
    bonJeu = Label(fenetreAide , text ="Amusez-vous bien")
    boutonQuitter = Button(fenetreAide , text = "quitter", command = fenetreAide.destroy)
    
    label1.grid(row = 1 , column = 2 ,  sticky='nesw' )
    toucheX.grid(row = 2 , column = 1 , columnspan = 3,  sticky='w' )
    toucheESP.grid(row = 3 , column = 1 , columnspan = 3, sticky='w')
    toucheFleche.grid(row = 4 , column = 1 , columnspan = 3 , sticky='w')
    label2.grid(row = 5 , column = 2 ,  sticky='nesw' )
    leBut.grid(row = 6, column = 1 , columnspan = 3)
    bonJeu.grid(row = 7 , column = 2 ,  sticky='nesw' )

    boutonQuitter.grid(row=8, column=2, sticky='e', padx=15 , columnspan = 2)
    

class Ennemie:
    def __init__(self, canvas, ennemie,i):
        self.Pcanvas=canvas
        self.Pfilename = PhotoImage(file="Data/X-wing_2.png")
        self.X = 150
        self.Y = 50
        self.Pimage = self.Pcanvas.create_image(self.X + i*100,self.Y, image=self.Pfilename)
        self.direction = 0
        self.limite = 0
        self.YMAX = 0

    def Mouvement(self):
        #Fonction permmettant le déplacement du vaisseau ennemie
        #Méthode : Si le vaisseau se trouve dans la fenêtre, il se déplace soit à gauche soit à droite suivant la valeur de direction
        #Ensuite si le vaiseau s'apprête à sortir de l'écran on initialise une valeur limite à 1 pour qu'il ne rentre plus dans le premier if
        #puis on initalise une autre valeur qui servira de limite quant au déplacement du vaisseau vers le bas; cette dernière valeur récupère la coordonnée
        #en Y du vaisseau puis lui rajoute une certaine valeur, par la suit cette valeur sera comparée avec la prochaine coordonnée du vaisseau.
        #Si la différence est égale à 0, on repasse la valeur limite à 0 puis on recommence le déplacement avec la direction changée
        if self.Getcoord()[1] < 850 :
            if self.Getcoord()[0] > 5 and self.Getcoord()[0] < 1345 and self.limite == 0 : #légerement inférieur a la taille du canavs
                self.Direction(self.direction)
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
                print(abs(self.Getcoord()[1] - self.YMAX))
                self.Pcanvas.move(self.Pimage, 0, 20)
            elif abs(self.Getcoord()[1] - self.YMAX) <= 0 and self.limite == 1:
                self.limite = 0
                self.Direction(self.direction)
        else :
            self.Pimage.destroy             
        fenetre.Fenetre.after(10,self.Mouvement)

    def Getcoord(self):
        # fonction pour récuperer les coordonnées du Vaisseau
        return self.Pcanvas.coords(self.Pimage)

    def Direction(self, sens):
        if self.direction == 0:
            self.Pcanvas.move(self.Pimage, 10, 0)
        elif self.direction == 1:
            self.Pcanvas.move(self.Pimage, -10, 0)


class Camis:
    def __init__(self , canvas ):
        self.Pcanvas=canvas
        #self.ImageFond = "Data/X-wing_2.png"
        self.vaisseau = Canvas(self.Pcanvas, width = 20 , height = 20 , background = 'white') 
        #self.Fond = self.vaisseau.create_image(0, 0, image=self.ImageFond, anchor='nw')
        self.vaisseau.place(x = 1350 / 2 , y = 850 - 100)  
         
    def mouvementG(self , event ):
        print('gauche')
        self.Pcanvas.move(self.vaisseau, -10, 0)

    def mouvementD (self , event):
        print('droite')
        self.Pcanvas.move(self.vaisseau, 10, 0)
       

#def mouvementAllié(event):
    #print('coucou')
    #touche=event.keysym
    #if touche =='Left':
       # vaisseau.mouvementG
        
    #elif touche =='Right':
        #vaisseau.mouvementD
    

  



def nouvelle_partie (Toile):
    amis = Camis(Toile)
    creation_ennemie(Toile)
    return(amis)
  
def creation_ennemie(Toile):
    global listeEN
    listeEN = []
    for  i in range(10):
        listeEN.append(Ennemie(Toile,1,i)) 
    fenetre.Fenetre.after(10,a) 
    return listeEN 

def Debut_Partie(event):
    print(len(listeEN))
    for i in range(len(listeEN)):
        listeEN[i].Mouvement()

###################################################################################################################################################
#                                                            Main
###################################################################################################################################################

fenetre = CInterface()
fenetre.Fenetre.bind('x',Debut_Partie)
#fenetre.Fenetre.bind("<Left>", mouvementAllié)
#fenetre.Fenetre.bind("<Right>", mouvementAllié)
fenetre.Mainloop()
