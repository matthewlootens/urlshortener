from flask import Flask, send_from_directory, redirect, url_for, request, render_template
import sqlite3, sys, hashlib
from BaseConverter import BaseConverter

app = Flask(__name__)
CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNOPQRSTUVWXYZ"
DOMAIN = 'http://localhost:5000/'
DBFILENAME = './url.db'

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/submitURL', methods=['PUT', 'POST'])
def queryDatabase():
    # parse request to get url
    # catch KeyError
    url = request.form['url']

    # generate a hash value
    converter = BaseConverter()
    converter.setBaseCharacters(CHARACTERS)

    m = hashlib.sha256()
    m.update(url.encode('utf-8'))

    hashVal = int(m.hexdigest()[:8], 16)
    hashCode = converter.convert(hashVal)

    # send to database
    conn = sqlite3.connect(DBFILENAME)
    c = conn.cursor()
    c.execute('INSERT INTO url (fullurl, shorturl) VALUES(?, ?)', (url, hashCode))
    conn.commit()

    # update page to show url
    shortenedURL = DOMAIN + hashCode

    return render_template('response.html', shortenedURL=shortenedURL)

@app.route('/<shortenedURL>')
def redirect2(shortenedURL):
    # query database
    conn = sqlite3.connect(DBFILENAME)
    c = conn.cursor()
    c.execute("SELECT fullurl FROM url WHERE shorturl=?", (shortenedURL,))
    fullURL = c.fetchone()

    return redirect(fullURL[0])

if __name__ == '__main__':
    # filename = sys.argv[1]
    app.run(port = 8080)
