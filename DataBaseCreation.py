import sqlite3
import sys


def createDatabase():
    connection = sqlite3.connect('bloodbank.db')
    connection.execute("PRAGMA foreign_keys = 1")
    cursor = connection.cursor()

    table1 = """CREATE TABLE IF NOT EXISTS bloodbank (
  bank_id      VARCHAR not null,
  name         varchar(25) not null,
  address      varchar(50) not null, 
  stock    integer not null,
  primary key (bank_id)
);"""
    cursor.execute(table1)

    table2 = """CREATE TABLE IF NOT EXISTS employee (
  name    varchar not null, 
  employee_id varchar not null,
  contact_no varchar not null,
  email_address varchar,
  login_id varchar not null,
  password varchar not null,
  Bbank_id VARCHAR not null,
  employeetype VARCHAR not null,
  primary key (employee_id),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table2)

    table3 = """CREATE TABLE IF NOT EXISTS medicalassistant (
  contact_number    integer not null,
  email_address varchar(20),
  Eemployee_id      varchar(7) not null,
  login_id varchar(20) not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table3)

    table4 = """CREATE TABLE IF NOT EXISTS receptionist (
  contact_number    integer not null,
  email_address varchar(20),
  Eemployee_id      varchar(7) not null,
  login_id varchar(20) not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table4)
            
    table5 = """CREATE TABLE IF NOT EXISTS bbt (
  Eemployee_id      varchar(7) not null,
  contact_number    integer not null,
  email_address varchar(20),
  login_id varchar(20) not null,
  Bbank_id VARCHAR not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table5)
    
    
    table6 = """CREATE TABLE IF NOT EXISTS admin (
  Eemployee_id      varchar(7) not null,
  contact_number    integer not null,
  email_address varchar(20),
  login_id varchar(20) not null,
  Bbank_id VARCHAR not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table6)

    table7 = """CREATE TABLE IF NOT EXISTS donor (
  d_id    integer not null,
  name varchar(15) not null,
  age integer,
  blood_group varchar(3) not null,
  address varchar(50),
  password varchar(15) not null,
  login_id varchar(20) not null,
  primary key (d_id,login_id)
);"""
    cursor.execute(table7)

    table8 = """CREATE TABLE IF NOT EXISTS patient (
  patient_id    integer not null,
  name varchar(15) not null,
  contact_number    integer,
  blood_group varchar(3),
  address varchar(50),
  password varchar(15) not null,
  login_id varchar(20) not null,
  primary key (patient_id,login_id)
);"""
    cursor.execute(table8)

    table9 = """CREATE TABLE IF NOT EXISTS provides (
  date  date not null,
  volume integer not null,
  Bbank_id      integer not null,
  Ppatient_id   integer not null,
  primary key (Bbank_id,Ppatient_id),
  foreign key (Bbank_id) references bloodbank(bank_id),
  foreign key (Ppatient_id) references patient(patient_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table9)
    
    table10 = """CREATE TABLE IF NOT EXISTS donate (
  date  date not null,
  volume integer not null,
  Dd_id      integer not null,
  primary key (Dd_id),
  foreign key (Dd_id) references donor(d_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table10)

    table11 = """CREATE TABLE IF NOT EXISTS bloodbank_inventory (
  blood_type varchar(3),
  Bbank_id integer not null,
  volume      integer not null,
  primary key (Bbank_id,blood_type ),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);"""
    cursor.execute(table11)
    connection.commit()
    connection.close()
