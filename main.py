import random
from ft_mail_and_log import ft_mail_and_log

contacts_tab = []

def lire_exception(fichier):
    exclusions = {}
    with open(fichier, 'r') as f:
        for line in f:
            line = line.strip()  # Supprimer les espaces vides autour
            if not line or line.startswith("#"):
                continue  # Ignorer les lignes vides ou les commentaires
            
            # Diviser la ligne en éléments
            elements = line.split(";")
            numero = int(elements[0])  # Premier élément : numéro
            exceptions = [int(e) for e in elements[5:]]  # Derniers éléments : exceptions
            
            exclusions[numero] = exceptions
    
    return exclusions

def lire_contacts(fichier):
    with open("contacts.txt", "r", encoding='utf-8') as fichier:
        for line in fichier:
            line = line.strip()
            if not line or line.startswith('#') or line[0] == '\n':
                continue
            infos = line.split(";")
            contacts_tab.append(infos)
    return contacts_tab

def generer_associations(exclusions):
    numeros = list(exclusions.keys())
    associations = {}
    if essayer_associer(0, numeros, associations, exclusions, set()):
        return associations
    else:
        raise ValueError("Impossible de trouver une solution avec les restrictions fournies.")

def essayer_associer(index, numeros, associations, exclusions, deja_utilises):
    if index == len(numeros):
        return True

    numero = numeros[index]
    possibles = [n for n in numeros if n != numero and n not in exclusions[numero] and n not in deja_utilises]

    random.shuffle(possibles)  # Mélanger pour essayer des options aléatoires

    for choix in possibles:
        associations[numero] = choix
        deja_utilises.add(choix)

        if essayer_associer(index + 1, numeros, associations, exclusions, deja_utilises):
            return True

        # Si cela ne fonctionne pas, revenir en arrière
        deja_utilises.remove(choix)
        del associations[numero]

    return False

# Lecture des contacts et génération des associations
try:
    fichier = 'contacts.txt'  # Nom du fichier texte
    contacts_tab = lire_contacts(fichier)
    exclusions = lire_exception(fichier)
    # print(exclusions)
    resultat = generer_associations(exclusions)
    with open("logs.txt", 'w') as l:
        print("", file=l)
    for numero, associe in resultat.items():
        print(f"\nnumero : {numero}, associe : {associe}")
        mail_santa = contacts_tab[numero - 1][2]
        lang = contacts_tab[numero - 1][3]
        nom = contacts_tab[numero - 1][1]
        target = contacts_tab[associe - 1][1]
        ft_mail_and_log(mail_santa, lang, nom, target)

except ValueError as e:
    print(e)
except IndexError as e:
    print("Une erreur d'index s'est produite : vérifiez vos données de contact.")
