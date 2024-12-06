import sqlite3
from flask import Flask, render_template, g, jsonify
import json  # Untuk mengubah data menjadi JSON

app = Flask(__name__)
DATABASE = 'humas.db'

# Fungsi untuk mendapatkan koneksi database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # Agar hasil query berupa dictionary
    return db

# Fungsi untuk melakukan query pada database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# Fungsi untuk menutup koneksi database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Route utama (untuk menampilkan grafik di halaman web)
@app.route('/')
def index():
    query = """
        SELECT bulan, status, COUNT(*) AS jumlah
        FROM murid
        GROUP BY bulan, status
        ORDER BY CASE
            WHEN bulan = 'Jan' THEN 1
            WHEN bulan = 'Feb' THEN 2
            WHEN bulan = 'Mar' THEN 3
            WHEN bulan = 'Apr' THEN 4
            WHEN bulan = 'Mei' THEN 5
            WHEN bulan = 'Jun' THEN 6
            WHEN bulan = 'Jul' THEN 7
            WHEN bulan = 'Agu' THEN 8
            WHEN bulan = 'Sep' THEN 9
            WHEN bulan = 'Okt' THEN 10
            WHEN bulan = 'Nov' THEN 11
            WHEN bulan = 'Des' THEN 12
        END
    """
    data = query_db(query)
    
    # Debugging: Print raw data before processing
    print("Raw Data:", data)

    # Inisialisasi data bulanan untuk grafik
    chart1_data = {month: {"Net Profit": 0, "Revenue": 0} for month in ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]}

    # Memproses hasil query
    for row in data:
        bulan = row['bulan']
        status = row['status']
        jumlah = row['jumlah']
        if status == 'net_profit':
            chart1_data[bulan]["Net Profit"] += jumlah
        elif status == 'revenue':
            chart1_data[bulan]["Revenue"] += jumlah

    # Debugging: Check processed chart1 data
    print("Processed Chart 1 Data:", chart1_data)

    # Sort months manually to ensure correct order
    month_order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    sorted_chart1_data = {month: chart1_data[month] for month in month_order}

    # Debugging: Check sorted chart data
    print("Sorted Chart 1 Data:", sorted_chart1_data)

    # Mengirim data ke template (untuk tampilan web)
    return render_template(
        'beranda.html',
        chart1_data=json.dumps(sorted_chart1_data)  # Convert ke JSON
    )

# API untuk mendapatkan data chart1 (jumlah murid per bulan)
@app.route('/api/chart1', methods=['GET'])
def get_chart1_data():
    query = """
        SELECT bulan, status, COUNT(*) AS jumlah
        FROM murid
        GROUP BY bulan, status
        ORDER BY CASE
            WHEN bulan = 'Jan' THEN 1
            WHEN bulan = 'Feb' THEN 2
            WHEN bulan = 'Mar' THEN 3
            WHEN bulan = 'Apr' THEN 4
            WHEN bulan = 'Mei' THEN 5
            WHEN bulan = 'Jun' THEN 6
            WHEN bulan = 'Jul' THEN 7
            WHEN bulan = 'Agu' THEN 8
            WHEN bulan = 'Sep' THEN 9
            WHEN bulan = 'Okt' THEN 10
            WHEN bulan = 'Nov' THEN 11
            WHEN bulan = 'Des' THEN 12
        END
    """
    data = query_db(query)

    # Inisialisasi data chart1
    chart1_data = {month: {"pkl": 0, "belum-pkl": 0} for month in ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]}

    # Memproses hasil query untuk chart1
    for row in data:
        bulan = row['bulan']
        status = row['status']
        jumlah = row['jumlah']
        if status == 'pkl':
            chart1_data[bulan]["pkl"] += jumlah
        elif status == 'belum-pkl':
            chart1_data[bulan]["belum-pkl"] += jumlah

    # Sort months manually to ensure correct order
    month_order = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
    sorted_chart1_data = {month: chart1_data[month] for month in month_order}

    return jsonify(sorted_chart1_data)


# API untuk mendapatkan data chart2 (jumlah murid per status)
@app.route('/api/chart2', methods=['GET'])
def get_chart2_data():
    query = """
        SELECT bulan, status, COUNT(*) AS jumlah
        FROM murid
        GROUP BY bulan, status
    """
    data = query_db(query)

    # Inisialisasi data chart2
    chart2_data = {"PKL": 0, "Pra PKL": 0, "Belum PKL": 0}

    # Memproses hasil query untuk chart2
    for row in data:
        status = row['status']
        jumlah = row['jumlah']
        if status == 'pkl':
            chart2_data["PKL"] += jumlah
        elif status == 'pra-pkl':
            chart2_data["Pra PKL"] += jumlah
        elif status == 'belum-pkl':
            chart2_data["Belum PKL"] += jumlah

    return jsonify(chart2_data)

# Route untuk halaman BKK
@app.route('/bkk')
def bkk():
    return render_template('bkk.html')

# Route untuk halaman Sosial
@app.route('/sosial')
def sosial():
    return render_template('sosial.html')

if __name__ == '__main__':
    app.run(debug=True)
