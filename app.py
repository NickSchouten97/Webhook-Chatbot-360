from flask import Flask, request, jsonify, json
import os

app = Flask(__name__)

details = {'AlgemeneInformatie' : {}, 'Feedback' : {}}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    #Get conversation context
    req = request.get_json(force=True)
    parameter = req.get('queryResult').get('parameters')
    intent = req.get('queryResult').get('intent').get('displayName')
    print(parameter)

    #Welcome text including system name of user
    if req.get('queryResult').get('action') == 'input.welcome':
        username = os.getlogin()
        welcomeText = 'Welkom bij de 360 graden feedback chatbot ' + username + '! Wie wilt u voor welke periode beoordelen?'
        details.get('AlgemeneInformatie').update({'gebruiker': username})
        return jsonify({'fulfillmentText': welcomeText})

    #Filling JSON
    for key in parameter.keys():
        if key == "beoordeelde" or key == "project" or key == "begindatum" or key == "einddatum" or key == "rolgebruiker" or key == "rolbeoordeelde" or key == "relatie":
            details.get('AlgemeneInformatie').update(parameter)
        elif key == "sterkpunt" or key == "redensterkpunt" or key == "sterkpunt2" or key == "redensterkpunt2" or key == "sterkpunt3" or key == "redensterkpunt3" or key == "verbeterpunt" or key == "redenverbeterpunt" or key == "verbeterpunt2" or key == "redenverbeterpunt2" or key == "verbeterpunt3" or key == "redenverbeterpunt3" or key == "overall":
            details.get('Feedback').update(parameter)
    
    #Confirmation question for Algemene Informatie
    if req.get('queryResult').get('intent').get('displayName') == 'GetRelatie':
        detailsConfText = 'Kloppen deze gegevens? - Uw naam: %s - Uw rol: %s - Naam beoordeelde: %s - Rol beoordeelde: %s - Project: %s - Periode: %s tot %s - Relatie: %s'
        detailsInfo = (os.getlogin(), details.get('AlgemeneInformatie').get('rolgebruiker'), details.get('AlgemeneInformatie').get('beoordeelde'), details.get('AlgemeneInformatie').get('rolbeoordeelde'), details.get('AlgemeneInformatie').get('project'), details.get('AlgemeneInformatie').get('begindatum'), details.get('AlgemeneInformatie').get('einddatum'), details.get('AlgemeneInformatie').get('relatie'))
        return jsonify({'fulfillmentText': detailsConfText % detailsInfo})
    
    #Writing JSON file to pc
    with open('details.json', 'w') as json_file:
        json.dump(details, json_file)
    return details

if __name__ == '__main__':
   app.run()