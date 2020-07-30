import os
import re
import math
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

training_docs = []
training_labels = []
num_classes = 4
class_counts = [0, 0, 0, 0]
class_strings = ["", "", "", ""]
class_token_counts = [0, 0, 0, 0]
cond_prob = {}
vocabulary = set()


def parse(file):
    path = "Docs/" + file
    data = open(path, 'r', encoding= 'unicode_escape').read()
    return data


def preprocess():
    recruiters = os.listdir("Docs/Train Data/Recruiters")
    software_engineers = os.listdir("Docs/Train Data/Software Engineers")
    electrical_engineers = os.listdir("Docs/Train Data/Electrical Engineers")
    mechanical_engineers = os.listdir("Docs/Train Data/Mechanical Engineers")
    business_analysts = os.listdir("Docs/Train Data/Business Analysts")

    for i in range(len(recruiters)):
        training_docs.append(parse("Train Data/Recruiters/" + recruiters[i]))
        training_labels.append(0)
    
    for i in range(len(software_engineers)):
        training_docs.append(parse("Train Data/Software Engineers/" + software_engineers[i]))
        training_labels.append(1)

    for i in range(len(electrical_engineers)):
        training_docs.append(parse("Train Data/Electrical Engineers/" + electrical_engineers[i]))
        training_labels.append(2)

    for i in range(len(mechanical_engineers)):
        training_docs.append(parse("Train Data/Mechanical Engineers/" + mechanical_engineers[i]))
        training_labels.append(3)

    # for i in range(len(business_analysts)):
    #     training_docs.append(parse("Train Data/Business Analysts/" + business_analysts[i]))
    #     training_labels.append(4)


def naive_bayes():
    for i in range(num_classes):
        class_strings.append("")
        cond_prob[i] = {}
    
    for i in range(len(training_labels)):
        class_counts[training_labels[i]] += 1
        class_strings[training_labels[i]] += training_docs[i] + " "

    for i in range(num_classes):
        tokens = class_strings[i].split(" ")
        class_token_counts[i] = len(tokens)

        for token in tokens:
            vocabulary.add(token)
            if token in cond_prob[i].keys():
                count = cond_prob[i][token] + 1
            else:
                cond_prob[i][token] = 1
    
    for i in range(num_classes):
        vocabulary_size = len(vocabulary)
        temp = cond_prob[i]

        for key, value in temp.items():
            token = key
            count = value
            count = (count + 1) / (class_token_counts[i] + vocabulary_size)


def classify(doc):
    label = 0
    vocabulary_size = len(vocabulary)
    score = []

    for i in range(num_classes):
        score.append(math.log((class_counts[i] * 1.0) / len(training_docs)))

    tokens = doc.split(" ")

    for i in range(num_classes):
        for token in tokens:
            if token in cond_prob[i]:
                score[i] += math.log(cond_prob[i][token])
            else:
                score[i] += math.log(1.0 / (class_token_counts[i] + vocabulary_size))

    max_score = score[0]

    for i in range(len(score)):
        if score[i] > max_score:
            label = i
            max_score = score[i]
    print(label)
    return label


def test_accuracy():
    recruiters = os.listdir("Docs/Test Data/Recruiters")
    software_engineers = os.listdir("Docs/Test Data/Software Engineers")
    electrical_engineers = os.listdir("Docs/Test Data/Electrical Engineers")
    mechanical_engineers = os.listdir("Docs/Test Data/Mechanical Engineers")
    business_analysts = os.listdir("Docs/Test Data/Business Analysts")

    test_labels = []
    result_labels = []

    for i in range(len(recruiters)):
        result_labels.append(classify(parse("Test Data/Recruiters/" + recruiters[i])))
        test_labels.append(0)
    
    for i in range(len(software_engineers)):
        result_labels.append(classify(parse("Test Data/Software Engineers/" + software_engineers[i])))
        test_labels.append(1)

    for i in range(len(electrical_engineers)):
        result_labels.append(classify(parse("Test Data/Electrical Engineers/" + electrical_engineers[i])))
        test_labels.append(2)

    for i in range(len(mechanical_engineers)):
        result_labels.append(classify(parse("Test Data/Mechanical Engineers/" + mechanical_engineers[i])))
        test_labels.append(3)

    for i in range(len(business_analysts)):
        result_labels.append(classify(parse("Test Data/Business Analysts/" + business_analysts[i])))
        test_labels.append(4)

    correct = 0

    for i in range(len(result_labels)):
        if result_labels[i] == test_labels[i]:
            correct += 1

    accuracy = (correct * 100.0) / len(result_labels)
    print("Accuracy - ", accuracy)

def classify_profile(profile):
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

    label = classify(profile_data)

    if label == 0:
        return "Given profile is of a Recruiter"
    elif label == 1:
        return "Given profile is of a Software Engineer"
    elif label == 2:
        return "Given profile is of a Electrical Engineer"
    elif label == 3:
        return "Given profile is of a Mechanical Engineer"
    elif label == 4:
        return "Given profile is of a Business Analyst"
