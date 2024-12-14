from flask import *
from flask_mysqldb import *
from datetime import datetime

app=Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'

app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'mydb2'

mysql = MySQL(app)

# For user session management
app.config['SECRET_KEY'] = 'mysecretkey'

@app.route("/home")
def home():
    dbconn = mysql.connection
    cursor1 = dbconn.cursor()
    
    id = request.args.get('id', default=1, type=int)
    cursor1.execute("Select * from mydb2.artwork limit 4")
    artworks = cursor1.fetchall()

   
    print(artworks)
    return render_template('index3.html', artworks=artworks)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/createsession", methods = ['post'])
def createsession():
    email = request.form['email']
    password = request.form['password']

    dbconn = mysql.connection
    cursor1 = dbconn.cursor()
    cursor2 = dbconn.cursor()

    # Cursor to check if user is admin
    cursor1.execute("select * from admin where email = %s and password = %s", (email, password,))
    user1 = cursor1.fetchone()
    
    # Cursor to check if user is registered_user
    cursor2.execute("select * from registered_users where email = %s", (email,))
    user2 = cursor2.fetchone()

    if user1:                  # Admin can access the admin_dashboard
        session['is_admin'] = True
        session['email'] = user1[0]
        return redirect("/admin_dashboard")
    elif user2:                # Registered_user can add to cart
        session['is_user'] = True
        session['email'] = user2[3]
        print("THis is the email that is logged in: ", session['email'])
        print(session['is_user'])
        return redirect('/home')
    else:
        return redirect("/login")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/customer_query", methods=['POST'])
def customer_query():
    name=request.form['name']
    email=request.form['email']
    message=request.form['message']

    dbconn=mysql.connection
    cursor=dbconn.cursor()
    cursor.execute("INSERT INTO customer_query VALUES (%s,%s,%s)", (name, email, message))
    dbconn.commit()
    cursor.close()

    return ("Your query has been submitted successfully. You will hear from us soon!")

@app.route('/products/<int:product_id>', methods=['GET'])
def products(product_id):  
    print(product_id)
    dbconn = mysql.connection
    cursor = dbconn.cursor()
    cursor.execute("Select * from artwork where id = %s", (product_id,))
    res = cursor.fetchone()
    print(res)
    return render_template('products.html',res = res)

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

@app.route("/registration")
def registration():
    session['is_admin'] = False
    session['is_user'] = False
    dbconn=mysql.connection
    cursor1=dbconn.cursor()
    cursor1.execute("SELECT event_name FROM mydb2.events WHERE event_date BETWEEN CURRENT_DATE() AND '2025-01-30'")
    results1=cursor1.fetchall()
    cursor1.close()
    return render_template("registration.html", results1=results1)

    
    #return render_template("registration.html")


@app.route("/reg_confirm", methods=['POST'])
def reg_confirm():
    fname=request.form['fname']
    lname=request.form['lname']
    email=request.form['email']
    password=request.form['password']
    cpassword=request.form['cpassword']
    pno=request.form['pno']
    event=request.form['event']

    dbconn=mysql.connection
    cursor=dbconn.cursor()
    cursor.execute("INSERT INTO registered_users(fname, lname, email, password, c_password, phone, event) VALUES (%s,%s,%s,%s,%s,%s,%s)", (fname,lname,email,password,cpassword,pno,event,))
    dbconn.commit()
    cursor.close()
    
    return render_template("reg_confirm.html", event=event)

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
    cursor1.execute("SELECT * FROM mydb2.events WHERE event_date BETWEEN CURRENT_DATE() AND '2025-01-30'")
    results1=cursor1.fetchall()
    print(results1)
    cursor1.close()
    cursor2=dbconn.cursor()
    cursor2.execute("SELECT * FROM mydb2.events WHERE event_date>'2025-01-30'")
    results2=cursor2.fetchall()
    cursor2.close()
    return render_template("events.html", results1=results1, results2=results2)

@app.route("/artists")
def artists():
    dbconn=mysql.connection
    cursor=dbconn.cursor()
    cursor.execute("SELECT * FROM artists")
    results=cursor.fetchall()
    cursor.close()
    return render_template("artists.html", results=results)


@app.route('/filter_artwork', methods=['GET'])
def filter_artwork():
    try:
        cursor = mysql.connection.cursor()
        filter_category = request.args.get('category')
        cursor.execute("SELECT * FROM artwork WHERE category = %s", (filter_category,))
        res = cursor.fetchall()
        print(res)
        cursor.close()
        return render_template('filter_artwork.html', res=res)
    except Exception as e:
        return render_template("artwork.html")

@app.route('/products/<int:product_id>', methods=['GET'])
def products(product_id):  
    print(product_id)
    dbconn = mysql.connection
    cursor = dbconn.cursor()
    cursor.execute("Select * from artwork where id = %s", (product_id,))
    res = cursor.fetchone()
    print(res)
    return render_template('products.html',res = res)

@app.route("/cart", methods=['POST','GET'])
def cart():
    if 'is_user' in session and session['is_user']:
        product_id = request.form.get('product_id')
        print(product_id)
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        cursor.execute("Select * from artwork where id = %s", (product_id,))
        res = cursor.fetchone()
        print(res)
        return render_template("cart.html", res = res)
    else:
        return redirect("/login")
    
@app.route("/checkout", methods = ['post'])
def checkout():
    if 'is_user' in session and session['is_user']:
        product_name = request.form.get('product_name')
        price = request.form.get('price')
        order_date = datetime.now().strftime('%Y-%m-%d')
        status = 'processing'
        user_email = session['email']

        # Insert the order details into the 'orders' table
        dbconn = mysql.connection
        cursor = dbconn.cursor()
        # cursor.execute("insert into orders (order_date, product_name, price, user_email, status) values (%s, %s, %s, %s, %s,)", (order_date, product_name, price, user_email, status,) )
        cursor.execute("Insert into orders (order_date, product_name, price , status, user_email) values (%s, %s, %s, %s, %s)", (order_date, product_name, price, status, user_email,))
        dbconn.commit()
        cursor.close()
        return render_template("checkout.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if session['is_admin']:
        return render_template("admin_dashboard.html")
    else:
        return redirect("/login")

@app.route("/view_orders", methods=['GET'])
def view_orders():
    # Get the filter parameter from the URL (if any)
    status_filter = request.args.get('status', '')

    # Build the query depending on whether a filter is applied
    query = "SELECT * FROM orders"
    params = ()

    if status_filter:
        query += " WHERE status = %s"
        params = (status_filter,)

    # Execute the query with or without filter
    cursor = mysql.connection.cursor()
    cursor.execute(query, params)
    res = cursor.fetchall()

    return render_template("view_orders.html", res=res)

@app.route("/confirm_orders", methods=["POST"])
def confirm_orders():
    selected_orders = request.form.getlist("selected_orders")  # Get list of selected order IDs

    if selected_orders:
        cursor = mysql.connection.cursor()
        
        # Update status of selected orders to 'Confirmed'
        cursor.execute("""
            UPDATE orders
            SET status = 'Confirmed'
            WHERE id IN (%s)
        """ % ",".join(["%s"] * len(selected_orders)), tuple(selected_orders))
        
        mysql.connection.commit()
        cursor.close()
        
        flash("Selected orders have been confirmed!", "success")
        return redirect("/view_orders")
    
    flash("No orders selected.", "warning")
    return redirect("/view_orders")


@app.route("/add_event")
def add_event():
    if session['is_admin']:
        return render_template("add_event.html")
    else:
        return redirect("/login")

@app.route("/adding_events", methods = ['post'])
def adding_events():
    event_name = request.form['name']
    event_date = request.form['date']
    description = request.form['description']
    event_img = request.files['event_img']

    event_filename = event_img.filename
    event_poster_path = "static/images/"+event_filename
    event_img.save(event_poster_path)
    
    dbconn = mysql.connection
    cursor = dbconn.cursor()
    cursor.execute("Insert into events (event_name, event_date, description, event_img) values (%s, %s, %s, %s)", (event_name, event_date, description, event_poster_path,))
    dbconn.commit()
    cursor.close()
    return render_template("admin_dashboard.html",message = "Successfully Added the Event")

@app.route("/logout")
def logout():
    if 'is_admin' in session and session['is_admin']:
        session.pop('email',None)
        session.pop('is_admin',None)
    elif 'is_user' in session and session['is_user']:
        session.pop('email',None)
        session.pop('is_user',None)
    else:
        return redirect("/home")
    return redirect("/home")


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
    
@app.route("/add_event")
def add_event():
    if session['is_admin']:
        dbconn = mysql.connection
        cursor1 = dbconn.cursor()
        cursor1.execute("SELECT * from events")
        res = cursor1.fetchall()
        return render_template("add_event.html",res = res)
    else:
        return redirect("/login")

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
    
@app.route('/modify_event')
def modify_event():
    conn = mysql.connection()
    cursor = conn.cursor()
    # Fetch all event names from the database
    cursor.execute("SELECT event_name FROM events")
    events = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return render_template("modifyevent.html", events=events)

def modifying_event():
       # Process the form submission
       event_id = request.form['event_id']
       event_name = request.form['event_name']
       event_date = request.form['event_date']
       description = request.form['description']
       event_img = request.files['event_img']

       # Handle the image upload logic if needed
       # For example, save the image file locally
       if event_img:
           event_img.save(f"static/images/{event_img.filename}")

       conn = mysql.connect()
       cursor = conn.cursor()

       # Update the event in the database
       query = """
       UPDATE events 
       SET event_name = %s, event_date = %s, description = %s, event_img = %s 
       WHERE event_id = %s
       """
       cursor.execute(query, (event_name, event_date, description, event_img.filename, event_id))
       conn.commit()

       cursor.close()
       conn.close()
       return "Event Modified Successfully!"

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

app.run(debug=True, port=5003)

