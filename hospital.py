

import streamlit as st
import mysql.connector
from datetime import date

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Shreyas@123",  # Replace with your MySQL password
    database="hospitalmanagement"
)
cursor = db.cursor()

# Functions
def add_patient(name, age, gender, phone, address):
    query = "INSERT INTO patients (name, age, gender, phone, address) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (name, age, gender, phone, address))
    db.commit()
    st.success("Patient added successfully!")

def view_patients():
    cursor.execute("SELECT * FROM patients")
    return cursor.fetchall()

def add_doctor(name, specialty, phone):
    query = "INSERT INTO doctors (name, specialty, phone) VALUES (%s, %s, %s)"
    cursor.execute(query, (name, specialty, phone))
    db.commit()
    st.success("Doctor added successfully!")

def view_doctors():
    cursor.execute("SELECT * FROM doctors")
    return cursor.fetchall()

def book_appointment(patient_id, doctor_id, appointment_date):
    query = "INSERT INTO appointments (patient_id, doctor_id, appointment_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (patient_id, doctor_id, appointment_date))
    db.commit()
    st.success("Appointment booked successfully!")

def view_appointments():
    cursor.execute("""
        SELECT a.appointment_id, p.name AS patient_name, d.name AS doctor_name, a.appointment_date
        FROM appointments a
        JOIN patients p ON a.patient_id = p.patient_id
        JOIN doctors d ON a.doctor_id = d.doctor_id
    """)
    return cursor.fetchall()

# Streamlit Interface
st.title("Hospital Management System")

menu = ["Add Patient", "View Patients", "Add Doctor", "View Doctors", "Book Appointment", "View Appointments"]
choice = st.sidebar.selectbox("Menu", menu)

if choice == "Add Patient":
    st.subheader("Add a New Patient")
    name = st.text_input("Patient Name")
    age = st.number_input("Age", min_value=0, max_value=120, step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")
    if st.button("Add Patient"):
        add_patient(name, age, gender, phone, address)

elif choice == "View Patients":
    st.subheader("Patient List")
    patients = view_patients()
    for patient in patients:
        st.write(patient)

elif choice == "Add Doctor":
    st.subheader("Add a New Doctor")
    name = st.text_input("Doctor Name")
    specialty = st.text_input("Specialty")
    phone = st.text_input("Phone Number")
    if st.button("Add Doctor"):
        add_doctor(name, specialty, phone)

elif choice == "View Doctors":
    st.subheader("Doctor List")
    doctors = view_doctors()
    for doctor in doctors:
        st.write(doctor)

elif choice == "Book Appointment":
    st.subheader("Book an Appointment")
    patient_id = st.number_input("Patient ID", min_value=1, step=1)
    doctor_id = st.number_input("Doctor ID", min_value=1, step=1)
    appointment_date = st.date_input("Appointment Date", min_value=date.today())
    if st.button("Book Appointment"):
        book_appointment(patient_id, doctor_id, appointment_date)

elif choice == "View Appointments":
    st.subheader("Appointment List")
    appointments = view_appointments()
    for appointment in appointments:
        st.write(appointment)
