import os

from flask import Flask, session, render_template, request,jsonify,json
from flask import Flask
from flask_socketio import SocketIO, emit
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

channelids = {}
chats=[]


@app.route("/", methods=["GET","POST"])
def index():

	return render_template("index.html")


@app.route("/first", methods=["GET","POST"])
def first():

	return render_template("first.html")


@app.route("/logging", methods=["POST"])
def logging():
	if request.method=="POST":
		username = request.form.get("username")
		return render_template("logging.html", username=json.dumps(username))

	else: return render_template("index.html")


@app.route("/first/<channel>")
def channel(channel):
	if (channel in channelids):
		index = channelids[channel]
		data = chats[index]
		return render_template("channel.html", channel=channel, chatdata=data)
	else: return "404"

@app.route("/createchannel", methods=["POST"])
def createchannel():
	channel = request.form.get("channel")
	if (channel in channelids):
		return render_template("first.html", message="that channel already exists!")
	else:
		index = int(len(channelids))
		channelids[channel] = index
		newchat = []
		chats.append(newchat)
		return render_template("createchannel.html", channel=json.dumps(channel))

@app.route("/handlmessage", methods=["POST"])
def handlmessage():
	message = request.form.get("message")
	channel = request.form.get("channel")
	index = channelids[channel]
	if (len(chats[index])>=100):
		chats[index].pop(0)
	chats[index].append(message)
	data = chats[index]
	return jsonify({"success": True})

@socketio.on("submit message")
def sendmsg(data):
	message=data["message"]
	channel=data["channel"]
	emit("announce message", {"msg":message,"channel":channel}, broadcast=True)