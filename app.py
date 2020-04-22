from flask import Flask, request, jsonify, json

app = Flask(__name__)

details = {'AlgemeneInformatie' : {}, 'Feedback' : {}}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    req = request.get_json(force=True)
    parameter = req.get('queryResult').get('parameters')
    for key in parameter.keys():
        if key == "gebruiker" or key == "beoordeelde" or key == "project" or key == "begindatum" or key == "einddatum" or key == "rolgebruiker" or key == "rolbeoordeelde" or key == "relatie":
            details.get('AlgemeneInformatie').update(parameter)
        elif key == "sterkpunt" or key == "redensterkpunt" or key == "verbeterpunt" or key == "redenverbeterpunt" or key == "overall":
            details.get('Feedback').update(parameter)
    with open('details.json', 'w') as json_file:
        json.dump(details, json_file)
    return details

if __name__ == '__main__':
   app.run()