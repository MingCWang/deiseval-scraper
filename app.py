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

     
    cursor.execute("DROP TABLE IF EXISTS course_data;")
    
    cursor.execute('''CREATE TABLE course_data (
    id serial PRIMARY KEY,
    course text,
    courseTitle text,
    syllabus text,
    instructor text,
    term text,
    requirements text[], -- Assuming it's an array
    prerequisites text,
    description text
    );''')
    
    
    insert_query = """
INSERT INTO course_data (course, courseTitle, syllabus, instructor, term, requirements, prerequisites, description)
VALUES (%(course)s, %(courseTitle)s, %(syllabus)s, %(instructor)s, %(term)s, %(requirements)s, %(prerequisites)s, %(description)s);
"""
    print("Inserting data into the database...")
    for data in data_list:
        cursor.execute(insert_query, data)

    cursor.execute("COPY (SELECT * FROM course_data) TO '/Users/minstonewang/Development/projects/deis-course-web-scraper/courses.csv' DELIMITER ',' CSV HEADER;")
    
except (Exception, psycopg2.Error) as error:
    print(f"Error while connecting to the database: {error}")

finally:
    # Close the database connection when done
    if connection:
        cursor.close()
        connection.commit()
        connection.close()
        print("Database connection closed.")

