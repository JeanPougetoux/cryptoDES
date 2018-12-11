import ConvAlphaBin
import Extract_ConstantesDES

from ConvAlphaBin import conv_bin
from Extract_ConstantesDES import recupConstantesDES

const = recupConstantesDES()

def readKey(path) :
    f=open(path, "r")
    txt=f.read()
    f.close()
    
    key=dict()
    
    j=0
    
    for i in range (0, len(txt)) :
        # if(i!=0 and (i+1)%8==0) : continue
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

def getSubKeys(keyPath) :
    originalKey = readKey(keyPath)
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
    
def ronde(left, right, key) :
    newRight = permute2Matrix(right, const["E"][0])
    newRight = orOperation(newRight, key)
    
    subBlocs = getSubBlocs(newRight)
    
    for i in range(0, len(subBlocs)) :
        subBlocs[i]=processBloc(subBlocs[i], const["S"+str(i+1)])
    
    return("", "")
    

def encryptBinaryMessage(binaryString, keyPath) :
    subKeys = getSubKeys(keyPath)
    packets = getPacketsFromBinaryString(binaryString)
    
    for i in range(0, len(packets)) :
        packets[i] = permute2Matrix(packets[i], const["PI"][0])
        (left, right) = splitKey(packets[i]) 
        #for j in range(0, 1) :
        (nleft, nright) = ronde(left, right, subKeys[1])
        
    return packets

packets = encryptBinaryMessage("1101110010111011110001001101010111100110111101111100001000110010100111010010101101101011111000110011101011011111", "key.txt")
            
