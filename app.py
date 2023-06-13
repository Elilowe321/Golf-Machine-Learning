from flask import Flask, render_template, request
import SeniorProject

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def result():
    #Get Data from user
    full_name = request.form['full_name']
    year = request.form['year']
    day1 = request.form['day1']
    day2 = request.form['day2']
    day3 = request.form['day3']

    
    prediction = SeniorProject.data_retrieval(full_name, year, int(day1), int(day2), int(day3))

    result = f"<pre>Full Name: {full_name}\nYear: {year}\nDay 1: {day1}\nDay 2: {day2}\nDay 3: {day3}\nPrediction: {prediction}</pre>"
    
    
    return render_template("result.html", result=result)

if __name__ == '__main__':
    app.run()