import json
from flask import Flask, request, jsonify
from GSheets import GoogleSheets
app = Flask(__name__)

sheets = GoogleSheets()

@app.route('/record',methods = ['POST'])
def get_record():
    record = json.loads(request.data)
    sheets.update(record)
    return jsonify(record)


if __name__ == '__main__':
   app.run(debug = True)
