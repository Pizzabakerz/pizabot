from flask import Flask,jsonify
import aiml
import pymongo
import os

# init database connection
client = pymongo.MongoClient("mongodb+srv://pizzaboy:j1a2c3k4@pizzabot-zhid3.mongodb.net")
db = client.message

app = Flask(__name__)

@app.route('/')

def hello():
    return 'helllo welcome to pizzabot api enter your message as /msg/message and use clear to clear db'

#passing usr name
@app.route('/msg/<usermessage>', methods = ['GET','POST'])

def msg(usermessage):    
    output = []
    if (usermessage == "clear"):
        db.message.remove({})
        output.append({})
    else:

        kernel = aiml.Kernel()

        if os.path.isfile("bot_brain.brn"):
            kernel.bootstrap(brainFile = "bot_brain.brn")
        else:
            kernel.bootstrap(learnFiles = os.path.abspath("data/std-startup.xml"), commands = "load aiml b")
            kernel.saveBrain("bot_brain.brn")

        """kernel = aiml.Kernel()
        kernel.learn("data/std-startup.xml")
        kernel.respond("load aiml b")"""
        value = str(kernel.respond(usermessage))
        db.message.insert({"user":usermessage,"bot":value})

        for q in db.message.find():
            output.append({'user' : q['user'], 'bot' : q['bot']})
    

    return jsonify({'message' : output})

if __name__ =='__main__':
    app.run()