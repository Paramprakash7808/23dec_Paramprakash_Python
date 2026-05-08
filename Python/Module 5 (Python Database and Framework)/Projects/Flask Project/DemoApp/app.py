from flask import Flask

app = Flask(__name__) #App Initialization

@app.route('/')
def index():
    return 'Flask'

app.run(debug=True)