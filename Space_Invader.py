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
        self.Fenetre.attributes('-fullscreen' , True)

        self.fullScreenState = False
        self.Fenetre.bind("<F11>", self.toggleFullScreen)
        self.Fenetre.bind("<Escape>", self.quitFullScreen)
        
      
        self.FichierGif_Fond = "Data/StarWars.png"  # Le fichier .gif de l'image de fond est dans le répertoire "Gif_Autres", au même niveau que ce programme
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

