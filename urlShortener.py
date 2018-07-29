"""
Todo:
    * redirect only works if url has scheme included; need to auto add http
    * normalize URLs?
        * lowercasae scheme and host
        * captilize escape sequences
        * remove default port

        Doesn't necessarily preserve original URL semantics
        * strip leading and trailing whitespace
        * strip trailing slash
        * store protocol, hostname, and filename separately?
"""

from flask import Flask, send_from_directory, redirect, url_for, request, render_template
import sqlite3, sys, hashlib
from BaseConverter import BaseConverter

app = Flask(__name__)
CHARACTERS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLNOPQRSTUVWXYZ"
DOMAIN = 'http://localhost:5000/'
DBFILENAME = './url.db'

converter = BaseConverter()
converter.characterSet = CHARACTERS

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/submitURL', methods=['PUT', 'POST'])
def queryDatabase():
    # parse request to get url
    # catch KeyError
    url = request.form['url']

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
    app.run(port = 8080)
