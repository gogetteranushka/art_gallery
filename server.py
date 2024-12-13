from flask import *
from flask_mysqldb import *
app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb2'

mysql = MySQL(app)

@app.route("/home")
def home():
    #return render_template("index3.html")
    return render_template("index2.html")


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/products/<int:product_id>', methods=['GET'])
def products(product_id):  
    print(product_id)
    dbconn = mysql.connection
    cursor = dbconn.cursor()
    cursor.execute("Select * from artwork where id = %s", (product_id,))
    res = cursor.fetchone()
    print(res)
    return render_template('products.html',res = res)

@app.route("/cart", methods=['POST'])
def cart():
    product_id = request.form.get('product_id')
    print(product_id)
    dbconn = mysql.connection
    cursor = dbconn.cursor()
    cursor.execute("Select * from artwork where id = %s", (product_id,))
    res = cursor.fetchone()
    print(res)
    return render_template("cart.html", res =res)

@app.route("/registration")
def registration():
    return render_template("registration.html")

@app.route("/reg_confirm", methods=['POST'])
def reg_confirm():
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']
    password=request.form['password']
    cpassword=request.form['cpassword']
    pno=request.form['pno']
    event=request.form['event']

    # Simple validation for password and confirm password match
    if password != cpassword:
        return "Passwords do not match. Please try again."

    dbconn=mysql.connection
    cursor=dbconn.cursor()
    cursor.execute("INSERT INTO mydb2.registered_users(fname, lname, email, password, c_password, phone, event) VALUES (%s,%s,%s,%s,%s,%s,%s)", (fname,lname,email,password,cpassword,pno,event,))
    dbconn.commit()
    cursor.close()
    
    return render_template("reg_confirm.html", event=event)

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/artwork")
def artwork():
    dbconn = mysql.connection
    cursor = dbconn.cursor()
    cursor.execute("Select * from artwork")
    res = cursor.fetchall()
    
    return render_template("artwork.html", res = res)

@app.route("/events")
def events():
    dbconn=mysql.connection
    cursor1=dbconn.cursor()
    cursor1.execute("SELECT * FROM events")
    results1=cursor1.fetchall()
    cursor1.close()
    # cursor2=dbconn.cursor()
    # cursor2.execute("SELECT * FROM events")
    # results2=cursor2.fetchall()
    # cursor2.close()
    return render_template("events.html", results1=results1)

@app.route("/artists")
def artists():
    dbconn=mysql.connection
    cursor=dbconn.cursor()
    cursor.execute("SELECT * FROM mydb.artists")
    results=cursor.fetchall()
    cursor.close()
    return render_template("artists.html", results=results)


@app.route('/filter_artwork', methods=['GET'])
def filter_artwork():
    try:
        cursor = mysql.connection.cursor()
        filter_category = request.args.get('category')
        #print(filter_category)
        cursor.execute("SELECT * FROM mydb2.artwork WHERE category = %s", (filter_category,))
        res = cursor.fetchall()
        print(res)
        cursor.close()
        return render_template('filter_artwork.html', res=res)
    except Exception as e:
        return render_template("artwork.html")


@app.route("/admin_dashboard")
def admin_dashboard():
    return render_template("admin_dashboard.html")


@app.route('/add_artist', methods=['GET'])
def add_artist():
    # Render the add artist form
    return render_template('add_artist.html')

@app.route('/adding_artists', methods=['POST'])
def adding_artists():
    try:
        # Handle form submission (as in the earlier example)
        artist_id = request.form['artist_id']
        artist_name = request.form['name']
        hails_from = request.form.get('hails_from', '')
        description = request.form.get('bio', '')
        artist_img = request.files['artist_img']
        
        # Save uploaded image
        img_path = f"static/uploads/{artist_img.filename}"
        artist_img.save(img_path)
        
        # Insert into the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("""
            INSERT INTO artists (artist_id, artist_name, hails_from, description, artist_img)
            VALUES (%s, %s, %s, %s, %s)
        """, (artist_id, artist_name, hails_from, description, img_path))
        dbconn.commit()
        cursor.close()

        # Show success message
        return render_template("success.html", message="Artist added successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")
    
@app.route('/add_artwork', methods=['GET'])
def add_artwork():
    # Render the add artwork form
    return render_template('add_artwork.html')

@app.route('/adding_artworks', methods=['POST'])
def adding_artworks():
    try:
        # Handle form submission (same logic as before)
        artwork_id = request.form['artwork_id']
        category = request.form.get('category', '')
        name = request.form['name']
        artist_name = request.form['artist_name']
        year = request.form.get('year', None)
        size = request.form.get('size', '')
        price = request.form.get('price', None)
        description = request.form.get('description', '')
        product_file = request.files['product_path']
        
        # Save uploaded file
        file_path = f"static/uploads/{product_file.filename}"
        product_file.save(file_path)
        
        # Insert into the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("""
            INSERT INTO artwork (id, category, name, product_path, artist_name, year, size, price, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (artwork_id, category, name, file_path, artist_name, year, size, price, description))
        dbconn.commit()
        cursor.close()

        # Show success message
        return render_template("success.html", message="Artwork added successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")
    
@app.route('/add_event', methods=['GET'])
def add_event():
    # Render the add event form
    return render_template('add_event.html')

@app.route('/adding_event', methods=['POST'])
def adding_event():
    try:
        # Handle form submission for adding an event
        event_id = request.form['event_id']
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        description = request.form.get('description', '')
        event_img = request.files['event_img']
        
        # Save uploaded image
        if event_img:
            img_path = f"static/uploads/{event_img.filename}"
            event_img.save(img_path)
        else:
            img_path = ''

        # Insert into the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("""
            INSERT INTO events (event_id, event_name, event_date, description, event_img)
            VALUES (%s, %s, %s, %s, %s)
        """, (event_id, event_name, event_date, description, img_path))
        dbconn.commit()
        cursor.close()

        # Show success message
        return render_template("success.html", message="Event added successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")
    
@app.route('/modify_artist', methods=['GET'])
def modify_artist():
    # Render the add event form
    return render_template('modify_artist.html')   

@app.route('/modifying_artist', methods=['POST'])
def modifying_artist():
    try:
        artist_id = request.form['artist_id']
        artist_name = request.form['artist_name']
        artist_bio = request.form.get('artist_bio', '')

        # Update artist in the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("""
            UPDATE artists
            SET artist_name = %s, artist_bio = %s
            WHERE artist_id = %s
        """, (artist_name, artist_bio, artist_id))
        dbconn.commit()
        cursor.close()

        return render_template("success.html", message="Artist modified successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")
    
@app.route('/modify_event', methods=['GET'])
def modify_event():
    # Render the add event form
    return render_template('modify_event.html')

@app.route('/modifying_event', methods=['POST'])
def modifying_event():
    try:
        event_id = request.form['event_id']
        event_name = request.form['event_name']
        event_date = request.form['event_date']
        description = request.form.get('description', '')
        event_img = request.files['event_img']
        
        if event_img:
            img_path = f"static/uploads/{event_img.filename}"
            event_img.save(img_path)
        else:
            img_path = ''
        
        # Update event in the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("""
            UPDATE events
            SET event_name = %s, event_date = %s, description = %s, event_img = %s
            WHERE event_id = %s
        """, (event_name, event_date, description, img_path, event_id))
        dbconn.commit()
        cursor.close()

        return render_template("success.html", message="Event modified successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")
    
@app.route('/modify_artwork', methods=['GET'])
def modify_artwork():
    # Render the add event form
    return render_template('modify_artwork.html')

@app.route('/modifying_artwork', methods=['POST'])
def modifying_artwork():
    try:
        artwork_id = request.form['artwork_id']
        category = request.form.get('category', '')
        name = request.form['name']
        artist_name = request.form['artist_name']
        year = request.form.get('year', None)
        size = request.form.get('size', '')
        price = request.form.get('price', None)
        description = request.form.get('description', '')
        product_file = request.files['product_path']
        
        # Handle file upload
        if product_file:
            file_path = f"static/uploads/{product_file.filename}"
            product_file.save(file_path)
        else:
            file_path = ''
        
        # Update artwork in the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("""
            UPDATE artwork
            SET category = %s, name = %s, artist_name = %s, year = %s, size = %s, price = %s, description = %s, product_path = %s
            WHERE id = %s
        """, (category, name, artist_name, year, size, price, description, file_path, artwork_id))
        dbconn.commit()
        cursor.close()

        return render_template("success.html", message="Artwork modified successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")
    
@app.route('/delete_artist', methods=['GET'])
def delete_artist():
    # Render the add event form
    return render_template('delete_artist.html')
    
@app.route('/deleting_artist', methods=['POST'])
def deleting_artist():
    try:
        artist_id = request.form['artist_id']

            # Delete artist from the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("DELETE FROM artists WHERE artist_id = %s", (artist_id,))
        dbconn.commit()
        cursor.close()

        return render_template("success.html", message="Artist deleted successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")
    
@app.route('/delete_artwork', methods=['GET'])
def delete_artwork():
    # Render the add event form
    return render_template('delete_artwork.html')

@app.route('/deleting_artwork', methods=['POST'])
def deleting_artwork():
    try:
        artwork_id = request.form['artwork_id']

        # Delete artwork from the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("DELETE FROM artwork WHERE id = %s", (artwork_id,))
        dbconn.commit()
        cursor.close()

        return render_template("success.html", message="Artwork deleted successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")


@app.route('/delete_event', methods=['GET'])
def delete_event():
    # Render the add event form
    return render_template('delete_event.html')

@app.route('/deleting_event', methods=['POST'])
def deleting_event():
    try:
        event_id = request.form['event_id']

        # Delete event from the database
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("DELETE FROM events WHERE event_id = %s", (event_id,))
        dbconn.commit()
        cursor.close()

        return render_template("success.html", message="Event deleted successfully!")
    except Exception as e:
        return render_template("error.html", message=f"An error occurred: {e}")

# @app.route('/orders')
# def orders():
#     try:
#         # Fetch orders from the database
#         dbconn = mysql.connection
#         cursor = dbconn.cursor()
#         cursor.execute("SELECT * FROM orders")
#         orders = cursor.fetchall()
#         cursor.close()

#         # Render orders in the template
#         return render_template("orders.html", orders=orders)
#     except Exception as e:
#         return render_template("error.html", message=f"An error occurred: {e}")

app.run(debug=True, port=5002)

