import csv
def exporter(tableau, nom_fichier):
  fichier = open(nom_fichier, "w",newline='')
  writer = csv.writer(fichier)
  writer.writerows(tableau)

def lit_fichier(nom_fichier: str)-> dict:
  tab_rep = []
  dic_rep = {}
  #on charge le fichier et on le transforme en liste
  nom_fichier += ".csv"
  with open(nom_fichier, "r", newline = "", encoding = "utf-8") as fichier_ouvert:
    tab_rep = list(csv.DictReader(fichier_ouvert, delimiter=","))
    for row in range(0, len(tab_rep)):
      dic_rep[row+1] = tab_rep[row] 
    return dic_rep

def lit_fichier_equipes_professeurs()->dict:
  dic_rep = {}
  dic_prof = {}
  with open("equipes_professeurs.csv", "r", encoding = "utf-8") as fichier_ouvert:
    #N_Classe
    #N_Matiere
    #N_Professeurs
    tab_rep = list(csv.reader(fichier_ouvert, delimiter=","))
    tab_rep[0]= ["N_equipe_prof","N_Classe", "N_Matiere", "N_Professeur"]
    for i in range(1,len(tab_rep)):
      tab_rep[i]= [tab_rep[i][0],tab_rep[i][0][0:2],tab_rep[i][0][2:4],tab_rep[i][0][4:6]]  
  exporter(tab_rep, "csv_temp.csv")
  print(tab_rep)
  dic_rep = lit_fichier("csv_temp")
  return dic_rep


row = lit_fichier_equipes_professeurs()
print(row)
#for i in row:
  #print(i,row[i]

