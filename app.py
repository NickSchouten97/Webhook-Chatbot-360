from flask import Flask, request, jsonify, json
import os

app = Flask(__name__)

details = {'AlgemeneInformatie' : {}, 'Feedback' : {}}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    #Get conversation context
    req = request.get_json(force=True)
    parameter = req.get('queryResult').get('parameters')

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
        detailsConfText = 'Kloppen deze gegevens?\n' + \
            '- Uw naam: ' + details.get('AlgemeneInformatie').get('gebruiker') + '\n' + \
            '- Uw rol: ' + details.get('AlgemeneInformatie').get('rolgebruiker') + '\n' + \
            '- Naam beoordeelde: ' + details.get('AlgemeneInformatie').get('beoordeelde') + '\n' + \
            '- Rol beoordeelde: ' + details.get('AlgemeneInformatie').get('rolbeoordeelde') + '\n' + \
            '- Project: ' + details.get('AlgemeneInformatie').get('project') + '\n' + \
            '- Periode: ' + details.get('AlgemeneInformatie').get('begindatum') + ' tot ' + details.get('AlgemeneInformatie').get('einddatum') + '\n' + \
            '- Relatie: ' + details.get('AlgemeneInformatie').get('relatie')
        return jsonify({'fulfillmentText': detailsConfText})
    
    #Confirmation question for Feedback
    if req.get('queryResult').get('intent').get('displayName') == 'GetOverall':
        if len(details.get('Feedback').get('sterkpunt3')) > 0 and len(details.get('Feedback').get('verbeterpunt3')) > 0:
            detailsConfText = 'Kloppen deze gegevens?\n' + \
                '- Sterk punt 1: ' + details.get('Feedback').get('sterkpunt') + '\n' + \
                '- Reden sterk punt 1: ' + details.get('Feedback').get('redensterkpunt') + '\n' + \
                '- Sterk punt 2: ' + details.get('Feedback').get('sterkpunt2') + '\n' + \
                '- Reden sterk punt 2: ' + details.get('Feedback').get('redensterkpunt2') + '\n' + \
                '- Sterk punt 3: ' + details.get('Feedback').get('sterkpunt3') + '\n' + \
                '- Reden sterk punt 3: ' + details.get('Feedback').get('redensterkpunt3') + '\n' + \
                '- Verbeter punt 1: ' + details.get('Feedback').get('verbeterpunt') + '\n' + \
                '- Reden Verbeter punt 1: ' + details.get('Feedback').get('redenverbeterpunt') + '\n' + \
                '- Verbeter punt 2: ' + details.get('Feedback').get('verbeterpunt2') + '\n' + \
                '- Reden Verbeter punt 2: ' + details.get('Feedback').get('redenverbeterpunt2') + '\n' + \
                '- Verbeter punt 3: ' + details.get('Feedback').get('verbeterpunt3') + '\n' + \
                '- Reden Verbeter punt 3: ' + details.get('Feedback').get('redenverbeterpunt3') + '\n' + \
                '- Overall: ' + details.get('Feedback').get('overall')
        return jsonify({'fulfillmentText': detailsConfText})
    
    #Writing JSON file to pc
    with open('details.json', 'w') as json_file:
        json.dump(details, json_file)
    return details

if __name__ == '__main__':
   app.run()