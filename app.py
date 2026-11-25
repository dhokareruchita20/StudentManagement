from flask import Flask, render_template, request, redirect
import pymysql

app = Flask(__name__)

def get_db_connection():
    connection = pymysql.connect(
       host="student-management-db.cl4e2cwq2kq2.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="YOUR_DB_PASSWORD",
        database="studentdb",
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        connection = get_db_connection()

        with connection.cursor() as cursor:
            sql = "INSERT INTO students (name, email) VALUES (%s, %s)"
            cursor.execute(sql, (name, email))

        connection.commit()
        connection.close()

        return redirect('/')

    connection = get_db_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()

    connection.close()

    return render_template('index.html', students=students)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)