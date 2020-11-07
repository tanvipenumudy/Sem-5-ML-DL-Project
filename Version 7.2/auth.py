from werkzeug.security import generate_password_hash, check_password_hash
from flask import Blueprint, render_template, redirect, url_for, request, flash, send_file
from app import db
from flask_login import login_user
from models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask import Markup
import datetime
import numpy as np
import os
from fpdf import FPDF
from model.load import *
from model.load1 import *
from model.load2 import *
from model.load3 import *
from model.load4 import *

auth = Blueprint('auth', __name__)
app_root = os.path.dirname(os.path.abspath(__file__))

def MonthCal(deadline):
    currentDate = datetime.datetime.now()
    deadlineDate= datetime.datetime.strptime(deadline,'%d-%m-%Y')
    daysLeft = deadlineDate - currentDate
    years = ((daysLeft.total_seconds())/(365.242*24*3600))
    yearsInt=int(years)
    months=(years-yearsInt)*12
    monthsInt=int(months)
    BTM = (yearsInt*12)+monthsInt
    BTM = abs(BTM)
    return BTM

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index')) 

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')
    if(email == '' or name == '' or password == ''):
            flash('Please enter all the fields.')
            return redirect(url_for('auth.signup'))
    user = User.query.filter_by(email=email).first() 
    if(user): 
        flash(Markup('Email address already exists. Please go to <a href="http://127.0.0.1:5000/login" class="alert-link">Login Page</a>'))
        return redirect(url_for('auth.signup'))
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()   
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))
    login_user(user, remember=remember)
    return redirect(url_for('profile'))

@auth.route('/about')
@login_required
def about():
    return render_template('about.html', name=current_user.name)

@auth.route('/schonell', methods=['GET', 'POST'])
@login_required
def schonell():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.schonell = req['score']
        db.session.commit()
        model, model1 = init()
        pred = model.predict([[MonthCal(user.dob),user.schonell]])
        classes = pred[0]
        final=np.where(classes==max(classes))
        if(final[0]==0):
            sch = "Good"
        elif(final[0]==1):
            sch = "Mild"
        elif(final[0]==2):
            sch = "Average"
        elif(final[0]==3):
            sch = "Severe"
        elif(final[0]==4):
            sch = "Well"
        print(sch)
        user.sch = sch
        db.session.commit()
        pred1 = model1.predict([[user.schonell]])
        ans = int(round(pred1[0][0]))
        print(ans)
        user.sch1 = ans
        db.session.commit()
    return render_template('schonell.html')

@auth.route('/wepman', methods=['GET', 'POST'])
@login_required
def wepman():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.wepman = req['score']
        db.session.commit()
        model = init2()
        pred = model.predict([[user.wepman*2.5]])
        if(pred[0]==0):
            wep = "No"
        else:
            wep = "Yes"
        print(wep)
        user.wep = wep
        db.session.commit()
    return render_template('wepman.html')

@auth.route('/burt', methods=['GET', 'POST'])
@login_required
def burt():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.burt = req['score']
        db.session.commit()
        model, model1 = init1()
        pred = model.predict([[MonthCal(user.dob),user.burt]])
        classes = pred[0]
        final=np.where(classes==max(classes))
        if(final[0]==0):
            bur = "Good"
        elif(final[0]==1):
            bur = "Mild"
        elif(final[0]==2):
            bur = "Average"
        elif(final[0]==3):
            bur = "Severe"
        elif(final[0]==4):
            bur = "Well"
        print(bur)
        user.bur = bur
        db.session.commit()
        pred1 = model1.predict([[user.burt]])
        ans = int(round(pred1[0][0]))
        print(ans)
        user.bur1 = ans
        db.session.commit()
    return render_template('burt.html')

@auth.route('/score', methods=['GET', 'POST'])
@login_required
def score():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    return render_template('score.html', schonell=user.schonell, wepman=user.wepman, burt=user.burt, memory=user.memory, passage=user.passage, clas=user.clas)

@auth.route('/passage1', methods=['GET', 'POST'])
@login_required
def passage1():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.passage = req['score']
        user.passtime = req['time']
        db.session.commit()
        model, mm = init3()
        res = np.array([[1,user.passage,user.passtime]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            pas = "Mild"
        elif(pred[0]==1):
            pas = "No"
        else:
            pas = "Yes"
        print(pas)
        user.pas = pas
        db.session.commit()
    return render_template('passage1.html')

@auth.route('/passage2', methods=['GET', 'POST'])
@login_required
def passage2():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.passage = req['score']
        user.passtime = req['time']
        db.session.commit()
        model, mm = init3()
        res = np.array([[2,user.passage,user.passtime]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            pas = "Mild"
        elif(pred[0]==1):
            pas = "No"
        else:
            pas = "Yes"
        print(pas)
        user.pas = pas
        db.session.commit()
    return render_template('passage2.html')

@auth.route('/passage3', methods=['GET', 'POST'])
@login_required
def passage3():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.passage = req['score']
        user.passtime = req['time']
        db.session.commit()
        model, mm = init3()
        res = np.array([[3,user.passage,user.passtime]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            pas = "Mild"
        elif(pred[0]==1):
            pas = "No"
        else:
            pas = "Yes"
        print(pas)
        user.pas = pas
        db.session.commit()
    return render_template('passage3.html')

@auth.route('/passage4', methods=['GET', 'POST'])
@login_required
def passage4():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.passage = req['score']
        user.passtime = req['time']
        db.session.commit()
        model, mm = init3()
        res = np.array([[4,user.passage,user.passtime]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            pas = "Mild"
        elif(pred[0]==1):
            pas = "No"
        else:
            pas = "Yes"
        print(pas)
        user.pas = pas
        db.session.commit()
    return render_template('passage4.html')

@auth.route('/passage5', methods=['GET', 'POST'])
@login_required
def passage5():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.passage = req['score']
        user.passtime = req['time']
        db.session.commit()
        model, mm = init3()
        res = np.array([[5,user.passage,user.passtime]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            pas = "Mild"
        elif(pred[0]==1):
            pas = "No"
        else:
            pas = "Yes"
        print(pas)
        user.pas = pas
        db.session.commit()
    return render_template('passage5.html')

@auth.route('/passage6', methods=['GET', 'POST'])
@login_required
def passage6():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.passage = req['score']
        user.passtime = req['time']
        db.session.commit()
        model, mm = init3()
        res = np.array([[6,user.passage,user.passtime]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            pas = "Mild"
        elif(pred[0]==1):
            pas = "No"
        else:
            pas = "Yes"
        print(pas)
        user.pas = pas
        db.session.commit()
    return render_template('passage6.html')

@auth.route('/passage7', methods=['GET', 'POST'])
@login_required
def passage7():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.passage = req['score']
        user.passtime = req['time']
        db.session.commit()
        model, mm = init3()
        res = np.array([[7,user.passage,user.passtime]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            pas = "Mild"
        elif(pred[0]==1):
            pas = "No"
        else:
            pas = "Yes"
        print(pas)
        user.pas = pas
        db.session.commit()
    return render_template('passage7.html')

@auth.route('/forward', methods=['GET', 'POST'])
@login_required
def forward():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.memory = req['score']
        db.session.commit()
    return render_template('forward.html')

@auth.route('/backward1', methods=['GET', 'POST'])
@login_required
def backward1():
    return render_template('backward.html')

@auth.route('/backward', methods=['GET', 'POST'])
@login_required
def backward():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    if(request.method == 'POST'):
        req = request.get_json()
        user.memory = user.memory + req['score']
        db.session.commit()
        model, model1, mm, mm1 = init4()
        res = np.array([[MonthCal(user.dob),user.memory]])
        res = mm.transform(res)
        pred = model.predict(res)
        if(pred[0]==0):
            mem = "Good"
        elif(pred[0]==1):
            mem = "Mild"
        elif(pred[0]==2):
            mem = "Average"
        elif(pred[0]==3):
            mem = "Severe"
        elif(pred[0]==4):
            mem = "Well"
        print(mem)
        user.mem = mem
        db.session.commit()
        res1 = np.array([[user.memory]])
        res1 = mm1.transform(res1)
        pred1 = model1.predict(res1)
        ans = int(round(pred1[0]))
        print(ans)
        user.mem1 = ans
        db.session.commit()
    return render_template('backward.html')

@auth.route('/download', methods=['GET','POST'])
@login_required
def download():
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    return render_template('download.html', schonell=user.schonell, wepman=user.wepman, burt=user.burt, memory=user.memory, passage=user.passage, clas=user.clas)

@auth.route('/generate', methods=['GET','POST'])
@login_required
def generate():
    from datetime import date
    from datetime import datetime
    from app import current_user
    user = User.query.get_or_404(current_user.id)
    # uid = str(user.id)
    # source = os.path.join(app_root,'reports')
    # if(not os.path.exists(source)):
    #    os.makedirs(source)
    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    now = datetime.now()
    dt = now.strftime("%d/%m/%Y %H:%M:%S")
    pdf = FPDF() 
    pdf.add_page() 
    pdf.set_font("Arial") 
    pdf.cell(200, 20, txt = "Informal Educational Assessment Report for LD",  ln = 1, align = 'C') 
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Child's Details -", ln = 2, align = 'L')
    pdf.cell(200, 10, txt = "Name: "+user.cname, ln = 2, align = 'L')
    pdf.cell(200, 10, txt = "Date of Assessment: "+d1, ln = 2, align = 'L')
    pdf.cell(200, 10, txt = "DOB: "+user.dob, ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Gender: "+user.gender, ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'School: '+user.school, ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Class: "+str(user.clas), ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = "Mother Tongue: "+user.lang, ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Mother's Name: " +user.mother, ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Father's Name: "+user.father, ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = "Parental Concerns: "+user.concern, ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Learning Assessment Results and Performance - ", ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Test-I: Schonell's Spelling Test -", ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "i. Schonell's Test Score: " +str(user.schonell), ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "ii. Spelling Age: "+str((user.sch1)//12)+' years'+' '+str((user.sch1)%12)+' months'+'*', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = "iii. Schonell's Test (Performance): "+user.sch+'*', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Test-II: Burt's Reading Test -", ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = "i. Burt's Test Score: " +str(user.burt), ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "ii. Reading Age: "+str((user.bur1)//12)+' years'+' '+str((user.bur1)%12)+' months'+'*', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = "iii. Burt's Test (Performance): "+user.bur+'*', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L')
    pdf.cell(200, 10, txt = "Test-III: Auditory Sequential Memory Test (Digit Span) -", ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "i. Auditory Sequential Memory Test Score: " +str(user.memory), ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "ii. Auditory Sequential Memory Age: "+str((user.mem1)//12)+' years'+' '+str((user.mem1)%12)+' months', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = "iii. ASM Test (Performance): "+user.mem, ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Test-IV: Wepman's Auditory Discrimination Test -", ln = 2, align = 'L')   
    pdf.cell(200, 10, txt = "i. Wepman's Test Score: " +str(user.wepman), ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "ii. Auditory Disability: "+user.wep+'*', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "Test-V: Grade-Level Comprehensive Understanding Test -", ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "i. Comprehensive Understanding Test Score: " +str(user.passage), ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = "ii. Comprehensive Understanding Difficulty: "+user.pas, ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = 'Performance Level - ', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = 'Severe - Needs Remediation', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = 'Mild - Observation Required, Needs to Review after 1 Year ', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = 'Average - Performing on an Average Level', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = 'Good - Performing Above Average', ln = 2, align = 'L')
    pdf.cell(200, 10, txt = 'Well - Performing Really Well', ln = 2, align = 'L')
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L')  
    pdf.cell(200, 10, txt = '*Upto 98 Percent Accurate', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = '', ln = 2, align = 'L') 
    pdf.cell(200, 10, txt = 'Report Generated on '+dt, ln = 2, align = 'C') 
    source1 = os.path.join(app_root,"Report.pdf")
    pdf.output(source1)
    # source1 = os.path.join(app_root,"Report.pdf")
    return send_file(source1, as_attachment=True)

@auth.route('/account_set')
@login_required
def account_set():
	return render_template('settings.html')

@auth.route('/meditate')
@login_required
def meditate():
	return render_template('meditate.html')

@auth.route('/set1', methods=["GET", "POST"])
@login_required
def set1():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('setting1.html')
    else:
        new_email = request.form.get('email')
        if(new_email == ''):
            flash('Email field is left blank.')
            return redirect(url_for('auth.set1'))

        user = User.query.get_or_404(current_user.id)
        user.email = new_email
        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.set1'))
        flash('Successfully Updated!')
        return redirect(url_for('auth.set1'))

@auth.route('/set2', methods=["GET", "POST"])
@login_required
def set2():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('setting2.html')
    else:
        new_psw = request.form.get('password')
        con_psw = request.form.get('confirmpass')
        if(new_psw == '' or con_psw == ''):
            flash('Password field is left blank.')
            return redirect(url_for('auth.set2'))
        if(new_psw != con_psw):
            flash('Passwords do not match')
            return redirect(url_for('auth.set2'))
        passhash = generate_password_hash(new_psw, method='sha256')
        user = User.query.get_or_404(current_user.id)
        user.password = passhash
        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.set2'))
        flash('Successfully Updated!')
        return redirect(url_for('auth.set2'))

@auth.route('/details', methods=['GET','POST'])
@login_required
def details():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('details.html')
    else:
        user = User.query.get_or_404(current_user.id)
        cname = request.form.get('cname')
        dob = request.form.get('dob')
        temp = dob.split("-")
        temp = temp[::-1]
        dob = '-'.join(temp)
        school = request.form.get('school')
        clas = request.form.get('clas')
        gender = request.form.get('gender')
        lang = request.form.get('lang')
        mother = request.form.get('mother')
        father = request.form.get('father')
        phone = request.form.get('phone')
        location = request.form.get('location')
        concern = request.form.get('concern')
        user.cname = cname
        user.dob = dob
        user.school = school
        user.clas = clas
        user.gender = gender
        user.lang = lang
        user.mother = mother
        user.father = father
        user.phone = phone
        user.location = location
        user.concern = concern
        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.details'))
        return redirect(url_for('auth.change'))


@auth.route('/change')
@login_required
def change():
    user = User.query.get_or_404(current_user.id)
    cname=user.cname 
    dob=user.dob
    school=user.school  
    clas=user.clas 
    gender=user.gender 
    lang=user.lang  
    mother=user.mother 
    father=user.father 
    phone=user.phone 
    location=user.location 
    concern=user.concern
    return render_template('change.html', cname=cname, dob=dob, school=school, clas=clas, gender=gender, lang=lang, mother=mother, father=father, phone=phone, location=location, concern=concern)

@auth.route('/change1')
@login_required
def change1():
    user = User.query.get_or_404(current_user.id)
    cname=user.cname 
    dob=user.dob
    school=user.school  
    clas=user.clas 
    gender=user.gender 
    lang=user.lang  
    mother=user.mother 
    father=user.father 
    phone=user.phone 
    location=user.location 
    concern=user.concern
    return render_template('change1.html', cname=cname, dob=dob, school=school, clas=clas, gender=gender, lang=lang, mother=mother, father=father, phone=phone, location=location, concern=concern)

@auth.route('/cname', methods=['GET','POST'])
@login_required
def cname():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('cname.html')
    else:
        user = User.query.get_or_404(current_user.id)
        cname = request.form.get('cname')
        user.cname = cname

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.cname'))
        return redirect(url_for('auth.change'))

@auth.route('/dob', methods=['GET','POST'])
@login_required
def dob():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('dob.html')
    else:
        user = User.query.get_or_404(current_user.id)
        dob = request.form.get('dob')
        temp = dob.split("-")
        temp = temp[::-1]
        dob = '-'.join(temp)
        user.dob = dob
        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.dob'))
        return redirect(url_for('auth.change'))

@auth.route('/school', methods=['GET','POST'])
@login_required
def school():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('school.html')
    else:
        user = User.query.get_or_404(current_user.id)
        school = request.form.get('school')
        user.school = school

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.school'))
        return redirect(url_for('auth.change'))

@auth.route('/clas', methods=['GET','POST'])
@login_required
def clas():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('clas.html')
    else:
        user = User.query.get_or_404(current_user.id)
        clas = request.form.get('clas')
        user.clas = clas

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.clas'))
        return redirect(url_for('auth.change'))

@auth.route('/gender', methods=['GET','POST'])
@login_required
def gender():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('gender.html')
    else:
        user = User.query.get_or_404(current_user.id)
        gender = request.form.get('gender')
        user.gender = gender

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.gender'))
        return redirect(url_for('auth.change'))

@auth.route('/lang', methods=['GET','POST'])
@login_required
def lang():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('lang.html')
    else:
        user = User.query.get_or_404(current_user.id)
        lang = request.form.get('lang')
        user.lang = lang

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.lang'))
        return redirect(url_for('auth.change'))

@auth.route('/mother', methods=['GET','POST'])
@login_required
def mother():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('mother.html')
    else:
        user = User.query.get_or_404(current_user.id)
        mother = request.form.get('mother')
        user.mother = mother

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.mother'))
        return redirect(url_for('auth.change'))

@auth.route('/father', methods=['GET','POST'])
@login_required
def father():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('father.html')
    else:
        user = User.query.get_or_404(current_user.id)
        father = request.form.get('father')
        user.father = father

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.father'))
        return redirect(url_for('auth.change'))

@auth.route('/phone', methods=['GET','POST'])
@login_required
def phone():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('phone.html')
    else:
        user = User.query.get_or_404(current_user.id)
        phone = request.form.get('phone')
        user.phone = phone

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.phone'))
        return redirect(url_for('auth.change'))
    
@auth.route('/location', methods=['GET','POST'])
@login_required
def location():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('location.html')
    else:
        user = User.query.get_or_404(current_user.id)
        location = request.form.get('location')
        user.location = location

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.location'))
        return redirect(url_for('auth.change'))

@auth.route('/concern', methods=['GET','POST'])
@login_required
def concern():
    from app import current_user
    if(request.method == 'GET'):
        return render_template('concern.html')
    else:
        user = User.query.get_or_404(current_user.id)
        concern = request.form.get('concern')
        user.concern = concern

        try:
            db.session.commit()
        except:
            flash('Technical error, failed to update')
            return redirect(url_for('auth.concern'))
        return redirect(url_for('auth.change'))

@auth.route('/delete')
def delete():
    return render_template('delete.html')

@auth.route('/cancel account')
def cancel():
    from app import current_user
    if current_user is None:
        return redirect(url_for('index'))
    try:
        db.session.delete(current_user)
        db.session.commit()
    except:
        return 'unable to delete the user.'
    flash('Your account has been deleted')
    return redirect(url_for('auth.login'))



