import csv
#---------------Fonctions outils--------------------#
def exporter(tableau:list, nom_fichier:str):#->csv
  """
  entrée
          tableau        list       table à convertir en csv
          nom_fichier    str        nom du fichier csv 
  sortie
          rien           csv        fichier csv sur l'ordinateur
  """
  fichier = open(nom_fichier, "w",newline='')
  writer = csv.writer(fichier)
  writer.writerows(tableau)

def change_index(dico:dict, long:tuple, nom_index:str)->dict:
  for i in range(1,len(dico)+1):
   new_key = dico[str(i)][str(nom_index)][long[0]:long[1]]
   #print(type(new_key))
   dico[new_key]=dico.pop(str(i))
  return dico
#-----------------------------------------------------#

def lit_fichier(nom_fichier: str)-> dict:
  """
  entrée
          nom_fichier     str     le nom du fichier csv à transformer en dictionnaire
  sortie
          dic_rep         dict    dictionnaire du fichier csv avec les bons indexs 
  """
  #déclaration des variables utilisées
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
  entrée
          rien
  sortie
          dic_rep       dict        dictionnaire de la tableau equipes_professeurs.csv
  """
  #déclaration des variables utilisées
  dic_rep = {}
  dic_prof = {}
  #on ouvre la table equipes_professeurs
  with open("equipes_professeurs.csv", "r", encoding = "utf-8") as fichier_ouvert:
    tab_rep = list(csv.reader(fichier_ouvert, delimiter=","))
    tab_rep[0]= ["N_equipe_prof","N_Classe", "N_Matiere", "N_Professeur"]
  #on ordonne dans une liste avec des virgules les différents indexs
    for i in range(1,len(tab_rep)):
      tab_rep[i]= [tab_rep[i][0],tab_rep[i][0][0:2],tab_rep[i][0][2:4],tab_rep[i][0][4:6]]
  #on exporte la table réordonnée pour la transformer en dictionnaire  
  exporter(tab_rep, "csv_temp.csv")
  dic_rep = lit_fichier("csv_temp")
  #on change les indexs avec la classe et la matière avec la méthode pop
  dic_indexe = change_index(dic_rep,(0,4),"N_equipe_prof")
  return dic_indexe
  


def cree_edt():
  pass


#------------Déclaration variables globales-------------#
tab_classes = lit_fichier("classes")
tab_professeurs = lit_fichier("professeurs")
tab_matieres = lit_fichier("matieres")
tab_jours = lit_fichier("jours")
tab_sequences = None
tab_equipes_professeurs = lit_fichier_equipes_professeurs()
#-------------------------------------------------------#



#--------------------------Test-----------------------------#
row = tab_equipes_professeurs
#row = change_index(tab_equipes_professeurs,(0,4),"N_equipe_prof")

for i in row:
  print(i,row[i])
#print(row)

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
