from flask import Flask, request, redirect
from markupsafe import escape
import json
import hashlib

app = Flask(__name__)

urls = [
    {
      "id": "12345", "long": "https://www.google.com/", "short": "http://localhost/12345"
    },
    {
      "id": "09876", "long": "www.bing.com", "short": "http://localhost/09876"
    }
    ]

'''
Takes full url and returns the shortened version
'''
@app.route("/shorten/",methods = ['POST'])
def shorten():
    req = request.get_json()
    url = req['url']
    # using sha1 hash, no hash ids function in python
    # get hex digest to shorten hash
    hash = hashlib.sha1(url.encode("UTF-8")).hexdigest()
    # pull first 6 characters to make tiny url
    return hash[0:6]
    # push tiny url into database
    # encode the value before database submission
    # url = encode(req['url'])

'''
Takes shortened url and returns the full url
'''
@app.route("/lengthen/", methods=['GET'])
def lengthen():
    # get the url ID
    id = request.args.get('id')
    # pull id from database if exists
    for itm in urls:
        if itm['id'] == id:
            # return full url
            return itm['long']
    # return 'error' message to user
    return "The ID entered does not map to an existing URL"

'''
Takes a short url id and redirects the user to the long url
'''
@app.route("/<id>")
def redirect(id):
    # urlID = escape(id)
    urlID = str(id)
    # for itm in urls:

        # if itm['id'] == urlID:
            # return f"it worked! yay {itm['long']}"
    return redirect("https://www.google.com")
    # return "The specified ID does not match any entries"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
