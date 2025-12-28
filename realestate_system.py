import mysql.connector
from mysql.connector import Error
import google.generativeai as genai
import os
from datetime import datetime

# Configure Gemini AI
genai.configure(api_key=os.environ.get('GEMINI_API_KEY', 'your-api-key-here'))
model = genai.GenerativeModel('gemini-pro')

def get_db_connection():
    """Create and return database connection"""
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="realestatemanagement"
        )
    except Error as e:
        print(f"Database connection error: {e}")
        return None

def ai_property_recommendations(user_preferences):
    """Use Gemini AI to provide intelligent property recommendations"""
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    cur.execute("SELECT * FROM main_table")
    properties = cur.fetchall()
    
    if not properties:
        print("No properties available for recommendations")
        db.close()
        return
    
    property_data = "\n".join([
        f"ID: {p[0]}, Category: {p[1]}, Type: {p[2]}, Location: {p[4]}, "
        f"Area: {p[5]} sqft, Price: {p[6]}, Rating: {p[7]}"
        for p in properties
    ])
    
    prompt = f"""Based on the following user preferences: {user_preferences}
    
Available properties:
{property_data}

Provide top 3 property recommendations with reasoning. Be concise and specific."""
    
    try:
        response = model.generate_content(prompt)
        print("\n===== AI PROPERTY RECOMMENDATIONS =====")
        print(response.text)
        print("=" * 40)
    except Exception as e:
        print(f"AI recommendation error: {e}")
    finally:
        db.close()

def orderprop():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    
    try:
        ptype = input("Enter property type: ")
        pcat = input("Enter property category: ")
        
        query = "SELECT * FROM main_table WHERE PTYPE LIKE %s AND PCAT LIKE %s"
        cur.execute(query, (f'%{ptype}%', f'%{pcat}%'))
        data = cur.fetchall()
        
        if data:
            print("---------------")
            print("Property found!")
            
            for property in data:
                print(f"Property ID: {property[0]}")
                print(f"Property Category: {property[1]}")
                print(f"Property Type: {property[2]}")
                print(f"Ownership: {property[3]}")
                print(f"Locality: {property[4]}")
                print(f"Area in sqft: {property[5]}")
                print(f"Price: {property[6]}")
                print(f"Ratings: {property[7]}")
                print("-----------------")
            
            choice = input("Do you want to purchase ANY property? (yes/no): ")
            if choice.lower() == 'yes':
                username = input("Enter your name: ")
                orderid = int(input("Enter order ID: "))
                propertyid = int(input("Enter property ID: "))
                pcat = input("Enter property category: ")
                ptype = input("Enter property type: ")
                price = int(input("Enter property price: "))
                
                query = "INSERT INTO order_table VALUES (%s, %s, %s, %s, %s, %s)"
                cur.execute(query, (username, orderid, propertyid, pcat, ptype, price))
                db.commit()
                
                print("========= Order placed successfully ===============")
                print("Thank you for choosing us!")
                print("===============================================")
            else:
                print("Thank you for visiting!")
                print("===============================================")
        else:
            print("========== No properties found ==========")
            
    except ValueError:
        print("========== Invalid input ==========")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()
    
    after_signin()

def viewpropertycategorydetails():
    print(">>>>>>>>> PROPERTY CATEGORIES <<<<<<<<")
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    cur.execute("SELECT DISTINCT PCAT FROM main_table")
    data = cur.fetchall()
    
    print("======= Available Property Categories =======")
    for i in data:
        print(f"* {i[0]}")
    print("\n")
    
    try:
        print("=====SELECT YOUR CHOICE FROM THE ABOVE======")
        inpcat = input("Enter your desired property category: ")
        
        query = "SELECT * FROM main_table WHERE PCAT=%s"
        cur.execute(query, (inpcat,))
        det = cur.fetchall()
        
        if det:
            print("====== PROPERTY DETAILS ======")
            for a in det:
                print("-----------------")
                print(f"Property ID: {a[0]}")
                print(f"Category: {a[1]}")
                print(f"Type: {a[2]}")
                print(f"Ownership: {a[3]}")
                print(f"Locality: {a[4]}")
                print(f"Area in sqft: {a[5]}")
                print(f"Price: {a[6]}")
                print(f"Ratings: {a[7]}")
                print("-----------------\n")
        else:
            print("========== No properties found for the selected category ==========")
            
    except ValueError:
        print("<<<<<< INVALID INPUT >>>>>>")
    finally:
        db.close()
    
    after_signin()

def viewpropertycategory():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    cur.execute("SELECT DISTINCT PCAT FROM main_table")
    data = cur.fetchall()
    
    print("=========== PROPERTY CATEGORIES ============")
    for i in data:
        print(f"* {i[0]}")
    print("\n")
    
    db.close()
    after_signin()

def deleteproperty():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    print("<<<<<<DELETING PROPERTY DETAILS FROM THE SOFTWARE>>>>>>")
    print("\n")
    print("====== DO AT YOUR OWN RISK ======")
    
    try:
        pid = int(input("Enter property id: "))
        query = "DELETE FROM main_table WHERE PID=%s"
        cur.execute(query, (pid,))
        db.commit()
        
        if cur.rowcount > 0:
            print("\n*******PROPERTY DETAILS DELETED SUCCESSFULLY*******\n")
        else:
            print("=========== PROPERTY DOES NOT EXIST ==============")
            
    except ValueError:
        print("========= INVALID INPUT ========")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()
    
    after_login()

def view_order_details():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    
    try:
        cur.execute("SELECT * FROM order_table")
        orders = cur.fetchall()
        
        if orders:
            print("===== ORDER DETAILS OF CUSTOMERS =====")
            for order in orders:
                print("-------------------------")
                print(f"Username: {order[0]}")
                print(f"Order ID: {order[1]}")
                print(f"Property ID: {order[2]}")
                print(f"Property Category: {order[3]}")
                print(f"Property Type: {order[4]}")
                print(f"Price: {order[5]}")
                print("-------------------------\n")
        else:
            print("======== No orders found ==========\n")
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()
    
    after_login()

def updateproperty():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    print("<<<<<< UPDATING PROPERTY DETAILS >>>>>>")
    
    try:
        property_id = int(input("Enter the Property ID to update: "))
        cur.execute("SELECT * FROM main_table WHERE PID = %s", (property_id,))
        property_details = cur.fetchone()
        
        if property_details:
            print("Current Property Details:")
            print("-------------------------")
            print(f"Property ID: {property_details[0]}")
            print(f"Category: {property_details[1]}")
            print(f"Type: {property_details[2]}")
            print(f"Ownership: {property_details[3]}")
            print(f"Locality: {property_details[4]}")
            print(f"Area in sqft: {property_details[5]}")
            print(f"Price: {property_details[6]}")
            print(f"Ratings: {property_details[7]}")
            print("-------------------------")
            
            new_category = input("Enter new property category: ")
            new_type = input("Enter new property type: ")
            new_price = int(input("Enter new price: "))
            new_ownership = input("Enter new ownership status: ")
            
            update_query = """
                UPDATE main_table 
                SET PCAT = %s, PTYPE = %s, PRICE = %s, OWNERSHIP = %s 
                WHERE PID = %s
            """
            cur.execute(update_query, (new_category, new_type, new_price, new_ownership, property_id))
            db.commit()
            
            print("******* PROPERTY DETAILS UPDATED SUCCESSFULLY *******")
            print("\nUpdated Property Details:")
            print("-------------------------")
            print(f"Property ID: {property_id}")
            print(f"Category: {new_category}")
            print(f"Type: {new_type}")
            print(f"Ownership: {new_ownership}")
            print(f"Price: {new_price}")
            print("-------------------------")
        else:
            print("========== PROPERTY NOT FOUND ==========")
            
    except ValueError:
        print("========= INVALID INPUT: Please enter a valid Property ID =========")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()
    
    after_login()

def viewpropertytype():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    cur.execute("SELECT DISTINCT PTYPE FROM main_table")
    data = cur.fetchall()
    
    print("=" * 5, "PROPERTY TYPES", "=" * 5)
    for i in data:
        print(f"* {i[0]}")
    print("\n<<<<<<<< HOPE YOU ARE GETTING APPROPRIATE RESULTS >>>>>>>>\n")
    
    db.close()
    after_signin()

def viewpropertyarea():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    
    try:
        print("<<<< AREA DETAILS >>>>\n")
        cur.execute("SELECT * FROM main_table")
        data = cur.fetchall()
        area_req = int(input("Enter under required area (sqft): "))
        
        found = False
        for i in data:
            if i[5] <= area_req:
                found = True
                print("--------------------")
                print(f">Property ID: {i[0]}")
                print(f">Property Category: {i[1]}")
                print(f">Property Type: {i[2]}")
                print(f">Ownership: {i[3]}")
                print(f">Locality: {i[4]}")
                print(f">Area in sqft: {i[5]}")
                print(f">Price: {i[6]}")
                print(f">Ratings: {i[7]}")
                print("--------------------\n")
        
        if not found:
            print("No properties found within the specified area")
            
    except ValueError:
        print("<<<<<<<< INVALID INPUT >>>>>>>>>\n")
    finally:
        db.close()
    
    after_signin()

def viewpropertylocation():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    
    try:
        print("<<<< LOCATION DETAILS >>>>\n")
        location = input("ENTER YOUR DESIRED LOCATION: ")
        
        query = "SELECT * FROM main_table WHERE LOCALITY LIKE %s"
        cur.execute(query, (f'%{location}%',))
        properties = cur.fetchall()
        
        if properties:
            print(f"-----PROPERTY DETAILS AT: {location}-----\n")
            for prop in properties:
                print("-----------------")
                print(f"Property ID: {prop[0]}")
                print(f"CATEGORY: {prop[1]}")
                print(f"PROPERTY TYPE: {prop[2]}")
                print(f"PRICE: {prop[6]}")
                print(f"LOCALITY: {prop[4]}")
                print("-----------------\n")
        else:
            print("======== No properties found in the specified location ========")
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()
    
    after_signin()

def viewpropertyownership():
    print("-----CHECK FOR PROPERTY OWNERSHIP-----\n")
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    
    try:
        p_category = input("Enter your desired property category: ")
        p_type = input("Enter your required property type: ")
        print()
        
        query = "SELECT * FROM main_table WHERE PCAT=%s AND PTYPE=%s"
        cur.execute(query, (p_category, p_type))
        data = cur.fetchall()
        
        if data:
            for prop in data:
                print("------------------")
                print(f"FOR: {prop[4]}")
                print(f"CATEGORY: {prop[1]}")
                print(f"TYPE: {prop[2]}")
                print(f"==OWNERSHIP:== {prop[3]}")
                print(f"LOCATION: {prop[4]}")
                print("------------------\n")
        else:
            print("======== No properties found matching the criteria ========")
            
    except ValueError:
        print("<<<<<<< INVALID INPUT >>>>>>>\n")
    finally:
        db.close()
    
    print("-----------THANK YOU-----------")
    after_signin()

def sign_up_user():
    print("-----SIGN UP USER-----\n")
    print("Enter 1 for User login")
    print("Enter 2 for Exit\n")
    
    try:
        ch = int(input("Enter your choice: "))
        if ch == 1:
            userloginfo()
        elif ch == 2:
            exit()
        else:
            print("====== Invalid input ======\n")
            sign_up_user()
    except ValueError:
        print("====== Invalid input ======\n")
        sign_up_user()

def userloginfo():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    print("-----LOGIN PORTAL FOR USERS-----")
    
    try:
        cur.execute("SELECT * FROM user_login")
        user_data = cur.fetchall()
        
        username = input("Enter username: ")
        password = input("Enter password: ")
        
        user_found = False
        for user in user_data:
            if user[0] == username and user[1] == password:
                user_found = True
                print("=== USER EXIST ===\n")
                print(f"USERNAME: {user[0]}")
                print(f"PASSWORD: {user[1]}")
                break
        
        if not user_found:
            print("=== USER NOT FOUND ===\n")
            userloginfo()
            return
            
    except Error as e:
        print(f"Database error: {e}\n")
    finally:
        db.close()
    
    print("====== LOGIN HAS BEEN SUCCESSFUL =======\n")
    after_signin()

def after_signin():
    print("======== WELCOME TO REAL ESTATE MANAGEMENT SYSTEM ========\n")
    print("-> 1 for view all properties")
    print("-> 2 for view all property types")
    print("-> 3 for view property location")
    print("-> 4 for view property details under required area")
    print("-> 5 for view property ownership")
    print("-> 6 for view rental properties")
    print("-> 7 for view property details under required category")
    print("-> 8 for view property categories")
    print("-> 9 for order property")
    print("-> 10 for AI property recommendations")
    print("-> 11 for exit\n")
    
    try:
        ch = int(input("Enter your choice: "))
        
        if ch == 1:
            viewallproperty()
        elif ch == 2:
            viewpropertytype()
        elif ch == 3:
            viewpropertylocation()
        elif ch == 4:
            viewpropertyarea()
        elif ch == 5:
            viewpropertyownership()
        elif ch == 6:
            viewrentalproperty()
        elif ch == 7:
            viewpropertycategorydetails()
        elif ch == 8:
            viewpropertycategory()
        elif ch == 9:
            orderprop()
        elif ch == 10:
            preferences = input("Describe your property preferences (budget, location, type): ")
            ai_property_recommendations(preferences)
            after_signin()
        elif ch == 11:
            exit()
        else:
            print("======== Invalid choice ========\n")
            after_signin()
    except ValueError:
        print("======== Invalid input ========\n")
        after_signin()

def addproperty():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    print("<<<<<<ADDING PROPERTY DETAILS INTO THE SOFTWARE>>>>>>\n")
    
    try:
        pcat = input("Enter property category: ")
        ptype = input("Enter property type: ")
        pid = int(input("Enter property ID: "))
        area = int(input("Enter area in sqft: "))
        loc = input("Enter locality: ")
        own = input("Enter ownership: ")
        price = int(input("Enter price: "))
        rat = int(input("Enter customer ratings: "))
        
        query = "INSERT INTO main_table VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(query, (pid, pcat, ptype, own, loc, area, price, rat))
        db.commit()
        
        print("\n<<<<<< PROPERTY DETAILS ADDED SUCCESSFULLY >>>>>>\n")
        
    except ValueError:
        print("\n<<<<<<< INVALID INPUT >>>>>>>\n")
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()
    
    after_login()

def viewallproperty():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    print("<<<<<<<<<<<< UPDATED PROPERTY DETAILS >>>>>>>>>>>>>\n")
    
    cur.execute("SELECT * FROM main_table")
    data = cur.fetchall()
    
    print("======== ALL PROPERTIES ARE SHOWN BELOW =========")
    for prop in data:
        print("\n---------------")
        print(f"Property id: {prop[0]}")
        print(f"Property category: {prop[1]}")
        print(f"Property type: {prop[2]}")
        print(f"Ownership: {prop[3]}")
        print(f"Locality: {prop[4]}")
        print(f"Area in sqft: {prop[5]}")
        print(f"Price: {prop[6]}")
        print(f"Customer ratings: {prop[7]}")
        print("----------------")
    print()
    
    db.close()
    after_signin()

def adminloginfo():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    print("******LOGIN PORTAL FOR ADMIN*******")
    
    try:
        admin_name = input("Enter admin name: ")
        password = int(input("Enter password: "))
        
        cur.execute("SELECT * FROM admin_login")
        admin_data = cur.fetchall()
        
        authenticated = False
        for admin in admin_data:
            if admin[0] == admin_name and admin[1] == password:
                authenticated = True
                print("LOGIN FOR ADMIN")
                print(f"NAME: {admin_name}")
                print(f"PASS: {password}\n")
                break
        
        if not authenticated:
            print("======== DATA UNMATCHED ========")
            print("======= PLEASE TRY AGAIN ========\n")
            db.close()
            adminloginfo()
            return
            
    except ValueError:
        print("<<<<<<< INVALID INPUT >>>>>>\n")
        print("<<<<< TRY AGAIN >>>>>")
        db.close()
        adminloginfo()
        return
    finally:
        db.close()
    
    print("<<<< LOGIN HAS DONE SUCCESSFULLY >>>>\n")
    after_login()

def after_login():
    print("======== WELCOME TO REAL ESTATE MANAGEMENT SYSTEM ========\n")
    print("=========ADMIN PAGE FOR PROPERTY MODIFICATION ONLY=======\n")
    print("PRESS 1 FOR ADDING PROPERTY")
    print("PRESS 2 FOR DELETING PROPERTY")
    print("PRESS 3 FOR UPDATING PROPERTY")
    print("PRESS 4 FOR VIEWING ORDER DETAILS OF CUSTOMERS")
    print("PRESS 5 FOR EXIT\n")
    
    try:
        choice = int(input("ENTER YOUR CHOICE: "))
        
        if choice == 1:
            addproperty()
        elif choice == 2:
            deleteproperty()
        elif choice == 3:
            updateproperty()
        elif choice == 4:
            view_order_details()
        elif choice == 5:
            exit()
        else:
            print("========= INVALID CHOICE ==========\n")
            print("====== PLEASE TRY AGAIN ======")
            after_login()
    except ValueError:
        print("========= INVALID INPUT ==========\n")
        after_login()

def viewrentalproperty():
    db = get_db_connection()
    if not db:
        return
    
    cur = db.cursor()
    print("<<<<<< VIEWING RENTAL PROPERTIES >>>>>>\n")
    
    try:
        query = "SELECT * FROM main_table WHERE OWNERSHIP = 'Rent'"
        cur.execute(query)
        rental_properties = cur.fetchall()
        
        if rental_properties:
            print("-----RENTAL PROPERTY DETAILS-----")
            for prop in rental_properties:
                print("-----------------")
                print(f"Property ID: {prop[0]}")
                print(f"Property Category: {prop[1]}")
                print(f"Property Type: {prop[2]}")
                print(f"Ownership: {prop[3]}")
                print(f"Locality: {prop[4]}")
                print(f"Area in sqft: {prop[5]}")
                print(f"Price Per quarter: {prop[6]}")
                print(f"Ratings: {prop[7]}")
                print("-----------------\n")
        else:
            print("======== No rental properties found ==========")
            
    except Error as e:
        print(f"Database error: {e}")
    finally:
        db.close()
    
    after_signin()

def main():
    while True:
        print("=" * 54)
        print("================WELCOME TO SPEDOSERV==================")
        print("============REALESTATE MANAGEMENT SYSTEM==============")
        print("=" * 54)
        print("\n=========PLEASE UNDERGO THE FOLLOWING STEPS TO ACCESS THIS SOFTWARE=========\n")
        print("1. LOGIN AS ADMIN")
        print("2. LOGIN AS USER")
        print("3. EXIT")
        
        try:
            choice = input("ENTER YOUR CHOICE: ")
            
            if choice == "1":
                adminloginfo()
            elif choice == "2":
                sign_up_user()
            elif choice == "3":
                print("===== THANK YOU FOR USING SPEDOSERV ======")
                break
            else:
                print("======== INVALID CHOICE ========\n")
                
        except ValueError:
            print("<<<<<< INVALID INPUT >>>>>>\n")
            print("<<<<<<< PLEASE TRY AGAIN >>>>>>>")

if __name__ == "__main__":
    main()
