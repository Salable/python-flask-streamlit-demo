from flask import Flask
from flask import request, jsonify
from flask_cors import cross_origin
import openai
from openai import OpenAI
import dotenv
import os
import uuid
from salable.license import check_grantee_id, create_license

dotenv.load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# system prompt for openai
system_prompt='''You are a helpful assistant that responds with csv compatible text. Always respond with the following city, longitude, latitude and then a new line and then the corresponding data in the following row. Do not provide anything other than the header and text that is requested. Remove any explanations and other non-csv data.what's the lattitude and longitude of the center of '''

app = Flask(__name__)

# app status
@app.route('/',methods=  ['GET'])
def app_status():
    return jsonify({"response":"OK"})

# search
@app.route('/search',methods=  ['POST'])
@cross_origin()
def search():
    data = request.get_json()
    if not data["api_key"]:
        return jsonify({"error": "no api key"})
    is_licensed=check_grantee_id(data["api_key"])["licensed"]
    if is_licensed:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": system_prompt+data["query"],
                }
            ],
            model="gpt-4",
        )
        response=chat_completion.choices[0].message.content
        print(response)
        return jsonify({"request": data["query"], "response": response})
    else: 
        return jsonify({"error": "not licensed"})


@app.route('/purchase',methods=  ['GET'])
@cross_origin()
def check_api_key():
    api_key = request.args.get('api_key')
    is_licensed=check_grantee_id(api_key)["licensed"]
    if is_licensed:
        return jsonify({"grantee_id": api_key, "licensed": True})
    else:
        return jsonify({"grantee_id": api_key,"licensed": False})
@app.route('/purchase',methods=  ['POST'])
@cross_origin()
def purchase_api_key():
    data = request.get_json()
    if "grantee_id" not in data or "member_id" not  in data:
        random_uuid = str(uuid.uuid4())
        response=create_license(grantee_id=random_uuid, member_id=random_uuid)
        return jsonify({"grantee_id": response["data"]["granteeId"], "licensed": True})
    response=create_license(grantee_id=data["grantee_id"], member_id=data["member_id"])
    if response["licensed"]:
        return jsonify({"grantee_id": response["data"]["granteeId"], "licensed": True})
    else:
        return jsonify({"error": "not licensed"})

    
# run if called from command line
if __name__ == '__main__':
   app.run(host="0.0.0.0",port=8080, debug=False)