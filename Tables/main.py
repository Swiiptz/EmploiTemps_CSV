import csv
#---------------Fonctions outils--------------------#
def exporter(tableau:list, nom_fichier:str):#->csv
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

def change_index(dico:dict, long:tuple, nom_index:str, ajout:str)->dict:
  """
  entree  
          dico       dict     dictionnaire principale
          long       tuple    longeur de l'id
          nom_index  str      nom de l'index a changer
          ajout      str      ajout d'un caractere a l'index (optionnel)
  sortie
          dico       dict     dictionnaire avec l'index change
  """
  for i in range(1,len(dico)+1):
   new_key = ajout+dico[str(i)][str(nom_index)][long[0]:long[1]]
   #print(type(new_key))
   dico[new_key]=dico.pop(str(i))
  return dico

def ajout_dic(dico:dict, dico_ann:dict, num_var:str, nom_var:str, taille, longeur:tuple):
  for i in dico.keys():
    index_dic_rep = dico[i][num_var]
    integer_index = int(index_dic_rep)
    if len(str(integer_index)) == taille:
      index_dic_rep = index_dic_rep[longeur[0]:longeur[1]]
    #print(index_dic_rep, nom_var, num_var, i, dico_ann)
    dico[i][nom_var]=dico_ann[index_dic_rep][nom_var]
  return dico

def choix_non_reconnu(var: str,table):
  global choix_non
  if var not in table:
    choix_non = 1
    print("Choix non reconnu, fin du programme")
  else :
    return None


#-----------------------------------------------------#

def lit_fichier(nom_fichier: str)-> dict:
  """
  entree
          nom_fichier     str     le nom du fichier csv Ã  transformer en dictionnaire
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

def lit_fichier_equipes_professeurs()->dict:
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
  


def cree_edt():
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
  return dic_rep

def Etat_Acceuil()->int:
 global stop
 choix = input("Bonjour. Que voulez-vous faire ?\n0 : Sortir\n1 : Afficher l'emploi du temps d'une classe\n2 : Afficher l'emploi du temps d'un professeur\n3 : Afficher la presence ou non des classes a une heure donnee\n\nEntrez votre choix, puis validez :")
 if choix == "0":
  print("Fin du programme")
  stop = 1
 elif choix == "1":
  Etat_choix_classe()
 elif choix == "2":
  Etat_choix_enseignant()
 elif choix == "3":
  Etat_choix_jour_hhmm()
 else:
  choix_non_reconnu()

def Etat_choix_classe()->int:
  global choix_classe
  print("Entrez le numero de la classe dont vous voulez voir l'emploi du temps\n0 : Retour a l'acceuil")
  for i in tab_classes:
    print(i, ":",tab_classes[i]["Nom_Classe"])
  choix_classe = input('Votre Choix :')
  #if choix_classe not in tab_classes:
  choix_non_reconnu(choix_classe,tab_classes)
  if choix_classe=="0":
    Etat_Acceuil()

def Etat_choix_enseignant()->int:
  global choix_professeur 
  print("Entrez le numero de l'enseignant dont vous voulez voir l'emploi du temps\n0 : Retour a l'acceuil")
  for i in tab_professeurs:
    print(i, ":", tab_professeurs[i]["Nom_Professeur"])
  choix_professeur = input('Votre Choix :')
  if choix_professeur=='0':
    Etat_Acceuil()
  #if choix_professeur not in tab_professeurs:
  choix_non_reconnu(choix_professeur,tab_professeurs)
  
  

def Etat_choix_jour_hhmm()->int:
  global choix_jour
  global choix_hhmm
  test_hhmm = []
  for i in tab_sequences:
    hhmm = tab_sequences[i]["heure_debut"]
    test_hhmm.append(hhmm)
  print("Entrez le jour auquel vous souhaitez avoir l'etat des classes")
  for i in tab_jours:
    print(i,":",tab_jours[i]["Nom_jour"])
  choix_jour = input("Votrez choix :")
  if choix_jour == "0":
    Etat_Acceuil()
  if choix_jour not in tab_jours:
    print("choix_non_reconnu")
  choix_hhmm = input("Entrez l'heure (hh:mm, tranche de 30min de 8:30 a 18:00) a laquelle vous souhaitez avoir l'etat des classes :")
  #if choix_hhmm not in test_hhmm:
  choix_non_reconnu(choix_hhmm,test_hhmm)
  


#------------Declaration variables globales-------------#
tab_classes = lit_fichier("classes")
tab_professeurs = lit_fichier("professeurs")
tab_matieres = lit_fichier("matieres")
tab_jours = lit_fichier("jours")
tab_sequences = cree_edt()
tab_equipes_professeurs = lit_fichier_equipes_professeurs()
#-------------------------------------------------------#




#--------------------------Test-----------------------------#
row = tab_equipes_professeurs
Etat_Acceuil()
#Etat_choix_classe()
#print(cree_edt())
#print(len(cree_edt()))
#for i in row:
#  print(i,row[i])


#-----------------------------------------------------------#


"""
list1= [{'N_equipe_prof':'2999999','N_':'5000000'}, {'N_equipe_prof':'200000','N_':'58888888'}]
cle1= [1,2]
dico_test={}
for i in range(0,len(list1)):
  cle = str(cle1[i])
  dico_test[cle]=list1[i-1]
print(dico_test)

dico_test = change_index(dico_test, (0,4),"N_equipe_prof")

for i in range(1,len(dico_test)):
  print(str(i))
  print(dico_test[str(i)]['N_equipe_prof'])
  n_cle = str(dico_test[str(i)]['N_equipe_prof'])
  n_cle = n_cle[0:4]
  dico_test[n_cle]=dico_test[str(i)]
  del dico_test[str(i)]

print(dico_test)
"""
