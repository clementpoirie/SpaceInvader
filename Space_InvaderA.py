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
from tkinter import Tk, Label, Button, Canvas, PhotoImage

###################################################################################################################################################
#                                                          Classes
###################################################################################################################################################


class CInterface:
    def CreerFenetre(self):
        "Creation de la fenetre"
        self.Fenetre = Tk()
        self.Fenetre.title("space invader")
        self.Fenetre.attributes('-fullscreen', True)

        self.fullScreenState = False
        self.Fenetre.bind("<F11>", self.toggleFullScreen)
        self.Fenetre.bind("<Escape>", self.quitFullScreen)

        # Le fichier .gif de l'image de fond est dans le répertoire "Gif_Autres", au même niveau que ce programme
        self.FichierGif_Fond = "Data/StarWars.png"
        self.ImageFond = PhotoImage(file=self.FichierGif_Fond)
        self.LargeurFenetre = self.ImageFond.width()
        self.HauteurFenetre = self.ImageFond.height()

    def toggleFullScreen(self, event):
        self.fullScreenState = not self.fullScreenState
        self.Fenetre.attributes("-fullscreen", self.fullScreenState)

    def quitFullScreen(self, event):
        self.fullScreenState = False
        self.Fenetre.attributes("-fullscreen", self.fullScreenState)

    def CreerToile(self):
        "Creation de la Toile (Canevas)"
        self.Toile = Canvas(self.Fenetre, width=self.LargeurFenetre,
                            height=self.HauteurFenetre, background='white')
        self.Toile.grid(row=0, column=0)
        self.Toile.delete(ALL)
        self.Fond = self.Toile.create_image(
            0, 0, image=self.ImageFond, anchor='nw')

    def Mainloop(self):
        self.Fenetre.mainloop()


class Ennemie:
    def __init__(self, canvas, ennemie):
        self.Pcanvas = canvas
        self.Pfilename = PhotoImage(file=ennemie)
        self.Pimage = self.Pcanvas.create_image(
            -100, 255, anchor='NW', image=self.Pfilename)
        self.direction = 0
        self.limite = 0

    def Mouvement(self):
        #Fonction permmettant le déplacement du vaisseau ennemie
        #Méthode : Si le vaisseau se trouve dans la fenêtre, il se déplace soit à gauche soit à droite suivant la valeur de direction
        #Ensuite si le vaiseau s'apprête à sortir de l'écran on initialise une valeur limite à 1 pour qu'il ne rentre plus dans le premier if
        #puis on initalise une autre valeur qui servira de limite quant au déplacement du vaisseau vers le bas; cette dernière valeur récupère la coordonnée
        #en Y du vaisseau puis lui rajoute une certaine valeur, par la suit cette valeur sera comparée avec la prochaine coordonnée du vaisseau.
        #Si la différence est égale à 0, on repasse la valeur limite à 0 puis on recommence le déplacement avec la direction changée
        if self.Pcanvas.Getcoord()[0] > 0 and self.Pcanvas.Getcoord()[0] < 100 and self.limite == 0 : #légerement inférieur a la taille du canavs
            self.Direction(self.direction)
        if self.Pcanvas.Getcoord()[0] >= 100 and self.limite == 0:
            self.direction = 1
            self.limite = 1
            YMAX = self.Pcanvas.Getcoord()[1]+20
        if self.Pcanvas.Getcoord()[0] <= 0 and self.limite == 0:
            self.direction = 0
            self.limite = 1
            YMAX = self.Pcanvas.Getcoord()[1]+20
        if abs(self.Pcanvas.Getcoord()[1] - YMAX) > 0 and self.limite == 1:
            self.Pcanvas.move(self.Pimage, 0, 2)
        if abs(self.Pcanvas.Getcoord()[1] - YMAX) <= 0 and self.limite == 1:
            self.limite = 0

    def Getcoord(self):
        # fonction pour récuperer les coordonnées du Vaisseau
        return self.Pcanvas.coords(self.Pimage)

    def Direction(self, sens):
        if self.direction == 0:
            self.Pcanvas.move(self.Pimage, 2, 0)
        elif self.direction == 1:
            self.Pcanvas.move(self.Pimage, -2, 0)
###################################################################################################################################################
#                                                            Main
###################################################################################################################################################


fenetre = CInterface()
fenetre.Mainloop()