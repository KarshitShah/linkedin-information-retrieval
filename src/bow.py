
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans
import re

def main():
	document1 = ''
	document2 = ''
	sentences = []
	with open('Fabiola.txt','r',encoding='utf8') as book1:
		with open('EagleCliff.txt','r', encoding='utf8') as book2:

			document1 = book1.read()
			document2 = book2.read()
			document = document1+document2
			sentences = re.split('\.',document)
	#print(sentences)
	tfidf = TfidfVectorizer(use_idf=True, 
                        smooth_idf=False, min_df=10,  
                        ngram_range=(1,1),stop_words='english')
	data = tfidf.fit_transform(sentences)
	dataframe=pd.DataFrame(data.toarray(),columns=tfidf.get_feature_names())
	print(dataframe)
	model = KMeans(n_clusters=2,max_iter=100).fit(dataframe)

	lines_for_predicting = ["But one journey of in Italy, France, EagleCliff to be Bible the journey from earth towards heaven", "EagleCliff"]
	output = model.predict(tfidf.transform(lines_for_predicting))
	print(output)
	#print(data)




if __name__=='__main__':
	main()