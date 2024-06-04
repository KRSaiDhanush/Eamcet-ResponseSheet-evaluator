from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
url_file = 'urls.txt'  # Path to the text file

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    url = request.form['url']

    # Save the URL to the file
    f=open(url_file, 'r+')
    
    urls=f.readlines()
    flag=True
    for ele in urls:
        if ele.strip()==url :
            flag=False
            break
    if flag:
        f.write(url + '\n')
    f.close()

    # Send a GET request to the URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract answers
    elements = soup.find_all(class_='rightAns')
    Answers = [element.get_text().strip()[0] for element in elements]
    mathsAnswers = Answers[:80]
    physicsAnswers = Answers[80:120]
    chemistryAnswers = Answers[120:]

    # Extract chosen answers
    elements = soup.find_all(class_='menu-tbl')
    ChoosenAnswers = [element.find_all()[-1].get_text() for element in elements]
    MathsChoosenAnswers = ChoosenAnswers[:80]
    PhysicsChoosenAnswers = ChoosenAnswers[80:120]
    ChemistryChoosenAnswers = ChoosenAnswers[120:]

    # Calculate correct and wrong answers
    mathsCorrect = sum(1 for i in range(len(mathsAnswers)) if MathsChoosenAnswers[i] == mathsAnswers[i])
    mathsWrong = len(mathsAnswers) - mathsCorrect

    physicsCorrect = sum(1 for i in range(len(physicsAnswers)) if PhysicsChoosenAnswers[i] == physicsAnswers[i])
    physicsWrong = len(physicsAnswers) - physicsCorrect

    chemistryCorrect = sum(1 for i in range(len(chemistryAnswers)) if ChemistryChoosenAnswers[i] == chemistryAnswers[i])
    chemistryWrong = len(chemistryAnswers) - chemistryCorrect

    total_marks = mathsCorrect + physicsCorrect + chemistryCorrect

    return render_template('results.html', total_marks=total_marks, mathsCorrect=mathsCorrect,
                           physicsCorrect=physicsCorrect, chemistryCorrect=chemistryCorrect)

@app.route('/urls', methods=['GET'])
def get_urls():
    with open(url_file, 'r') as f:
        urls = f.readlines()
    urls = [url.strip() for url in urls]
    return jsonify(urls)


app.run(debug=True, port=5001)