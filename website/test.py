#app.py
from flask import Flask, render_template, jsonify, request
# from flask_mysqldb import MySQL,MySQLdb #pip install flask-mysqldb https://github.com/alexferl/flask-mysqldb
 
app = Flask(__name__)
   
# app.secret_key = "caircocoders-ednalan-2020"
   
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'testingdb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)
       
@app.route('/', methods=['GET', 'POST'])
def index():
    # cursor = mysql.connection.cursor()
    # cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    message = ''    
    if request.method == 'POST':
        fullname = request.form.getlist('field[]')
        # for value in fullname:  
        #     cur.execute("INSERT INTO fullnames (full_name) VALUES (%s)",[value])
        #     mysql.connection.commit()       
        # cur.close()
        # message = "Succesfully Register"
    return render_template("indextest.html")
  
 
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.5')