import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from werkzeug.exceptions import default_exceptions
from datetime import datetime
from random import choice

from helpers import apology

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route("/about")
def about():

    return render_template("about.html")

@app.route("/")
def index():

    # Gets time variables:
    date = datetime.utcnow()
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    second = date.second

    # Determines the season:
    if month > 11 or month < 3:
        season = "It is winter."
    elif month > 2 and month < 6:
        season = "It is spring."
    elif month > 5 and month < 9:
        season = "It is summer."
    else:
        season = "It is autumn."

    # Month number to month:
    if month == 1:
        month = "January"
    elif month == 2:
        month = "February"
    elif month == 3:
        month = "March"
    elif month == 4:
        month = "April"
    elif month == 5:
        month = "May"
    elif month == 6:
        month = "June"
    elif month == 7:
        month = "July"
    elif month == 8:
        month = "August"
    elif month == 9:
        month = "September"
    elif month == 10:
        month = "October"
    elif month == 11:
        month = "November"
    else:
        month = "December"

    # Determines daytime:
    if hour > 6 and hour < 18:
        light = "It is day."
        daytime = True
    else:
        light = "It is night."
        daytime = False

    if daytime == True:
        bgcolor = "white"
        textcolor = "black"
    else:
        bgcolor = "black"
        textcolor = "white"

    # Creates lists:
    phraselist = open("phraselist.txt").readlines()
    nounlist = open("nounlist.txt").readlines()
    nounlistperiod = open("nounlistperiod.txt").readlines()
    nounliste = open("nounliste.txt").readlines()
    verblist = open("verblist.txt").readlines()
    symbollist = open("symbollist.txt").readlines()

    # Determines shadow color:
    if(second%2==0):
        shadow = "red"
    else:
        shadow = "blue"

    # Determine nouns (making sure that duplicates are unlikely):
    n1 = choice(nounlist)
    n1e = choice(nounliste)
    n1p = choice(nounlistperiod)
    n2 = choice(nounlist)
    while n2 == n1:
        n2 = choice(nounlist)
    n2p = choice(nounlistperiod)
    while n2p == n1p:
        n2p = choice(nounlist)
    n2e = choice(nounliste)
    while n2e == n1e:
        n2e = choice(nounlist)
    n3 = choice(nounlist)
    while n3 == n2 or n3 == n1:
        n3 = choice(nounlist)
    n3p = choice(nounlistperiod)
    while n3p == n2p or n3p == n1p:
        n3p = choice(nounlist)
    n4 = choice(nounlist)
    while n4 == n3 or n4 == n2 or n4 == n1:
        n4 = choice(nounlist)
    n4p = choice(nounlistperiod)
    while n4p == n3p or n4p == n2p or n4p == n1p:
        n4p = choice(nounlist)

    # Determine verbs (making sure that duplicates are unlikely):
    v1 = choice(verblist)
    v2 = choice(verblist)
    while v2 == v1:
        v2 = choice(nounlist)
    v3 = choice(verblist)
    while v3 == v2 or v3 == v1:
        v3 = choice(nounlist)

    # Determine symbol:
    s1 = choice(symbollist)

    # Determine phrase:
    p = choice(phraselist)

    # Insert nouns and verbs into phrase:
    p = p.replace("n1p", n1p)
    p = p.replace("n2p", n2p)
    p = p.replace("n3p", n3p)
    p = p.replace("n4p", n4p)
    p = p.replace("n1)", n1e)
    p = p.replace("n2)", n2e)
    p = p.replace("n1", n1)
    p = p.replace("n2", n2)
    p = p.replace("n3", n3)
    p = p.replace("n4", n4)
    p = p.replace("v1", v1)
    p = p.replace("v2", v2)
    p = p.replace("v3", v3)

    # Split phrase into sentences (this is to make each sentence start on a new line when printed):
    if '#' in p:
        plist = p.split ('#')
        p1 = plist[0]
        p2 = plist[1]
        if len(plist) > 2:
            p3 = plist[2]
            if len(plist) > 3:
                p4 = plist[3]
            else:
                p4 = ""
        else:
            p3 = ""
            p4 = ""
    else:
        p1 = p
        p2 = ""
        p3 = ""
        p4 = ""

    # Determines the length of the string and size of text:
    plen = len(p)
    if plen > 100:
        textsize = "tinymaintext"
    elif plen > 65:
        textsize = "smallmaintext"
    elif plen > 40:
        textsize = "mediummaintext"
    elif plen > 30:
        textsize = "bigmaintext"
    else:
        textsize = "hugemaintext"

    return render_template("index.html", shadow = shadow, textsize = textsize, s1 = s1, p1 = p1, p2 = p2, p3 = p3, p4 = p4,
    textcolor = textcolor, bgcolor = bgcolor, light = light, season = season, date = date, year = year, month = month, day = day,
    hour = hour, second = second)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
