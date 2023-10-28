import psycopg2
import json

try:
    connection = psycopg2.connect(
        host="localhost",         # Hostname or IP address of your database server
        database="courses",  # Name of your database
        user="minstonewang",     # Your PostgreSQL username
        password=""  # Your PostgreSQL password
    )
    cursor = connection.cursor()
    
    print("Connected to the database!")

    # Perform database operations here
    with open("data.json", "r") as json_file:
        data_list = json.load(json_file)
     
    print(data_list[0])
     
    # cursor.execute('''CREATE TABLE course_data (
    # id serial PRIMARY KEY,
    # course varchar(255),
    # courseTitle varchar(255),
    # syllabus varchar(255),
    # instructor varchar(255),
    # term varchar(255),
    # requirements varchar(255)[], -- Assuming it's an array
    # description text
    # );''')
    
    
#     insert_query = """
# INSERT INTO course_data (course, courseTitle, syllabus, instructor, term, requirements, description)
# VALUES (%(course)s, %(courseTitle)s, %(syllabus)s, %(instructor)s, %(term)s, %(requirements)s, %(description)s);
# """
#     print("Inserting data into the database...")
#     for data in data_list:
#         cursor.execute(insert_query, data)

    cursor.execute("COPY (SELECT * FROM course_data) TO '/Users/minstonewang/Desktop/courses.csv' DELIMITER ',' CSV HEADER;")
    
except (Exception, psycopg2.Error) as error:
    print(f"Error while connecting to the database: {error}")

finally:
    # Close the database connection when done
    if connection:
        cursor.close()
        connection.commit()
        connection.close()
        print("Database connection closed.")

