from tkinter import * 
from bs4 import BeautifulSoup
from urllib.parse import unquote, quote
import urllib.request
import sys
import os 
import pickle
import unicodedata
from random import randint

# Gère le clic de l'utilisateur sur un mot
def clic(evt):
    j=liste.curselection()
    nouvMot = str(liste.get(j))

    labelo['text'] = "Vous êtes actuellement sur la page de : {}".format(nouvMot) 
    print("")
    print("---Mot actuel---")
    print(nouvMot)
    print('---Liste des mots parcourus---')
    for mot in listeDesMots:
        print(mot)
    if nouvMot == leMotDeFin[0]:
        liste.destroy()
        scrollbar.destroy()
        labelo['text'] = "Félicitation ! Vous avez trouvé le bon mot en {} coups !".format(len(listeDesMots))  
        labelo.pack(pady=(100, 400), padx=(180, 180))

    else:
        liste.delete(0,100000)
        norm = unicodedata.normalize('NFKD', nouvMot)
        mot = norm.encode('ASCII', 'ignore').decode(encoding='UTF-8').replace(" ","_")

        #mot2 = quote(nouvMot.replace(" ","_"))
        #print(mot2)

        listeDesMots.append(mot)
        laRecherche = 'https://fr.wikipedia.org/wiki/{}'.format(mot)
        return newliste(recherche(laRecherche),liste)

# Gère le bouton retour pour retourner sur la page précédente
def retour():
    print('*Retour arrière effectué*')
    if (len(listeDesMots) >= 1):       
        labelo['text'] = "Vous êtes actuellement sur la page de : {}".format(listeDesMots[len(listeDesMots)-2])
        laRech = "https://fr.wikipedia.org/wiki/" + listeDesMots[len(listeDesMots)-2]
        return newliste(recherche(laRech),liste)

# Permet de recupérer tout les liens d'une page grace à BeautifulSoup en supprimant ceux qui ne sont pas intéressant
def recherche(leLien):
    links = []
    with urllib.request.urlopen(unquote(leLien)) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')
        for line in soup('h1', {"class":"firstHeading"}):
            title = str(line.contents[0])
            title = title.replace("<i>", "").replace("</i>", "")
            links.append(title)
            
        for anchor in soup('div', {"class":"mw-parser-output"}):
            for mot in anchor('a'):
                aSupp = unquote(str(mot.get('href')).replace("_"," "))
                badLinks = ['#','https:','http:','/w/','/Fichier:','/Modèle:','/Spécial:','/Catégorie:','/Aide:','/Wikipédia:','/Portail:','/API','//books','/Discussion:','/Projet:']
                if not any(st in aSupp for st in badLinks):
                    links.append(aSupp.replace("/wiki/",""))
                
        links = list(set(links))
        return links

# Permet de créer une nouvelle liste
def newliste(mots, laListe):
    i = 1
    for mot in mots:
        laListe.insert(i, mot)
        i=i+1

def popUp():
    popup = Tk()
    popup.wm_title("Règles")
    label = Label(popup, text="Vous devez, en partant du mot de départ donné, arriver au mot cible tout en utilisant uniquement les liens la page en cours. \nL'objectif est d'arriver à l'article cible en un minimum de clics. \n\n Vous avez à votre disposition un bouton \"retour\" qui vous permet de retourner sur le mot précedent \n(Vous ne pourrez pas remonter de plusieurs mot d'un coup, il ne faut pas que ça soit trop simple non plus) \nEnfin, une fois que la partie est terminée, votre score s'affichera ! ")
    label.pack()
    leave = Button(popup, text="Okay", command = popup.destroy)
    leave.pack(pady=(10))
    popup.mainloop()


# main
leMotDeDeb = recherche('https://fr.wikipedia.org/wiki/Caroline_du_Nord')
leMotDeFin = recherche('https://fr.wikipedia.org/wiki/Atlanta')
#https://fr.wikipedia.org/wiki/Special:Page_au_hasard

fenetre = Tk()
fenetre.title('WikiGaaaame')
fenetre.geometry('700x700')
scrollbar = Scrollbar(fenetre)
scrollbar.pack(side=RIGHT, fill=Y)

frame = Frame(fenetre)
frame.pack()
canvas = Canvas(fenetre, bg="grey", width=800, height=800)
canvas.pack()
liste = Listbox(canvas, height='30', width='100')
listeDesMots =[]

label1 = Label(canvas, text="WikiGame")
label1.pack()
label2 = Label(canvas, text="Le mot de départ est : {}".format(leMotDeDeb[0]))
label2.pack()
label3 = Label(canvas, text="Et le mot cible est : {}".format(leMotDeFin[0]))
label3.pack()
labelo = Label(canvas, text="")
labelo.pack()
    
liste.bind('<ButtonRelease-1>',clic)

newliste(leMotDeDeb, liste)
liste.pack()

liste.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=liste.yview)

Button(canvas, text="Fermer", command=fenetre.quit).pack(side=RIGHT, pady=(10), padx=(10))
Button(canvas, text="Retour", command=retour).pack(side=LEFT, pady=(10), padx=(10))
Button(canvas, text='Règles', command=popUp).pack(side=BOTTOM, pady=(10), padx=(10))

fenetre.mainloop()