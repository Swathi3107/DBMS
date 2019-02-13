from flask import Flask,flash,logging,redirect,url_for,session,request
from flask import render_template
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,\
    IntegerField,RadioField,SelectField
from passlib.hash import sha256_crypt
import backend
from functools import wraps
app=Flask(__name__)
import sqlite3
from datetime import datetime,timedelta

emailid=0
shop_id=0
orderlist = []
finaltotal=0


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

class RegisterForm(Form):
    fname=StringField('First Name',[validators.Length(min=1,max=30)])
    lname=StringField('Last Name',[validators.Length(min=1,max=30)])
    phno=IntegerField('Phone number')
    gender = RadioField('Gender', choices = [('M','Male'),('F','Female')])
    age=IntegerField('Age',[validators.NumberRange(min=1,max=100)])
    address=StringField('Address',[validators.Length(min=1,max=50)])
    email=StringField('EmailID',[validators.Length(min=5,max=25)])
    password=PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm',message='Passwords do not match')
    ])
    confirm=PasswordField('Confirm password')

@app.route('/register',methods=['GET','POST'])
def register():
    form=RegisterForm(request.form)
    if request.method=='POST' and form.validate():
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()
        fname=form.fname.data
        lname=form.lname.data
        phno=form.phno.data
        gender=form.gender.data
        age=form.age.data
        address=form.address.data
        email=form.email.data
        password=sha256_crypt.encrypt(str(form.password.data))
        cur.execute("INSERT INTO CUSTOMER(FNAME,LNAME,PHNO,GENDER,AGE,ADDRESS,EMAILID,PASSWORD) VALUES(?,?,?,?,?,?,?,?)",
                    (fname, lname, phno, gender, age, address, email, password,))
        conn.commit()
        conn.close()
        flash('You are now registered and can now log in','success')

        return redirect(url_for('login'))

    return render_template('register.html',form=form)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password_candidate=request.form['password']
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()
        username=cur.execute("SELECT FNAME FROM CUSTOMER WHERE EMAILID=(?)",(str(email),)).fetchone()
        result=cur.execute("SELECT PASSWORD FROM CUSTOMER WHERE EMAILID=(?)",(str(email),)).fetchone()
        try:
            if str(result[0])!=None:
                if sha256_crypt.verify(password_candidate,result[0]):
                    app.logger.info('password matched')
                    session['logged_in'] = True
                    session['username'] = username[0]
                    session['email']=email
                    flash('You are now logged in', 'success')
                    global orderlist
                    orderlist=[]
                    global finaltotal
                    finaltotal=0
                    return redirect(url_for('hotels'))
                else:
                    #app.logger.info('password not matched')
                    error = 'Password not matched'
                    return render_template('login.html', error=error)
        except:
            error='Username not found'
            return render_template('login.html',error=error)
        conn.commit()
        conn.close()
    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    global orderlist
    orderlist = []
    global finaltotal
    finaltotal=0
    return redirect(url_for('login'))

@app.route('/hotels')
@is_logged_in
def hotels():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    shops=cur.execute("SELECT NAME FROM SHOP").fetchall()
    conn.commit()
    conn.close()
    return render_template('hotels.html',shops=shops)


@app.route('/hotel/PizzaHut/')
@is_logged_in
def pizzahut():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    shopid=1
    foods=cur.execute("SELECT NAME,PRICE FROM FOOD WHERE SHOPID=1").fetchall()
    conn.commit()
    conn.close()
    return render_template('pizzahut.html')

@app.route('/hotel/ShriSagar/')
@is_logged_in
def sagar():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    shopid=2
    foods=cur.execute("SELECT NAME,PRICE FROM FOOD WHERE SHOPID=2").fetchall()
    conn.commit()
    conn.close()
    return render_template('sagar.html')

@app.route('/hotel/Jalpan/')
@is_logged_in
def jalpan():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    shopid=3
    foods=cur.execute("SELECT NAME,PRICE FROM FOOD WHERE SHOPID=3").fetchall()
    conn.commit()
    conn.close()
    return render_template('jalpan.html')


@app.route('/hotel/BurgerKing/')
@is_logged_in
def burger():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    shopid=4
    foods=cur.execute("SELECT NAME,PRICE FROM FOOD WHERE SHOPID=4").fetchall()
    conn.commit()
    conn.close()
    return render_template('burger.html')

@app.route('/hotel/Rajdhani/')
@is_logged_in
def rajdhani():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    shopid=5
    foods=cur.execute("SELECT NAME,PRICE FROM FOOD WHERE SHOPID=5").fetchall()
    conn.commit()
    conn.close()
    return render_template('rajdhani.html')

@app.route('/hotel/Mtr/')
@is_logged_in
def mtr():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    shopid=6
    foods=cur.execute("SELECT NAME,PRICE FROM FOOD WHERE SHOPID=6").fetchall()
    conn.commit()
    conn.close()
    return render_template('mtr.html')

global idd


@app.route('/orderspizza',methods=['GET','POST'])
@is_logged_in
def orderspizza():
    if request.method == 'POST':
        shopid=1
        user=session['username']
        foodlist=["Veg Exotica","Veggie Italiano",
                  "Veggie Supreme","Country Feast","Tandoori Paneer","Spiced Paneer"]
        quanlist=[request.form['no1'],request.form['no2'],request.form['no3'],
                  request.form['no4'],request.form['no5'],request.form['no6']]
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()

        shopname = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=1").fetchone()
        custid = cur.execute("SELECT CUSTID FROM CUSTOMER WHERE FNAME=(?)", (str(user),)).fetchone()
        i = 0

        for x in range(6):
            food=foodlist[x]
            quantity=quanlist[x]
            quantity=int(quantity)
            if(quantity>0):
                price=cur.execute("SELECT PRICE FROM FOOD WHERE NAME=(?)",(str(food),)).fetchone()
                total=quantity*int(price[0])
                global finaltotal
                finaltotal=finaltotal+int(total)
                boyid=cur.execute("SELECT BOYID FROM BOY WHERE SHOPID=1").fetchone()
                cur.execute("INSERT INTO ORDERS(CUSTID,FOODNAME,PRICE,QUANTITY,TOTAL,SHOPID) VALUES(?,?,?,?,?,?)",
                            (int(custid[0]),str(food),int(price[0]),quantity,int(total),int(shopid),))

                orderlist.insert(i, [shopname, food, quantity, price[0], total])
                i = i + 1

        conn.commit()
        conn.close()

        return render_template("orders.html",orderlist=orderlist)

@app.route('/orderssagar',methods=['GET','POST'])
@is_logged_in
def orderssagar():
    if request.method == 'POST':
        shopid=2
        user = session['username']
        foodlist=["Masala Dosa","Rava Idly",
                  "Mangaluru Bajji","Idly Vada","Khara Bath","Kesari Bath"]
        quanlist=[request.form['no1'],request.form['no2'],request.form['no3'],
                  request.form['no4'],request.form['no5'],request.form['no6']]
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()

        shopname = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=2").fetchone()
        custid = cur.execute("SELECT CUSTID FROM CUSTOMER WHERE FNAME=(?)", (str(user),)).fetchone()
        i = 0

        for x in range(6):
            food=foodlist[x]
            quantity=quanlist[x]
            quantity=int(quantity)
            if(quantity>0):
                price=cur.execute("SELECT PRICE FROM FOOD WHERE NAME=(?)",(str(food),)).fetchone()
                total=quantity*int(price[0])
                global finaltotal
                finaltotal = finaltotal + int(total)
                boyid=cur.execute("SELECT BOYID FROM BOY WHERE SHOPID=2").fetchone()
                cur.execute("INSERT INTO ORDERS(CUSTID,FOODNAME,PRICE,QUANTITY,TOTAL,SHOPID) VALUES(?,?,?,?,?,?)",
                            (int(custid[0]),str(food),int(price[0]),quantity,int(total),int(shopid),))

                orderlist.insert(i, [shopname, food, quantity, price[0], total])
                i = i + 1

        conn.commit()
        conn.close()

        return render_template("orders.html",orderlist=orderlist)

@app.route('/ordersjalpan',methods=['GET','POST'])
@is_logged_in
def ordersjalpan():
    if request.method == 'POST':
        shopid=3
        user = session['username']
        foodlist=["Chole Bhature","Malai ki Kheer",
                  "Aloo Samosa","Channa Masala","Butter Nann","Roti Curry"]
        quanlist=[request.form['no1'],request.form['no2'],request.form['no3'],
                  request.form['no4'],request.form['no5'],request.form['no6']]
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()

        shopname = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=3").fetchone()
        custid = cur.execute("SELECT CUSTID FROM CUSTOMER WHERE FNAME=(?)", (str(user),)).fetchone()
        i = 0

        for x in range(6):
            food=foodlist[x]
            quantity=quanlist[x]
            quantity=int(quantity)
            if(quantity>0):
                price=cur.execute("SELECT PRICE FROM FOOD WHERE NAME=(?)",(str(food),)).fetchone()
                total=quantity*int(price[0])
                global finaltotal
                finaltotal = finaltotal + int(total)
                boyid=cur.execute("SELECT BOYID FROM BOY WHERE SHOPID=3").fetchone()
                cur.execute("INSERT INTO ORDERS(CUSTID,FOODNAME,PRICE,QUANTITY,TOTAL,SHOPID) VALUES(?,?,?,?,?,?)",
                            (int(custid[0]),str(food),int(price[0]),quantity,int(total),int(shopid),))

                orderlist.insert(i, [shopname, food, quantity, price[0], total])
                i = i + 1

        conn.commit()
        conn.close()

        return render_template("orders.html",orderlist=orderlist)

@app.route('/ordersburger',methods=['GET','POST'])
@is_logged_in
def ordersburger():
    if request.method == 'POST':
        shopid=4
        user = session['username']
        foodlist=["American Cheese Supreme","McSpicy Paneer Burger",
                  "Big Spicy Paneer Wrap","Veg Maharaja Mac","Mc Veggie","French Fries"]
        quanlist=[request.form['no1'],request.form['no2'],request.form['no3'],
                  request.form['no4'],request.form['no5'],request.form['no6']]
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()

        shopname = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=4").fetchone()
        custid = cur.execute("SELECT CUSTID FROM CUSTOMER WHERE FNAME=(?)", (str(user),)).fetchone()
        i = 0
        global finaltotal
        for x in range(6):
            food=foodlist[x]
            quantity=quanlist[x]
            quantity=int(quantity)
            if(quantity>0):
                price=cur.execute("SELECT PRICE FROM FOOD WHERE NAME=(?)",(str(food),)).fetchone()
                total=quantity*int(price[0])
                finaltotal = finaltotal + int(total)

                boyid=cur.execute("SELECT BOYID FROM BOY WHERE SHOPID=4").fetchone()
                cur.execute("INSERT INTO ORDERS(CUSTID,FOODNAME,PRICE,QUANTITY,TOTAL,SHOPID) VALUES(?,?,?,?,?,?)",
                            (int(custid[0]),str(food),int(price[0]),quantity,int(total),int(shopid),))

                orderlist.insert(i, [shopname, food, quantity, price[0], total])
                i = i + 1

        conn.commit()
        conn.close()

        return render_template("orders.html",orderlist=orderlist)

@app.route('/ordersrajdhani',methods=['GET','POST'])
@is_logged_in
def ordersrajdhani():
    if request.method == 'POST':
        shopid=5
        user = session['username']
        foodlist=["Gobi Manchuri","Butter Kulcha",
                  "Panneer Rolls","Chola Batura","Palak Panneer","Parota"]
        quanlist=[request.form['no1'],request.form['no2'],request.form['no3'],
                  request.form['no4'],request.form['no5'],request.form['no6']]
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()

        shopname = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=5").fetchone()
        custid = cur.execute("SELECT CUSTID FROM CUSTOMER WHERE FNAME=(?)", (str(user),)).fetchone()
        i = 0

        for x in range(6):
            food=foodlist[x]
            quantity=quanlist[x]
            quantity=int(quantity)
            if(quantity>0):
                price=cur.execute("SELECT PRICE FROM FOOD WHERE NAME=(?)",(str(food),)).fetchone()
                total=quantity*int(price[0])
                global finaltotal
                finaltotal = finaltotal + int(total)
                boyid=cur.execute("SELECT BOYID FROM BOY WHERE SHOPID=5").fetchone()
                cur.execute("INSERT INTO ORDERS(CUSTID,FOODNAME,PRICE,QUANTITY,TOTAL,SHOPID) VALUES(?,?,?,?,?,?)",
                            (int(custid[0]),str(food),int(price[0]),quantity,int(total),int(shopid),))

                orderlist.insert(i, [shopname, food, quantity, price[0], total])
                i = i + 1

        conn.commit()
        conn.close()

        return render_template("orders.html",orderlist=orderlist)

@app.route('/ordersmtr',methods=['GET','POST'])
@is_logged_in
def ordersmtr():
    if request.method == 'POST':
        shopid=6
        user = session['username']
        foodlist=["Masala Vada","Pani puri",
                  "Puri Saagu","Masal Dosa","Chapathi","Bonda"]
        quanlist=[request.form['no1'],request.form['no2'],request.form['no3'],
                  request.form['no4'],request.form['no5'],request.form['no6']]
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()

        shopname=cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=6").fetchone()
        custid = cur.execute("SELECT CUSTID FROM CUSTOMER WHERE FNAME=(?)", (str(user),)).fetchone()
        i=0

        for x in range(6):
            food=foodlist[x]
            quantity=quanlist[x]
            quantity=int(quantity)
            if(quantity>0):
                price=cur.execute("SELECT PRICE FROM FOOD WHERE NAME=(?)",(str(food),)).fetchone()
                total=quantity*int(price[0])
                global finaltotal
                finaltotal = finaltotal + int(total)
                boyid=cur.execute("SELECT BOYID FROM BOY WHERE SHOPID=6").fetchone()
                cur.execute("INSERT INTO ORDERS(CUSTID,FOODNAME,PRICE,QUANTITY,TOTAL,SHOPID) VALUES(?,?,?,?,?,?)",
                            (int(custid[0]),str(food),int(price[0]),quantity,int(total),int(shopid),))

                orderlist.insert(i,[shopname,food,quantity,price[0],total])
                i=i+1

        conn.commit()
        conn.close()

        return render_template("orders.html",orderlist=orderlist)

@app.route('/bill',methods=['GET','POST'])
@is_logged_in
def bill():
    global finaltotal
    finaltotal=finaltotal*1.18
    now = datetime.now()
    now_plus_10 = now + timedelta(minutes=25)
    return render_template("bill.html",finaltotal=finaltotal,datee=now_plus_10.time())

@app.route('/boylogin',methods=['GET','POST'])
def boylogin():
    if request.method=='POST':
        boyname=request.form['name']
        boyname=str(boyname)
        conn = sqlite3.connect("learnfood.db")
        cur = conn.cursor()

        if boyname=="delpiz":
            custname = []
            custno = []
            custaddr = []
            shopname = []
            shopaddr = []
            ord2 = cur.execute("SELECT ORDERID FROM ORDERS WHERE SHOPID=1").fetchall()
            item2 = cur.execute("SELECT FOODNAME FROM ORDERS WHERE SHOPID=1").fetchall()
            quan2 = cur.execute("SELECT QUANTITY FROM ORDERS WHERE SHOPID=1").fetchall()
            cust2 = cur.execute("SELECT CUSTID FROM ORDERS WHERE SHOPID=1").fetchall()
            shop2 = cur.execute("SELECT SHOPID FROM ORDERS WHERE SHOPID=1").fetchall()
            for idd in cust2:
                name = cur.execute("SELECT FNAME FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custaddr.append(str(name[0]))
                name = cur.execute("SELECT PHNO FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custno.append(str(name[0]))

            for iddd in shop2:
                name = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopaddr.append(str(name[0]))

            return render_template("boylogin.html", ord=ord2, names=custname, address=custaddr, phnos=custno,
                                   items=item2, quan=quan2, shop=shopname, shopa=shopaddr)
        if boyname=="delsag":
            custname = []
            custno=[]
            custaddr=[]
            shopname=[]
            shopaddr=[]
            ord2 = cur.execute("SELECT ORDERID FROM ORDERS WHERE SHOPID=2").fetchall()
            item2 = cur.execute("SELECT FOODNAME FROM ORDERS WHERE SHOPID=2").fetchall()
            quan2 = cur.execute("SELECT QUANTITY FROM ORDERS WHERE SHOPID=2").fetchall()
            cust2 = cur.execute("SELECT CUSTID FROM ORDERS WHERE SHOPID=2").fetchall()
            shop2 = cur.execute("SELECT SHOPID FROM ORDERS WHERE SHOPID=2").fetchall()
            for idd in cust2:
                name=cur.execute("SELECT FNAME FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custaddr.append(str(name[0]))
                name = cur.execute("SELECT PHNO FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custno.append(str(name[0]))

            for iddd in shop2:
                name = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopaddr.append(str(name[0]))

            return render_template("boylogin.html", ord=ord2,names=custname,address=custaddr,phnos=custno,items=item2,quan=quan2,shop=shopname,shopa=shopaddr)
        if boyname=="deljal":
            custname = []
            custno = []
            custaddr = []
            shopname = []
            shopaddr = []
            ord2 = cur.execute("SELECT ORDERID FROM ORDERS WHERE SHOPID=3").fetchall()
            item2 = cur.execute("SELECT FOODNAME FROM ORDERS WHERE SHOPID=3").fetchall()
            quan2 = cur.execute("SELECT QUANTITY FROM ORDERS WHERE SHOPID=3").fetchall()
            cust2 = cur.execute("SELECT CUSTID FROM ORDERS WHERE SHOPID=3").fetchall()
            shop2 = cur.execute("SELECT SHOPID FROM ORDERS WHERE SHOPID=3").fetchall()
            for idd in cust2:
                name = cur.execute("SELECT FNAME FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custaddr.append(str(name[0]))
                name = cur.execute("SELECT PHNO FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custno.append(str(name[0]))

            for iddd in shop2:
                name = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopaddr.append(str(name[0]))

            return render_template("boylogin.html", ord=ord2, names=custname, address=custaddr, phnos=custno,
                                   items=item2, quan=quan2, shop=shopname, shopa=shopaddr)
        if boyname=="delbur":
            custname = []
            custno = []
            custaddr = []
            shopname = []
            shopaddr = []
            ord2 = cur.execute("SELECT ORDERID FROM ORDERS WHERE SHOPID=4").fetchall()
            item2 = cur.execute("SELECT FOODNAME FROM ORDERS WHERE SHOPID=4").fetchall()
            quan2 = cur.execute("SELECT QUANTITY FROM ORDERS WHERE SHOPID=4").fetchall()
            cust2 = cur.execute("SELECT CUSTID FROM ORDERS WHERE SHOPID=4").fetchall()
            shop2 = cur.execute("SELECT SHOPID FROM ORDERS WHERE SHOPID=4").fetchall()
            for idd in cust2:
                name = cur.execute("SELECT FNAME FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custaddr.append(str(name[0]))
                name = cur.execute("SELECT PHNO FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custno.append(str(name[0]))

            for iddd in shop2:
                name = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopaddr.append(str(name[0]))

            return render_template("boylogin.html", ord=ord2, names=custname, address=custaddr, phnos=custno,
                                   items=item2, quan=quan2, shop=shopname, shopa=shopaddr)
        if boyname=="delraj":
            custname = []
            custno = []
            custaddr = []
            shopname = []
            shopaddr = []
            ord2 = cur.execute("SELECT ORDERID FROM ORDERS WHERE SHOPID=5").fetchall()
            item2 = cur.execute("SELECT FOODNAME FROM ORDERS WHERE SHOPID=5").fetchall()
            quan2 = cur.execute("SELECT QUANTITY FROM ORDERS WHERE SHOPID=5").fetchall()
            cust2 = cur.execute("SELECT CUSTID FROM ORDERS WHERE SHOPID=5").fetchall()
            shop2 = cur.execute("SELECT SHOPID FROM ORDERS WHERE SHOPID=5").fetchall()
            for idd in cust2:
                name = cur.execute("SELECT FNAME FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custaddr.append(str(name[0]))
                name = cur.execute("SELECT PHNO FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custno.append(str(name[0]))

            for iddd in shop2:
                name = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopaddr.append(str(name[0]))

            return render_template("boylogin.html", ord=ord2, names=custname, address=custaddr, phnos=custno,
                                   items=item2, quan=quan2, shop=shopname, shopa=shopaddr)
        if boyname=="delmtr":
            custname = []
            custno = []
            custaddr = []
            shopname = []
            shopaddr = []
            ord2 = cur.execute("SELECT ORDERID FROM ORDERS WHERE SHOPID=6").fetchall()
            item2 = cur.execute("SELECT FOODNAME FROM ORDERS WHERE SHOPID=6").fetchall()
            quan2 = cur.execute("SELECT QUANTITY FROM ORDERS WHERE SHOPID=6").fetchall()
            cust2 = cur.execute("SELECT CUSTID FROM ORDERS WHERE SHOPID=6").fetchall()
            shop2 = cur.execute("SELECT SHOPID FROM ORDERS WHERE SHOPID=6").fetchall()
            for idd in cust2:
                name = cur.execute("SELECT FNAME FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custaddr.append(str(name[0]))
                name = cur.execute("SELECT PHNO FROM CUSTOMER WHERE CUSTID=(?)", (idd[0],)).fetchone()
                custno.append(str(name[0]))

            for iddd in shop2:
                name = cur.execute("SELECT NAME FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopname.append(str(name[0]))
                name = cur.execute("SELECT ADDRESS FROM SHOP WHERE SHOPID=(?)", (iddd[0],)).fetchone()
                shopaddr.append(str(name[0]))

            return render_template("boylogin.html", ord=ord2, names=custname, address=custaddr, phnos=custno,
                                   items=item2, quan=quan2, shop=shopname, shopa=shopaddr)
        else:
            flash("Boy Login name wrong",'danger')

        conn.commit()
        conn.close()
    return render_template("boylogin.html")



if __name__=="__main__":
    app.secret_key='secret123'
    app.debug=True
    app.run()
