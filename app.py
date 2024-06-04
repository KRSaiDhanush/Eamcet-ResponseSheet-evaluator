from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # URL of the web page
    url = request.form['url']

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all elements with the specified class name
    elements = soup.find_all(class_='rightAns')
    Answers = [element.get_text().strip()[0] for element in elements]
    mathsAnswers = Answers[:80]
    physicsAnswers = Answers[80:120]
    chemistryAnswers = Answers[120:]

    # Find all elements with the specified class name
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


'''if __name__ == "__main__":
    app.run(debug=True, port=5001)'''
