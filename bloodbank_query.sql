-- 1. drop the database bloodbank if it exists
-- 2. create the database bloodbank
-- 3. set the current DB context to the newly created database, and then execute the DDL statements.
drop database if exists bloodbank;
create database bloodbank;
use bloodbank;

CREATE TABLE bloodbank (
  bank_id      integer not null,
  name         varchar(25) not null,
  address      varchar(50) not null, 
  stock		   integer not null,
  primary key (bank_id)
);

CREATE TABLE employee (
  name    			varchar(15) not null, 
  employee_id		varchar(7) not null,
  contact_no		integer(10) not null,
  email_address		varchar(20),
  login_id			varchar(20) not null,
  password			varchar(15) not null,
  Bbank_id			integer not null,
  primary key (employee_id,login_id,contact_no,email_address),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE medicalassistant (
  contact_number    integer not null,
  email_address		varchar(15),
  Eemployee_id      varchar(7) not null,
  login_id			varchar(20) not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE receptionist (
  contact_number    integer not null,
  email_address		varchar(15),
  Eemployee_id      varchar(7) not null,
  login_id			varchar(20) not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE bbt (
  Eemployee_id      varchar(7) not null,
  contact_number    integer not null,
  email_address		varchar(15),
  login_id			varchar(20) not null,
  Bbank_id			integer not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE admin (
  Eemployee_id      varchar(7) not null,
  contact_number    integer not null,
  email_address		varchar(15),
  login_id			varchar(20) not null,
  Bbank_id			integer not null,
  primary key (Eemployee_id),
  foreign key (Eemployee_id) references employee(employee_id),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE donor (
  d_id   		integer not null,
  name	 		varchar(15) not null,
  age	 		integer,
  blood_group 	varchar(3) not null,
  address		varchar(50),
  password 		varchar(15) not null,
  login_id		varchar(20) not null,
  primary key (d_id,login_id)
);

CREATE TABLE patient (
  patient_id   		integer not null,
  name	 			varchar(15) not null,
  contact_number    integer,
  blood_group 		varchar(3),
  address			varchar(50),
  password 			varchar(15) not null,
  login_id			varchar(20) not null,
  primary key (patient_id,login_id)
);

CREATE TABLE provides (
  date  		date not null,
  volume 		integer not null,
  Bbank_id      integer not null,
  Ppatient_id   integer not null,
  primary key (Bbank_id,Ppatient_id),
  foreign key (Bbank_id) references bloodbank(bank_id),
  foreign key (Ppatient_id) references patient(patient_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE donate (
  date  		date not null,
  volume 		integer not null,
  Dd_id      	integer not null,
  primary key (Dd_id),
  foreign key (Dd_id) references donor(d_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

CREATE TABLE bloodbank_inventory (
  blood_type	varchar(3),
  Bbank_id 		integer not null,
  volume      	integer not null,
  primary key (Bbank_id,blood_type ),
  foreign key (Bbank_id) references bloodbank(bank_id)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);



----

INSERT bloodbank VALUES
(2,'San-Jose', 'grandview123 sanjose', 20);

INSERT employee VALUES
('kapil', '012345',987654321,'kapilsir@vector', 'kapilsir@bloodbank', 'kapil', 2);

Select e.name, b.bank_id, m.Eemployee_id, b.name from employee e, medicalassistant m, bloodbank b
where m.Eemployee_id = e.employee_id and b.bank_id = e.B_bank_id;