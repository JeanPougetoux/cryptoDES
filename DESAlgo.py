import ConvAlphaBin
import Extract_ConstantesDES

from ConvAlphaBin import conv_bin
from ConvAlphaBin import conv_text
from Extract_ConstantesDES import recupConstantesDES

const = recupConstantesDES()

def decimalToBinary(n):
    return bin(n).replace("0b","").zfill(4)

def readKey(txt) :    
    key=dict()
    
    j=0
    
    for i in range (0, len(txt)) :
        key[j]=int(txt[i])
        j+=1
    
    return key
    
    
    
    
def permute2Matrix(matrix, permuteMatrix) :
    permuted=dict()
    
    for i in range (0, len(permuteMatrix)) :
        permuted[i]=matrix[permuteMatrix[i]]
        
    return permuted
    
    
def splitKey(key) :
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
        
    
    
    
    
def concatenateKeys(keyLeft, keyRight) :
    key = dict()
    index = 0
    
    for i in range(0, len(keyLeft)) :
        key[index] = keyLeft[i]
        index+=1
        
    for i in range(0, len(keyRight)) :
        key[index] = keyRight[i]
        index+=1
        
    return key
    
def shiftLeft(matrix) :
    newMatrix = dict()
    
    for i in range(0, len(matrix)) :
        j = i - 1
        if j == -1 :
            j = len(matrix) - 1
        newMatrix[j] = matrix[i]
        
    return newMatrix

def getSubKeys(txt) :
    originalKey = readKey(txt)
    originalPermutedKey = permute2Matrix(originalKey, const["CP_1"][0])
    
    subKeys = dict()
    (left, right) = splitKey(originalPermutedKey)
    
    for i in range(1, 17) :
        left = shiftLeft(left)
        right = shiftLeft(right)
        tempKey = concatenateKeys(left, right)
        permutedTempKey = permute2Matrix(tempKey, const["CP_2"][0])
        subKeys[i] = permutedTempKey
    
    return subKeys
    


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

def orOperation(matrix, otherMatrix) :
    newMatrix = dict()
    
    for i in range(0, len(matrix)) :
        res = int(matrix[i]) + int(otherMatrix[i])
        if(res > 1) :
            res = 0
        newMatrix[i] = res
    
    return newMatrix

def reverseOrOperation(finalMatrix, oldMatrix) :
    newMatrix = dict()
    
    for i in range(0, len(finalMatrix)) :
        res = int(finalMatrix[i]) - int(oldMatrix[i])
        res = res**2
        newMatrix[i] = res
    return newMatrix
        

        
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
def ronde(left, right, key) :
    newRight = permute2Matrix(right, const["E"][0])
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
            
    newRight = permute2Matrix(newRight, const["PERM"][0])
    newRight = orOperation(newRight, left)
    
    return(right, newRight)

def unRonde(left, right, key) :
    oldComputedRight = permute2Matrix(left, const["E"][0])
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
            
    oldComputedRight = permute2Matrix(oldComputedRight, const["PERM"][0])
    oldLeft = reverseOrOperation(right, oldComputedRight)
    
    return (oldLeft, left)
    
    

def encryptBinaryMessage(binaryString, key) :
    subKeys = getSubKeys(key)
    packets = getPacketsFromBinaryString(binaryString)
    s=""
    
    for i in range(0, len(packets)) :
        packets[i] = permute2Matrix(packets[i], const["PI"][0])
        (left, right) = splitKey(packets[i]) 
        
        for j in range(0, 16) :
            (left, right) = ronde(left, right, subKeys[j+1])
        
        packets[i] = concatenateKeys(left, right)
        packets[i] = permute2Matrix(packets[i], const["PI_I"][0])
        
        for j in range(0, len(packets[i])) :
            s+=str(packets[i][j])
    return s

def decryptBinaryMessage(binaryString, key) :
    subKeys = getSubKeys(key)
    packets = getPacketsFromBinaryString(binaryString)
    s=""
    
    for i in range(0, len(packets)) :
        packets[i] = permute2Matrix(packets[i], const["PI"][0])
        (oldLeft, oldRight) = splitKey(packets[i])
        for j in range(0, 16) :
            (oldLeft, oldRight) = unRonde(oldLeft, oldRight, subKeys[16-j])
        
        packets[i] = concatenateKeys(oldLeft, oldRight)
        packets[i] = permute2Matrix(packets[i], const["PI_I"][0])
        for j in range(0, len(packets[i])) :
            s+=str(packets[i][j])
    return conv_text(s)
        
    

    
    

def encryptRealMessage(message, key) :
    binary = conv_bin(message)
    return encryptBinaryMessage(binary, key)