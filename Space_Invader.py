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
from tkinter import Tk, Label, Button , PhotoImage , Canvas , ALL

###################################################################################################################################################
#                                                          Classes
###################################################################################################################################################
class Cinterface():
    "La classe Cinterface : permet de gérer l'interface graphique"
    
    def __init__(self):
        self.CreerFenetre()
        self.CreerToile()
        
        
    def CreerFenetre(self):   
        "Creation de la fenetre"
        self.Fenetre = Tk()        
        self.Fenetre.title("space invader")   
        self.LargeurEcran = self.Fenetre.winfo_screenwidth()
        self.HauteurEcran = self.Fenetre.winfo_screenheight()
        self.FlagEcranPetit = False
        self.FichierGif_Fond = "Data/StarWars.png"  # Le fichier .gif de l'image de fond est dans le répertoire "Gif_Autres", au même niveau que ce programme
        self.ImageFond = PhotoImage(file=self.FichierGif_Fond)
        self.LargeurFenetre = self.ImageFond.width()
        self.HauteurFenetre = self.ImageFond.height()
        
        # Si la hauteur de l'image est supérieure à la hauteur de l'écran, réduction de la hauteur de la fenetre à 600 pixels
        if self.HauteurFenetre + 100 > self.HauteurEcran :
            self.EcranPetit=True
            self.HauteurFenetre = 600
            self.DecalagePixel_y = 25
        else:
            self.EcranPetit=False
            self.HauteurFenetre = self.ImageFond.height()
            self.DecalagePixel_y = 0

    def CreerToile(self):
        "Creation de la Toile (Canevas)"
        self.Toile = Canvas(self.Fenetre, width=self.LargeurFenetre, height=self.HauteurFenetre, background = 'white')
        self.Toile.grid(row=0, column=0)    
        self.Toile.delete(ALL)
        self.Fond = self.Toile.create_image(0,0,image = self.ImageFond,anchor='nw')
    
    def Mainloop(self):
        self.Fenetre.mainloop()
        

#class Ennemie :
   # def __init__(self):
    
   # def Tirer(self):




###################################################################################################################################################
#                                                            Main
###################################################################################################################################################

Interface = Cinterface()
Interface.Mainloop()

