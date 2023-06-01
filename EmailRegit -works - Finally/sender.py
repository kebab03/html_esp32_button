from flask import Flask, render_template, jsonify, request, session, redirect, g
import sqlite3
import os
import threading
import smtplib
from email.mime.text import MIMEText
from waitress import serve
from flask import session


app = Flask(__name__)
app.secret_key = "your_secret_key"

# SMTP email configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "kebab2803"
SMTP_PASSWORD = "eeazzvwbyctfvpkr"
SENDER_EMAIL = "kebab2803@gmail.com"

# SQLite database setup
DATABASE = "users.db"


def get_database_connection():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT, password TEXT)")
    return db


@app.teardown_appcontext
def close_database_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


# Routes
@app.route("/", methods=["GET", "POST"])
def home():
    if "email" in session:
        return redirect("/dashboard")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if login_user(email, password):
            session["email"] = email
            return redirect("/dashboard")
        else:
            return render_template("index.html", error="Invalid email or password.")
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if "email" in session:
        return redirect("/dashboard")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if register_user(email, password):
            session["email"] = email
            send_registration_email(email)
            return redirect("/dashboard")
        else:
            return render_template("register.html", error="Email already registered.")
    return render_template("register.html")


# Define global variables to store the values
saved_num_buttons = 0
saved_button_labels = []
saved_button_states = []

@app.route('/toggle', methods=['GET', 'POST'])
def toggle():
    global saved_num_buttons, saved_button_labels, saved_button_states
    if request.method == 'POST':
        num_buttons = int(request.form['num_buttons'])
        button_labels = [request.form[f'button{i+1}'] for i in range(num_buttons)]
        button_states = ['off'] * num_buttons
        saved_num_buttons = num_buttons
        saved_button_labels = button_labels
        saved_button_states = button_states
        #data = request.get_json()
        print("--Line 85 -----data from esp32  /toogle ----------------")
        #print(data)
        print("--Line 87---fine ---data from esp32 ----------------")
    
        return render_template('toggle.html', num_buttons=num_buttons, button_labels=button_labels,
                               button_states=button_states)
    else:
        if saved_num_buttons == 0:
            return render_template('toggle.html', num_buttons=1, button_labels=[], button_states=[])
        else:
            return render_template('toggle.html', num_buttons=saved_num_buttons, button_labels=saved_button_labels,
                                   button_states=saved_button_states)

@app.route('/state', methods=['POST'])
def update_state():
    global saved_button_states, saved_button_labels

    data = request.get_json()
    print("----Line 112------data from esp32 /state----------------")
    print(data)
    button_id = int(data.get('buttonId'))
    #
    new_state = data.get('state')
    button_label = data.get('buttonLabel')

    print("---Line 108 ---------data from esp32 /state-------button_id---------")
    print(button_id)
    print("-@@@@@@@@@@--data from esp32 /state-------button_label---------")
    print(button_label)

    print("-----------fine /state ---data from esp32 ----------------")
       
    saved_button_states[button_id] = new_state
    saved_button_labels[button_id] = button_label

    return jsonify({'message': f'State updated for button {button_label}'})
aved_button_id = None
aved_button_label = None
saved_button_Pin =[]
@app.route('/Pstate', methods=['GET', 'POST'])
def Pupdate_state():
    global saved_button_Pin,aved_button_id, aved_button_label,Sbutton_data,button_data
    global saved_button_Pin 
    saved_button_label="default"
    saved_button_id=None
    Sbutton_data=[]
    if request.method == 'POST':
        data = request.get_json()
        button_id = int(data.get('buttonId'))
        buttonPin = data.get('buttonPin')
        button_label = data.get('buttonLabel')
        #saved_button_Pin[button_id] = buttonPin
        saved_button_Pin.append(buttonPin)  # Append buttonPin to the list
    
        aved_button_label = button_label
        print("------POST----data from esp32 /Pstate-------button_id---------")
        print(button_id)
        print("-line 134 ----------data from esp32 /state-------buttonPin---------")
        print(buttonPin)
        print("---line 135 ######## POST ###--data from esp32 /Pstate-------button_label---------")
        print(button_label)
        print("---Line 138 ---------data from esp32 /Pstate----------------")
        print(data)
        print("-----------fine /Pstate ---data from esp32 ----------------")
        Sbutton_data = [{'buttonId': button_id, 'buttonLabel':button_label}]
        print("-line 141-------button data  dentro---------------------")
        print("#####  Line 142 ############   button_data   type  ######################")
        print(type(Sbutton_data))
        print(Sbutton_data)
        aved_button_id = button_id
        aved_button_label = button_label

        
        print("Line 157 saved_button_PIN")
        print(saved_button_Pin)
        print("Line 158 saved_button_labels")
        print(aved_button_label)
        session['button_id'] = button_id
        session['button_label'] = button_label
        print("lINE 150 session['button_label']")
        print(session['button_label'])

        return render_template('hity.html', button_data=Sbutton_data)
    if Sbutton_data==[]:
        print("#line 151  impongo  Sbutton_data valori default   fuori Sbutton data#############")
        print(Sbutton_data)
        
    # Retrieve button ID and label from session variables
        button_id = session.get('button_id')
        button_label = session.get('button_label')
        print("Line 165session.get('button_id')")
        print(session.get('button_id'))
        Sbutton_data=[{'buttonId': button_id, 'buttonLabel':button_label}]
        print("#line 155   Sbutton_data DOPO  fuori Sbutton data#############")
        print(Sbutton_data)
    message = 'State updated Pstate for button'  # Define the message variable
    

    
    # Use the global variables where needed
    button_id = aved_button_id
    button_label = aved_button_label
    button_data= [{'buttonId': button_id, 'buttonLabel':button_label}]

    print("Line 182 saved_button_Pin")
    print(saved_button_Pin)
    print("Line 184 saved_button_labels")
    print(saved_button_labels)
#################à

    result = []

    for i in range(len(saved_button_Pin)):
        
        button_id = saved_button_Pin[i]
        button_label = saved_button_labels[i]
        result.append({'buttonId': button_id, 'buttonLabel': button_label})
        print(" lINE  204  --result---:")

    print(result)

    print(" lINE  209  --result-TYPE--:")

    print(type(result))

    # Ensure that button_index is within the valid range
    button_index = 0
    if len(saved_button_labels) > 0:
        button_index = len(saved_button_labels) - 1
    print("#line 198  ##################     fuori Sbutton data####################")
    print(button_data)
    #return render_template('hity.html', button_data=[{'buttonId': button_index, 'buttonLabel': saved_button_labels}])
    #return render_template('hitcopy.html', button_data=button_data)
    #return render_template('hityfN.html', button_data=button_data)
    return render_template('hityfN.html', button_data=result)
#    return render_template('hit.html', buttonPin=saved_button_Pin, buttonLabel=saved_button_labels)


#  
# @app.route('/Pstate', methods=['GET','POST'])
# def Pupdate_state():
#     global saved_button_Pin, saved_button_labels
#     if request.method == 'POST':
#         data = request.get_json()
#         button_id = int(data.get('buttonId'))
#         buttonPin = data.get('buttonPin')
#         button_label = data.get('buttonLabel')
#         saved_button_Pin=buttonPin;
#         saved_button_labels=button_label;
#         print("--------------data from esp32 /state-------button_id---------")
#         print(button_id)
#         print("--------------data from esp32 /state-------buttonPin---------")
#         print(buttonPin)
#         print("---#################--data from esp32 /state-------button_label---------")
#         print(button_label)
#         print("--------------data from esp32 /Pstate----------------")
#         print(data)
#         print("-----------fine /Pstate ---data from esp32 ----------------")
#         return render_template('hity.html',buttonId=button_id,buttonLabel=button_label)
#         #return jsonify({'message': button_label,'button_id': buttonPin})
#     #saved_button_states[button_id] = new_state
#     #saved_button_labels[button_id] = button_label
#     message = 'State updated Pstate for button'  # Define the message variable
#     print("saved_button_Pin")
#     print(saved_button_Pin)
#     print("saved_button_labels")
#     print(saved_button_labels)
    
#     #return render_template('toggle.html', buttonId=buttonPin, button_labels=button_label)
#     return render_template('hit.html', buttonPin=saved_button_Pin,buttonLabel=saved_button_labels)
#                                #button_states=button_states)
#     #return jsonify({'message': button_label,'button_id': buttonPin})
#     #return jsonify({'message': message})  # Use 'message' as a string key in the JSON response

# @app.route('/state', methods=['GET'])
# def get_state():
#     state_data = []
#     for button_index, state in enumerate(saved_button_states):
#         print(" line 205 button_index ")
#         print(button_index)

#         print("/state line 208 state : ")
#         print(state)
#         button_label = saved_button_labels[button_index]
#         state_data.append({"id": button_index, "buttonLabel": button_label, "state": state})
#     return jsonify({'buttons': state_data})
@app.route('/state', methods=['GET'])
def get_state():
    state_data = []
    for button_index, state in enumerate(saved_button_states):
        print(" line 225 button_index ")
        print(button_index)
        if button_index >= len(saved_button_labels):
            # Handle the case where the index is out of range
            # You can choose to skip or handle it differently based on your requirements
            continue

        button_label = saved_button_labels[button_index]
        
        print("/state line 232 state : ")
        print(state)
        state_data.append({"id": button_index, "buttonLabel": button_label, "state": state})
    return jsonify({'buttons': state_data})


@app.route('/toggle-state', methods=['POST'])
def toggle_state():
    if 'email' not in session:
        return jsonify(error='Unauthorized access')

    index = int(request.json['index'])  # Get the index of the button
    button_id = f'button{index + 1}'  # Button ID based on the index

    # Toggle the state of the button
    if saved_button_states[index] == 'on':
        saved_button_states[index] = 'off'
    else:
        saved_button_states[index] = 'on'

    return jsonify(switch=saved_button_states[index])


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "email" not in session:
        return redirect("/")

    if request.method == "POST":
        num_buttons = int(request.form["num_buttons"])
        button_labels = []
        for i in range(num_buttons):
            label = request.form.get("button" + str(i + 1))
            button_labels.append(label)

        global saved_num_buttons, saved_button_labels, saved_button_states
        saved_num_buttons = num_buttons
        saved_button_labels = button_labels
        saved_button_states = ['off'] * num_buttons

    return render_template("dashboard.html", username=session["email"], num_buttons=saved_num_buttons)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop("email", None)
    return redirect("/")


# Helper functions
def register_user(email, password):
    db = get_database_connection()
    cursor = db.execute("SELECT * FROM users WHERE email=?", (email,))
    if cursor.fetchone() is not None:
        return False
    db.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
    db.commit()
    return True


def login_user(email, password):
    db = get_database_connection()
    cursor = db.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return cursor.fetchone() is not None


def send_registration_email(email):
    msg = MIMEText("Thank you for registering!")
    msg["Subject"] = "Registration Confirmation"
    msg["From"] = SENDER_EMAIL
    msg["To"] = email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SENDER_EMAIL, [email], msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print("Error sending email:", str(e))
        print("SMTP debug response:", server.get_debuglevel())


if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=80, threads=2)
    #serve(app, host='0.0.0.0', port=443, threads=2)

