
from gensim.models import word2vec  
import pickle
import sys

def setup_model(amount, output):
	MODEL_FILE = output
	#start to use word2vec
	sentences = word2vec.Text8Corpus('./trans_files/train_files/'+str(amount)+'.txt')   
	model = word2vec.Word2Vec(sentences, size = 80,window = 3)  #size = 80, window = 3, parameters can be changed 
	pickle.dump(model, open('./trans_files/models/'+MODEL_FILE, 'wb'))
	model = pickle.load(open('./trans_files/models/'+MODEL_FILE, 'rb'))
	print("Finish Loading Model!")
	return model
