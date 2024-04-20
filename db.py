import mysql.connector as mysql

try:
    # Connecting to database

    conn = mysql.connect(

        host="localhost",
        user="root",
        password="root"
    )

    # Defining the cursor

    curs = conn.cursor()

    # Creating the database

    curs.execute("CREATE DATABASE IF NOT EXISTS AO_Hotel;")

    # Selecting the AO Hotel database

    curs.execute("USE AO_Hotel;")

    # Creating users table

    create_table1 = """ CREATE TABLE IF NOT EXISTS users(
                            user_id INT AUTO_INCREMENT PRIMARY KEY,
                            username VARCHAR(30) NOT NULL,
                            email VARCHAR(50) NOT NULL,
                            phone VARCHAR(11) NOT NULL,
                            gender VARCHAR(6) NOT NULL,
                            password VARCHAR(25) NOT NULL
                        );
                   """
    curs.execute(create_table1)

    # Creating reservation table

    create_table2 = """ CREATE TABLE IF NOT EXISTS reservation(
                            reservation_key INT AUTO_INCREMENT PRIMARY KEY,
                            user_id INT NOT NULL,
                            room_type VARCHAR(6) NOT NULL,
                            num_of_rooms INT NOT NULL,
                            checkin_date DATE NOT NULL,
                            checkout_date DATE NOT NULL,
                            price INT NOT NULL,
                            FOREIGN KEY (user_id) REFERENCES users(user_id)
                        );
                    """
    curs.execute(create_table2)

    # Saving the changes to the database

    conn.commit()

# Handling connection errors

except mysql.Error as err:
    print(f"Error in the database: {err}")
