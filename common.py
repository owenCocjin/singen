#!/usr/bin/python3
'''-----------------------+
|        FUNCTIONS        |
+-----------------------'''
def brutetheSIN(sin, onlyValid=False):  #Make it recursive!
	#Base case
	if sin.getSIN().count('x')==1:
		xPos=sin.getSIN().index('x')
		for i in range(10):
			sin.setSIN(i, xPos)

			#If onlyValid flag is set, only pring valid SINs
			if onlyValid:
				if sin.validate()[0]:
					print(verify(sin.getSIN()))
			else:
				print(verify(sin.getSIN()))
		sin.setSIN('x', xPos)
		return sin

	else:
		xPos=sin.getSIN().index('x')
		for i in range(10):
			sin.setSIN(i, xPos)
			brutetheSIN(sin, onlyValid)
		sin.setSIN('x', xPos)
		return sin

def error(location, message="Unknown Error", code=-1):
	print(f"\033[31m[\033[34m|\033[31mX]\033[0m({location}): {message}")
	if code<=0:
		exit(code)

def verify(sin):
	'''Returns a formatted SIN, saying if it is valid or not'''
	curSIN=Sin(sin)
	valid, total=curSIN.validate()
	toReturn=f"{curSIN.getSINFormatted(False)} -> "

	#Return incomplete
	if not valid and total==False:
		toReturn+=("\033[33mIncomplete!")
	#Return valid
	elif valid:
		toReturn+=("\033[32mValid!")
	#Return invalid
	elif not valid and total%10!=0:
		toReturn+=("\033[31mInvalid!")
	toReturn+=('\033[0m')
	return toReturn

def verifyDetailed(sin):
	toReturn="==============================\n"
	curSIN=Sin(sin)
	toReturn+=f"{curSIN}\n=============================="
	return toReturn


'''---------------------+
|        CLASSES        |
+---------------------'''
class Sin():
	provinces=[
		["CRA-assigned to tax payers without a SIN"],
		["Nova Scotia", "New Brunswick", "P.E.I.", "Newfoundland & Labrador"],
		["Quebec"],
		["Quebec"],
		["Ontario"],
		["Ontario"],
		["Northwestern Ontario", "Manitoba", "Saskatchewan", "Alberta", "Northwest Territories", "Nunavut"],
		["British Columbia", "Yukon"],
		["Unused"],
		["Temporary Residence"]
		]
	def __init__(self, number=''):
		self.number={
		0:8,
		1:'x',
		2:'x',
		3:'x',
		4:'x',
		5:'x',
		6:'x',
		7:'x',
		8:'x'
		}
		if 0<len(str(number))<=9:
			for i, n in enumerate(number):
				try:
					self.number[i]=int(n)
				except:
					self.number[i]='x'
		try:
			self.provinces=Sin.provinces[int(self.number[0])]
		except:
			self.provinces=Sin.provinces[8]

	def __str__(self):
		#Variables
		provs='\n'
		sin=''
		#Print Provinces
		for i in self.provinces:
			provs+='\t- '+i+'\n'
		#Set SIN
		for i in range(9):
			if i%3==0:
				sin+=' '
			sin+="{}{}\033[0m".format(
			(lambda x=str(self.number[i]): "\033[31m" if x=='x' else '')(),
			str(self.number[i]),
			)

		#Determine validity
		valid, total=self.validate()
		#Incomplete
		if not valid and total==False:
			validity=("\033[33mIncomplete!\033[0m")
		#Valid
		elif valid:
			validity=("\033[32mValid!\033[0m")
		#Invalid
		elif not valid and total%10!=0:
			validity=("\033[31mInvalid!\033[0m")
		print('\033[0m', end='')

		return f"\033[1mProvince(s):\033[0m {provs[:-1]}\n\n\033[1mSIN:\033[0m {sin} -> {validity}"

	def getSIN(self):
		toReturn=''
		for i in self.number:
			toReturn+=str(self.number[i])
		return toReturn
	def getSINFormatted(self, fancy=True):
		sin=''
		for i in range(9):
			if i%3==0:
				sin+=' '
			if fancy:
				sin+="{}{}\033[0m".format(
				(lambda x=str(self.number[i]): "\033[31m" if x=='x' else '')(),
				str(self.number[i]),
				)
			else:
				sin+=str(self.number[i])
		return sin.strip()
	def setSIN(self, num, pos=-1):
		num=str(num)  #Can't set each individual digit if num isn't a string
		#if pos is -1, assume num is full SIN
		if pos==-1 and len(num)<=9:
			for i, n in enumerate(num):
				try:
					self.number[i]=n
				except ValueError:
					self.number[i]='x'
					#error("common.setSIN", "{} is invalid!".format(num[i]))
		elif pos==-1 and len(num)>9:
			error("common.setSIN", "Passed SIN is too long!")
		#If pos is valid, set that digit in that position
		elif 0<=pos<=9:
			try:
				self.number[pos]=int(num)
			except ValueError:
				self.number[pos]='x'
		else:
			error("common.setSIN", "Invalid position!")

		#Set province
		try:
			self.provinces=Sin.provinces[int(self.number[0])]
		except:
			self.provinces=Sin.provinces[8]

	def getProvince(self):
		return self.provinces

	def validate(self):
		#Returns False for both return values if SIN number contains 'x'
		#Returns True and total if valid
		#Returns False and total if invalid
		if False in [False for i in self.number if self.number[i]=='x']:
			return False, False

		total=0
		for i in range(9):
			curNumber=str(self.number[i]*((i%2)+1))
			if len(curNumber)>1:
				for i in curNumber:
					total+=int(i)
			else:
				total+=int(curNumber)
		if total%10==0:
			return True, total
		else:
			return False, total
