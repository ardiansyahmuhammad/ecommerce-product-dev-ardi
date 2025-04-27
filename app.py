from flask import Flask, render_template_string
import pymysql

app = Flask(__name__)

# Database config
db_host = "database-1.ctmgwauom6ws.ap-southeast-1.rds.amazonaws.com"  # Ganti dengan RDS endpoint kamu
db_user = "admin"
db_password = "Ardi12593"
db_name = "database-1"

# S3 config
s3_base_url = "https://ecommer-product-dev-ardi.s3.amazonaws.com"  # Ganti dengan nama bucket kamu

def get_products():
    connection = pymysql.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            return products
    finally:
        connection.close()

@app.route("/")
def home():
    products = get_products()
    html = "<h1>Product Catalog</h1><ul>"
    for p in products:
        html += f"<li><strong>{p['name']}</strong> - Rp{int(p['price'])}<br><img src='{s3_base_url}/{p['image_filename']}' width='200'></li>"
    html += "</ul>"
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
