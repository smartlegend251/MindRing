from flask import Flask, render_template, request, redirect, url_for, flash, session,send_file
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt
from functools import wraps 
import socket

import re               #importing wraps which is a module installed from another module called functools
import os
from werkzeug.utils import secure_filename
from flask_login import login_user,logout_user
from flask_login import UserMixin
from flask_login import LoginManager
from plyer import notification
import datetime

app = Flask(__name__)
app.secret_key = 'many random bytes'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'productive'

mysql = MySQL(app)


login_manager = LoginManager()
login_manager.init_app(app)

class Admin(UserMixin):
    def __init__(self, adminid, uname, password):
        self.adminid = adminid
        self.uname = uname
        self.password = password

    def get_id(self):
        return self.adminid
    




@login_manager.user_loader
def load_admin(uname):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM adminlogin WHERE uname = %s", (uname,))
    data = cur.fetchone()

    if data:
        adminid = data[0]
        username = data[1]
        password = data[2]
        return Admin(adminid, username, password)

    return None



@app.route('/adminlogin', methods = ['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        uname = request.form['uname']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM adminlogin WHERE uname = %s AND password = %s", (uname, password))
        data = cur.fetchone()
        if data:
            adminid = data[0] 
            uname = data[2]
            password = data[3]
            admin = Admin(adminid, uname, password)
            login_user(admin)
            return redirect(url_for('adminpanel'))
        else:
            print('wrong password')
            flash('Invalid credentials, please enter valid credentials')
            return redirect(url_for('adminlogin'))
    return render_template('adminlogin.html')


def password_validation(pwd):
    password = pwd
    flag = 0
    while True:
        if (len(password) < 8):
            flag = -1
            break
        elif not re.search("[a-z]", password):
            flag = -1
            break
        elif not re.search("[A-Z]", password):
            flag = -1
            break
        elif not re.search("[0-9]", password):
            flag = -1
            break
        elif re.search("\s", password):
            flag = -1
            break
        else:
            flag = 0
            return True
            break

    if flag == -1:
        return False

    




@app.route('/', methods=['GET', 'POST'])
def welcome():
    return render_template('welcome.html')

@app.route('/homepage',  methods=['GET', 'POST'])
@login_required
def homepage():
    flash('Thannk you for logging in')
    return render_template('homepage.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM user WHERE username = %s", [username])
        # cur.execute("SELECT * FROM user WHERE password = %s", [password])
        res = cur.fetchone()
        if res:
            pwd = res[3]
            if sha256_crypt.verify(password, pwd):
                session["logged_in"]=True
                session["userId"] = res[0]
                # flash('Logged in')
                return redirect(url_for('homepage'))
            else:
                print('Wrong password')
                flash('Invalid credentials or User does not exist/registered')
                # return redirect(url_for('register'))
        
    return render_template('login.html')



    # if request.method == 'POST':
    #     uname = request.form['uname']
    #     password = request.form['password']
    #     cur = mysql.connection.cursor()
    #     cur.execute("SELECT * FROM adminlogin WHERE uname = %s", [uname])
    #     cur.execute("SELECT * FROM adminlogin WHERE password = %s", [password])
    #     res = cur.fetchone()
    #     return redirect(url_for('adminpanel'))
    # return render_template('adminlogin.html')   



# Regenerate



@app.route('/adminpanel', methods = ['GET', 'POST'])
def adminpanel():
    # userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM user")
    
    # cur.execute("SELECT  * FROM tasks" )
    
    data= cur.fetchall()
    cur.close()
    return render_template('adminpanel.html', user=data)
    

@app.route('/deleteuser/<string:id_data>', methods = ['GET', 'POST'])
def deleteuser(id_data):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM user WHERE id =%s",[id_data])
    mysql.connection.commit()
    flash("User Has Been Deleted Successfully")
    return redirect(url_for('adminpanel'))



@app.route('/feedback', methods = ['POST','GET'])
def feedback():
    if request.method == "POST":
    
        date= request.form['date']
        email= request.form['email']
        message= request.form['message']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO feedback ( date, email, message) VALUES (%s, %s, %s)", ( date, email, message))
        mysql.connection.commit()
        return redirect(url_for('homepage'))
    return render_template('feedbackuser.html')


@app.route('/fbpanel', methods =['POST', 'GET'] )
def fbpanel():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM feedback")
    
    # cur.execute("SELECT  * FROM tasks" )
    
    data= cur.fetchall()
    cur.close()
    return render_template('adfeedpanel.html', feedback=data) 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password'])) 
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO user (name, username, password) VALUES(%s, %s, %s)", [
                    name, username, password])
        mysql.connection.commit()
        cur.close()
        flash('Thank you for registering with MindRing')
        return redirect(url_for('login'))
    return render_template("register.html")



# @app.route('/todo')
# @login_required
# def check_task_notifications():
#     with app.app_context():
#         while True:
#             # Get the current date and time
#             current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#             # Retrieve tasks that have a tasktime equal to the current datetime
#             cur = mysql.connection.cursor()
#             cur.execute("SELECT * FROM tasks WHERE tasktime = %s", [current_datetime])
#             tasks = cur.fetchall()
#             cur.close()
# # @app.route('/todo' , methods = ['POST','GET'])
# def todo():
#     userId=session["userId"]
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
    
#     # cur.execute("SELECT  * FROM tasks" )
#     # userId=session["userId"]
    
#     data = cur.fetchall()
#     cur.close()
#     return render_template('todo.html', tasks=data)

# @app.route('/inserttask', methods = ['POST'])
# def inserttask():
#     userId=session["userId"]
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
#     if request.method == "POST":
#         # flash("Task Added Successfully")
#         taskname = request.form['taskname']
#         taskdesc= request.form['taskdesc']
#         tasktime = request.form['tasktime']
#         taskstatus = request.form['taskstatus']

#         cur = mysql.connection.cursor()
#         cur.execute("INSERT INTO tasks (id, taskname, taskdesc, tasktime, taskstatus) VALUES (%s,%s, %s, %s, %s)", (userId,taskname, taskdesc, tasktime, taskstatus))
#         mysql.connection.commit()
#         return redirect(url_for('todo'))



# @app.route('/updatetask',methods=['POST','GET'])
# def updatetask():
#     userId=session["userId"]
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
#     if request.method == 'POST':
#         taskid_data = request.form['taskid']
#         taskname = request.form['taskname']
#         taskdesc = request.form['taskdesc']
#         tasktime = request.form['tasktime']
#         taskstatus = request.form['taskstatus']
        
#         cur = mysql.connection.cursor()
#         cur.execute("""
#                UPDATE tasks
#                SET taskname=%s, taskdesc=%s, tasktime=%s, taskstatus=%s 
#                WHERE taskid=%s
#                """, (taskname, taskdesc, tasktime, taskstatus, taskid_data))
#         # flash("Task Updated Successfully")
#         mysql.connection.commit()
#         return redirect(url_for('todo'))

# @app.route('/deletetask/<string:taskid_data>', methods = ['GET'])
# def deletetask(taskid_data):
#     userId=session["userId"]
#     cur = mysql.connection.cursor()
#     cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
#     # flash("Record Has Been Deleted Successfully")
#     cur = mysql.connection.cursor()
#     cur.execute("DELETE FROM tasks WHERE taskid=%s", (taskid_data,))
#     mysql.connection.commit()                                                                                                                                   
#     return redirect(url_for('todo'))



@app.route('/todo')
@login_required

def todo():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
    
    # cur.execute("SELECT  * FROM tasks" )
    # userId=session["userId"]
    
    data = cur.fetchall()
    cur.close()
    return render_template('todo.html', tasks=data)

@app.route('/inserttask', methods = ['POST'])
def inserttask():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
    if request.method == "POST":
        # flash("Task Added Successfully")
        taskname = request.form['taskname']
        taskdesc= request.form['taskdesc']
        tasktime = request.form['tasktime']
        taskstatus = request.form['taskstatus']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tasks (id, taskname, taskdesc, tasktime, taskstatus) VALUES (%s,%s, %s, %s, %s)", (userId,taskname, taskdesc, tasktime, taskstatus))
        mysql.connection.commit()
        return redirect(url_for('todo'))


@app.route('/updatetask',methods=['POST','GET'])
def updatetask():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
    if request.method == 'POST':
        taskid_data = request.form['taskid']
        taskname = request.form['taskname']
        taskdesc = request.form['taskdesc']
        tasktime = request.form['tasktime']
        taskstatus = request.form['taskstatus']
        
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE tasks
               SET taskname=%s, taskdesc=%s, tasktime=%s, taskstatus=%s 
               WHERE taskid=%s
               """, (taskname, taskdesc, tasktime, taskstatus, taskid_data))
        # flash("Task Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('todo'))

@app.route('/deletetask/<string:taskid_data>', methods = ['GET'])
def deletetask(taskid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM tasks WHERE id=%s", [userId])
    # flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE taskid=%s", (taskid_data,))
    mysql.connection.commit()                                                                                                                                   
    return redirect(url_for('todo'))




@app.route('/note')
@login_required

def note():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM notes WHERE id=%s", [userId])
    
    # cur.execute("SELECT  * FROM tasks" )
    # userId=session["userId"]
    
    data = cur.fetchall()
    cur.close()
    return render_template('note.html', notes=data)


@app.route('/insertnote', methods = ['POST'])
def insertnote():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM notes WHERE id=%s", [userId])
    if request.method == "POST":
        # flash("Note Added Successfully")
        notetitle = request.form['notetitle']
        notecontent= request.form['notecontent']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO notes (id, notetitle, notecontent) VALUES (%s,%s, %s)", (userId, notetitle, notecontent))
        mysql.connection.commit()
        return redirect(url_for('note'))

@app.route('/editnote/<string:noteid_data>', methods=['POST', 'GET'])
def editnote(noteid_data):

    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM notes WHERE id=%s", [userId])

    if request.method == 'POST':
        noteid_data = request.form['noteid']
        notetitle = request.form['notetitle']
        notecontent= request.form['notecontent']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE notes
               SET notetitle=%s, notecontent=%s
               WHERE noteid=%s
               """, (notetitle, notecontent,  noteid_data))
        # flash("Notes Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('note'))
    data = cur.fetchall()
    cur.close()
    return render_template('editnote.html', notes=data)

@app.route('/deletenote/<string:noteid_data>', methods = ['GET'])
def deletenote(noteid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM notes WHERE id=%s", [userId])
    # flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM notes WHERE noteid=%s", (noteid_data,))
    mysql.connection.commit()
    return redirect(url_for('note'))

@app.route('/project')
@login_required
def project():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM projects WHERE id=%s", [userId])
    
    # cur.execute("SELECT  * FROM projects" )
    # userId=session["userId"]
    
    data = cur.fetchall()
    cur.close()
    return render_template('project.html', projects=data)




@app.route('/insertproject', methods = ['POST', 'GET'])
@login_required

def insertproject():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM projects WHERE id=%s", [userId])
    if request.method == "POST":
        # flash("Project Created Successfully")
        projectname = request.form['projectname']
        name = request.form['name']
        designation = request.form['designation']
        task = request.form['task']
        priority = request.form['priority']
        status = request.form['status']
        duedate = request.form['duedate']
        team = request.form['team']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO projects (id, projectname, name, designation, task, priority, status, duedate, team) VALUES (%s,%s, %s,%s, %s, %s, %s, %s, %s)", 
        (userId, projectname, name, designation, task, priority, status, duedate, team))
        mysql.connection.commit()
        return redirect(url_for('project'))


@app.route('/updateproject', methods = ['POST', 'GET'])
@login_required

def updateproject():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM projects WHERE id=%s", [userId])
    if request.method == "POST":
        projectid_data = request.form['projectid']
        projectname = request.form['projectname']
        name = request.form['name']
        designation = request.form['designation']
        task = request.form['task']
        priority = request.form['priority']
        status = request.form['status']
        duedate = request.form['duedate']
        team = request.form['team']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE projects
                    SET projectname = %s, name=%s, designation=%s, task=%s, priority=%s, status=%s, duedate=%s, team=%s
                    WHERE projectid=%s
                    """, (projectname, name, designation, task, priority, status, duedate, team, projectid_data))
        # flash("Details Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('project'))



@app.route('/deleteproject/<string:projectid_data>', methods = ['GET'])
@login_required

def deleteproject(projectid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM projects WHERE id=%s", [userId])
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM projects WHERE projectid=%s", (projectid_data,))
    mysql.connection.commit()
    return redirect(url_for('project'))




@app.route('/pronote')
@login_required
def pronote():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pronotes WHERE id=%s", [userId])
    
    # cur.execute("SELECT  * FROM pronotes" )
    # userId=session["userId"]
    
    data = cur.fetchall()
    cur.close()
    return render_template('pronote.html', pronotes=data)



@app.route('/insertpronote', methods = ['POST', 'GET'])
@login_required

def insertpronote():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pronotes WHERE id=%s", [userId])
    if request.method == "POST":
        flash("Note Added Successfully")
        pronotehead = request.form['pronotehead']
        pronotecon= request.form['pronotecon']
        val= request.form['val']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pronotes (id, pronotehead, pronotecon, val) VALUES (%s,%s, %s, %s)", (userId, pronotehead, pronotecon, val))
        mysql.connection.commit()
        return redirect(url_for('pronote'))                                                                                             


@app.route('/deletepronote/<string:pronoteid_data>', methods = ['GET'])
def deletepronote(pronoteid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pronotes WHERE id=%s", [userId])
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pronotes WHERE pronoteid=%s",  (pronoteid_data,))
    mysql.connection.commit()
    return redirect(url_for('pronote'))


@app.route('/updatepronote/<string:pronoteid_data>', methods = ['POST', 'GET'])
@login_required

def updatepronote(pronoteid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pronotes WHERE id=%s", [userId])
    if request.method == "POST":
        pronoteid_data = request.form['pronoteid']
        pronotehead = request.form['pronotehead']
        pronotecon = request.form['pronotecon']
        # dailyentry = request.form['dailyentry']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE pronotes
                    SET pronotehead = %s,  pronotecon =%s
                    WHERE pronoteid=%s
                    """, (pronotehead,  pronotecon, pronoteid_data))
        flash("Details Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('pronote'))
    data = cur.fetchall()
    cur.close()
    return render_template('updatepronote.html', pronotes= data)




@app.route('/pernote')
# @login_required
def pernote():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pernotes WHERE id=%s", [userId])
    
    # cur.execute("SELECT  * FROM pernotes" )
    # userId=session["userId"]
    
    data = cur.fetchall()
    cur.close()
    return render_template('pernote.html', pernotes=data)


@app.route('/insertpernote', methods = ['POST', 'GET'])
def insertpernote():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pernotes WHERE id=%s", [userId])
    if request.method == "POST":
        flash("Note Added Successfully")
        # pernotehead = request.form['pernotehead']
        pernotecon= request.form['pernotecon']
        val= request.form['val']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pernotes (id, val, pernotecon) VALUES (%s, %s, %s)", (userId, val, pernotecon))
        mysql.connection.commit()
        return redirect(url_for('pernote'))


@app.route('/deletepernote/<string:pernoteid_data>', methods = ['GET'])
def deletepernote(pernoteid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pernotes WHERE id=%s", [userId])
    flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM pernotes WHERE pernoteid=%s", (pernoteid_data,))
    mysql.connection.commit()
    return redirect(url_for('pernote'))


@app.route('/updatepernote/<string:pernoteid_data>', methods = ['POST', 'GET'])
@login_required

def updatepernote(pernoteid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM pernotes WHERE id=%s", [userId])
    if request.method == "POST":
        pernoteid_data = request.form['pernoteid']
        pernotecon = request.form['pernotecon']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE pernotes
                    SET  pernotecon =%s
                    WHERE pernoteid=%s
                    """, (pernotecon, pernoteid_data))
        flash("Details Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('pernote'))
    data = cur.fetchall()
    cur.close()
    return render_template('updatepernote.html', pernotes= data)



@app.route('/journal', methods = ['GET'])
@login_required

def journal():

    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM journal WHERE id=%s", [userId])
    data = cur.fetchall()
    cur.close()
    return render_template('journal.html', journal=data)



@app.route('/insertjournal', methods = ['POST', 'GET'])
def insertjournal():
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM journal WHERE id=%s", [userId])
    if request.method == "POST":
        entrytitle = request.form['entrytitle']
        entrydate  = request.form['entrydate']
        dailyentry = request.form['dailyentry']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO journal (id, entrytitle, entrydate, dailyentry) VALUES (%s, %s, %s, %s)", (userId, entrytitle, entrydate, dailyentry))
        mysql.connection.commit()
        return redirect(url_for('journal'))


@app.route('/updatejournal/<string:journalid_data>', methods = ['POST', 'GET'])
@login_required

def updatejournal(journalid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM journal WHERE id=%s", [userId])
    if request.method == "POST":
        journalid_data = request.form['journalid']
        entrytitle = request.form['entrytitle']
        entrydate = request.form['entrydate']
        dailyentry = request.form['dailyentry']
        cur = mysql.connection.cursor()
        cur.execute("""
                    UPDATE journal
                    SET entrytitle = %s,  entrydate =%s, dailyentry=%s
                    WHERE journalid=%s
                    """, (entrytitle,  entrydate, dailyentry, journalid_data))
        flash("Details Updated Successfully")
        mysql.connection.commit()
        return redirect(url_for('journal'))
    data = cur.fetchall()
    cur.close()
    return render_template('updatejournal.html', journal= data)


@app.route('/deletejournal/<string:journalid_data>', methods = ['GET'])
def deletejournal(journalid_data):
    userId=session["userId"]
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM journal WHERE id=%s", [userId])
    # flash("Record Has Been Deleted Successfully")
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM journal WHERE journalid=%s", (journalid_data,))
    mysql.connection.commit()
    return redirect(url_for('journal'))


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('welcome'))


@app.route('/perspace', methods=['GET', 'POST'])
def perspace():
    return render_template('perspace.html')

@app.route('/professpace', methods=['GET', 'POST'])
def professpace():
    return render_template('professpace.html')

# app.config['UPLOAD_FOLDER'] = 'D:/ser'


@app.route('/meditatenew', methods=['GET', 'POST'])
def meditatenew():
    return render_template('Meditationnew.html')

@app.route('/relaxnew', methods=['GET', 'POST'])
def relaxnew():
    return render_template('Relaxtionnew.html')

@app.route('/Create_Path')
def createpath():
    folder_path = r'C:\server_path'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"The folder '{folder_path}' has been created."
    else:
        return f"The folder '{folder_path}' already exists."



# @app.route('/login')
# def loginpage():
#     return render_template('loginpage.html')


# @app.route('/v/')
# def videoplayer():
#     if not request.args.get('url'): return redirect('/')
#     return render_template('videoplayer.html', url=request.args.get('url'));


# @app.route('/videor/playingr/<videos>')
# def playingr(videos):
#     return render_template("videoplayerr.html ", host=host, port=port, videoe=videos)


# @app.route('/videor')
# def videor():
#     filename = request.args.get('filename')
#     return send_file("E:/server_path/relax/" + filename, mimetype='video/mp4')


# @app.route('/relaxing')
# def relax():
#     folder_pathr = r'C:\server_path/relax'
#     if not os.path.exists(folder_pathr):
#         os.makedirs(folder_pathr)
#         return f"The folder '{folder_pathr}' has been created."
#     else: 

#         videose = os.listdir('E:/server_path/relax')
#         return render_template('Relaxation.html', host=host, port=port, videos=videose )


@app.route('/Meditation')
def meditation():
    # videos = os.listdir('C:/Users/flash/Desktop/Test list/Project TUBE/uploads')
    folder_path = r'C:\server_path/meditation'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"The folder '{folder_path}' has been created."
    else: 

        videos = os.listdir('C:\server_path/meditation')
        return render_template('Meditation.html', host=host, port=port, videos=videos )

@app.route('/video')
def video():
    filename = request.args.get('filename')
    return send_file("C:\server_path/meditation/" + filename, mimetype='video/mp4')    


@app.route('/video/playing/<video>')
def playing(video):
    return render_template("videoplayer.html ", host=host, port=port, video=video)





# relaxation path 

@app.route('/relaxing')
def relaxing():
    # videos = os.listdir('C:/Users/flash/Desktop/Test list/Project TUBE/uploads')
    folder_path = r'C:\server_path/relax'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        return f"The folder '{folder_path}' has been created."
    else: 

        video = os.listdir('C:/server_path/relax')
        return render_template('Relaxation.html', host=host, port=port, videos=video )


@app.route('/videor')
def videor():
    filename = request.args.get('filename')
    return send_file("C:\server_path/relax/" + filename, mimetype='video/mp4' )
    


@app.route('/video/playing/relaxing/<videos>')
def playingr(videos):
    return render_template("videoplayerrelax.html ", host=host, port=port, video=videos)






# @app.route('/myvideos')
# def myvideos():
#     # videos = os.listdir('C:/Users/flash/Desktop/Test list/Project TUBE/uploads')
#     videos = os.listdir('D:/server_path/meditation')
#     return render_template('myvideos.html', host=host, port=port, videos=videos )





# @app.route('/myvideosr')
# def myvideosr():
#     # videos = os.listdir('C:/Users/flash/Desktop/Test list/Project TUBE/uploads')
#     videos = os.listdir('E:/server_path/relax')
#     return render_template('Relaxation.html', host=host, port=port, video=videos )


def get_wireless_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address



@app.route('/upload')
def uploads(): 
    return render_template('uploads.html')


if __name__ == "__main__":
      
    wireless_ip = get_wireless_ip()
    host= wireless_ip

    port = '5000'

    app.run(host=host,port=port,debug=True )
    # app.run(debug=True)