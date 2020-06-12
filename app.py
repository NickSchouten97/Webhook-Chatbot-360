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

    #Welcome text including system name of user
    if req.get('queryResult').get('action') == 'input.welcome':
        username = os.getlogin()
        welcomeText = 'Welkom bij de 360 graden feedback chatbot ' + username + '! Wie wilt u voor welke periode beoordelen?'
        details.get('AlgemeneInformatie').update({'gebruiker': username})
        return jsonify({'fulfillmentText': welcomeText})

    #Filling JSON
    for key in parameter.keys():
        if key == "gebruiker" or key == "beoordeelde" or key == "project" or key == "begindatum" or key == "einddatum" or key == "rolgebruiker" or key == "rolbeoordeelde" or key == "relatie":
            details.get('AlgemeneInformatie').update(parameter)
        elif key == "sterkpunt" or key == "redensterkpunt" or key == "sterkpunt2" or key == "redensterkpunt2" or key == "sterkpunt3" or key == "redensterkpunt3" or key == "verbeterpunt" or key == "redenverbeterpunt" or key == "verbeterpunt2" or key == "redenverbeterpunt2" or key == "verbeterpunt3" or key == "redenverbeterpunt3" or key == "overall":
            details.get('Feedback').update(parameter)
    
    #Confirmation question for Algemene Informatie
    if intent == 'GetRelatie' or intent == 'GetNaamBeoordeeldeNieuw2' or intent == 'GetNaamGebruikerNieuw2' or intent == 'GetProjectNieuw2' or intent == 'GetRelatieNieuw2' or intent == 'GetPeriodeNieuw2' or intent == 'GetRolBeoordeeldeNieuw2' or intent == 'GetRolGebruikerNieuw3':
        detailsConfText = 'Kloppen deze gegevens? - Uw naam: %s - Uw rol: %s - Naam beoordeelde: %s - Rol beoordeelde: %s - Project: %s - Periode: %s tot %s - Relatie: %s'
        detailsInfo = (details.get('AlgemeneInformatie').get('gebruiker'), details.get('AlgemeneInformatie').get('rolgebruiker'), details.get('AlgemeneInformatie').get('beoordeelde'), details.get('AlgemeneInformatie').get('rolbeoordeelde'), details.get('AlgemeneInformatie').get('project'), details.get('AlgemeneInformatie').get('begindatum'), details.get('AlgemeneInformatie').get('einddatum'), details.get('AlgemeneInformatie').get('relatie'))
        return jsonify({'fulfillmentText': detailsConfText % detailsInfo})

    #Right text for changing the username
    if intent == 'NaamGebruikerAanpassen2':
        usrText = 'Waar wilt u de naam ' + details.get('AlgemeneInformatie').get('gebruiker') + ' naar aanpassen?'
        return jsonify({'fulfillmentText': usrText})

    #Right text for changing sterke punten
    if intent == 'GetSterkPunt1Nieuw' or intent == 'GetSterkPunt2Nieuw' or intent == 'GetSterkPunt3Nieuw' or intent == 'GetRedenSterkPunt1Nieuw' or intent == 'GetRedenSterkPunt2Nieuw' or intent == 'GetRedenSterkPunt3Nieuw':
        if details.get('Feedback').get('sterkpunt3'):
            feedbackConfText = 'Klopt deze feedback? - Sterk punt 1: %s - Reden sterk punt 1: %s - Sterk punt 2: %s - Reden sterk punt 2: %s - Sterk punt 3: %s - Reden sterk punt 3: %s'
            feedbackInfo = (details.get('Feedback').get('sterkpunt'), details.get('Feedback').get('redensterkpunt'), details.get('Feedback').get('sterkpunt2'), details.get('Feedback').get('redensterkpunt2'), details.get('Feedback').get('sterkpunt3'), details.get('Feedback').get('redensterkpunt3'))
            return jsonify({'fulfillmentText': feedbackConfText % feedbackInfo})
        elif details.get('Feedback').get('sterkpunt2'):
            feedbackConfText = 'Klopt deze feedback? - Sterk punt 1: %s - Reden sterk punt 1: %s - Sterk punt 2: %s - Reden sterk punt 2: %s'
            feedbackInfo = (details.get('Feedback').get('sterkpunt'), details.get('Feedback').get('redensterkpunt'), details.get('Feedback').get('sterkpunt2'), details.get('Feedback').get('redensterkpunt2'))
            return jsonify({'fulfillmentText': feedbackConfText % feedbackInfo})
        elif details.get('Feedback').get('sterkpunt'):
            feedbackConfText = 'Klopt deze feedback? - Sterk punt 1: %s - Reden sterk punt 1: %s'
            feedbackInfo = (details.get('Feedback').get('sterkpunt'), details.get('Feedback').get('redensterkpunt'))
            return jsonify({'fulfillmentText': feedbackConfText % feedbackInfo})
    
    #Right text for confirmation question sterke punten
    if intent == 'FeedbackOnjuistSterkPunt1' or intent == 'FeedbackOnjuistSterkPunt2' or intent == 'FeedbackOnjuistSterkPunt3' or intent == 'FeedbackOnjuistRedenSterkPunt1' or intent == 'FeedbackOnjuistRedenSterkPunt2' or intent == 'FeedbackOnjuistRedenSterkPunt3':
        if details.get('Feedback').get('sterkpunt3'):
            return jsonify({'fulfillmentText': 'Welk van de zes bovenstaande punten wilt u aanpassen?'})
        elif details.get('Feedback').get('sterkpunt2'):
            return jsonify({'fulfillmentText': 'Welk van de vier bovenstaande punten wilt u aanpassen?'})
        elif details.get('Feedback').get('sterkpunt1'):
            return jsonify({'fulfillmentText': 'Welk van de twee bovenstaande punten wilt u aanpassen?'})
    
    #Right text for changing verbeterpunten
    if intent == 'GetVerbeterPunt1Nieuw' or intent == 'GetVerbeterPunt2Nieuw' or intent == 'GetVerbeterPunt3Nieuw' or intent == 'GetRedenVerbeterpunt1Nieuw' or intent == 'GetRedenVerbeterpunt2Nieuw' or intent == 'GetRedenVerbeterpunt3Nieuw' or intent == 'GetOverallNieuw':
        if details.get('Feedback').get('verbeterpunt3'):
            feedbackConfText = 'Klopt deze feedback? - Verbeterpunt 1: %s - Reden verbeterpunt 1: %s - Verbeterpunt 2: %s - Reden verbeterpunt 2: %s - Verbeterpunt 3: %s - Reden verbeterpunt 3: %s - Overall: %s'
            feedbackInfo = (details.get('Feedback').get('verbeterpunt'), details.get('Feedback').get('redenverbeterpunt'), details.get('Feedback').get('verbeterpunt2'), details.get('Feedback').get('redenverbeterpunt2'), details.get('Feedback').get('verbeterpunt3'), details.get('Feedback').get('redenverbeterpunt3'), details.get('Feedback').get('overall'))
            return jsonify({'fulfillmentText': feedbackConfText % feedbackInfo})
        elif details.get('Feedback').get('verbeterpunt2'):
            feedbackConfText = 'Klopt deze feedback? - Verbeterpunt 1: %s - Reden verbeterpunt 1: %s - Verbeterpunt 2: %s - Reden verbeterpunt 2: %s - Overall: %s'
            feedbackInfo = (details.get('Feedback').get('verbeterpunt'), details.get('Feedback').get('redenverbeterpunt'), details.get('Feedback').get('verbeterpunt2'), details.get('Feedback').get('redenverbeterpunt2'), details.get('Feedback').get('overall'))
            return jsonify({'fulfillmentText': feedbackConfText % feedbackInfo})
        elif details.get('Feedback').get('verbeterpunt'):
            feedbackConfText = 'Klopt deze feedback? - Verbeterpunt 1: %s - Reden verbeterpunt 1: %s - Overall: %s'
            feedbackInfo = (details.get('Feedback').get('verbeterpunt'), details.get('Feedback').get('redenverbeterpunt'), details.get('Feedback').get('overall'))
            return jsonify({'fulfillmentText': feedbackConfText % feedbackInfo})
    
    #Right text for confirmation question verbeterpunten
    if intent == 'FeedbackOnjuistVerbeterPunt1' or intent == 'FeedbackOnjuistVerbeterPunt2' or intent == 'FeedbackOnjuistVerbeterpunt3' or intent == 'FeedbackOnjuistRedenVerbeterpunt1' or intent == 'FeedbackOnjuistRedenVerbeterpunt2' or intent == 'FeedbackOnjuistRedenVerbeterpunt3' or intent == 'FeedbackOnjuistOverall':
        if details.get('Feedback').get('verbeterpunt3'):
            return jsonify({'fulfillmentText': 'Welk van de zeven bovenstaande punten wilt u aanpassen?'})
        elif details.get('Feedback').get('verbeterpunt2'):
            return jsonify({'fulfillmentText': 'Welk van de vijf bovenstaande punten wilt u aanpassen?'})
        elif details.get('Feedback').get('verbeterpunt1'):
            return jsonify({'fulfillmentText': 'Welk van de drie bovenstaande punten wilt u aanpassen?'})

    #Writing JSON file to pc
    if intent.startswith('GetBevestigingVerbeter') or intent.startswith('GetBevestigingRedenVerbeter') or intent.startswith('GetBevestigingOverall'):
        with open('details.json', 'w') as json_file:
            json.dump(details, json_file)
        return details
    
    return details

if __name__ == '__main__':
   app.run()