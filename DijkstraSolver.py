#author: Lilian Letard (Eruthys)
#date: 04/01/2019
from PIL import Image
import csv, time

def debug(value):
    output="[\n"
    i=0
    for obj in value:
        i+=1
        output+= str(obj)+", " if i%11!=0 else str(obj)+", \n"
    print(output + "]")

def affichage(value):
    output=""
    for i in range (len(value)-1):
        output+= str(value[i])+", "
    output+= str(value[i+1])
    return output

def dijkstra_color(pixels,width, height, serialisation,depart_arrivee,coox,cooy):#Layer de conversion des couleurs en type de cellules
    rgb=pixels[coox,cooy]
    if rgb[0]+rgb[1]+rgb[2] == 255*3:
        serialisation[cooy*width+coox]=2
    elif rgb[0]+rgb[1]+rgb[2] == 255:
        serialisation[cooy*width+coox]=3
        depart_arrivee.append(cooy*width+coox)
    else:
        serialisation[cooy*width+coox]=0

def dijkstra_croisement(width, serialisation,i):#regarde si une cellule vide est un croisement plus de 2 possibilite de chemin
    nb=0
    if serialisation[i]==2:
        if serialisation[i-1] > 0:
            nb+=1
        if serialisation[i+width] > 0:
            nb+=1
        if serialisation[i+1] > 0:
            nb+=1
        if serialisation[i-width] > 0:
            nb+=1
        if nb>2:
            return 3
        if nb<2:
            return 5
        else:
            return 2
    else:
        return serialisation[i]

def dijkstra_vers_serialisation(labyrinthe):
    pixels=labyrinthe.load()
    width, height = labyrinthe.size
    serialisation=width*height*[0]
    depart_arrivee=[]
    for x in range (0,width):#boucle pour serialiser le labyrinthe
        for y in range(0,height):
            dijkstra_color(pixels,width, height, serialisation,depart_arrivee,x,y)
    for i in range (0,width*height):
        serialisation[i]=dijkstra_croisement(width, serialisation,i)
    return serialisation, depart_arrivee

def cellule_alentour(width, height, serialisation, chemin, cell_index):#on regarde si des cellules environnantes sont du type vide (2)
# Retourne 2 si cellule et égale à 2, 5 si cellule à 5, 36 si celulle à 3 ou 6, sinon 0 si aucun mouvement possible
    if tout_traite_alentour(width, height, serialisation,cell_index):
        return 0
    if serialisation[cell_index-1] in {2,3,5,6}: # à gauche
        chemin.append(cell_index-1)
        if serialisation[cell_index-1] in {3,6}:
            return 36
        elif serialisation[cell_index-1]==5 :
            return 5
        else :
            return 2
    elif (cell_index+width)<(width*height) and serialisation[cell_index+width] in {2,3,5,6}  :
        chemin.append(cell_index+width)
        if serialisation[cell_index+width] in {3,6}:
            return 36
        elif serialisation[cell_index+width]==5:
            return 5
        else :
            return 2
    elif serialisation[cell_index+1] in {2,3,5,6}:
        chemin.append(cell_index+1) # à droite
        if serialisation[cell_index+1] in {3,6}:
            return 36
        elif serialisation[cell_index+1]==5 :
            return 5
        else:
            return 2
    elif (cell_index-width)>0 and serialisation[cell_index-width] in {2,3,5,6}: # en haut
        chemin.append(cell_index-width)
        if serialisation[cell_index-width] in {3,6}:
            return 36
        elif serialisation[cell_index-width]==5:
            return 5
        else:
            return 2

def tout_traite_alentour(width, height, serialisation,cell_index):#on regarde si des cellules environnantes sont du type croisement (3)
    reponse,rep1,rep2,rep3,rep4 = False, False, False,False,False
    if cell_index%width ==0 or serialisation[cell_index-1] in {9,0} :
        rep1 = True
    if (cell_index+1)%width ==0 or serialisation[cell_index+1] in {9,0}:
        rep2 = True
    if cell_index>width*(height-1):
        rep3=True
    elif serialisation[cell_index+width] in {9,0}:
        rep3 = True

    if cell_index<width:
        rep4=True
    elif serialisation[cell_index-width] in {9,0}:
        rep4 = True
    reponse = rep1 and rep2 and rep3 and rep4
    return reponse

def chemin_explore(serialisation,cell_index):
    if serialisation[cell_index] in {3,2}:
        serialisation[cell_index]=9

def dijkstra_parcours_graphe(width, height, serialisation, depart_arrivee):
    n=0
    boucle=1
    croisement_liste=[]
    chemin=[]
    matrice =[[0 for j in range (width*height)] for k in range(height*width)]
    croisement_liste.append(depart_arrivee[0])
    chemin.append(croisement_liste[n])
    while boucle==1:
        chemin_explore(serialisation,chemin[len(chemin)-1])
        retour=cellule_alentour(width, height, serialisation,chemin,chemin[len(chemin)-1])
        if retour==36:
            matrice[chemin[0]][chemin[len(chemin)-1]]=[len(chemin)-1,[]]
            for i in range (len(chemin)):
                matrice[chemin[0]][chemin[len(chemin)-1]][1].append(chemin[i])
            matrice[chemin[len(chemin)-1]][chemin[0]]=[len(chemin)-1,[]]
            for i in range (len(chemin)):
                matrice[chemin[len(chemin)-1]][chemin[0]][1].append(chemin[len(chemin)-1-i])
            if chemin[len(chemin)-1] not in croisement_liste :
                croisement_liste.append(chemin[len(chemin)-1])
            if len(chemin)==2:
                serialisation[chemin[1]]=9
            chemin.clear()
            chemin.append(croisement_liste[n])
        if retour==5:
            if len(chemin)==2:
                serialisation[chemin[1]]=9
            chemin.clear()
            chemin.append(croisement_liste[n])
        if retour==0:
            for g in range (len(croisement_liste)):
                serialisation[croisement_liste[g]]=3
            serialisation[chemin[0]]=9
            n+=1
            if n==len(croisement_liste):
                break
            chemin.clear()
            chemin.append(croisement_liste[n])
    return croisement_liste, chemin, matrice

def remplissage_dijkstra(index_sommet,distance_avant, croisement_liste, matrice, tableau):
    longueur_tableau=len(croisement_liste)
    for g in range(1,longueur_tableau+1):
        if tableau[len(tableau)-2][g]=="-":
            tableau[len(tableau)-1].append("-")
        elif g==index_sommet:
            tableau[len(tableau)-1].append("-")
        elif matrice[tableau[len(tableau)-1][0]][tableau[0][g]] !=0:
            if tableau[len(tableau)-2][g] == "oo":
                tableau[len(tableau)-1].append(matrice[tableau[len(tableau)-1][0]][tableau[0][g]][0]+distance_avant)

            elif matrice[tableau[len(tableau)-1][0]][tableau[0][g]][0]+distance_avant<tableau[len(tableau)-2][g]:
                    tableau[len(tableau)-1].append(matrice[tableau[len(tableau)-1][0]][tableau[0][g]][0]+distance_avant)
            else:
                tableau[len(tableau)-1].append(tableau[len(tableau)-2][g])
        else:

            if str(tableau[len(tableau)-2][g]).isdigit():
                tableau[len(tableau)-1].append(tableau[len(tableau)-2][g])
            else:
                 tableau[len(tableau)-1].append("oo")

def dijkstra(serialisation, croisement_liste, depart_arrivee, chemin, matrice):
    distance=[]
    tableau=[]
    longueur_tableau=len(croisement_liste)
    index=croisement_liste.index(depart_arrivee[1])
    croisement_liste[index],croisement_liste[len(croisement_liste)-1]=croisement_liste[len(croisement_liste)-1],croisement_liste[index]
    tableau.append([])
    tableau[len(tableau)-1].append("n°sommet")
    for g in range (longueur_tableau):
        tableau[len(tableau)-1].append(croisement_liste[g])
    tableau.append([])
    tableau[len(tableau)-1].append("etape initial")
    for g in range(1,longueur_tableau+1):
        if g==1:
            tableau[len(tableau)-1].append(0)
        else:
            tableau[len(tableau)-1].append("oo")

    for _ in range(longueur_tableau-1):
        distance.clear()
        for g in range (1,longueur_tableau):

            if tableau[len(tableau)-1][g] not in {"oo","-"}:
                distance.append(tableau[len(tableau)-1][g])
        distance.sort()
        for g in range(1,longueur_tableau+1):
            if tableau[len(tableau)-1][g]==distance[0]:
                sommet=tableau[0][g]
                break
        tableau.append([])
        tableau[len(tableau)-1].append(sommet)
        remplissage_dijkstra(g,distance[0], croisement_liste, matrice, tableau)
    return tableau

def chemin_dijkstra(depart_arrivee,tableau):
    chemin=[tableau[0][len(tableau[0])-1]]
    while chemin[len(chemin)-1]!=depart_arrivee[0]:
        sommet=chemin[len(chemin)-1]
        index_sommet=tableau[0].index(sommet)
        for g in range(len(tableau)):
            position=len(tableau)-1-g
            if tableau[position][index_sommet]!="-" and tableau[position-1][index_sommet]!=tableau[position][index_sommet]:
                chemin.append(tableau[position][0])
                break
    return chemin

def chemin_entre_sommet(chemin_sommet,depart_arrivee,matrice):
    chemin2=[]
    for g in range (0,len(chemin_sommet)-1):
        for y in range (matrice[chemin_sommet[g]][chemin_sommet[g+1]][0]):
            chemin2.append(matrice[chemin_sommet[g]][chemin_sommet[g+1]][1][y])
    chemin2.append(depart_arrivee[1])
    return chemin2

def par_dijkstra(labyrinthe):
    width, height = labyrinthe.size
    serialisation,depart_arrivee = dijkstra_vers_serialisation(labyrinthe)
    croisement_liste, chemin, matrice = dijkstra_parcours_graphe(width, height, serialisation, depart_arrivee)
    tableau = dijkstra(serialisation, croisement_liste, depart_arrivee, chemin, matrice)
    chemin_sommet=chemin_dijkstra(depart_arrivee,tableau)
    chemin_sommet.reverse()
    chemin_final=chemin_entre_sommet(chemin_sommet,depart_arrivee,matrice)
    return chemin_final

def init_dijkstra():
    labyrinthe=Image.open("maze.png")
    time1=time.time()
    res = par_dijkstra(labyrinthe)
    time2=time.time()
    print("l'un des chemins le plus court est " + affichage(res)+" avec un deplacement en "+str(len(res)-1)+ " coups")
    print("il a fallu "+str(time2-time1)+" seconde.s")