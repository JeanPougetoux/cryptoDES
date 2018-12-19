import ConvAlphaBin
import Extract_ConstantesDES

from ConvAlphaBin import conv_bin
from ConvAlphaBin import nib_vnoc
from Extract_ConstantesDES import recupConstantesDES

const = recupConstantesDES()

# Convertit un nombre décimal en une chaîne binaire sur 4 caractères
def decimalToBinary(n):
    return bin(n).replace("0b","").zfill(4)

# Convertit un texte (binaire) en dictionnaire de chiffre
# exemple : "01" -> {0: "0", 1: "1"}
def convertStringToDict(txt) :    
    res=dict()

    for i in range (0, len(txt)) :
        res[i]=int(txt[i])
    
    return res

# Permute une matrice avec une autre matrice de permutation
def permuteTwoMatrix(matrix, permuteMatrix) :
    permuted=dict()
    
    for i in range (0, len(permuteMatrix)) :
        permuted[i]=matrix[permuteMatrix[i]]
        
    return permuted
    
# Sépare un dictionnaire en deux autres dictionnaires (left et right)
def splitDict(key) :
    length = len(key)
    halfLength = length / 2
    
    left = dict()
    right = dict()
    
    for i in range (0, length) :
        if(i < halfLength) :
            left[i] = key[i]
        else :
            right[i % halfLength] = key[i]
            
    return left, right

# Concatène deux dictionnaires en un seul dictionnaire
def concatenateDicts(dictLeft, dictRight) :
    res = dict()
    index = 0
    
    for i in range(0, len(dictLeft)) :
        res[index] = dictLeft[i]
        index+=1
        
    for i in range(0, len(dictRight)) :
        res[index] = dictRight[i]
        index+=1
        
    return res
    
# Déplace tous les éléments vers la gauche (met à jour les index)
# exemple : {0:"1", 1:"2", 2:"3"} -> {0:"2", 1:"3", 2:"1"}
def shiftLeft(originalDict) :
    res = dict()
    
    for i in range(0, len(originalDict)) :
        j = i - 1
        if j == -1 :
            j = len(originalDict) - 1
        res[j] = originalDict[i]
        
    return res

# Effectue le traitement permettant de récupérer les 16 sous-clés 
# (à partir de la clé au format string)
def getSubKeys(txt) :
    originalKey = convertStringToDict(txt)
    originalPermutedKey = permuteTwoMatrix(originalKey, const["CP_1"][0])
    
    subKeys = dict()
    (left, right) = splitDict(originalPermutedKey)
    
    for i in range(1, 17) :
        left = shiftLeft(left)
        right = shiftLeft(right)
        tempKey = concatenateDicts(left, right)
        permutedTempKey = permuteTwoMatrix(tempKey, const["CP_2"][0])
        subKeys[i] = permutedTempKey
    
    return subKeys
    
# Va faire à partir d'une string binaire des paquets (dictionnaire) 
# de 64 bits, complètera le dernier par des 0
def getPacketsFromBinaryString(binaryString) :
    packets = dict()
    index = -1
    
    for i in range(0, len(binaryString)) :
        if(i == 0 or i % 64 == 0) :
            index+=1
            packets[index] = dict()
        packets[index][i % 64] = binaryString[i]
    
    numbPackets = len(packets)
    lenLastPacket = len(packets[numbPackets - 1])
    
    if(lenLastPacket != 64) :
        for i in range (lenLastPacket, 64) :
            packets[numbPackets - 1][i] = 0
        
    return packets

# Ou exclusif sur deux matrices, renvoie la nouvelle matrice
def orOperation(matrix, otherMatrix) :
    newMatrix = dict()
    
    for i in range(0, len(matrix)) :
        res = int(matrix[i]) + int(otherMatrix[i])
        if(res > 1) :
            res = 0
        newMatrix[i] = res
    
    return newMatrix
        
# Sépare une matrice en sous-matrices contenant chacune 6 éléments (similaire
# à getPackets mais sur une matrice, avec seulement des paquets de 6 et sans 
# complétion des 0 à la fin)
def getSubBlocs(matrix) :
    subBlocs = dict()
    index = 0
    subBlocs[index]=dict()
    
    for i in range(0, len(matrix)) :
        if i!=0 and (i)%6==0 :
            index+=1
            subBlocs[index]=dict()
            
        subBlocs[index][i%6] = matrix[i]
    return subBlocs

# Effectue le traitement sur chaque bloc lors des rondes et décrit dans le cours (Rondes.3)
def processBloc(bloc, s) :
    line=int(str(bloc[0])+str(bloc[5]), 2)
    tempColumn = ""
    for i in range(1, 5) :
        tempColumn+=str(bloc[i])
    column=int(tempColumn, 2)
    
    numb=decimalToBinary(s[line][column])
    
    dictBloc = dict()
    
    for i in range(0, len(numb)) :
        dictBloc[i]=numb[i]
    
    return dictBloc

# Traitement correspondant à une ronde dans le cours, il y en aura 16
def ronde(left, right, key) :
    newRight = permuteTwoMatrix(right, const["E"][0])
    newRight = orOperation(newRight, key)
    
    subBlocs = getSubBlocs(newRight)
    
    for i in range(0, len(subBlocs)) :
        subBlocs[i]=processBloc(subBlocs[i], const["S"][i])
        
    newRight = dict()
    indexRight = 0
    
    for i in range(0, len(subBlocs)) :
        for j in range(0, len(subBlocs[i])) :
            newRight[indexRight] = subBlocs[i][j]
            indexRight+=1
            
    newRight = permuteTwoMatrix(newRight, const["PERM"][0])
    newRight = orOperation(newRight, left)
    
    return(right, newRight)

# Traitement permettant de "défaire" une ronde et de récupérer les parties
# gauche et droite originelles
def unRonde(left, right, key) :
    oldComputedRight = permuteTwoMatrix(left, const["E"][0])
    oldComputedRight = orOperation(oldComputedRight, key)
    
    subBlocs = getSubBlocs(oldComputedRight)
    
    for i in range(0, len(subBlocs)) :
        subBlocs[i]=processBloc(subBlocs[i], const["S"][i])
    
    oldComputedRight = dict()
    indexRight = 0
    
    for i in range(0, len(subBlocs)) :
        for j in range(0, len(subBlocs[i])) :
            oldComputedRight[indexRight] = subBlocs[i][j]
            indexRight+=1
    
    oldComputedRight = permuteTwoMatrix(oldComputedRight, const["PERM"][0])
    oldLeft = orOperation(right, oldComputedRight)
    
    return (oldLeft, left)
    
# Crypte une string binaire grâce à une clef
def encryptBinaryMessage(binaryString, key) :
    subKeys = getSubKeys(key)
    packets = getPacketsFromBinaryString(binaryString)
    s = ""
    
    for i in range(0, len(packets)) :
        packets[i] = permuteTwoMatrix(packets[i], const["PI"][0])
        (left, right) = splitDict(packets[i]) 
        
        for j in range(0, 16) :
            (left, right) = ronde(left, right, subKeys[j+1])
        
        packets[i] = concatenateDicts(left, right)
        packets[i] = permuteTwoMatrix(packets[i], const["PI_I"][0])
        
        for j in range(0, len(packets[i])) :
            s+=str(packets[i][j])
    return nib_vnoc(s)

# Décrypte une string binaire grâce à une clef
def decryptBinaryMessage(binaryString, key) :
    subKeys = getSubKeys(key)
    packets = getPacketsFromBinaryString(binaryString)
    s = ""
    
    for i in range(0, len(packets)) :
        packets[i] = permuteTwoMatrix(packets[i], const["PI"][0])
        (oldLeft, oldRight) = splitDict(packets[i])
        
        for j in range(0, 16) :
            (oldLeft, oldRight) = unRonde(oldLeft, oldRight, subKeys[16-j])
        
        packets[i] = concatenateDicts(oldLeft, oldRight)
        packets[i] = permuteTwoMatrix(packets[i], const["PI_I"][0])
        
        for j in range(0, len(packets[i])) :
            s+=str(packets[i][j])
    return nib_vnoc(s)
        
# Décrypte une string grâce à une clef (la convertit 
# en binaire et appelle decryptBinaryMessage)
def decryptRealMessage(message, key) :
    binary = conv_bin(message)
    return decryptBinaryMessage(binary, key)

# Crypte une string grâce à une clef (la convertit 
# en binaire et appelle encryptBinaryMessage)
def encryptRealMessage(message, key) :
    binary = conv_bin(message)
    return encryptBinaryMessage(binary, key)


