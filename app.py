import sqlite3

from flask import request, render_template, Flask


class Item(object):
    def __init__(self, dateTime, name, phone, message, orderType):
        self.dateTime = dateTime
        self.name = name
        self.phone = phone
        self.message = message
        self.orderType = orderType


init = 0
if (init == 1):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''DROP TABLE orders''')
    c.execute('''CREATE TABLE orders(name text, phone text, orderMsg text, orderType text ,timeDate text)''')
    conn.commit()
    c.close()

orderTypeList = []
orderTypeList.append("Morning")
orderTypeList.append("12")
orderTypeList.append("Evining")
orderTypeList.append("Extra")

currentOrders = []

conn = sqlite3.connect('orders.db')

c = conn.cursor()

c.execute('''SELECT * FROM orders''')
current = c.fetchall()

# Load All The DateBase To Vars
for item in current:
    print("db Loaded ", item)
    name = item[0]
    phone = item[1]
    message = item[2]
    orderType = item[3]
    dateTime = item[4]
    currentOrders.append(Item(dateTime=dateTime, name=name, phone=phone, message=message, orderType=orderType))

conn.close()

app = Flask(__name__)


@app.route('/')
def index_page():
    return render_template("index.html", itemlist=itemlist, orderTypeList=orderTypeList, currentOrders=currentOrders)


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
                        timeDate = datetime.datetime.now().strftime("%d%m%y %H%M%S")

                        conn = sqlite3.connect('orders.db')
                        if history != "None":
                            message = history
                        c = conn.cursor()
                        c.execute('''INSERT INTO orders(name, phone, orderMsg, orderType ,timeDate)
                                          VALUES(?,?,?,?,?)''', (name, phone, message, orderType, timeDate))
                        conn.commit()
                        conn.close()
                        print('First user inserted')

        except Exception as e:
            print("ERROR ", e)

    elif request.method == "GET":
        return "get"
    else:
        return "else method "


if __name__ == '__main__':
    itemlist = [x for x in range(100)]
    app.run(debug=True)
