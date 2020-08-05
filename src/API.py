from flask import Flask, request, render_template
from NaiveBayes import preprocess, naive_bayes, classify_profile
from InvertedIndex import get_stopwords, inverted_index, intersect, get_results
from Clustering import processTrainingData, classify_profile_cluster, driver, buildModel, predict
import json

app=Flask(__name__) # defining the app using flask:

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/home', methods=['POST'])
def get_template():
    if request.form["choice"] == "domain":
        return render_template('find_domain.html')
    else:
        return render_template('retrieve_profiles.html')


# @app.route('/result', methods=['POST'])
# def retrieve_data():
#     url = request.form.get("url", None)
#     query = request.form.get("queries", None)

#     if url:
#         domain=classify_profile(url)
#         return render_template('find_domain.html', data=domain)
#     else:
#         queries = query.split(' ')
#         test = get_results(queries)
#         result = []

#         for value in test.values():
#             values = value.split("-;")
#             data = {
#                 "name": values[0],
#                 "url": values[1],
#                 "title": values[2]
#              }
#             result.append(data)

#         return render_template('retrieve_profiles.html', data=result)


@app.route('/result', methods=['POST'])
def retrieve_data():
    url = request.form.get("url", None)
    query = request.form.get("queries", None)
    cluster = request.form.get("url_cluster", None)

    if url:
        domain=classify_profile(url)
        return render_template('find_domain.html', data=domain)
    elif query:
        queries = query.split(' ')
        test = get_results(queries)
        result = []

        for value in test.values():
            values = value.split("-;")
            data = {
                "name": values[0],
                "url": values[1],
                "title": values[2]
             }
            result.append(data)

        return render_template('retrieve_profiles.html', data=result)

    else:
        profile_data = classify_profile_cluster(cluster)
        lines_for_predicting=[profile_data]
        driver()
        #### you will get a list of output :
        predicted_list_of_clusters=predict(lines_for_predicting)
        return render_template('find_domain.html', data=predicted_list_of_clusters[0])
        


        





if __name__=='__main__':
    preprocess()
    naive_bayes()
    get_stopwords()
    inverted_index()
    app.run(debug=True, host="localhost", port=5000)
