import datetime
import sqlite3

from flask import *


class Item(object):
    def __init__(self, timeDate, name, phone, message, orderType):
        self.timeDate = timeDate
        self.name = name
        self.phone = phone
        self.message = message
        self.orderType = orderType


app = Flask(__name__)


@app.route('/clear_db')
def clear_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''DROP TABLE orders''')
    c.execute('''CREATE TABLE orders(timeDate text , name text, phone text, orderMsg text, orderType text)''')
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
        timeDate = item[0]
        name = item[1]
        phone = item[2]
        message = item[3]
        orderType = item[4]

        todayDate = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S").split(" ")[0]

        if todayDate not in timeDate:
            continue

        if querydate:
            if orderType == querydate:
                currentOrders.append(
                    Item(timeDate=timeDate, name=name, phone=phone, message=message, orderType=orderType))
        elif querydate == "":
            currentOrders.append(Item(timeDate=timeDate, name=name, phone=phone, message=message, orderType=orderType))
        elif querydate == "All Day":
            currentOrders.append(Item(timeDate=timeDate, name=name, phone=phone, message=message, orderType=orderType))

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
                        timeDate = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

                        conn = sqlite3.connect('orders.db')
                        if history != "None":
                            message = history
                        c = conn.cursor()
                        c.execute('''INSERT INTO orders(timeDate ,name, phone, orderMsg, orderType)
                                          VALUES(?,?,?,?,?)''', (timeDate, name, phone, message, orderType))
                        conn.commit()
                        conn.close()


        except Exception as e:
            print("ERROR ", e)

        return redirect(url_for('index_page'))


if __name__ == '__main__':
    app.run(debug=True,port=80)
