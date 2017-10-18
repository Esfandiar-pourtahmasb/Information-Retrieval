import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

def draw10dots(word,model):
	words = []
	vectors = []
	colors   = ['#cc3300','#00cc99','#0066cc','#cc0066','#ffb366','#d9ff66','#66ffff','#66b3ff','#b399ff','#ffff99']
	words = model.most_similar(word)
	for word in words:
		vectors.append(model[word[0]])

	X = np.array(vectors)
	pca = PCA(n_components=2)
	points = pca.fit_transform(X)
	area = np.pi * (3)**2  
	x = []
	y = []
	for i in range(len(words)):
		x.append(points[i][0])
		y.append(points[i][1])

		plt.scatter(x[i], y[i], s=area, c=colors[i], alpha=0.5, label = words[i][0])
	plt.legend(loc = 2)
	plt.show()
