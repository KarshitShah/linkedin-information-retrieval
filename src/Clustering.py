import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.cluster import KMeans
import re,os
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from sklearn.metrics import silhouette_score


lists=[]
Model=None
TFIDF_score=None

def listAllDocs(file):
    path = "./Docs2/" + file
    tokens = re.split('[\' \" ., \n \\ /;:-]', open(path, 'r',  encoding='utf-8',
                 errors='ignore').read().lower())
    sentence=' '.join(tokens)
    sentence=sentence.strip()
    lists.append(sentence)
    return tokens

def processTrainingData():
    files = os.listdir("./Docs2")
    for i in range(len(files)):
            tokens = listAllDocs(files[i])
    print(lists)

def classify_profile_cluster(profile):
    profile_data = ""
    driver = webdriver.Firefox(executable_path='../geckodriver')
    driver.get(profile)
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    
    title = soup.find('h2', { "class" : "top-card-layout__headline" })
    profile_data += title.getText()
    profile_data += " "

    summary = soup.find('p')
    profile_data += summary.getText()
    profile_data += " "

    experiences = soup.find_all('div', {"class": "result-card__contents experience-item__contents" })
    for experience in experiences:
        profile_data += experience.getText()
        profile_data += " "

    universities = soup.find_all('h3', {"class": "result-card__title"})
    for university in universities:
        profile_data += university.getText()
        profile_data += " "

    degrees = soup.find_all('h3', {"class": "result-card__subtitle"})
    for degree in degrees:
        profile_data += degree.getText()
        profile_data += " "

    projects = soup.find_all('li', {"class": "result-card personal-project"})
    for project in projects:
        profile_data += project.getText()
        profile_data += " "
        
    return profile_data

def buildModel(n_clusters=5, max_iters=1000):
    
    tfidf = TfidfVectorizer(use_idf=True, smooth_idf=False, min_df=10, ngram_range=(1,1),stop_words='english')
    data = tfidf.fit_transform(lists)
    dataframe=pd.DataFrame(data.toarray(),columns=tfidf.get_feature_names())
    model = KMeans(n_clusters=5,max_iter=100).fit(dataframe)
    
    print('Printing the accuracy of the model : ')
    clusterer = KMeans(n_clusters=5,max_iter=1000)
    preds = clusterer.fit_predict(dataframe)
    score = silhouette_score(dataframe, preds)
    print(score)
    return model, tfidf


def predict(lines_for_predicting, model=Model, tfidf=TFIDF_score):
    # lines_for_predicting=[lists[300], lists[110], lists[150]]
    # predicting output labels :
    output = model.predict(tfidf.transform(lines_for_predicting))
    print(output)
    return output


def driver():
    processTrainingData()
    print(lists)
    model, tfidf=buildModel()
    Model=model
    TFIDF_score=tfidf
    # uncomment the following lines in order to run this as a normal python program

    # profile_data=classify_profile_cluster('https://www.linkedin.com/in/kedar-nadkarni/')
    # lines_for_predicting=[profile_data]
    # predict(Model, TFIDF_score, lines_for_predicting)

## uncomment the following lines and the above driver methods lines in order to run this as a normal program

# if __name__=='__main__':
#     processTrainingData()
#     print(lists)
#     model, tfidf=buildModel()
#     profile_data=classify_profile('https://www.linkedin.com/in/kedar-nadkarni/')
#     lines_for_predicting=[profile_data]
#     predict(model, tfidf, lines_for_predicting)






