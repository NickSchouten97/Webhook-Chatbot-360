from flask import Flask, request, jsonify, json

app = Flask(__name__)

details = {'AlgemeneInformatie' : {}, 'Feedback' : {}}

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    #Get conversation context
    req = request.get_json(force=True)
    parameter = req.get('queryResult').get('parameters')
    
    #Filling JSON
    for key in parameter.keys():
        if key == "gebruiker" or key == "beoordeelde" or key == "project" or key == "begindatum" or key == "einddatum" or key == "rolgebruiker" or key == "rolbeoordeelde" or key == "relatie":
            details.get('AlgemeneInformatie').update(parameter)
        elif key == "sterkpunt" or key == "redensterkpunt" or key == "sterkpunt2" or key == "redensterkpunt2" or key == "sterkpunt3" or key == "redensterkpunt3" or key == "verbeterpunt" or key == "redenverbeterpunt" or key == "verbeterpunt2" or key == "redenverbeterpunt2" or key == "verbeterpunt3" or key == "redenverbeterpunt3" or key == "overall":
            details.get('Feedback').update(parameter)

    #Add question if answer is missing
    if parameter.get('rolbeoordeelde') == '':
        rolbeoordeeldetext = 'Wat was de rol van ' + details.get('AlgemeneInformatie').get('beoordeelde') + '?'
        return jsonify({'fulfillmentText': rolbeoordeeldetext})

    if parameter.get('redensterkpunt') == '':
        redensterkpunttext = 'U heeft aangegeven dat ' + details.get('AlgemeneInformatie').get('beoordeelde') + ' goed is in ' + details.get('Feedback').get('sterkpunt') + ', waarom vindt u dat?'
        return jsonify({'fulfillmentText': redensterkpunttext})

    if parameter.get('redenverbeterpunt') == '':
        redenverbeterpunttext = 'U heeft aangegeven dat ' + details.get('AlgemeneInformatie').get('beoordeelde') + ' goed is in ' + details.get('Feedback').get('verbeterpunt') + ', waarom vindt u dat?'
        return jsonify({'fulfillmentText': redenverbeterpunttext})
    
    #Writing JSON file to pc
    with open('details.json', 'w') as json_file:
        json.dump(details, json_file)
    return details

if __name__ == '__main__':
   app.run()