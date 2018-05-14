import datetime
import sqlite3

from flask import *


class Item(object):
    def __init__(self, tTime, dDate, name, phone, message, orderType, id):
        self.tTime = tTime
        self.dDate = dDate
        self.name = name
        self.phone = phone
        self.message = message
        self.orderType = orderType
        self.id = id


app = Flask(__name__)


@app.route('/clear_db/<id>')
def clear_db(id):
    try:
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute('DELETE FROM orders WHERE id=?', (id,))
        conn.commit()
    except Exception as e:
        print("Exception", e)
    finally:
        conn.close()

    if id == "aAll":
        print("wanna clear id : ", id)
        conn = sqlite3.connect('orders.db')
        c = conn.cursor()
        c.execute('''DROP TABLE orders''')
        c.execute(
            '''CREATE TABLE orders(id integer PRIMARY KEY, tTime text ,dDate text , name text, phone text, orderMsg text, orderType text)''')
        conn.commit()
        c.close()
    return redirect(url_for('index_page'))


@app.route('/', methods=['POST', 'GET'])
def index_page():
    orderTypeList = []
    orderTypeList.append("Breakfast")
    orderTypeList.append("Lunch")
    orderTypeList.append("Dinner")
    orderTypeList.append("Night")
    orderTypeList.append("Special")

    currentOrders = []

    conn = sqlite3.connect('orders.db')

    c = conn.cursor()

    c.execute('''SELECT * FROM orders''')
    current = c.fetchall()
    querydate = ""

    if len(request.form) != 0:
        if request.form['timeDate'] != None:
            querydate = request.form['timeDate']

    # Load All The DateBase To Vars
    for item in current:
        iId = item[0]
        tTimeVal = item[1]
        dDateVal = item[2]
        name = item[3]
        phone = item[4]
        message = item[5]
        orderType = item[6]

        dDate = datetime.datetime.now().strftime("%d-%m-%y")
        tTime = datetime.datetime.now().strftime("%H:%M:%S")
        if dDate not in dDateVal:
            continue

        if querydate != "All Day" and querydate != "":
            if orderType == querydate:
                currentOrders.append(
                    Item(tTime=tTime, dDate=dDate, name=name, phone=phone, message=message, orderType=orderType,
                         id=iId))
        else:
            currentOrders.append(
                Item(tTime=tTime, dDate=dDate, name=name, phone=phone, message=message, orderType=orderType, id=iId))

    conn.close()

    return render_template("index.html", orderTypeList=orderTypeList, currentOrders=currentOrders)


@app.route('/order', methods=['POST', 'GET'])
def order_func_page():
    if request.method == "POST":

        try:
            if request.form['name'] != None:
                if request.form['phone'] != None:
                    if request.form['history']:
                        name = request.form['name']
                        phone = request.form['phone']
                        history = request.form['history']
                        message = request.form['message']
                        orderType = request.form['orderType']

                        import datetime
                        tTime = datetime.datetime.now().strftime("%H:%M:%S")
                        dDate = datetime.datetime.now().strftime("%d-%m-%y")

                        conn = sqlite3.connect('orders.db')
                        if history != "None":
                            message = history
                        c = conn.cursor()
                        c.execute('''INSERT INTO orders(tTime,dDate ,name, phone, orderMsg, orderType)
                                          VALUES(?,?,?,?,?,?)''', (tTime, dDate, name, phone, message, orderType))
                        conn.commit()
                        conn.close()


        except Exception as e:
            print("ERROR ", e)

        return redirect(url_for('index_page'))


if __name__ == '__main__':
    app.run(debug=True, port=80)
