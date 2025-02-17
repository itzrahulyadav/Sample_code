from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/welcome')
def welcome():
    return "Welcome to the home page"


if __name__ == '__main__':
    app.run(debug=True)
