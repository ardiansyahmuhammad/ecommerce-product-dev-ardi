from flask import Flask, render_template_string
import pymysql

app = Flask(__name__)

# Database config
db_config = {
    "host": "database-1.ctmgwauom6ws.ap-southeast-1.rds.amazonaws.com",  # RDS endpoint kamu
    "user": "admin",
    "password": "Ardi12593",
    "database": "database-1",
    "cursorclass": pymysql.cursors.DictCursor
}

# S3 config
s3_base_url = "https://ecommer-product-dev-ardi.s3.amazonaws.com"  # Bucket kamu

def get_products():
    """Fetch products from MySQL database."""
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM products")
            products = cursor.fetchall()
            return products
    except Exception as e:
        print(f"Database connection error: {e}")
        return []
    finally:
        if 'connection' in locals():
            connection.close()

@app.route("/")
def home():
    """Display products catalog."""
    products = get_products()
    
    if not products:
        return "<h1>No products found or database error.</h1>"

    html = "<h1>Product Catalog</h1><ul>"
    for p in products:
        image_url = f"{s3_base_url}/{p['image_filename']}"
        html += (
            f"<li>"
            f"<strong>{p['name']}</strong> - Rp{int(p['price'])}<br>"
            f"<img src='{image_url}' width='200' alt='Product Image'>"
            f"</li>"
        )
    html += "</ul>"
    return render_template_string(html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
