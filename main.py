from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn import svm
from sklearn import tree
from scipy import spatial
from sys import argv
import argparse
import numpy  as np

class OCR:
	def __init__(self, trainningFile, testFile):
		self.trainningFile = trainningFile[:-4]
		self.testFile = testFile[:-4]

	# Separa características e rotúlos em diferentes arquivos
	def separateFiles(self, trainningFile, testFile):	
		with open(trainningFile, 'r') as file:
			labels = []
			characteristics = []
			data = np.loadtxt(file)
			for line in data:
				labels.append(line[len(data[0])-1])			
			for line in data:
				characteristics.append(line[:-1])	
			np.savetxt(self.trainningFile+'_labels.txt', labels)
			np.savetxt(self.trainningFile+'_characteristics.txt', characteristics)	
		with open(testFile, 'r') as file:
			labels = []
			characteristics = []						
			data = np.loadtxt(file)
			for line in data:
				labels.append(line[len(data[0])-1])			
			for line in data:
				characteristics.append(line[:-1])	
			np.savetxt(self.testFile+'_labels.txt', labels)
			np.savetxt(self.testFile+'_characteristics.txt', characteristics)
	
	# Extrai os dados do arquivo e retorna uma matriz
	def extract(self, fileName):
		with open(fileName) as file:
			data = np.loadtxt(file)
		return data

	def knn(self, trainning_characteristics, trainning_labels ,test_characteristics):
		neigh = KNeighborsClassifier(n_neighbors=arg_parser.k)
		neigh.fit(trainning_characteristics, trainning_labels)

		classified = neigh.predict(test_characteristics)
		prob = neigh.predict_proba(test_characteristics)
		
		return classified
	
	def svm(self, trainning_characteristics, trainning_labels, test_characteristics):
		clf = svm.SVC(gamma=0.0001, C=100)
		x = trainning_characteristics
		y = trainning_labels
		clf.fit(x, y)
		classified = clf.predict(test_characteristics)
		
		return classified

	def decision_tree(self, trainning_characteristics, trainning_labels, test_characteristics):
		x = trainning_characteristics
		y = trainning_labels
		clf = tree.DecisionTreeClassifier()
		clf = clf.fit(x, y)
		classified = clf.predict(test_characteristics)
		
		return classified

	def buildConfusionMatrix(self, classified, test_labels):	
		confusionMatrix = confusion_matrix(test_labels, classified)
		return confusionMatrix

		


if __name__ == '__main__':
	# Define argumentos para execução do programa
	arg_parser = argparse.ArgumentParser()
	arg_parser.add_argument("trainning_file", help="arquivo de treinamento")
	arg_parser.add_argument("test_file", help="arquivo de teste")
	arg_parser.add_argument("k", type=int, help="numero k")
	arg_parser = arg_parser.parse_args()

	ocr = OCR(arg_parser.trainning_file, arg_parser.test_file)

	ocr.separateFiles(arg_parser.trainning_file, arg_parser.test_file)

	trainningLabelsFile = arg_parser.trainning_file[:-4]+'_labels.txt'
	trainningCharacteristicsFile = arg_parser.trainning_file[:-4]+'_characteristics.txt'	

	trainning_labels = ocr.extract(trainningLabelsFile)
	trainning_characteristics = ocr.extract(trainningCharacteristicsFile)

	testLabelsFile = arg_parser.test_file[:-4]+'_labels.txt'
	testCharacteristicsFile = arg_parser.test_file[:-4]+'_characteristics.txt'

	test_labels = ocr.extract(testLabelsFile)
	test_characteristics = ocr.extract(testCharacteristicsFile)

	classified = ocr.decision_tree(trainning_characteristics, trainning_labels, test_characteristics)

	matrix = ocr.buildConfusionMatrix(classified, test_labels)

	for i in matrix:
		print(i)

	accuracy = accuracy_score(test_labels, classified)
	
	print("Acuracia: ", accuracy)