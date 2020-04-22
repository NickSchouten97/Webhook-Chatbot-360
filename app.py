from flask import Flask, request, jsonify, json

app = Flask(__name__)

details = {'AlgemeneInformatie' : {}}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    details.get('AlgemeneInformatie').update(req.get('queryResult').get('parameters'))
    print(details)
    with open('details.json', 'w') as json_file:
        json.dump(details, json_file)
    return details

if __name__ == '__main__':
   app.run()