from flask import Flask, render_template, request, redirect, url_for, flash
import os
from bson.objectid import ObjectId
from dotenv import load_dotenv
import pymongo
import datetime

load_dotenv()

app = Flask(__name__)

# read in the SESSION_KEY variable from the operating system environment
SESSION_KEY = os.environ.get('SESSION_KEY')
# set the session key
app.secret_key = SESSION_KEY
UPLOAD_PRESET = os.environ.get("UPLOAD_PRESET")
CLOUD_NAME = os.environ.get("CLOUD_NAME")

# connect to mongo
MONGO_URI = os.environ.get('MONGO_URI')
client = pymongo.MongoClient(MONGO_URI)

# define my db_name
DB_NAME = "insta_blogger"


# home page

@app.route('/')
def index():
    return render_template('index.template.html', title="Home")

# Create a insta blogger


@app.route('/create')
def create():
    return render_template('create.template.html', title="Create",
                           cloud_name=CLOUD_NAME,
                           upload_preset=UPLOAD_PRESET)


# process the create form
@app.route('/create', methods=['POST'])
def process_create():
    # extract information from the form
    title = request.form.get('title')
    categories = request.form.get('categories')
    date = request.form.get('create-date')
    thought = request.form.get('thought')
    uploaded_file_url = request.form.get('uploaded_file_url')

    # convert the string of the data into an actual date object
    date = datetime.datetime.strptime(date, "%Y-%m-%d")

    client[DB_NAME].pictures.insert_one({
        'title': title,
        'categories': categories,
        'create_date': date,
        'thoughts': thought,
        'uploaded_file_url': uploaded_file_url
    })
    return "blog created"

# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
