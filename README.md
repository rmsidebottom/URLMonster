# URLMonster

1. [Introduction](#introduction)
2. [Components](#components)
3. [Current Problems](#current-problems)
4. [Future Improvements](#future-improvements)

# Introduction
Python Flask application that will convert URLs; both long to short and short to long.

In its present form, it works by taking in a URL and computing its SHA1 hash. From there it takes the first 6 digits to use as the ID to make a short url. Currently it is set up to run on localhost and will return a short url like `localhost:5000/123456`.

# Components
This URL shortener has three components; a Python script, a mySQL backend, and a basic front end webpage ([index.html](index.html)).

## Python Backend
When making calls to the data, all queries are made with the cursor setting `prepared=True` to mitigate injection attacks. Parameterized queries are also used to help.

### `/` - GET request
This route is set up to serve the `index.html` file and the form it hosts. From here a user can submit a URL they will to shorten.

Sample url: `http://127.0.0.1:5000/`

### `/shorten/` - POST request
Upon submission of the form, or a cURL request to this endpoint, a SHA1 hash of the URL is generated and the first 6 characters are pulled. The database is queried and if there is a match, the shorturl is returned to the user and that is it.

If no match is found, an insert query is formed and the hashid, url, and short url are added into the database.

Sample url: `http://127.0.0.1:5000/shorten/`
Sample data: `{"url": "https://www.google.com/"}`

### `/lengthen/?=` - GET request
This function takes in a hash id and spits out the long url. It does not redirect the user to the link.

Sample url: `http://127.0.0.1:5000/lengthen/?id=123456`

### `/<id>` - GET request
This function will redirect the user to the URL that matches the ID submitted. With the ID, the database is queried searching for a match. If a match is found, the url is checked to see if it begins with `https://` or `http://` as the Flask redirect requires that. If needed, `https://` is predended to the url. Lastly, the redirect function is called and the user is redirected to the site.

Sample url: `http://127.0.0.1:5000/123456`

### Security

## mySQL Database
This is a simple database backend used simply because I already had it installed locally on my computer. If you are using mySQL, you can configure yours by running the setup script contained in this repo ([db_setup.sh](db_setup.sh)). Prior to beginning, create a text file (`secrets.txt`) containing what the mySQL password should be or is (if the mySQL instance is already set up). This is read in by both the db script and the python files.

To set up the database from scratch with a fresh mySQL installation, run `./db_setup.sh setup` to trigger the script to run the `mysql_secure_installation` command. This will set the root password to the password contained in the `secrets.txt` file (needs to be created).

After the mysql installation, the script will set up the database and table needed to run the script. It can also create test entries if needed. The test entries are described below in the sample table. 

- Database name: `urlmonster`
- Table name: `links`
- Table schema: 
    - hashid varchar(6) (primary key) - this is the first 6 characters from the long URL's SHA1 hash.
    - longurl varchar(50) - the full URL submitted by the user
    - shorturl varchar(28) - the short URL for reference
    
### Table Setup
| **hashid varchar(6)** | longurl varchar(50) | shorturl varchar(28) |
| :---: | :---: | :---: |
| 123456 | www.google.com | http://localhost:5000/123456 |
| 098765 | www.bing.com | http://localhost:5000/098765 | 


## Basic Webpage
The webpage is currently a flat HTML file with a single form in it. The form has one button and one text box. Upon submission of the form, it triggers the `/shorten/` endpoint from the Flask app. When successful, it will return the shortened URL on the next screen. The page can currently be accessed at [http://localhost:5000/](http://localhost:5000).

# Current Problems

## Docker
The goal with docker was to containerize the application. This is where I ran into the bulk of my problems. Couldn't figure out how to install python 3.7, couldn't figure out how to start mySQL, etc. Lots of issues that need to be resolved here. Some might require big changes (mySQL error might be easier to fix by changing database backends) while others can be fixed more easily (simply change the python version used).

If I knew these would be issues going in, I would've developed this from the start using AWS (API Gateway, DynamoDB, Lambda) as I have created REST APIs previously using those tools. Terraform or Cloudformation would've been my medium for quickly deploying this to AWS.

## Hashing
The current algorithm used in hashing, SHA1, is not perfect for collisions especially since this is only using the first 6 characters. This is something that needs to be modified long term.

## Web attacks
More testing needs to be completed to determine how safe and secure this application is. It has some controls in place however it is certainly not exhaustive.

# Future Improvments
While it might be a simple application, improvements can certainly be made to update it to current day technology.

## Hashing Method
A better hashing algorithm would be preferred. Golang has a hash id function which would be ideal for this. I am unsure if there are going to be collisions by taking the first 6 characters from a SHA1 hash. For a proof of concept, this is fine but for a real application I will develop a different function for creating the hash id.

In addition to this, when checking the url in the `/shorten/` function, add in verifying the long url matches what the user submitted.

## Deployment Methods
While the Dockerfile currently does not work, this would be the first improvement on my list. Get this up and runnind and it very well might require using a different database compared to mySQL. The beauty of containerizing the application like this, is you can deploy one thing, the Dockerfile, and the whole application will be deployed.

## Cloud Resources
Another step I plan to take is to move this to the cloud. With the Dockerfile working, it will be easy to import it to any of the big cloud providers using their container services. It can also be made to run on kubernetes. 

In addition, it can be set up entirely using cloud resources. For instance, in AWS utilizing Lambda, API Gateway, and DynamoDB won't be difficult at all and should return similar results. Doing this might remove the need to use Flask but that's okay. This can then be deployed with Terraform or Cloudformation.

## Security
Future security improvements will be made around the database and the python code. It is currently set up to use parameterized queries for mySQL to fight SQL injection however, configuring custom encryption, escaping values, and possibly sanitizing input would also be good to add. Potentially adding a WAF infront of this as well however that is likely overkill for this application.

In addition, also adding SSL to the site to make it https would be welcome.

## Website
Building up an actual website for this is a must. It is easy enough to set up a REST API that can be queried, however not all users will want to submit cURL requests. Thus having a website that is a bit nicer and complete will be necessary. No goals of making anything super complex here.

