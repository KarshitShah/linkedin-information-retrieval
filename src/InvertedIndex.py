import csv
import os
import re

stopwords = []
termList = []
docLists = {}

def create_docs():
	with open('Datasets/SoftwareEngineers.csv', "r") as f:
	    i = 0
	    for row in f:
	        file = "Docs/Software Engineers/SoftwareEngineer" + str(i) + ".txt"
	        output = open(file, 'w')
	        output.write(row)
	        i += 1


def get_stopwords():
	with open('stopwords.txt') as sw:
		for line in sw:
			word = line.split()
			stopwords.append(word[0])


def parse(file):
	if "SoftwareEngineer" in file:
		file_name = "Docs/Software Engineers/" + file
	elif "ElectricalEngineer" in file:
		file_name = "Docs/Electrical Engineers/" + file
	elif "MechanicalEngineer" in file:
		file_name = "Docs/Mechanical Engineers/" + file
	elif "Recruiter" in file:
		file_name = "Docs/Recruiters/" + file
	elif "BusinessAnalyst" in file:
		file_name = "Docs/Business Analysts/" + file
	tokens = re.split('[\' \" ., \n \\ /;:-]', open(file_name, 'r').read().lower())
	return tokens

def inverted_index():
	files = os.listdir("Docs/Recruiters")
	files.extend(os.listdir("Docs/Software Engineers"))
	files.extend(os.listdir("Docs/Electrical Engineers"))
	files.extend(os.listdir("Docs/Mechanical Engineers"))
	files.extend(os.listdir("Docs/Business Analysts"))
	
	for i in range(len(files)):
		tokens = parse(files[i])
		for token in tokens:
			if token not in stopwords and token != "":

				if token not in termList:
					termList.append(token)
					docList = [files[i]]
					docLists[token] = docList
				else:
					index = termList.index(token)
					docList = docLists[token]
					if i not in docList:
						docList.append(files[i])
						docLists[token] = docList

def intersect(doc_lists):
    res_list = doc_lists[0]
    for list_t in doc_lists:
        temp_doc=[]
        for docs in list_t:
            if docs in res_list:
                temp_doc.append(docs)
        res_list=temp_doc
    return set(res_list)


def get_results(queries):
	lists=[]
	for query in queries:
		if query in docLists.keys():
			list_t = docLists[query]
			lists.append(list_t)
	files = intersect(lists)

	result = {}
	i = 0

	for file in files:
		if "SoftwareEngineer" in file:
			file_name = "Docs/Software Engineers/" + file
		elif "ElectricalEngineer" in file:
			file_name = "Docs/Electrical Engineers/" + file
		elif "MechanicalEngineer" in file:
			file_name = "Docs/Mechanical Engineers/" + file
		elif "Recruiter" in file:
			file_name = "Docs/Recruiters/" + file
		elif "BusinessAnalyst" in file:
			file_name = "Docs/Business Analysts/" + file
		values = open(file_name).read().split(',')
		result[i] = values[1] + "-;" + values[3] + "-;" + values[6]
		i += 1
	return result
