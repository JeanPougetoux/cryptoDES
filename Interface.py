import os.path
import DESAlgo

from DESAlgo import encryptRealMessage
from DESAlgo import decryptBinaryMessage

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
                f=open(entry, "r")
                txt=f.read()
                if(len(txt) == 0) :
                    print("Le fichier existe mais ne contient aucun caractère !\n")
                else :
                    return txt
        elif(entry == "3") :
            return None
        else :
            print("Les options autorisées sont 1, 2 et 3.\n")
            
def askForKey() :
    while(True) :
        entry = input("\nVoulez-vous taper la clef (1), ou bien donner le chemin d'un fichier la contenant (2) ? Retour : (3)\n")
        if(entry == "1") :
            entry = input("Tapez la clef : ")
            if(len(entry) != 64) :
                print("La clef tapée ne contient pas exactement 64 bits !\n")
            else :
                return entry
        elif(entry == "2") :
            entry = input("\nTapez le chemin du fichier (en partant du dossier de lancement du script) : ")
            if not os.path.isfile(entry) :
                print("Le fichier de ce nom n'existe pas !\n")
            else :
                f=open(entry, "r")
                txt=f.read()
                if(len(txt) != 64) :
                    print("Le fichier existe mais la clef contenu ne contient pas exactement 64 bits !\n")
                else :
                    return txt
        elif(entry == "3") :
            return None
        else :
            print("Les options autorisées sont 1, 2 et 3.\n")
        
def askForTextAndKey(cType) :
    text = askForText(cType)
    if text is None :
        return (None, None)
    key = askForKey()
    if key is None :
        return (None, None)
    return (text, key)

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
            
def displayToUser(txtAfterTreatment) :
    output = askForOutput()
    if (output is None) : return
    elif (output == 0) :
        print(txtAfterTreatment)
    else :
        f=open(output,"w+")
        f.write(txtAfterTreatment)
        
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
        displayToUser(decryptBinaryMessage(text, key))
    elif(entry == "3") :
        exit()
    else :
        print("Les options autorisées sont 1, 2 et 3.\n")

def interface() :
    while(True) :
        askForMainAction()
        
interface()