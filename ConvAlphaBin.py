		
#####################################################
#		   	 	DICTIONNAIRE BINAIRE				#
#####################################################

ALPHABET = ""
ALPHABET +="ABCDEFGHIJKLMNOPQRSTUVWXYZ"#Les 26 lettres de l'alphabet en majuscule
ALPHABET +="abcdefghijklmnopqrstuvwxyz"#Les 26 lettres de l'alphabet en minuscule
ALPHABET+=" " #caractère 53
ALPHABET+="." #caractère 54
ALPHABET+="," #caractère 55
ALPHABET+="!" #caractère 56
ALPHABET+="?" #caractère 57
ALPHABET+="'" #caractère 58
ALPHABET+='"' #caractère 59
ALPHABET+="é" #caractère 60
ALPHABET+="è" #caractère 61
ALPHABET+="à" #caractère 62
ALPHABET+="-" #caractère 63
ALPHABET+="\n" #caractère 64

ALPHABETBINAIRE=dict()
for i in range(0, 64) :
	x=bin(i)
	y='0000'+x[2:]
	ALPHABETBINAIRE[i]=y[-5]+y[-4]+y[-3]+y[-2]+y[-1]


#Renvoie a chaine de caractère txt avec uniquement les caractères de l'alphabet.
def FiltreTXT(txt) :
	res=""
	for c in txt :
		if(ALPHABET.find(c)!=-1) : res+=c
		elif(c=='ê' or c=='ë') : res+='e'
		elif(c=='â') : res+='a'
		elif(c=='ç') : res+='c'
		elif(c=='î') : res+='i'
		elif(c=='Ç') : res+='C'
		elif(c=='ù' or c=="û") : res+='u'
		elif(c=='ô') : res+='o'
		elif(c=='Ô') : res+='O'
		elif(c=='œ') : res+='oe'
		elif(c=="À") : res+='A'
		elif(c=="È" or c=="É") : res+='E'
	return res
	
#prend en paramètre un texte et renvoie la chaine binaire associée (en suivant le dictionnaire)
def conv_bin(txt) :
	X=""
	for c in FiltreTXT(txt) : X+=ALPHABETBINAIRE[ALPHABET.find(c)]
	return X


	