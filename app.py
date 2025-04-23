from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import mysql.connector
from mysql.connector import Error
import random
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv
import io

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key_here')

# MySQL Database connection details
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'booking_db')
    )

# Routes for the website pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
@app.route('/tech')
def tech():
    return render_template('admin_login.html')

# Handling the form submission for bookings
@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    name = request.form['name']
    contact_no = request.form['contact_no']
    service = request.form['service']
    service_date = request.form['service_date']
    special_request = request.form['special_request']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert the form data into the 'bookings' table
        cursor.execute(''' 
            INSERT INTO bookings (name, contact_no, service, service_date, special_request)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, contact_no, service, service_date, special_request))

        conn.commit()
        booking_id = cursor.lastrowid

        cursor.close()
        conn.close()

        flash('Your booking has been successfully submitted!', 'success')
        return redirect(url_for('booking_details', booking_id=booking_id))

    except Error as e:
        print(f"Error: {e}")
        flash('There was an error while submitting your booking. Please try again.', 'danger')
        return redirect(url_for('contact'))

@app.route('/booking_details/<int:booking_id>', methods=['GET', 'POST'])
def booking_details(booking_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Fetch the booking details from the database using the booking_id
        cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()

        cursor.close()
        conn.close()

        if booking:
            if request.method == 'POST':
                # Get the updated data from the form
                updated_name = request.form['name']
                updated_contact_no = request.form['contact_no']
                updated_service = request.form['service']
                updated_service_date = request.form['service_date']
                updated_special_request = request.form['special_request']

                # Update the booking details in the database
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()

                    cursor.execute('''
                        UPDATE bookings
                        SET name = %s, contact_no = %s, service = %s, service_date = %s, special_request = %s
                        WHERE id = %s
                    ''', (updated_name, updated_contact_no, updated_service, updated_service_date, updated_special_request, booking_id))

                    conn.commit()
                    cursor.close()
                    conn.close()

                    flash('Your booking has been successfully updated!', 'success')
                    return redirect(url_for('booking_details', booking_id=booking_id))

                except Error as e:
                    print(f"Error: {e}")
                    flash('There was an error updating your booking. Please try again.', 'danger')
                    return redirect(url_for('booking_details', booking_id=booking_id))

            return render_template('edit_booking_details.html', booking=booking)
        else:
            flash('Booking not found!', 'danger')
            return redirect(url_for('contact'))

    except Error as e:
        print(f"Error: {e}")
        flash('There was an error fetching the booking details. Please try again.', 'danger')
        return redirect(url_for('contact'))

# Admin Panel Route
@app.route('/admin')
def admin():
    sort_by = request.args.get('sort_by', 'id')
    search_term = request.args.get('search', '')

    query = "SELECT * FROM bookings WHERE name LIKE %s OR contact_no LIKE %s OR service LIKE %s"
    query_params = ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%')

    if sort_by == 'name':
        query += " ORDER BY name"
    elif sort_by == 'service':
        query += " ORDER BY service"
    elif sort_by == 'service_date':
        query += " ORDER BY service_date"

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query, query_params)
        bookings = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('admin.html', bookings=bookings)

    except Error as e:
        print(f"Error: {e}")
        return "There was an error fetching the bookings."

@app.route('/delete_booking/<int:booking_id>', methods=['GET'])
def delete_booking(booking_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        print(f"Trying to delete booking with ID: {booking_id}")  # Debugging Step

        # Delete the booking by ID
        cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))

        # Check if any row was deleted
        if cursor.rowcount == 0:
            print("No booking found with this ID!")  # Debugging Step
            return "No booking found with this ID."

        conn.commit()
        print("Booking deleted successfully!")  # Debugging Step

        cursor.close()
        conn.close()

        return redirect(url_for('admin'))

    except Error as e:
        print(f"Error: {e}")  # Print the actual error message
        return "There was an error deleting the booking."

# Manage Stock
@app.route('/manage_stock', methods=['GET', 'POST'])
def manage_stock():
    if request.method == 'POST':
        product_name = request.form['product_name']
        quantity = request.form['quantity']

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM stock WHERE product_name = %s", (product_name,))
            product = cursor.fetchone()

            if product:
                cursor.execute(''' 
                    UPDATE stock
                    SET quantity = quantity + %s
                    WHERE product_name = %s
                ''', (quantity, product_name))
            else:
                cursor.execute(''' 
                    INSERT INTO stock (product_name, quantity)
                    VALUES (%s, %s)
                ''', (product_name, quantity))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('manage_stock'))

        except Error as e:
            print(f"Error: {e}")
            return "There was an error updating the stock."

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM stock")
        stock_items = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('manage_stock.html', stock_items=stock_items)

    except Error as e:
        print(f"Error: {e}")
        return "There was an error fetching the stock."

@app.route('/update_stock', methods=['POST'])
def update_stock():
    try:
        data = request.get_json()  # Get bill details from frontend
        conn = get_db_connection()
        cursor = conn.cursor()

        for item in data['items']:
            product_name = item['description']
            quantity_sold = int(item['quantity'])

            # Check if product exists
            cursor.execute("SELECT quantity FROM stock WHERE product_name = %s", (product_name,))
            product = cursor.fetchone()

            if product:
                if product[0] >= quantity_sold:  # Check if enough stock is available
                    cursor.execute("UPDATE stock SET quantity = quantity - %s WHERE product_name = %s", 
                                   (quantity_sold, product_name))
                else:
                    return f"Not enough stock for {product_name}", 400
            else:
                return f"Product {product_name} not found in stock", 400

        conn.commit()
        cursor.close()
        conn.close()

        return "Stock updated successfully", 200

    except Exception as e:
        print(f"Error updating stock: {e}")
        return "Error updating stock", 500

# Function to fetch stock items
def get_stock_items():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, product_name, price, quantity FROM stock")
        stock_items = cursor.fetchall()
        cursor.close()
        conn.close()
        return stock_items

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

# Route to create a bill
@app.route('/create_bill', methods=['GET', 'POST'])
def create_bill():
    if request.method == 'POST':
        customer_name = request.form['customer_name']
        total_amount = float(request.form['total_amount'])  # Convert to float if needed
        items = request.form.getlist('items')  # List of selected items
        quantities = request.form.getlist('quantities')  # List of corresponding quantities
        
        # Create the bill in the database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Insert into the bills table (replace with actual table name and fields)
            cursor.execute(''' 
                INSERT INTO bills (bill_number, customer_name, total_amount)
                VALUES (%s, %s, %s)
            ''', (request.form['bill_no'], customer_name, total_amount))
            conn.commit()

            # Reduce stock based on selected items and quantities
            for i, item_id in enumerate(items):
                quantity = int(quantities[i])
                
                # Update the stock by reducing the quantity
                cursor.execute(''' 
                    UPDATE stock
                    SET quantity = quantity - %s
                    WHERE id = %s
                ''', (quantity, item_id))

            conn.commit()
            cursor.close()
            conn.close()

            return redirect(url_for('admin'))  # Redirect to admin page after successful bill creation
        
        except Exception as e:
            print(f"Error creating bill: {e}")
            flash(f"There was an error processing the bill: {e}", 'danger')
            return redirect(url_for('create_bill'))

    # Generate a random bill number (e.g., B123456)
    bill_number = 'B' + ''.join(random.choices(string.digits, k=6))

    # Fetch the available stock items
    stock = get_stock_items()

    # Pass bill_number to the template
    return render_template('create_bill.html', stock=stock, bill_number=bill_number)

# Route to render invoice page with stock items
@app.route('/invoice')
def invoice():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT product_name, quantity FROM stock")
        stock_items = cursor.fetchall()
        cursor.close()
        conn.close()

        return render_template('invoice.html', stock_items=stock_items)

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return "Error fetching stock items", 500

# Route to create invoice and update stock
@app.route('/create_invoice', methods=['POST'])
def create_invoice():
    data = request.json
    items = data['items']  # Items in the invoice

    # Seller and buyer details
    seller_name = data['seller_name']
    seller_address = data['seller_address']
    seller_gstin = data['seller_gstin']
    buyer_name = data['buyer_name']
    buyer_address = data['buyer_address']
    buyer_gstin = data['buyer_gstin']

    # Invoice details
    invoice_number = data['invoice_number']
    invoice_date = data['invoice_date']
    total_value = data['total_value']
    cgst = data['cgst']
    sgst = data['sgst']
    grand_total = data['grand_total']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update stock based on invoice items
        for item in items:
            product_name = item['description']  # Product name
            quantity_sold = int(item['quantity'])  # Quantity sold

            # Fetch current stock for the product
            cursor.execute("SELECT quantity FROM stock WHERE product_name = %s", (product_name,))
            result = cursor.fetchone()

            if result:
                current_stock = result[0]

                if current_stock >= quantity_sold:
                    new_stock = current_stock - quantity_sold
                    cursor.execute("UPDATE stock SET quantity = %s WHERE product_name = %s", (new_stock, product_name))
                else:
                    return jsonify({"error": f"Not enough stock for {product_name}"}), 400
            else:
                return jsonify({"error": f"Product {product_name} not found in stock"}), 404

        # Commit the stock updates
        conn.commit()
        cursor.close()
        conn.close()

        # Generate the PDF invoice
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=letter)

        # Invoice header
        pdf.drawString(100, 750, "TAX INVOICE")
        pdf.drawString(100, 730, f"Seller: {seller_name}")
        pdf.drawString(100, 710, f"Address: {seller_address}")
        pdf.drawString(100, 690, f"GSTIN: {seller_gstin}")
        pdf.drawString(100, 670, f"Buyer: {buyer_name}")
        pdf.drawString(100, 650, f"Address: {buyer_address}")
        pdf.drawString(100, 630, f"GSTIN: {buyer_gstin}")
        pdf.drawString(100, 610, f"Invoice No: {invoice_number}")
        pdf.drawString(100, 590, f"Date: {invoice_date}")

        # Table header for the invoice items
        pdf.drawString(100, 570, "Description     Quantity     Rate     Amount")
        y_position = 550

        # Add each item to the invoice
        for item in items:
            description = item['description']
            quantity = item['quantity']
            rate = item['rate']
            amount = float(quantity) * float(rate)
            pdf.drawString(100, y_position, f"{description}      {quantity}        {rate}       {amount}")
            y_position -= 20

        # Totals at the end of the invoice
        pdf.drawString(100, y_position - 20, f"Total Value: {total_value}")
        pdf.drawString(100, y_position - 40, f"CGST (9%): {cgst}")
        pdf.drawString(100, y_position - 60, f"SGST (9%): {sgst}")
        pdf.drawString(100, y_position - 80, f"Grand Total: {grand_total}")

        pdf.save()

        # Send the PDF as a response to the client
        pdf_buffer.seek(0)
        return send_file(pdf_buffer, as_attachment=True, download_name=f"Invoice_{invoice_number}.pdf", mimetype='application/pdf')

    except mysql.connector.Error as e:
        print(f"Error: {e}")
        return jsonify({"error": "Error updating stock"}), 500

if __name__ == '__main__':
    try:
        port = int(os.getenv('PORT', '3000'))
        if port < 0 or port > 65535:
            port = 3000
            print(f"Invalid port {port}, using default port 3000")
        app.run(host='0.0.0.0', port=port, debug=False)
    except ValueError as e:
        print(f"Invalid PORT value, using default port 3000: {e}")
        app.run(host='0.0.0.0', port=3000, debug=False)
    except Exception as e:
        print(f"Error starting the application: {e}")
        raise
