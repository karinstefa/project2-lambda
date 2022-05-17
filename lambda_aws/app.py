from flask import Flask
from boto3.dynamodb.conditions import Key
from flask_restful import Api, Resource
from dotenv import load_dotenv
import os
import boto3
from flask import request


app = Flask(__name__)
api = Api(app)
load_dotenv()
region_name = os.getenv('REGION_NAME')
table_name = os.getenv('TABLE_NAME')

dynamodb = boto3.resource('dynamodb',
                          region_name = region_name)

class BlackList(Resource):
    '''
    post:
        add the email at black list
    return : messages
    get: search email in the black list
    input: email
    ouput: info of dynamoDB
    '''
    def post(self):
        row = {'pk': 'email#email',
               'sk': request.json['email'],
               'info': {'email':request.json['email'],
                        'id_app':request.json['id_app'],
                        'reason':request.json['reason'],
                        'ip':request.json['ip'],
                        'create_datetime':request.json['create_datetime']
               }
               }
        print(table_name)
        dynamodb.Table(table_name).put_item(Item=row)
        return {'message': 'the email  was successfully added'}

    def get(self,email):
        table = dynamodb.Table(table_name)
        response = table.query(
            KeyConditionExpression=Key('pk').eq(
                'email#email') & Key('sk').eq(email)
        )
        if response['Items']:
            return response['Items'][0]['info']
        return {'message': 'the email was not found'}

api.add_resource(BlackList, '/blacklist', '/blacklist/<string:email>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8080)
