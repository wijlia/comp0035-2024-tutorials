from pathlib import Path
import pandas as pd
import sqlite3

from tutorialpkg.sample_code.example_sql_queries import sample_insert_queries


def unnormalised_db(df, db_path, table_name):
    # Create a connection to the database using sqlite3.
    conn = sqlite3.connect(db_path)

    # Save the dataframe to the databse, this will create a table called 
    # 'enrollments' and replace it if it exists. The index column is not saved 
    # to the table.
    # If the file does not exist then it will be created.
    df.to_sql(table_name, conn, if_exists='replace', index=False)

    # Close the connection.
    conn.close()


def normalised_db(db_path):
    student_sql = '''CREATE TABLE student (
                        student_id INTEGER PRIMARY KEY,
                        student_name STRING NOT NULL,
                        student_email STRING NOT NULL UNIQUE);
                        '''
    teacher_sql = '''CREATE TABLE teacher (
                        teacher_id INTEGER PRIMARY KEY,
                        teacher_name STRING NOT NULL,
                        teacher_email STRING NOT NULL UNIQUE);
                        '''
    course_sql = '''CREATE TABLE course (
                    course_id INTEGER PRIMARY KEY,
                    course_name STRING NOT NULL,
                    course_code INTEGER NOT NULL,
                    course_schedule STRING,
                    course_location STRING);
                    '''
    enrollment_sql = '''CREATE TABLE enrollment (
                            enrollment_id INTEGER PRIMARY KEY,
                            student_id INTEGER NOT NULL,
                            course_id INTEGER NOT NULL,
                            teacher_id INTEGER,
                            FOREIGN KEY (student_id) REFERENCES student(student_id) ON DELETE cascade ON UPDATE cascade,
                            FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE cascade ON UPDATE cascade,
                            FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id) ON UPDATE cascade ON DELETE SET NULL);
                            '''
    conn = sqlite3.connect(db_path)
    try:
        with conn:
            cursor = conn.cursor()

            cursor.execute('PRAGMA foreign_keys = ON;')

            cursor.execute('DROP TABLE IF EXISTS enrollment;')
            cursor.execute('DROP TABLE IF EXISTS course;')
            cursor.execute('DROP TABLE IF EXISTS teacher;')
            cursor.execute('DROP TABLE IF EXISTS student;')
            cursor.execute(student_sql)
            cursor.execute(teacher_sql)
            cursor.execute(course_sql)
            cursor.execute(enrollment_sql)
    except sqlite3.Error as err:
        print(f'An error occurred creating the database strucutre. Error: {err}')
    finally:
        if conn:
            conn.close()

def add_student_data(df, db_path):
    conn = sqlite3.connect(db_path)

    try:
        with conn:
            cursor = conn.cursor()
            cursor.execute('PRAGMA foreign_keys = ON;')

            # Insert data into student table (unique values only)
            student_sql = 'INSERT INTO student (student_name, student_email) VALUES (?, ?)'
            student_df = pd.DataFrame(df[['student_name', 'student_email']].drop_duplicates())
            student_data = student_df.values.tolist()
            cursor.executemany(student_sql, student_data)

            # Insert data into teacher table (unique values only)
            teacher_sql = 'INSERT INTO teacher (teacher_name, teacher_email) VALUES (?, ?)'
            teacher_df = pd.DataFrame(df[['teacher_name', 'teacher_email']].drop_duplicates())
            teacher_data = teacher_df.values.tolist()
            cursor.executemany(teacher_sql, teacher_data)

            # Insert data into course table (unique values only)
            course_sql = 'INSERT INTO course (course_name, course_code, course_schedule, course_location) VALUES (?, ?, ?, ?)'
            course_df = pd.DataFrame(df[['course_name', 'course_code', 'course_schedule', 'course_location']].drop_duplicates())
            course_data = course_df.values.tolist()
            cursor.executemany(course_sql, course_data)

            # Insert data into enrollment table
            for index, row in df.iterrows():
                # Find student_id
                student_email = row['student_email']
                select_student_sql = f'SELECT student_id FROM student WHERE student_email = "{student_email}"'
                result = cursor.execute(select_student_sql).fetchone()
                s_id = result[0]

                # Find teacher_id
                teacher_email = row['teacher_email']
                select_teacher_sql = f'SELECT teacher_id FROM teacher WHERE teacher_email = "{teacher_email}"'
                result = cursor.execute(select_teacher_sql).fetchone()
                t_id = result[0]

                # Find course_id
                course_code = row['course_code']
                select_course_sql = f'SELECT course_id FROM course WHERE course_code = "{course_code}"'
                result = cursor.execute(select_course_sql).fetchone()
                c_id = result[0]

                # Insert new row into the enrollment table
                enrollment_insert_sql = 'INSERT INTO enrollment (student_id, teacher_id, course_id) VALUES (?, ?, ?)'
                student_values = (s_id, t_id, c_id)
                cursor.execute(enrollment_insert_sql, student_values)
    except sqlite3.Error as err:
        print(f'An error occurred creating the database. Error: {err}')
    finally:
        if conn:
            conn.close()



def main():
    # Activity 5-2
    student_data_path = Path(__file__).parent.parent.joinpath('data_db_activity',
                                                              'student_data.csv')
    student_data_df = pd.read_csv(student_data_path)
    unn_db_path = Path(__file__).parent.parent.joinpath('data_db_activity',
                                                        'enrollments_unnormalised.db')
    unnormalised_db(student_data_df, unn_db_path, 'enrollments')

    # Activity 5-3
    norm_db_path = Path(__file__).parent.parent.joinpath('data_db_activity',
                                                         'enrollments_normalised.db')
    normalised_db(norm_db_path)
    add_student_data(student_data_df, norm_db_path)


if __name__ == '__main__':
    main()