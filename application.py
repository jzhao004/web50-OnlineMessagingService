import os

from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit

channellist = []

app = Flask(__name__)
app.config['SECRET_KEY'] = '\xcd\xf3\x81A9\xe2\xfby=\xcd\xc5?\x1e\xb8\xd2\xc8;{\x82"\xf7@\x84\xa3\x07'
socketio = SocketIO(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("displayname") is None:
        if request.method == "POST":
            displayname = request.form.get("displayname")
            session["displayname"] = displayname
            return render_template("channels.html", displayname=displayname, channellist=channellist)
        else:
            return render_template("index.html")
    else:
        return render_template("channels.html", displayname=session.get("displayname"), channellist=channellist)

@app.route("/channels", methods=["GET", "POST"])
def channels():
    if request.method == "POST":
        channelname = request.form.get("channelname")
        if channelname.lower() in [channel.lower() for channel in channellist]:
            return render_template("channels.html", displayname=session.get("displayname"), channellist=channellist, exist=True)
        else:
            channellist.insert(0, channelname)
            return render_template("channels.html", displayname=session.get("displayname"), channellist=channellist)
    else:
        return render_template("channels.html", displayname=session.get("displayname"), channellist=channellist)

@app.route("/channels/search", methods=["POST", "GET"])
def search():
    if request.method == "POST":
        searchquery = request.form.get("searchquery")
        joinedchannels = [channel for channel in channellist if searchquery.lower() in channel.lower()]
        if joinedchannels == []:
            return render_template("channels.html", displayname=session.get("displayname"), channellist=joinedchannels, empty=True)
        else:
            return render_template("channels.html", displayname=session.get("displayname"), channellist=joinedchannels)
    else:
        return render_template("channels.html", displayname=session.get("displayname"), channellist=joinedchannels)

@app.route("/channels/<channelname>")
def channel(channelname):
    return render_template("channel.html", displayname=session.get("displayname"), channelname=channelname)

@socketio.on("send message")
def sendmessage(data):
    displayname = data["displayname"]
    text = data["text"]
    time = data["time"]
    emit("new message", {'displayname':displayname, 'text':text, 'time':time}, broadcast=True)

@app.route("/signout")
def signout():
    session["displayname"] = None
    return render_template("index.html")
