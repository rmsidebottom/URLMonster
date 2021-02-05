import json
import hashlib
import mysql.connector
from flask import Flask, request, redirect
from markupsafe import escape
from pathlib import Path

app = Flask(__name__)

database = "urlmonster"
table = "links"
user = "root"
secretFile = "secrets.txt"
password = Path(secretFile).read_text()[:-1]

''' [
    {
      "id": "12345", "long": "https://www.google.com/", "short": "http://localhost/12345"
    },
    {
      "id": "09876", "long": "www.bing.com", "short": "http://localhost/09876"
    }
    ]'''

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
    # for itm in urls:
    #     if itm['id'] == id:
    #         # return full url
    #         return itm['long']
    # return 'error' message to user
    return "The ID entered does not map to an existing URL"

'''
Takes a short url id and redirects the user to the long url
'''
@app.route("/<id>")
def receiveID(id):
    # catch errors if possible
    try:
        # create connection to the database
        connection = mysql.connector.connect(
            host="localhost",
            user=user,
            password=password,
            database=database,
        )
        # prepare select statement, we know we want to turn the ID into a url
        select_statment = f"SELECT longurl from {table} where hashid = {id}"
        print(select_statment)
        # utilize prepared statements, returns obj of type MySQLCursorPrepared
        dbcursor = connection.cursor(prepared=True)
        dbcursor.execute(select_statment)
        # returns a tuple with url as a bytearray (url, '')
        data = dbcursor.fetchone()
        # close database connections
        if (connection.is_connected()):
            dbcursor.close()
            connection.close()
            print("MySQL connection is closed")
        # let the user know if they entered a value that we don't have
        if len(data) == 0:
            return "Invalid ID entered."
        # grab url and decode it
        url = data[0].decode()
        print(url)
        # check if url begins with http(s)
        if url.startswith("https://") or url.startswith("http://"):
            return redirect(url)
        else:
            return redirect(f"https://{url}")
    except mysql.connector.Error as e:
        print(e)
        return "There was an issue processing you request."
    # finally:

            # return ""
            # return redirect("https://www.google.com")
        return "Complete but no connection"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
