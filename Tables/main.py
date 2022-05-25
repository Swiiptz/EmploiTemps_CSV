#importation des bibliotheques
import csv
#---------------Fonctions outils--------------------#
def exporter(tableau:list, nom_fichier:str):#->csv #Fonction par Milan
  """
  entree
          tableau        list       table a convertir en csv
          nom_fichier    str        nom du fichier csv 
  sortie
          rien           csv        fichier csv sur l'ordinateur
  """
  fichier = open(nom_fichier, "w",newline='')
  writer = csv.writer(fichier)
  writer.writerows(tableau)

def change_index(dico:dict, long:tuple, nom_index:str, ajout:str)->dict: #Fonction par Milan
  """
  entree  
          dico       dict     dictionnaire principale
          long       tuple    longeur de l'id
          nom_index  str      nom de l'index a changer
          ajout      str      ajout d'un caractere a l'index (optionnel)
  sortie
          dico       dict     dictionnaire avec l'index change
  """
  #parcourt le dictionnaire pour changer les indexs
  for i in range(1,len(dico)+1):
   new_key = ajout+dico[str(i)][str(nom_index)][long[0]:long[1]]
   dico[new_key]=dico.pop(str(i))
  return dico

def ajout_dic(dico:dict, dico_ann:dict, num_var:str, nom_var:str, taille, longeur:tuple): #Fonction par Milan
  """
  entree
          dico      dict    dictionnaire principal ou la valeur sera ajoutee
          dico_ann  dict    dictionnaire secondaire dans lequel on recupere la valeur a ajouter
          num_var   str     nom index de la variable
          nom_var   str     nom de la variable
          taille            taille de la variable a verifier
          longueur  tuple   taille de la variable a recuperer (debut,fin)
  sortie
          dico      dict    dictionnaire avec la valeur ajoutee
  """
  #ouverture du dictionnaire avec une boucle for
  for i in dico.keys():
    index_dic_rep = dico[i][num_var]
    integer_index = int(index_dic_rep)
    #verification de la taille de la variable
    if len(str(integer_index)) == taille:
      index_dic_rep = index_dic_rep[longeur[0]:longeur[1]]
    #ajout de la variable au dictionnaire principale
    dico[i][nom_var]=dico_ann[index_dic_rep][nom_var]
  return dico

def choix_non_reconnu(var: str,table)->int: #Fonction par Milan
  """
  entree    
            var    str          nom de la variable a verifier 
            table  list/dict    table pour verifier si var est dedans
  sortie
            1      int          bit pour prevenir variable invalide
            None   None         renvoie rien si tout est valide
  """
  #verification de la presence de var dans la table specifiee
  if var not in table:
    choix_non = 1
    print("Choix non reconnu, fin du programme")
    #envoie du bit en cas d'erreur
    return 1
  else :
    return None

def ajout_heure(heure_debut:str,duree:str)->str: #Fonction par Milan
  """
  entree
            heure_debut    str    heure de debut du cours
            duree          str    duree du cours
  sortie
            heure_suiv     str    heure de debut + duree -> heure de fin

  """
  #separation des partie de la chaine heure de debut et duree
  hh = heure_debut[0:2]
  mm = heure_debut[3:]
  duree_hh = duree[0:2]
  duree_mm = duree[3:]
  #on additionne les differentes partie des deux chaines
  heure_suiv_hh = int(hh)+int(duree_hh)
  heure_suiv_mm = int(mm)+int(duree_mm)
  heure_suiv = str(heure_suiv_hh)+":"+str(heure_suiv_mm)
  heure_suiv_mm = heure_suiv[3:]
  heure_suiv_hh = heure_suiv[0:2]
  #on verifie les chaines
  if int(heure_suiv_mm) == 0 :
    heure_suiv = int(hh)+int(duree_hh)
    heure_suiv = str(heure_suiv)+":00"
  #passage de la base 10 a base 60 (60 min = heure)
  if heure_suiv_mm == "60":
    heure_suiv_hh = int(heure_suiv_hh)+1
    heure_suiv = str(heure_suiv_hh)+":00"
  return heure_suiv
#-----------------------------------------------------#

def lit_fichier(nom_fichier: str)-> dict: #Fonction par Milan
  """
  entree
          nom_fichier     str     le nom du fichier csv a transformer en dictionnaire
  sortie
          dic_rep         dict    dictionnaire du fichier csv avec les bons indexs 
  """
  #declaration des variables utilisees
  tab_rep = []
  dic_rep = {}
  #on charge le fichier et on le transforme en liste
  nom_fichier += ".csv"
  with open(nom_fichier, "r", newline = "", encoding = "utf-8") as fichier_ouvert:
    tab_rep = list(csv.DictReader(fichier_ouvert, delimiter=","))
    #on numerote les indexs pour le dictionnaire
    for row in range(0, len(tab_rep)):
      dic_rep[str(row+1)] = tab_rep[row] 
    return dic_rep

def lit_fichier_equipes_professeurs()->dict: #Fonction par Benjamin
  """
  entree
          rien
  sortie
          dic_rep       dict        dictionnaire de la tableau equipes_professeurs.csv
  """
  #declaration des variables utilisees
  dic_rep = {}
  #on ouvre la table equipes_professeurs
  with open("equipes_professeurs.csv", "r", encoding = "utf-8") as fichier_ouvert:
    tab_rep = list(csv.reader(fichier_ouvert, delimiter=","))
    tab_rep[0]= ["N_equipe_prof","N_Classe", "N_Matiere", "N_Professeur"]
  #on ordonne dans une liste avec des virgules les differents indexs
    for i in range(1,len(tab_rep)):
      tab_rep[i]= [tab_rep[i][0],tab_rep[i][0][0:2],tab_rep[i][0][2:4],tab_rep[i][0][4:6]]
  #on exporte la table reordonnee pour la transformer en dictionnaire  
  exporter(tab_rep, "csv_temp.csv")
  dic_rep = lit_fichier("csv_temp")
  #on change les indexs avec la classe et la matiere avec la methode pop
  dic_indexe = change_index(dic_rep,(0,4),"N_equipe_prof","")
  return dic_indexe

def cree_edt()->dict: #Fonction par Baptiste
  """
  entree      
          rien 
  sortie
          dic_rep     dict        dictionnaire des sequences avec les différents indexs  
  """
  #declaration des variables
  tab_equipes_professeurs = lit_fichier_equipes_professeurs()
  classe_mat_all = []
  prof_all = []
  compteur = 0
  dic_rep = lit_fichier("sequences")
  change_index(dic_rep,(0,None),"N_Sequence", "0")
  #initialisation des indexs pour l'ajout de professeurs a la table sequences
  for i in dic_rep.keys():
   matiere = dic_rep[i]["N_Matiere"]
   classe = dic_rep[i]["N_Classe"]
   long_matiere = len(matiere)
   long_classe=len(classe)
   #verification de la longueur des indexs
   if long_matiere ==1 :
    matiere = "0"+str(matiere)
   if long_classe==1:
    classe = "0"+str(classe)
   classe_mat = str(classe)+str(matiere)
   #creation d'une liste contenant tous les indexs
   classe_mat_all.append(classe_mat)
  #initialisation d'une liste permettant de recuperer les indexs des professeurs dans la table equipes professeurs
  for i in range(len(classe_mat_all)):
    prof = tab_equipes_professeurs[classe_mat_all[i]]["N_Professeur"]
    prof_all.append(prof)
  #association des numeros des professeurs a la table sequences
  for i in dic_rep.keys():
    if compteur > 371:
      break
    dic_rep[i]["N_Professeur"]=prof_all[compteur]
    compteur+=1
  #ajout des differentes variables a la table sequences
  ajout_dic(dic_rep,tab_professeurs,"N_Professeur","Nom_Professeur",1,(1,None))
  ajout_dic(dic_rep,tab_jours,"N_Jour","Nom_jour",100,(0,None))
  ajout_dic(dic_rep,tab_classes,"N_Classe","Nom_Classe",100,(0,None))
  ajout_dic(dic_rep,tab_matieres,"N_Matiere","Nom_Matiere",100,(0,None))
  return dic_rep

def Etat_Acceuil()->str: #Fonction par Milan
 """
 entree
        rien
 sortie
        menu de l'acceuil
 """ 
 global stop
 choix = input("Bonjour. Que voulez-vous faire ?\n0 : Sortir\n1 : Afficher l'emplois du temps d'une classe\n2 : Afficher l'emploi du temps d'un professeur\n3 : Afficher la presence ou non des classes a une heure donnee\n\nEntrez votre choix, puis validez :")
 #choix 0 fin du programme
 if choix == "0":
  print("Fin du programme")
  exit()
 #renvoie sur les differentes fonctions selon les choix
 elif choix == "1":
  Etat_choix_classe()
 elif choix == "2":
  Etat_choix_enseignant()
 elif choix == "3":
  Etat_choix_jour_hhmm()
 else:
  choix_non_reconnu()

def Etat_choix_classe()->int: #Fonction par Benjamin
  """
  entree
          rien
  sortie
          menu du choix de la classe
  """
  global choix_classe
  print("Entrez le numero de la classe dont vous voulez voir l'emploi du temps\n0 : Retour a l'acceuil")
  #affichage de toutes les classes
  for i in tab_classes:
    print(i, ":",tab_classes[i]["Nom_Classe"])
  choix_classe = input('Votre Choix :')
  #verification de l'entree de l'utilisateur
  choix_non_reconnu(choix_classe,tab_classes)
  #renvoie a l'acceuil
  if choix_classe=="0":
    Etat_Acceuil()
  #suite du programme avec l'affichage du choix de l'utilisateur
  edit_edp_classe(choix_classe)

def Etat_choix_enseignant()->int: #Fonction par Baptiste
  """
  entree
        rien
  sortie
        menu du choix de l'emplois du temps de l'enseignant
  """
  print('Entrez le numero de l\'enseignant dont vous voulez voir l\'emploit du temps\nEntrez votre choix,puis validez:')  
  print("0 : Retour a l'accueil")
  #affichage de tout les professeur
  for k in tab_professeurs.keys():
      b = str(tab_professeurs[k]['N_Matiere'])
      print(tab_professeurs[k]['N_Professeur'],":",tab_professeurs[k]['Nom_Professeur'],"("+tab_matieres[b]['Nom_Matiere']+")")
  x = input('Votre choix:')
  choix_str = str(x)
  long_x = int(x)
  #renvoie a l'acceuil
  if x=='0':
    Etat_Acceuil()
  #verification de l'entree de l'utilisateur
  elif long_x>len(tab_professeurs):
      choix_non_reconnu(x,tab_professeurs)
  edit_edp_professeurs(choix_str)

def Etat_choix_jour_hhmm()->int:  #Fonction par Baptiste
  """
  entree
            rien
  sortie
            menu du choix des jours
  """
  #declaration variable
  global choix_jour
  global choix_hhmm
  global choix_non
  test_hhmm = []
  #creation d'une table de l'entierete des heures des debuts de cours 
  for i in tab_sequences:
    hhmm = tab_sequences[i]["heure_debut"]
    test_hhmm.append(hhmm)
  print("Entrez le jour auquel vous souhaitez avoir l'etat des classes")
  #affichage des jours
  for i in tab_jours:
    print(i,":",tab_jours[i]["Nom_jour"])
  choix_jour = input("Votre choix :")
  #renvoie a l'acceuil
  if choix_jour == "0":
    Etat_Acceuil()
  choix_non_reconnu(choix_jour,tab_jours)
  #verification de l'entree de l'utilisateur
  if choix_non_reconnu(choix_jour,tab_jours)==1:
    return None
  choix_hhmm = input("Entrez l'heure (hh:mm, tranche de 30min de 8:30 a 18:00) a laquelle vous souhaitez avoir l'etat des classes :")
  #verification de l'entree de l'utilisateur
  choix_non_reconnu(choix_hhmm,test_hhmm)
  #suite avec l'affichage de l'emploi selon le jour et l'heure
  edit_etat_classe(choix_jour, choix_hhmm)

def edit_edp_classe(nclasse:str)->None: #Fonction par Benjamin
  """
  entree
          nclasse     str      indexs de la classes
  sortie
          rien        none     affiche l'emploi du temps de la classe en question
  """
  nom_classe = tab_classes[nclasse]["Nom_Classe"]
  print("Emploi du temps de la",nom_classe)
  #parcourt pour chaque jour
  for k in tab_jours:
    nom_jour = tab_jours[k]["Nom_jour"]
    print(nom_jour)
    n_jour = tab_jours[k]["N_Jour"]
    #parcourt la table sequences
    for i in tab_sequences:
      #verification si l'index et le jour sont ceux demandes par l'utilisateur
      if tab_sequences[i]["N_Classe"]==tab_classes[nclasse]["N_Classe"] and tab_sequences[i]["N_Jour"]==n_jour:
        #declaration des variables
        heure_debut = tab_sequences[i]["heure_debut"]
        duree = tab_sequences[i]["duree"]
        heure_suiv = ajout_heure(heure_debut,duree)
        nom_professeur = tab_sequences[i]["Nom_Professeur"]
        nom_matiere = tab_sequences[i]["Nom_Matiere"]
        print("\t",heure_debut+"-"+heure_suiv,"("+duree+")",":",nom_matiere,"/",nom_professeur)
 
def edit_edp_professeurs(nprofesseur:int)->None: #Fonction par Baptiste
  """
  entree
         nprofesseur    int     index du professeur
  sortie
          rien          rien    affiche emploi du temps du professeur demande
  """
  #declarations variables
  tab_prof_jour = {}
  tab_prof_jour_sort = {}
  zero_nprofesseur = nprofesseur
  #on verifie la taille de l'index du prof pour faire gaffe 
  if len(nprofesseur)==1:
      zero_nprofesseur = "0"+nprofesseur
  #permet de recuperer les jours pour chaque prof
  for i in tab_sequences:
    if tab_sequences[i]["N_Professeur"]==zero_nprofesseur:
      p_jour = tab_sequences[i]["N_Jour"]
      tab_prof_jour[p_jour]=p_jour
  #tri les jours dans l'ordre chronologique
  n_sort = sorted(tab_prof_jour)
  for i in n_sort:
    tab_prof_jour_sort[i]=i
  #boucle qui parcourt les jours
  for k in tab_prof_jour_sort:
    nom_jour = tab_jours[k]["Nom_jour"]
    print(nom_jour)
    n_jour = tab_prof_jour_sort[k]
    #parcourt tab_sequences
    for i in tab_sequences:
      n_prof = tab_professeurs[nprofesseur]["N_Professeur"]
      #verifie taille indexs
      if len(n_prof)==1:
        n_prof = "0"+n_prof
      #verifie l'index du professeur et le jour
      if tab_sequences[i]["N_Professeur"]==n_prof and tab_sequences[i]["N_Jour"]==n_jour :
        heure_debut = tab_sequences[i]["heure_debut"]
        duree = tab_sequences[i]["duree"]
        heure_suiv = ajout_heure(heure_debut,duree)
        nom_professeur = tab_sequences[i]["Nom_Professeur"]
        nom_matiere = tab_sequences[i]["Nom_Matiere"]
        print("\t",heure_debut+"-"+heure_suiv,"("+duree+")",":",nom_matiere,"/",nom_professeur)

def edit_etat_classe(njour:str,hhmm:str)->None: #Fonction par Milan
  """
  entree
          njour     str    index du jour   
          hhmm      str    heure de debut
  sortie
          rien      rien   affiche pour un jour les cours a partir de l'heure demandee
  """
  hhmm_in = hhmm
  dico_order = {}
  print("Liste des cours le {nom_jour} a {hhmm_in}".format(nom_jour = tab_jours[njour]["Nom_jour"],hhmm_in = hhmm))
  #parcourt tab sequences
  for i in tab_sequences:
    #verification si l'index du jour et l'heure sont les bons dans tab sequences
    if tab_sequences[i]["N_Jour"]==njour and tab_sequences[i]["heure_debut"]==hhmm:
        heure_debut = tab_sequences[i]["heure_debut"]
        duree = tab_sequences[i]["duree"]
        #utilisation de la fonction pour determiner l'heure de fin
        heure_suiv = ajout_heure(heure_debut,duree)
        nom_professeur = tab_sequences[i]["Nom_Professeur"]
        nom_matiere = tab_sequences[i]["Nom_Matiere"]
        nom_classe = tab_sequences[i]["Nom_Classe"]
        n_classe = tab_sequences[i]["N_Classe"]
        #variable a afficher
        var_final = "{nom_classe}\t{heure_debut}-{heure_suiv} ({duree}) : {nom_matiere} / {nom_professeur}".format(nom_classe = nom_classe, heure_debut=heure_debut, heure_suiv=heure_suiv, duree = duree, nom_matiere = nom_matiere, nom_professeur=nom_professeur)
        print(var_final)


#------------Declaration variables globales-------------#
tab_classes = lit_fichier("classes")
tab_professeurs = lit_fichier("professeurs")
tab_matieres = lit_fichier("matieres")
tab_jours = lit_fichier("jours")
tab_sequences = cree_edt()
tab_equipes_professeurs = lit_fichier_equipes_professeurs()
#-------------------------------------------------------#

#--------------------------Main-----------------------------#
def main():
  #print(tab_sequences)
  while True:
    Etat_Acceuil()

main()
#-----------------------------------------------------------#