import json
import requests
from flask_babel import _
from app import app

#translate functions takes the text to translate and the source and destination
#language codes as arguments
#returns a string with the translated text
#Checks if there is a key for the translation service, throw error if there isn't
#Error is a string which will show translated text -- to user knows what the error says


def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in app.config or \
            not app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    #Key needs to be provided for authentication -- created an auth dictionary
    #passes in the requests headers argument
    auth = {'Ocp-Apim-Subscription-Key': app.config['MS_TRANSLATOR_KEY']}
    #get method from requests package sends HTTP requests with GET argument
    #returns a JSON and the text source and destination needs to be given
    #as a query in the URL
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    #check that the status code is 200 (successful)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    #if successful -- body of the response has JSON encoded string with translation
    #json.loads function returns the raw body of the response
    return json.loads(r.content.decode('utf-8-sig'))