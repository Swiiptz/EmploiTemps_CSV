import csv
def lit_fichier(nom_fichier: str)-> dict:
  dic_rep = {}
  #on charge le fichier et on le transforme en liste
  nom_fichier += ".csv"
  with open(nom_fichier, "r") as fichier_ouvert:
    dic_rep = list(csv.DictReader(fichier_ouvert, delimiter=","))
    return dic_rep

print(lit_fichier("equipes_professeurs"))

    