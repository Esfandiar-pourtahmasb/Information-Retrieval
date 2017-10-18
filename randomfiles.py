from numpy.random import choice
import convertHTML
import os
#choose fix number of files randomly and train them
def choose_file(source, amount):
	txtfiles = os.listdir('./'+source)
	size = amount
	result = choice(txtfiles, size = int(amount))
	for allDir in result:
		convertHTML.html2txt_save_one('./'+source, allDir)
		child = os.path.join('./trans_files/ori_files', allDir.replace(".html",".txt"))
		txt = open(child, 'r',encoding='utf-8').read()
		f = open('./trans_files/train_files/'+str(size)+'.txt','a',encoding = 'utf-8')
		f.write(txt)
		f.close()