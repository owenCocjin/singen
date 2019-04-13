import sys  #Required!
#--------User's imports--------#
from common import *
import os


'''-------------------+
|        SETUP        |
+-------------------'''
#--------Variables--------#
flags=[]
args=[]

#--------Process sys.argv--------#
#Find flags in sys.argv and save them
for i in sys.argv[1:]:
	#If current arg starts with '-', it's a flag
	if i[0]=='-':
		#If curreng arg starts with '--', its it's own flag
		if i[1]=='-':
			#Add the whole flag
			flags.append(i[2:])
		else:
			#Count each individual char as a flag
			for i in i[1:]:
				flags.append(i)
	else:
		#counts as an argument
		args.append(i)


'''-----------------------+
|        VARIABLES        |
+-----------------------'''


'''-----------------------+
|        FUNCTIONS        |
+-----------------------'''
def n():
	'''Only print valid generated SINs'''
	if 'n' in flags:
		return True  #Meant to be assigned to onlyValid
	else:
		return False  #Meant to be assigned to onlyValid

def g():
	'''Generate SINs'''
	onlyValid=n()
	while True:  #Loop to keep in input
		template=str(input("Enter a SIN number. Fill gaps with 'x':\n     "))
		length=len(template)
		print('\033[F', end='')  #Moves cursor up to previous line
		#Remove any spaces
		spacePos=template.find(' ')
		while spacePos>=0:
			template=template[0:spacePos]+template[spacePos+1:]
			spacePos=template.find(' ')
		#Fill trailing spaces with x
		if len(template)<9:
			template+='x'*(9-len(template))
		#Truncate input
		elif len(template)>9:
			template=template[0:9]

		#Create template
		sin=''
		for i, t in enumerate(template):
			try:
				sin+=str(t)
			except:
				sin+='x'
		template=sin
		template=Sin(template)

		#If 'x's were found, continue
		if 'x' in template.getSIN():
			#Ask if current SIN is good and brute-forces valid SINs
			if input(f"SIN: {template.getSINFormatted()}{' '*length}\nIs this SIN okay?(y/n): ").lower() in "yes":
				brutetheSIN(template, onlyValid)
				break
		else:
			print(f"SIN: {template.getSIN()}\nThe given SIN is complete, so there's nothing to brute-force...")
			break

def v():
	if 'd' in flags:
		[print(verifyDetailed(i)) for i in args]
	else:
		[print(verify(i)) for i in args]
