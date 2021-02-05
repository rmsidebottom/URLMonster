import json
import hashlib
import mysql.connector
from flask import Flask, request, redirect, render_template
from markupsafe import escape
from pathlib import Path

app = Flask(__name__)

# set up general variables used throughout the application
database = 'urlmonster'
table = 'links'
user = 'root'
secretFile = 'secrets.txt'
# reading the password in like this results in a trailing newline
password = Path(secretFile).read_text()[:-1]
domain = 'localhost:5000/'

'''
Takes full url and returns the shortened version
'''
@app.route('/shorten/',methods = ['POST'])
def shorten():
    if request.get_json():
        req = request.get_json()
        url = req['url']
    elif request.form['url']:
        url = request.form['url']
    else:
        return "Unexpected input format. Submit json or through the form."
    # using sha1 hash, no hash ids function in python
    # get hex digest to shorten hash, pull first 6 characters to make tiny url
    hash = hashlib.sha1(url.encode('UTF-8')).hexdigest()[0:6]

    # first sql statement is to check if item exists
    sql_statement = f'SELECT longurl from {table} where hashid = \"{hash}\"'
    ans = runDbQuery(sql_statement)
    if ans['status']:
        return f'Your tinyurl is {domain}{hash}'
    else:
        # if it fails to find a database entry, there was either a problem
        # or the item exists, try again by trying to create an entry
        # if this fails, return an error
        shorturl = escape(f'{domain}{hash}')
        sql_statement = f'insert into {table} (hashid, longurl, shorturl) values (\"{hash}\",\"{escape(url)}\", \"{shorturl}\")'
        # push tiny url into database
        ans = runDbQuery(sql_statement)
        if ans['status']:
            return f'Your tinyurl is {shorturl}'
        else:
            return ans['message']

'''
Takes shortened url and returns the full url

id is the hash id returned when a URL is shortened
'''
@app.route('/lengthen/', methods=['GET'])
def lengthen():
    # get the url ID
    id = request.args.get('id')

    # prepare select statement, we know we want to turn the ID into a url
    sql_statement = f'SELECT longurl from {table} where hashid = \"{id}\"'

    # make the query
    ans = runDbQuery(sql_statement)

    # check if query succeeded
    if ans['status']:
        # grab url and decode it
        url = ans['result'][0].decode()
        # return url to satisfy request
        return url
    else:
        # on failure, return the message
        return ans['message']


'''
Takes a short url id and redirects the user to the long url

id is the hash id returned when a URL is shortened
'''
@app.route('/<id>')
def receiveID(id):
    # prepare select statement, we know we want to turn the ID into a url
    sql_statement = f'SELECT longurl from {table} where hashid = \"{id}\"'
    # make the query
    ans = runDbQuery(sql_statement)

    # check if query succeeded
    if ans['status']:
        # grab url and decode it
        url = ans['result'][0].decode()
        # check if url begins with http(s) then redirect user to that site
        if url.startswith('https://') or url.startswith('http://'):
            return redirect(url)
        else:
            return redirect(f'https://{url}')
    else:
        # on failure, return the message
        return ans['message']

'''
Set up the web application
'''
@app.route('/')
def index():
    return render_template('index.html')

# connect to the database and run a query
def runDbQuery(query):
    failure = {'status': False,
        'message': 'There was an issue processing you request.'}
    ret = {}
    try:
        # create connection to the database
        connection = mysql.connector.connect(
            host='localhost',
            user=user,
            password=password,
            database=database,
        )
        # utilize prepared statements, returns obj of type MySQLCursorPrepared
        dbcursor = connection.cursor(prepared=True)

        # check what statement needs to be run
        if query.lower().startswith('select'):
            dbcursor.execute(query)
            # returns a tuple with url as a bytearray (url, '')
            data = dbcursor.fetchone()
            # let the user know if they entered a value that we don't have
            if (not data) or (len(data) == 0):
                ret = failure
            else:
                ret = {'status': True, 'result': data}
        elif query.lower().startswith('insert'):
            dbcursor.execute(query)
            connection.commit()
            ret = {'status': True, 'message': 'Success'}

        # close database connections
        if (connection.is_connected()):
            dbcursor.close()
            connection.close()

        # return to the calling function, returns a status and a message or the
        # value pulled from the database
        return ret
    except mysql.connector.Error as e:
        print(e)
        return failure

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
