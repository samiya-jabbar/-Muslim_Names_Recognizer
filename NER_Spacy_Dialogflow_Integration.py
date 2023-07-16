from flask import Flask, request, jsonify
import spacy

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    query = data['queryResult']['queryText']
    #query = "My prophet name is Safiya"
    boy_name = None
    girl_name = None
    print(query)

    my_spacy_model = spacy.load("model-best") 

    # Extract Muslim boy and girl names using the SpaCy model
    doc = my_spacy_model(query)
    print('these are doc ets', doc.ents)
    for ent in doc.ents:
        print("Entered in loop")
        if ent.label_ == 'MUSLIM-BOY-NAME':
            boy_name = ent.text
            print('the text contains boy name:', boy_name)
            result = boy_name
        elif ent.label_ == 'MUSLIM-GIRL-NAME':
            girl_name = ent.text
            print('the text contains girl name:', girl_name)
            result = girl_name

    # Prepare the response
    response = {
        'fulfillmentText': f'Name recognized successfully as {result}',
        'outputContexts': [
            {
                'name': 'projects/<PROJECT_ID>/agent/sessions/<SESSION_ID>/contexts/context-name',
                'lifespanCount': 5,
                'parameters': {
                    'boy_name': boy_name,
                    'girl_name': girl_name
                }
            }
        ]
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
