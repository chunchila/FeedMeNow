import sqlite3

from flask import Flask, request, render_template

conn = sqlite3.connect('orders.db')

c = conn.cursor()

# c.execute('''CREATE TABLE orders(name text, phone text, orderMsg text, orderType text)''')

# conn.commit()

itemlist = [x for x in range(100)]

c.execute('''SELECT * FROM orders''')
allItems = c.fetchall()

for item in allItems:
    print("this is in database", item)
else:
    print("no items in allItems")

app = Flask(__name__)

app.config['secret_key'] = "dfdf";


@app.route('/')
def hello_world():
    return render_template("index.html", itemlist=itemlist)


@app.route('/order', methods=['POST', 'GET'])
def order_func():
    if request.method == "POST":

        try:
            if request.form['name'] != None:
                if request.form['phone'] != None:
                    if request.form['history']:
                        name = request.form['name']
                        phone = request.form['phone']
                        history = request.form['history']
                        c.execute('''INSERT INTO orders(name, phone, orderMsg, orderType)
                                          VALUES(?,?,?,?)''', (name, phone,))
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
