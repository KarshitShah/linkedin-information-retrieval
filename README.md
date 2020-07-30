# LinkedIn Information Retrieval and Classifier

This repo works as a classifier and an information retrieval system. It contains LinkedIn profiles of people from 5 different domains:

1. Technical Recruiters
2. Software Engineers
3. Mechanical Engineers
4. Electrical Engineers
5. Business Analysts

The classifier will help you classify profiles within these domains. Also, we have around 400 profiles which can be retrieved based on the keywords. This works as the Information Retrieval System.

To get this repository running, you'll need to follow the following steps:

- Clone this repo.
- Install virtual env using `pip3 install virtualenv`
- Create virtual env for this repo using `python3 -m venv env`
- Activate the virtual env by running `source env/bin/activate`
- Install all the required packeges by running `pip3 install -r requirements.txt`
- To run the app, run `python3 API.py` from the `src` directory
- To deactivate the virtual env, simply run `deactivate`
