#The main program is to validate the command format, then train model with data, and finally save the model to the local path for future use.
import sys
import os
import randomfiles
import convertHTML
import trainmodel
import showdots
import matplotlib
# =============
# validate the format of command
def validate(source, amount, output):	#validate the whole command
	validate_source(source)
	validate_amount(source, amount)
	validate_output(output)

def validate_source(source):			#validate source part
	if os.path.isdir('./'+source):
		validate_file(source)
	else:
		print("No such a file called", source, '!')
		exit()

def validate_file(source):				#validate the source's suffix
	ls = os.listdir('./'+source)
	for allDir in ls:
		if allDir.endswith('.html') or allDir.endswith('.DS_Store'):
			pass
		else:
			print('Files in the path have wrong suffix!')
			print(ls)
			exit()

def validate_amount(source, amount):	#validate the amount part
	amount = eval(amount)
	totalamount = len(os.listdir('./'+source))
	if type(amount) != int:
		print("Please type an integer!")
		exit()
	
	elif amount > totalamount:
		print("There is only %d files in the path!"%totalamount)
		exit()

def validate_output(output):			#validate the suffix of output model
	if output.endswith(".model"):
		pass
	else:
		print("The output file must be a model!")
		exit()

# ================================
# Train
def converthtml(source, amount):
	randomfiles.choose_file(source, amount)

def train_model(amount, output):
	model = trainmodel.setup_model(amount, output)
	return model

def draw_plots(word, model):
	showdots.draw10dots(word,model)

def train(source,amount):
	converthtml(source, amount)
	model = train_model(amount,output)
	return model

# ==================================
# main
if len(sys.argv) != 4:
	print("Wrong format! Please read readme.txt to get info.")
	exit()
source = sys.argv[1]
amount = sys.argv[2]
output = sys.argv[3]
validate(source, amount, output)
print("Start training...")
model = train(source,amount)
word = input('Input a word: ')
draw_plots(word, model)
matplotlib.pyplot.savefig('./trans_files/pictures/'+output.replace(".model",'')+word+'.png')

