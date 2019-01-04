#author: Lilian Letard (Eruthys)
#date: 04/01/2019
from PIL import Image
import copy,time

def debug(nb,value):
    output="[\n"
    i=0
    for obj in value:
        i+=1
        output+= str(obj)+", " if i%nb!=0 else str(obj)+", \n"
    print(output + "]")

def affichage(value):
    output=""
    for i in range (len(value)-1):
        output+= str(value[i])+", "
    output+= str(value[i+1])
    return output

def color(pixels, width,coox,cooy,dep_arriv,serialisation):#Layer de conversion des couleurs en type de cellules
    rgb=pixels[coox,cooy]
    if rgb[0]+rgb[1]+rgb[2] == 255*3:
        serialisation[cooy*width+coox]=2
    elif rgb[0]+rgb[1]+rgb[2] == 255:
        serialisation[cooy*width+coox]=1
        dep_arriv.append(cooy*width+coox)
    else:
        serialisation[cooy*width+coox]=0

def croisement(i, width, serialisation):#regarde si une cellule vide est un croisement (plus de 2 possibilitees de chemin)
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
        else:
            return 2
    else:
        return serialisation[i]

def glouton_vers_serialisation(labyrinthe):
    width, height = labyrinthe.size
    serialisation=width*height*[0]
    depart_arrivee=[]
    pixels=labyrinthe.load()
    for x in range (0,width):#boucle pour serialiser le labyrinthe
        for y in range(0,height):
            color(pixels, width,x,y,depart_arrivee,serialisation)
    for i in range (0,width*height):
        serialisation[i]=croisement(i, width, serialisation)
    return serialisation,depart_arrivee

def cell_mother(width, height ,depart_arrivee, serialisation, chemin):#regarde si une cellule arrive depart est environnente
    cell = chemin[len(chemin)-1]
    if cell not in {depart_arrivee[0]+height, depart_arrivee[0]-height} and len(chemin)>1:
        if serialisation[cell-1]==1:
            chemin.append(cell-1)
            return 2
        if cell<width*(height-1) and serialisation[cell+width]==1:
            chemin.append(cell+width)
            return 2
        if serialisation[cell+1]==1:
            chemin.append(cell+1)
            return 2
        if cell>width:
            if serialisation[cell-width]==1:
                chemin.append(cell-width)
                return 2

def chemin_explore(cell_number,cell_suivante, serialisation, backup_serialisation, chemin, backup_chemin):#change la valeur de a case ou on est passe pour signifier le passage
        if serialisation[cell_number]==2:
            serialisation[cell_number]=4
        if serialisation[cell_number]==3:
            serialisation[cell_number]=5
        if serialisation[cell_number]==5:
            backup_chemin.append(0)
            backup_chemin[len(backup_chemin)-1]=copy.deepcopy(chemin)
            taille=len(backup_chemin)-1
            taille2=len(backup_chemin[taille])-1
            del backup_chemin[taille][taille2]
            backup_serialisation.append(0)
            backup_serialisation[len(backup_serialisation)-1]=copy.deepcopy(serialisation)

            backup_serialisation[len(backup_serialisation)-1][cell_number]=3
            backup_serialisation[len(backup_serialisation)-1][cell_suivante]=4
        return 0

def surrounding_cell(width,height, serialisation, backup_serialisation, chemin, backup_chemin):#on regarde si des cellules environnantes sont du type vide (2)
    cell = chemin[len(chemin)-1]
    if serialisation[cell-1] in {2,3}:
        chemin.append(cell-1)
        chemin_explore(cell,cell-1, serialisation,backup_serialisation, chemin,backup_chemin)
        return 1
    elif cell<width*(height-1) and serialisation[cell+width] in {2,3}:
        chemin.append(cell+width)
        chemin_explore(cell,cell+width, serialisation,backup_serialisation, chemin,backup_chemin)
        return 1
    elif serialisation[cell+1] in {2,3}:
        chemin.append(cell+1)
        chemin_explore(cell,cell+1, serialisation,backup_serialisation, chemin,backup_chemin)
        return 1
    elif cell>width and serialisation[cell-width] in {2,3}:
            chemin.append(cell-width)
            chemin_explore(cell,cell-width, serialisation,backup_serialisation, chemin,backup_chemin)
            return 1
    else:#reviens a une intersection,cul de sac
        return 0

def supp(listea,listeb):
    del listea[len(listea)-1]
    del listeb[len(listeb)-1]

def glouton_parcours_graphe(width, height, depart_arrivee, serialisation):
    renvoie=1
    chemin=[]
    backup_serialisation=[]
    backup_chemin=[]
    solutions=[]
    chemin.append(depart_arrivee[0])
    while renvoie==1:
        fin=cell_mother(width, height, depart_arrivee, serialisation, chemin)
        if fin==2:
            solutions.append(0)
            solutions[len(solutions)-1]=copy.deepcopy(chemin)
            chemin=backup_chemin[len(backup_chemin)-1]
            serialisation=backup_serialisation[len(backup_serialisation)-1]
            supp(backup_serialisation,backup_chemin)
        renvoie=surrounding_cell(width, height, serialisation, backup_serialisation, chemin, backup_chemin)
        if renvoie==0:
            if len(backup_chemin)<1:
                renvoie=0
            else:
                chemin=backup_chemin[len(backup_chemin)-1]
                serialisation=backup_serialisation[len(backup_serialisation)-1]
                supp(backup_serialisation,backup_chemin)
                renvoie=1
    return solutions

def par_glouton(labyrinthe) :
    width, height = labyrinthe.size
    serialisation,depart_arrivee = glouton_vers_serialisation(labyrinthe)
    solutions= glouton_parcours_graphe(width, height, depart_arrivee, serialisation)
    solutions.sort(key=lambda v: len(v)) #Tri les solutions selon leur taille
    return solutions[0]

def init_glouton():
    labyrinthe=Image.open("unknown.png")
    time1=time.time()
    res=par_glouton(labyrinthe)
    time2=time.time()
    print("l'un des chemins le plus court est " + affichage(res)+" avec un deplacement en "+str(len(res)-1)+ " coups")
    print("il a fallu "+str(time2-time1)+" seconde.s")