import os.path
import DESAlgo

from DESAlgo import encryptRealMessage
from DESAlgo import decryptRealMessage

# Retourn False si le texte contient autre chose que des 0 ou des 1 ; sinon True
def checkIfBinaryString(string) :
    for i in range (0, len(string)) :
        if(string[i] != "0" and string[i] != "1") :
            return False
    return True

# Demande à l'utilisateur comment il veut donner le texte, la récupère (
# en lisant la console ou le fichier donné) puis vérifie qu'il est valide ; 
# retourne None si l'utilisateur veut annuler, sinon le texte
def askForText(cType) :
    while(True) :
        entry = input("\nVoulez-vous taper le texte à " + cType + " (1), ou bien donner le chemin d'un fichier le contenant (2) ? Retour : (3)\n")
        if(entry == "1") :
            entry = input("Tapez le texte : ")
            if(len(entry) == 0) :
                print("Le texte tapé ne contient aucun caractère !\n")
            else :
                return entry
        elif(entry == "2") :
            entry = input("\nTapez le chemin du fichier (en partant du dossier de lancement du script) : ")
            if not os.path.isfile(entry) :
                print("Le fichier de ce nom n'existe pas !\n")
            else :
                f=open(entry, "r", encoding='utf-8-sig')
                txt=f.read()
                if(len(txt) == 0) :
                    print("Le fichier existe mais ne contient aucun caractère !\n")
                else :
                    return txt
        elif(entry == "3") :
            return None
        else :
            print("Les options autorisées sont 1, 2 et 3.\n")

# Demande à l'utilisateur comment il veut donner la clef, la récupère (
# en lisant la console ou le fichier donné) puis vérifie qu'elle est valide ; 
# retourne None si l'utilisateur veut annuler, sinon la clef
def askForKey() :
    while(True) :
        entry = input("\nVoulez-vous taper la clef (1), ou bien donner le chemin d'un fichier la contenant (2) ? Retour : (3)\n")
        if(entry == "1") :
            entry = input("Tapez la clef : ")
            if(len(entry) != 64) :
                print("La clef tapée ne contient pas exactement 64 bits !\n")
            elif(not checkIfBinaryString(entry)) :
                print("La clef tapée contient autre chose que des 0 et des 1 !\n")
            else :
                return entry
        elif(entry == "2") :
            entry = input("\nTapez le chemin du fichier (en partant du dossier de lancement du script) : ")
            if not os.path.isfile(entry) :
                print("Le fichier de ce nom n'existe pas !\n")
            else :
                f=open(entry, "r", encoding='utf-8-sig')
                txt=f.read()
                if(len(txt) != 64) :
                    print("Le fichier existe mais la clef contenue ne contient pas exactement 64 bits !\n")
                elif not checkIfBinaryString(txt) :
                    print("Le fichier existe mais la clef contenue contient autre chose que des 0 et des 1 !\n")
                else :
                    return txt
        elif(entry == "3") :
            return None
        else :
            print("Les options autorisées sont 1, 2 et 3.\n")

# Appelle les méthodes qui récupéreront auprès de l'utilisateur
# le texte à crypter/décrypter et la clef ; retourne (None, None)
# si une erreur est survenue
def askForTextAndKey(cType) :
    text = askForText(cType)
    if text is None :
        return (None, None)
    key = askForKey()
    if key is None :
        return (None, None)
    return (text, key)

# Demande à l'utilisateur ou il veut que le résultat du traitement
# s'affiche, puis retourne 0 pour console, une string pour le nom du fichier
# ou None si il veut annuler
def askForOutput() :
    while(True) :
        entry = input("\nVoulez-vous afficher la sortie dans la console (1), ou bien dans un fichier de sortie (2) ? Retour : (3)\n")
        if(entry == "1") :
            return 0
        elif(entry == "2") :
            entry = input("\nTapez le nom du fichier à créer ou remplacer qui contiendra la sortie : ")
            if(len(entry) == 0) :
                print("Veuillez taper un nom de fichier valide !\n")
            else :
                return entry
        elif(entry == "3") :
            return None
        else :
            print("Les options autorisées sont 1, 2 et 3.\n")

# Affiche à l'utilisateur le résultat du traitement selon
# ses préférences : dans la console ou dans un fichier
def displayToUser(txtAfterTreatment) :
    output = askForOutput()
    if (output is None) : return
    elif (output == 0) :
        print(txtAfterTreatment)
    else :
        f=open(output,"w+", encoding='utf-8')
        f.write(txtAfterTreatment)
        
# Demande l'action principale à l'utilisateur (chiffre, déchiffrer ou quitter) et
# appelle les traitements selon ce qu'il choisira
def askForMainAction() :
    entry = input("\nVoulez-vous chiffrer (1) ou déchiffrer (2) ? Quitter : (3)\n")
    (text, key) = (None, None)
    
    if(entry == "1") :
        (text, key) = askForTextAndKey("chiffrer")
        if text is None or key is None : return
        displayToUser(encryptRealMessage(text, key))
    elif(entry == "2") :
        (text, key) = askForTextAndKey("déchiffrer")
        if text is None or key is None : return
        displayToUser(decryptRealMessage(text, key))
    elif(entry == "3") :
        exit()
    else :
        print("Les options autorisées sont 1, 2 et 3.\n")

# Méthode d'entrée de l'application
def interface() :
    while(True) :
        askForMainAction()
        
interface()