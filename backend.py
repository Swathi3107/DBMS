import sqlite3

def connect():
	conn = sqlite3.connect("learnfood.db")
	cur = conn.cursor()

	cur.execute("CREATE TABLE IF NOT EXISTS CUSTOMER(CUSTID INTEGER PRIMARY KEY autoincrement,\
				FNAME TEXT,LNAME TEXT,\
				PHNO NUMBER,GENDER TEXT,AGE NUMBER,ADDRESS TEXT,EMAILID TEXT,PASSWORD TEXT)")

	cur.execute("CREATE TABLE IF NOT EXISTS SHOP(SHOPID INTEGER PRIMARY KEY AUTOINCREMENT,\
				NAME TEXT,ADDRESS TEXT,PHNO INTEGER)")
	cur.execute("CREATE TABLE IF NOT EXISTS FOOD(FOODID INTEGER PRIMARY KEY AUTOINCREMENT,\
					NAME TEXT,PRICE NUMBER,SHOPID INTEGER,\
					FOREIGN KEY(SHOPID) REFERENCES SHOP(SHOPID))")
	cur.execute("CREATE TABLE IF NOT EXISTS BOY(BOYID INTEGER PRIMARY KEY AUTOINCREMENT,\
				NAME TEXT,PHNO INTEGER,SHOPID INTEGER,\
				FOREIGN KEY(SHOPID) REFERENCES SHOP(SHOPID))")

	cur.execute("CREATE TABLE IF NOT EXISTS ORDERS(ORDERID INTEGER PRIMARY KEY AUTOINCREMENT,\
				CUSTID INTEGER,FOODNAME TEXT,PRICE INTEGER,QUANTITY INTEGER,TOTAL INTEGER,\
				SHOPID INTEGER,\
				FOREIGN KEY(SHOPID) REFERENCES SHOP(SHOPID),\
				FOREIGN KEY(CUSTID) REFERENCES CUSTOMER(CUSTID))")

	conn.commit()
	conn.close()

def insert_hotel():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO SHOP(NAME,ADDRESS,PHNO) VALUES (?,?,?)", ("Pizza Hut","Vijayanagar",9575215214))
    cur.execute("INSERT INTO SHOP(NAME,ADDRESS,PHNO) VALUES (?,?,?)", ("Shri Sagar","Basaveshwaranagar",9577458214))
    cur.execute("INSERT INTO SHOP(NAME,ADDRESS,PHNO) VALUES (?,?,?)", ("Jalpan","Rajajinagar",9575856914))
    cur.execute("INSERT INTO SHOP(NAME,ADDRESS,PHNO) VALUES (?,?,?)", ("Burger King","Jayanagar",9571236214))
    cur.execute("INSERT INTO SHOP(NAME,ADDRESS,PHNO) VALUES (?,?,?)", ("Rajdhani","Chandra Layout",9575478514))
    cur.execute("INSERT INTO SHOP(NAME,ADDRESS,PHNO) VALUES (?,?,?)", ("MTR","Vijayanagar",9575452314))
    conn.commit()
    conn.close()

def insert_food():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Veg Exotica",360,1))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Veggie Italiano",499,1))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Veggie Supreme",425,1))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Country Feast",275,1))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Tandoori Paneer",350,1))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Spiced Paneer",415,1))

    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Masala Dosa",40,2))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Rava Idly",35,2))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Mangaluru Bajji",30,2))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Idly Vada",25,2))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Khara Bath",30,2))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Kesari Bath",35,2))

    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Chole Bhature",75,3))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Malai ki Kheer",150,3))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Aloo Samosa",45,3))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Channa Masala",150,3))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Butter Nann",65,3))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Roti Curry",40,3))

    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("American Cheese Supreme",250,4))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("McSpicy Paneer Burger",275,4))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Big Spicy Paneer Wrap",180,4))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Veg Maharaja Mac",250,4))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Mc Veggie",175,4))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("French Fries",125,4))

    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Gobi Manchuri",175,5))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Butter Kulcha",50,5))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Panneer Rolls",150,5))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Chola Batura",200,5))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Palak Panneer",150,5))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Parota",55,5))

    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Masala Vada",20,6))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Pani puri",25,6))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Puri Saagu",35,6))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Masal Dosa",45,6))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Chapathi",50,6))
    cur.execute("INSERT INTO FOOD(NAME,PRICE,SHOPID) VALUES(?,?,?)",("Bonda",35,6))

    conn.commit()
    conn.close()

def insert_boy():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()

    cur.execute("INSERT INTO BOY(NAME,PHNO,SHOPID) VALUES(?,?,?)",("delpiz",9852147852,1))
    cur.execute("INSERT INTO BOY(NAME,PHNO,SHOPID) VALUES(?,?,?)",("delsag",8523698521,2))
    cur.execute("INSERT INTO BOY(NAME,PHNO,SHOPID) VALUES(?,?,?)",("deljal",8745693257,3))
    cur.execute("INSERT INTO BOY(NAME,PHNO,SHOPID) VALUES(?,?,?)",("delbur",9854745896,4))
    cur.execute("INSERT INTO BOY(NAME,PHNO,SHOPID) VALUES(?,?,?)",("delraj",9856332254,5))
    cur.execute("INSERT INTO BOY(NAME,PHNO,SHOPID) VALUES(?,?,?)",("delmtr",9898986589,6))

    conn.commit()
    conn.close()


#connect()
#insert_hotel()
#insert_food()
#insert_boy()

def tri():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()

    cur.execute("create trigger if not exists calculate after insert on orders begin update orders set total = new.total*1.18 where orderid=new.orderid;end")
    cur.execute("CREATE TRIGGER trg_validate_products_before_insert BEFORE INSERT ON ORDERS BEGIN SELECT CASE WHEN NEW.quantity < 0 THEN RAISE(ABORT, 'Invalid Quantity') END;END;")
    conn.commit()
    conn.close()

#tri()
def stored_procedure():
    conn = sqlite3.connect("learnfood.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS SHOPBOY(SHOPID INTEGER PRIMARY KEY,BOYID INTEGER)")
    cur.execute("INSERT INTO SHOPBOY VALUES(1,1)")
    cur.execute("INSERT INTO SHOPBOY VALUES(2,2)")
    cur.execute("INSERT INTO SHOPBOY VALUES(3,3)")
    cur.execute("INSERT INTO SHOPBOY VALUES(4,4)")
    cur.execute("INSERT INTO SHOPBOY VALUES(5,5)")
    cur.execute("INSERT INTO SHOPBOY VALUES(6,6)")
    conn.commit()
    conn.close()
#stored_procedure()


# create procedure Menu
# @hotel varchar(20)
# as
# select * from hotels
# where hotel=@hotel
# go;

# exec Menu
# hotel="Pizza Hut";






