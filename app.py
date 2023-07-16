import streamlit as st
import mysql.connector
import pandas as pd
import requests
from streamlit_lottie import st_lottie
config = {
    'user': 'root',
    'password': 'IMkhan@123@#',
    'host': 'localhost',
    'port': 3305,  # Update the port number to 3305 because in installation i gave port 3305
    'database':'userdb'
}

def loti(url):
    r = requests.get(url)
    if r.status_code != 200:
       return None
    else:
        return r.json()
def create_connection():
    """Create a connection to the MySQL database."""
    db = mysql.connector.connect(**config)
    return db

def create_database(db):
    """Create the 'userdb' database if it doesn't exist."""
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS userdb")
    cursor.close()

def create_patients_table(db):
    """Create the patients table in the database."""
    cursor = db.cursor()

    create_patients_table_query = """
    CREATE TABLE IF NOT EXISTS patients (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        age INT,
        contact_number VARCHAR,
        address VARCHAR(255),
        date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMPCHAR(20),
        email VARCHAR(255),
    )
    """

    cursor.execute(create_patients_table_query)
    db.commit()
    st.write("Patients table created successfully.")

def modify_patients_table(db):
    cursor = db.cursor()

    alter_table_query = """
    ALTER TABLE patients
    ADD COLUMN doctor_name VARCHAR(255),
    ADD COLUMN disease VARCHAR(255),
    ADD COLUMN fee INTEGER(5),
    ADD COLUMN tests VARCHAR(255),
    ADD COLUMN cnic VARCHAR(20)
    """

    cursor.execute(alter_table_query)
    db.commit()
    st.write("Patients table modified successfully.")



def create_appointments_table(db):
    """Create the appointments table in the database."""
    cursor = db.cursor()

    create_appointments_table_query = """
    CREATE TABLE IF NOT EXISTS appointments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        patient_id INT,
        appointment_date DATE,
        appointment_time TIME,
        doctor_name VARCHAR(255),
        notes TEXT,
        FOREIGN KEY (patient_id) REFERENCES patients(id)
    )
    """

    cursor.execute(create_appointments_table_query)
    db.commit()
    st.write("Appointments table created successfully.")

def insert_patient_record(db, name, age, contact_number, email, address):
    """Insert a new patient record into the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    insert_patient_query = """
    INSERT INTO patients (name, age, contact_number, email, address)
    VALUES (%s, %s, %s, %s, %s)
    """

    patient_data = (name, age, contact_number, email, address)

    cursor.execute(insert_patient_query, patient_data)
    db.commit()
    st.write("Patient record inserted successfully.") 

def fetch_all_patients(db):
    """Fetch all records from the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch all patients
    select_patients_query = "SELECT * FROM patients"
    cursor.execute(select_patients_query)
    patients = cursor.fetchall()

    return patients       

def fetch_patient_by_id(db, patient_id):
    """Fetch a patient's record from the 'patients' table based on ID."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch the patient by ID
    select_patient_query = "SELECT * FROM patients WHERE id = %s"
    cursor.execute(select_patient_query, (patient_id,))
    patient = cursor.fetchone()

    return patient

def fetch_patient_by_contact(db, contact_number):
    """Fetch a patient's record from the 'patients' table based on contact number."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch the patient by contact number
    select_patient_query = "SELECT * FROM patients WHERE contact_number = %s"
    cursor.execute(select_patient_query, (contact_number,))
    patient = cursor.fetchone()

    return patient


def fetch_patient_by_cnis(db, cnis):
    """Fetch a patient's record from the 'patients' table based on CNIS."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch the patient by CNIS
    select_patient_query = "SELECT * FROM patients WHERE cnis = %s"
    cursor.execute(select_patient_query, (cnis,))
    patient = cursor.fetchone()

    return patient

     

def delete_patient_record(db, delete_option, delete_value):
    """Delete a patient record from the 'patients' table based on ID, name, or contact number."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Delete the patient record
    if delete_option == "ID":
        delete_patient_query = "DELETE FROM patients WHERE id = %s"
    elif delete_option == "Name":
        delete_patient_query = "DELETE FROM patients WHERE name = %s"
    elif delete_option == "Contact Number":
        delete_patient_query = "DELETE FROM patients WHERE contact_number = %s"

    cursor.execute(delete_patient_query, (delete_value,))
    db.commit()
    st.write("Patient record deleted successfully.")

def insert_appointment_record(db, patient_id, appointment_date, appointment_time, doctor_name, notes):
    """Insert a new appointment record into the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")
    appointment_time = appointment_time.strftime("%H:%M:%S")
    appointment_date = appointment_date.strftime("%Y-%m-%d")
    insert_appointment_query = """
    INSERT INTO appointments (patient_id, appointment_date, appointment_time, doctor_name, notes)
    VALUES (%s, %s, %s, %s, %s)
    """

    appointment_data = (patient_id, appointment_date, appointment_time, doctor_name, notes)

    cursor.execute(insert_appointment_query, appointment_data)
    db.commit()
    print("Appointment record inserted successfully.")


def fetch_all_appointments(db):
    """Fetch all records from the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch all appointments
    select_appointments_query = """
    SELECT id, patient_id, DATE_FORMAT(appointment_date, '%Y-%m-%d') AS appointment_date, 
           appointment_time, doctor_name, notes
    FROM appointments
    """
    cursor.execute(select_appointments_query)
    appointments = cursor.fetchall()

    return appointments

def show_all_appointments(db):
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")
    select_query = """
    SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes FROM appointments
    """
    cursor.execute(select_query)
    records = cursor.fetchall()

    if records:
        st.subheader("All Appointment Records")
        df = pd.DataFrame(records, columns=['ID', 'Patient ID', 'Appointment Date', 'Appointment Time', 'Doctor Name', 'Notes'])
        st.dataframe(df)
    else:
        st.write("No appointments found")           

def edit_appointment_record(db, appointment_id, new_appointment_date, new_appointment_time, new_doctor_name, new_notes):
    """Edit an appointment record in the 'appointments' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Update the appointment record
    update_appointment_query = """
    UPDATE appointments
    SET appointment_date = %s, appointment_time = CAST(%s AS TIME), doctor_name = %s, notes = %s
    WHERE id = %s
    """
    appointment_data = (new_appointment_date, new_appointment_time, new_doctor_name, new_notes, appointment_id)

    cursor.execute(update_appointment_query, appointment_data)
    db.commit()
    

def fetch_appointment_by_id(db, appointment_id):
    """Fetch an appointment's record from the 'appointments' table based on ID."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Fetch the appointment by ID
    select_appointment_query = """
       SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes
       FROM appointments
       WHERE id = %s
       """
    cursor.execute(select_appointment_query, (appointment_id,))
    appointment = cursor.fetchone()

    return appointment  


def fetch_appointment_by_patient_id(db, patient_id):

    query = """
    SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes
    FROM appointments
    WHERE patient_id = %s
    """
    cursor = db.cursor()
    cursor.execute("USE userdb")
    cursor.execute(query, (patient_id,))
    appointment = cursor.fetchone()
    #cursor.close()
    return appointment  


def fetch_appointment_by_doctor_name(db, doctor_name):
    query = """
    SELECT id, patient_id, appointment_date, CAST(appointment_time AS CHAR), doctor_name, notes
    FROM appointments
    WHERE doctor_name = %s
    """
    cursor = db.cursor()
    cursor.execute("USE userdb")
    cursor.execute(query, (doctor_name,))
    appointment = cursor.fetchone()
    #cursor.close()
    return appointment        


def search_appointment(db):
    search_option = st.selectbox("Select search option", ["ID", "Patient ID", "Doctor Name"],key="search_option")
    search_value = st.text_input("Enter search value",key="search_value")

    if st.button("Search"):
        if search_option == "ID":
            appointment = fetch_appointment_by_id(db, search_value)
        elif search_option == "Patient ID":
            appointment = fetch_appointment_by_patient_id(db, search_value)
        elif search_option == "Doctor Name":
            appointment = fetch_appointment_by_doctor_name(db, search_value)

        if appointment:
            st.subheader("Appointment Details")
            df = pd.DataFrame([appointment], columns=['ID', 'Patient ID', 'Appointment Date', 'Appointment Time', 'Doctor Name', 'Notes'])
            st.dataframe(df)
            st.session_state.edit_appointment = appointment
        else:
            st.write("Appointment not found")
    if 'edit_appointment' in st.session_state:
        edit_appointment(db)        

def edit_appointment(db):
    #if 'edit_appointment' in st.session_state:
        appointment = st.session_state.edit_appointment
        st.subheader("Edit Appointment Details")
        new_appointment_date = st.date_input("Appointment Date", value=appointment[2])
        new_appointment_time = st.text_input("Appointment Time", value=appointment[3])
        new_doctor_name = st.text_input("Doctor Name", value=appointment[4])
        new_notes = st.text_input("Notes", value=appointment[5])

        if st.button("Update Appointment"):
            edit_appointment_record(db, appointment[0], new_appointment_date, new_appointment_time, new_doctor_name, new_notes)
            st.write("Appointment record updated successfully.")
            del st.session_state.edit_appointment

def update_patient_record(db):
    """Update a patient's record in the 'patients' table."""

    search_option = st.selectbox("Select search option", ["ID", "Contact Number", "CNIS"], key="search_option")
    search_value = st.text_input("Enter search value", key="search_value")

    if st.button("Search :magic_wand:"):
        if search_option == "ID":
            patient = fetch_patient_by_id(db, search_value)
        elif search_option == "Contact Number":
            patient = fetch_patient_by_contact(db, search_value)
        elif search_option == "CNIS":
            patient = fetch_patient_by_cnis(db, search_value)

        if patient:
            st.subheader("Patient Details")
            df = pd.DataFrame([patient], columns=['ID', 'Name', 'Age', 'Contact Number', 'Email', 'Address', 'Date Added'])
            st.dataframe(df)
            st.session_state.edit_patient = patient
        else:
            st.write("Patient not found")

    if 'edit_patient' in st.session_state:
        edit_patient(db)


def edit_patient(db):
    """Edit a patient's record in the 'patients' table."""

    st.subheader("Edit Patient Details")
    new_name = st.text_input("Enter new name", value=st.session_state.edit_patient[1])
    new_age = st.number_input("Enter new age", value=st.session_state.edit_patient[2])
    new_contact = st.text_input("Enter new contact number", value=st.session_state.edit_patient[3])
    new_email = st.text_input("Enter new email", value=st.session_state.edit_patient[4])
    new_address = st.text_input("Enter new address", value=st.session_state.edit_patient[5])

    if st.button("Update :roller_coaster:"):
        patient_id = st.session_state.edit_patient[0]
        update_patient_info(db, patient_id, new_name, new_age, new_contact, new_email, new_address)
        


def update_patient_info(db, patient_id, new_name, new_age, new_contact, new_email, new_address):
    """Update a patient's record in the 'patients' table."""
    cursor = db.cursor()

    # Select the database
    cursor.execute("USE userdb")

    # Update the patient record
    update_patient_query = """
    UPDATE patients
    SET name = %s, age = %s, contact_number = %s, email = %s, address = %s
    WHERE id = %s
    """
    patient_data = (new_name, new_age, new_contact, new_email, new_address, patient_id)

    cursor.execute(update_patient_query, patient_data)
    db.commit()
    st.write("Patient record updated successfully.")





def main():
    # Title and sidebar
    st.title("Patient Management System :hospital:")
    lott1 = loti( "https://assets6.lottiefiles.com/packages/lf20_olluraqu.json")
    lotipatient = loti("https://assets6.lottiefiles.com/packages/lf20_vPnn3K.json")
    db = create_connection()

    #create_database(db)

    #config['database'] = 'userdb'  # Update the database name
    #db = create_connection()

    #create_patients_table(db)
    #create_appointments_table(db)
    #modify_patients_table(db)

    menu = ["Home","Add patient Record","Show patiet Records", "Search and Edit Patient","Deetel Patients Record",
            "Add patients Appointments","Show All Appointments","Search and Edit Patients Appointments"]
    options = st.sidebar.radio("Select an Option :dart:",menu)
    if options== "Home":
        st.subheader("Welcome to Hospital Mnagement System")
        st.write("Navigate from sidebar to access database")
        st_lottie(lott1,height=500)
        #st.image('hospital.jpg', width=600)

    elif options == "Add patient Record":
       st.subheader("Enter patient details :woman_in_motorized_wheelchair:")
       st_lottie(lotipatient,height = 200)
       name = st.text_input("Enter name of patient",key = "name")
       age = st.number_input("Enter age of patient",key = "age",value = 1)
       contact = st.text_input("Enter contact of patient",key = "contact")
       email = st.text_input("Enter Email of patient",key = "email")
       address = st.text_input("Enter Address of patient",key= "address")
       if st.button("add patient record"):
          cursor = db.cursor()
          select_query = """
          SELECT * FROM patients WHERE contact_number=%s
          """
          cursor.execute(select_query,(contact,))
          existing_patient = cursor.fetchone()
          if existing_patient:
            st.warning("A patient with the same contact number already exist")
          else:  
            insert_patient_record(db, name, age, contact, email, address)

    elif options=="Show patiet Records":
        patients = fetch_all_patients(db)
        if patients:
            st.subheader("All patients Records :magic_wand:")
            df = pd.DataFrame(patients, columns=['ID', 'Name', 'Age', 'Contact Number', 'Email', 'Address', 'Date Added'])
            st.dataframe(df)
        else:
            st.write("No patients found")
    elif options == "Search and Edit Patient":
         update_patient_record(db)
           

    elif options == "Deetel Patients Record":
         st.subheader("Search a patient to delate :skull_and_crossbones:")
         delete_option = st.selectbox("Select delete option", ["ID", "Name", "Contact Number"], key="delete_option")
         delete_value = st.text_input("Enter delete value", key="delete_value")

         if st.button("Delete"):
            delete_patient_record(db, delete_option, delete_value)

    elif options == "Add patients Appointments":
          patient_id = st.number_input("Enter patient ID:", key="appointment_patient_id")
          appointment_date = st.date_input("Enter appointment date:", key="appointment_date")
          appointment_time = st.time_input("Enter appointment time:", key="appointment_time")
          doctor_name = st.text_input("Enter doctor's name:", key="appointment_doctor_name")
          notes = st.text_area("Enter appointment notes:", key="appointment_notes")

          if st.button("Add Appointment"):
               insert_appointment_record(db, patient_id, appointment_date, appointment_time, doctor_name, notes)
               st.write("Appointment record added successfully.")    

    elif options=="Show All Appointments":
         show_all_appointments(db)


    elif options == "Search and Edit Patients Appointments":

        search_appointment(db) 
                

    db.close()

if __name__ == "__main__":
    main()
