from flask import Flask, request
import object_storage
from postgresql import *
import rabbitMQ

app = Flask(__name__)

@app.route('/')
def handle_nothing():
    return "hello world"


@app.route('/upload', methods=['POST'])
def upload_file():
    print("got u fucker 1")
    if 'file' not in request.files:
        return 'No file part'
    try:
        file = request.files['file']
        email = request.form['email']
        status = 'pending'
        print("got u fucker 2")
        new_id = db.insert_new_client(email, status)
        print(f"new id: {new_id}")
        file.filename = str(new_id)+".wav"
        object_storage.upload(file)
        rabbit.push_message(str(new_id))
    except Exception as e:
        return 'error while write file'

    return 'File uploaded successfully'


if __name__ == "__main__":
    db = Postgresql()
    rabbit = rabbitMQ.RabbitMQ()
    app.run(host='5.75.207.167',port=5003)
