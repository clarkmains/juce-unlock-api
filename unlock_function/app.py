""" Processes an unlock POST request from a JUCE Framework app and emulates
the authorisation process performed by the marketplace authorisation service.

The 'body' field of the event is a query string given as a string. The lambda
handler parses this to a dict 'query_strings' -

    {
        'product': ['TestApp'],
        'email': ['me@somewhere.com'],
        'pw': ['mypassword'],
        'os': ['Mac OSX 10.15.4'],
        'mach': ['ME06E516F2']
    }

The 'email' and 'pw' are then compared with the values in the environment to
emulate the auth process abd the unlock key is returned if auth is successful.
"""
import os
import urllib.parse


USER_EMAIL = os.environ['USER_EMAIL']
USER_PASSWORD = os.environ['USER_PASSWORD']
USER_KEY = os.environ['USER_KEY']


def authorised(email, password):
    if email == USER_EMAIL and password == USER_PASSWORD:
        return True
    else:
        return False


def lambda_handler(event, context):
    query_strings = urllib.parse.parse_qs(event.get('body'))
    email_list = query_strings.get('email', [])
    password_list = query_strings.get('pw', [])

    xml_body = '<?xml version="1.0" encoding="utf-8"?>'

    if authorised(email_list[0], password_list[0]):
        xml_body += '<MESSAGE message="Thanks for registering our product!">'
        xml_body += '<KEY>' + USER_KEY + '</KEY></MESSAGE>'
    else:
        xml_body += '''<ERROR error="Sorry, we were not able to authorise your request.
            Please provide a valid email address and password."></ERROR>'''

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/xml',
            'charset': 'utf-8'
        },
        'body': xml_body
    }
