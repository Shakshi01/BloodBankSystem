import logging
import sqlite3
import tkinter
from datetime import date
from sqlite3.dbapi2 import Cursor
from tkinter import *
from tkinter import messagebox, scrolledtext, ttk

from PIL import Image, ImageTk

from DataBaseCreation import createDatabase
from HashSaltPassword import *

createDatabase()
logging.basicConfig(filename='bloodBank.log',level=logging.INFO,format='%(asctime)s:%(levelname)s:%(lineno)d:%(funcName)s:%(message)s')


connection = sqlite3.connect('bloodbank.db')
cursor = connection.cursor()
x = ''

#screen number 1
def login():
    password_check = 0
    try:
        connection=sqlite3.connect('bloodbank.db')
        cursor=connection.cursor()
        cursor.execute("select * from employee where login_id=?",(loginEntry.get(),))
        row1 = cursor.fetchone()
        global x
        x=loginEntry.get()
        
        cursor.execute("select * from employee, medicalassistant where Eemployee_id=employee_id and login_id LIKE 'ME%' AND login_id=?",(loginEntry.get(),))
        row2=cursor.fetchone()
        cursor.execute("select * from employee, receptionist where Eemployee_id=employee_id and login_id LIKE 'RE%' AND login_id=?",(loginEntry.get(),))
        row3=cursor.fetchone()
        cursor.execute("select * from employee, bbt where Eemployee_id=employee_id and login_id LIKE 'BB%' AND login_id=?",(loginEntry.get(),))
        row4=cursor.fetchone()
        cursor.execute("select * from employee, admin where Eemployee_id=employee_id and login_id LIKE 'AD%' AND login_id=?",(loginEntry.get(),))
        row5=cursor.fetchone()
        
        databasepassword = ""
        if row1: 
            databasepassword = row1[5]
        
        passwrodCheck = checkPassword(passwordEntry.get(),databasepassword)

        if row1 and passwrodCheck:
            messagebox.showinfo('info','Succcessfully Loggedin')
            logging.info('Login:{} has logged in'.format(loginEntry.get()))


        else:
            messagebox.showinfo('info','Failed Loggingin')
            logging.error('Failed login: Attempt to login using {} login'.format(loginEntry.get(),))
        
        connection.commit()
    except ValueError as v:
        messagebox.showerror('Error','Check the Information you given')
        
    except sqlite3.DatabaseError as e:
        connection.rollback()
        messagebox.showerror("Failed ", e)
    except Exception as u:
        messagebox.showerror('Error', 'Enter All Details')
        
    else:
        passwordEntry.delete(0,END)
        loginEntry.delete(0,END)
        loginEntry.focus()  
        
        if connection is not None:
            connection.close()
        

def back():
    sign.withdraw()
    root.deiconify()
    loginEntry.focus_set()
    name.focus_set()
    
    
def signup():
    sign.deiconify()
    root.withdraw()
    employeeEntry.focus_set()
    
#db=connection
#role = employeetype

def signup():
    sign.deiconify()
    root.withdraw()
    name.focus_set()
    
def employeeadding_del():
    contactEntry.delete(0,END)
    email_addressEntry.delete(0,END)
    login_idEntry.delete(0,END)
    nameEntry.delete(0,END)
    passwordEntry.delete(0,END)
    #employeetypeEntry.delete(0,END)
    employeeEntry.delete(0,END)
    employeeEntry.focus()
    
def employeeadding():
    connection = None
    try:
        connection=sqlite3.connect('bloodbank.db')
        cursor=connection.cursor()
        cursor.execute("select employee_id from employee")
        employeeid_list = cursor.fetchall()
        email_address = email_addressEntry.get()
        name = nameEntry.get()
        employee_id = employeeEntry.get()
        contact_no = int(contactEntry.get())
        login_id = login_idEntry.get()
        passwordhash = passwordHashing(passwordEntry.get())
        password = passwordhash
        Bbank_id= bank_idEntry.get()
        #employeetype=employeetypeEntry.get()
        email_address_flag= True
        name_flag=True
        employee_id_flag= True
        contact_no_flag= True
        login_id_flag= True
        password_flag= True
        #employeetype_flag = True
        Bbank_id_flag = True
        
        if (employee_id,) in employeeid_list:
            messagebox.showerror("Error"," This Employee ID  Already Exists")
            logging.error('Failure to register as {} '.format(employee_id,))
            employeeadding_del()
            employee_id_flag = False
            #e_idEntry.focus_set()
            
        elif (employee_id,) is None:
            messagebox.showerror("Error"," Only Positive Employee ID")
            logging.error('Failure to register as {} '.format(employee_id,))
            employeeadding_del()
            employeeEntry.focus()
            employee_id_flag = False
            #e_idEntry.focus_set()

        else:
            employee_id_flag = True
        
        if any(i.isdigit() for i in name):
            messagebox.showerror("Error", "Numeric Characters are Not allowed in Name")
            logging.error('Failure to register as {} '.format(employee_id,))
            employeeadding_del()
            employeeEntry.focus()
            name_flag = False
            
        elif(len(name)<4):
            messagebox.showerror("Error", "Name Must Contain atleast 4 Characters ")
            logging.error('Failure to register as {} '.format(employee_id,))
            employeeadding_del()
            employeeEntry.focus()
            name_flag = False           
            
        else:
            name_flag = True
        
        
        if(len(str(contact_no))<10 or len(str(contact_no))>10):
            messagebox.showerror("Error", "Contact Number must Contain 10 Integers")
            logging.error('Failure to register as {} '.format(employee_id,))
            employeeadding_del()
            employeeEntry.focus()
            contact_no_flag = False 
        else:
            contact_no_flag = True
        
        
        
        if(len(login_id) < 5):
            messagebox.showerror("Error", "Login ID should Contain Atlease 5 Characters")
            logging.error('Failure to register as {} '.format(employee_id,))
            employeeadding_del()
            employeeEntry.focus()
            login_id_flag = False 
        else:
            login_id_flag = True
        
        
        if(len(passwordEntry.get()) < 5):
            messagebox.showerror("Error", "Password should Contain Atlease 5 Characters")
            logging.error('Failure to register as {} '.format(employee_id,))
            passwordEntry.delete(0,END)
            passwordEntry.focus_set() 
            login_id_flag = False 
        else:
            password_flag = True
            
        if(int(Bbank_id)<0):
            messagebox.showerror("Error", "Bank  ID Should be a positive number")
            logging.error('Failure to register as {} '.format(employee_id,))
            employeeadding_del()
            employeeEntry.focus()
            Bbank_id_flag = False 
        else:
            Bbank_id_flag = True
            
        if employee_id_flag == True and Bbank_id_flag == True and login_id_flag == True and contact_no_flag == True and password_flag == True and name_flag == True :
            
            cursor.execute("INSERT INTO employee Values (?,?,?,?,?,?,?)",(name,employee_id,str(contact_no),email_address,login_id,password,Bbank_id))
            connection.commit()
            msg = str(cursor.rowcount) +" Inserted the Records and Successfully Created the Account"
            messagebox.showinfo("Success ", msg)
            logging.info('Registration: {} {} ({}) has been added as {} to database '.format(name,employee_id,contact_no,email_address,login_id,))
            connection.commit()          
            # if employeetype=='Medical Assistant':
            #     cursor.execute("Insert into medicalassistant (?)",(employee_id,))
            #     connection.commit()
            # elif employeetype =='BBT':
            #     cursor.execute("Insert into bbt Values (?,?)",(employee_id,Bbank_id))
            #     connection.commit()
            # elif employeetype=='Receptionist':
            #     cursor.execute("Insert into receptionist (?)",(employee_id,))
            #     connection.commit()
            # elif employeetype=='Admin':
            #     cursor.execute("Insert into admin Values (?,?)",(employee_id,Bbank_id))
            #     connection.commit()
            cursor.execute("select * from employee")
            for i in cursor:
                print(i)


    except ValueError as v:
        messagebox.showerror('Error','Please enter Contact Number as Integer, Name as Character, Bank ID as Integer')
        logging.error('Failure to register as {} '.format(employee_id,))
        employeeadding_del()            
        employeeEntry.focus()
        
    except sqlite3.DatabaseError as e:
        connection.rollback()
        print(e.message)
        messagebox.showerror("Failure ", e)
        logging.error('Failure to register as {} '.format(employee_id,))
        employeeadding_del()
        employeeEntry.focus()
        
        if connection is not None:
            connection.rollback()
            
    except Exception as u:
        print(login_id, contact_no, email_address, name, employee_id, password, Bbank_id)
        messagebox.showerror('Error', 'Enter All Details')
        logging.error('Failure to register as {} '.format(employee_id,))
        # contactEntry.delete(0,END)
        # email_addressEntry.delete(0,END)
        # loginEntry.delete(0,END)
        # nameEntry.delete(0,END)
        # passwordEntry.delete(0,END)
        # #employeetypeEntry.delete(0,END)
        # employeeEntry.delete(0,END)
        employeeEntry.focus()
        
        
    else:
        if employee_id_flag == True and Bbank_id_flag == True and login_id_flag == True and contact_no_flag == True and password_flag == True and name_flag == True :
            employeeadding_del()
            employeeEntry.focus()
        #resetDbaTree(cursor)
        if connection is not None:
            connection.close()
        
        
    
root = Tk()  
root.geometry('888x500')  
root.title('Blood Supply Management System')

#my_img1 = my_img
#my_label1 = my_label
my_img= ImageTk.PhotoImage(Image.open("icon.ico"))
my_label=Label(root,image=my_img)
my_label.pack()
my_label.place(x=0,y=0)

#usernameLabel = loginidLabel
#usernamee = loginid
#usernameEntry = loginEntry
loginidLabel = Label(root, text="Login ID",font='Arial 20',borderwidth=5,padx=20)
loginidLabel.pack()
loginidLabel.place(x=300,y=100)
login1= StringVar()
loginEntry = Entry(root, textvariable=login1,font='Arial 20',borderwidth=5)  
#usernameEntry.grid(row=0, column=1)
loginEntry.pack(pady=2)
loginEntry.place(x=550,y=100)
print(loginEntry.get())


#password label and password entry box
passwordLabel = Label(root,text="Password",font='Arial 20',borderwidth=5,padx=30)
#passwordLabel.grid(row=1, column=0)  
passwordLabel.pack(pady=2)
passwordLabel.place(x=300,y=200)
passworde = StringVar()
passwordEntry = Entry(root, textvariable=passworde, show='*',font='Arial 20',borderwidth=5) 
#passwordEntry.grid(row=1, column=1) 
passwordEntry.pack(pady=2)
#validateLogin = partial(validateLogin, username, password)
passwordEntry.place(x=550,y=200)

#login button
loginEntry.focus_set()
loginButton = Button(root, text="Login", command=login,font='Arial 20',padx=20,fg='blue',borderwidth=5) 
#loginButton.grid(row=4, column=0) 
loginButton.pack(pady=2)
loginButton.place(x=350,y=300)


#registerButton = signupButton
#register = signup
#signup button
signupButton = Button(root, text="Signup", command=signup,font='Arial 20',padx=30,fg='blue',borderwidth=5) 
signupButton.pack(pady=2)
signupButton.place(x=550,y=300)





#reg = sign

#SIGNUP page
sign = Toplevel(root)
sign.title("SIGNUP")
sign.geometry("888x500")
sign.withdraw()

#my_img1 = signup_img1, my_label1 = signup_label1
signup_img1= ImageTk.PhotoImage(Image.open("icon.ico"))
signup_label1=Label(sign,image=signup_img1)
signup_label1.pack()
signup_label1.place(x=0,y=0)

 
 
name = Label(sign, text="Name",font='Arial 11',borderwidth=5,padx=25)
name.pack()
name.place(x=20,y=150)
nameEntry = Entry(sign,font='Arial 11',borderwidth=5)  
nameEntry.pack(pady=2)
nameEntry.place(x=120,y=150)       
    

#Labels
#employeeID
employee_id1 = Label(sign, text="Employee ID",font='Arial 11',borderwidth=5,padx=1)
employee_id1.pack()
employee_id1.place(x=20,y=50)
#fnEntry = employeeEntry
employeeEntry = Entry(sign, font='Arial 11', borderwidth=5)  
employeeEntry.pack(pady=2)
employeeEntry.place(x=120,y=50)

contact_no1 = Label(sign, text="Contact Number",font='Arial 11',borderwidth=5,padx=1)
contact_no1.pack()
contact_no1.place(x=450,y=50)
contactEntry = Entry(sign, font='Arial 11',borderwidth=5) 
contactEntry.pack(pady=2)
contactEntry.place(x=550,y=50)



email_address = Label(sign, text="Email Address",font='Arial 11',borderwidth=5,padx=25)
email_address.pack()
email_address.place(x=400,y=150)
email_addressEntry = Entry(sign,font='Arial 11',borderwidth=5)  
email_addressEntry.pack(pady=2)
email_addressEntry.place(x=550,y=150)

login_id1 = Label(sign, text="Login ID",font='Arial 11',borderwidth=5,padx=1)
login_id1.pack()
login_id1.place(x=20,y=250)
login_idEntry = Entry(sign,font='Arial 11',borderwidth=5)  
login_idEntry.pack(pady=2)
login_idEntry.place(x=120,y=250)

#passwordEntry1 = passwordEntry
password = Label(sign, text="Password",font='Arial 11',borderwidth=5,padx=5)
password.pack()
password.place(x=450,y=250)
passwordEntry = Entry(sign,font='Arial 11', show='*',borderwidth=5)  
passwordEntry.pack(pady=2)
passwordEntry.place(x=550,y=250)



bank_id1 = Label(sign, text="Bank ID",font='Arial 11',borderwidth=5,padx=5)
bank_id1.pack()
bank_id1.place(x=450,y=350)
bank_idEntry = Entry(sign,font='Arial 11',borderwidth=5)
bank_idEntry.pack(pady=2)
bank_idEntry.place(x=550,y=350)


# #op = page1
# #role1 = employeetype1
# #rolechoosen = employeetypeEntry
# page1 = tkinter.StringVar()
# employeetype1 = Label(sign, text="USER TYPE",font='Arial 11',borderwidth=5,padx=5)
# employeetype1.pack()
# employeetype1.place(x=20,y=350)
# employeetypeEntry = ttk.Combobox(sign, width = 27, textvariable=page1, state='readonly')
# employeetypeEntry['values']=('Medical Assistant','BBT','Receptionist ','Admin')
# employeetypeEntry.pack(pady=2)
# employeetypeEntry.place(x=120,y=350)
# employeetypeEntry.current()


#regstbutton = signupbutton

#register button to save to the database
sigbutton = Button(sign, text="Sign Up",font='Arial 20', command= employeeadding ,padx=20,fg='blue',borderwidth=5) 
#loginButton.grid(row=4, column=0) 
sigbutton.pack(pady=2)
sigbutton.place(x=50,y=420)

#back button
backButton = Button(sign, text="Back",font='Arial 20', command= back, padx=30, fg='blue', borderwidth=5) 
backButton.pack(pady=2)
backButton.place(x=550,y=420)
root.mainloop()









# #Detail page Engineer
# dash = Toplevel(root)
# dash.title("Engineer")
# dash.geometry("888x500")
# dash.withdraw()

# my_img2= ImageTk.PhotoImage(Image.open("pqr.jpeg"))
# my_label2=Label(dash,image=my_img2)
# my_label2.pack()
# my_label2.place(x=0,y=0)

# #Buttons
# addbutton = Button(dash, text="ADD TICKET",font='Arial 20', command=add_tick, padx=50,fg='blue',borderwidth=5) 
# #loginButton.grid(row=4, column=0) 
# addbutton.pack(pady=2)
# addbutton.place(x=350,y=30)

# '''mangbutton = Button(dash, text="Manager",font='Arial 20' ,padx=44,fg='blue',borderwidth=5) 
# #loginButton.grid(row=4, column=0) 
# mangbutton.pack(pady=2)
# mangbutton.place(x=350,y=130)'''

# viewbutton = Button(dash, text="VIEW MY TICKET",font='Arial 20', command=show_vieteng ,padx=20,fg='blue',borderwidth=5) 
# #loginButton.grid(row=4, column=0) 
# viewbutton.pack(pady=2)
# viewbutton.place(x=350,y=230)

# '''dbabutton = Button(dash, text="DataBaseAdmin",font='Arial 20' ,padx=1,fg='blue',borderwidth=5) 
# #loginButton.grid(row=4, column=0) 
# dbabutton.pack(pady=2)
# dbabutton.place(x=350,y=330)'''

# backbutton1 = Button(dash, text="Log Out",font='Arial 20', command= back ,padx=80,fg='blue',borderwidth=5) 
# #loginButton.grid(row=4, column=0) 
# backbutton1.pack(pady=2)
# backbutton1.place(x=350,y=430)


# #inside view button
# vieteng = Toplevel(dash)
# vieteng.title("Engineer")
# vieteng.geometry("888x500")
# vieteng.withdraw()

# my_img4= ImageTk.PhotoImage(Image.open("abcd.png"))
# my_label4=Label(vieteng,image=my_img4)
# my_label4.pack()
# my_label4.place(x=0,y=0)

# stdata = scrolledtext.ScrolledText(vieteng, height = 25, width = 120, font = "TkDefaultFont")
# stdata.pack(pady=2)
# stdata.place(x=20,y=20)


# backbutton3 = Button(vieteng, text="Back",font='Arial 20', command= back2 ,padx=80,fg='blue',borderwidth=5) 
# #loginButton.grid(row=4, column=0) 
# backbutton3.pack(pady=2)
# backbutton3.place(x=350,y=430)



# #inside the engineerdash and inside that addticket

# addtick = Toplevel(dash)
# addtick.title("Engineer")
# addtick.geometry("888x467")
# addtick.withdraw()

# my_img3= ImageTk.PhotoImage(Image.open("lmn.jpeg"))
# my_label3=Label(addtick,image=my_img3)
# my_label3.pack()
# my_label3.place(x=0,y=0)


# t_id = Label(addtick, text="t_id",font='Arial 11',borderwidth=5,padx=30)
# t_id.pack()
# t_id.place(x=20,y=100)
# #age = StringVar()
# t_idEntry = Entry(addtick,font='Arial 11',borderwidth=5)  
# #usernameEntry.grid(row=0, column=1)
# t_idEntry.pack(pady=2)
# t_idEntry.place(x=150,y=100)


# status_eng = Label(addtick, text="Status",font='Arial 11',borderwidth=5,padx=25)
# status_eng.pack()
# status_eng.place(x=450,y=100)

# #opt = ['open']
# #clicked= StringVar()
# #clicked.set(opt[0])
# m = tkinter.StringVar()
# statuschoosen = ttk.Combobox(addtick, width = 27, textvariable=m, state='readonly')
# statuschoosen['values']=('Open')
# #age = StringVar()
# #status_engEntry = Entry(addtick,font='Arial 11',borderwidth=5)  
# #usernameEntry.grid(row=0, column=1)
# statuschoosen.pack(pady=2)
# statuschoosen.place(x=580,y=100)
# statuschoosen.current()
# #statuschoosen.bind("<<comboboxselected>>",addtickengr)


# level_eng = Label(addtick, text="Level",font='Arial 11',borderwidth=5,padx=25)
# level_eng.pack()
# level_eng.place(x=20,y=200)

# #opt1 = ['A','B']
# #clicked1= StringVar()
# #clicked1.set(opt1[0])
# n = tkinter.StringVar()
# levelchoosen = ttk.Combobox(addtick, width = 27, textvariable=n, state='readonly')
# levelchoosen['values']=('A','B')


# #level_engEntry = Entry(addtick,font='Arial 11',borderwidth=5)  
# #usernameEntry.grid(row=0, column=1)
# #level_engEntry.pack(pady=2)
# #level_engEntry.place(x=150,y=200)

# levelchoosen.pack(pady=2)
# levelchoosen.place(x=150,y=200)
# levelchoosen.current()
# #levelchoosen.bind("<<comboboxselected>>",addtickengr)


# priority_eng = Label(addtick, text="Priority",font='Arial 11',borderwidth=5,padx=25)
# priority_eng.pack()
# priority_eng.place(x=450,y=200)
# #age = StringVar()
# #opt2 = ['High','Low']
# l = tkinter.StringVar()
# prioritychoosen = ttk.Combobox(addtick, width = 27, textvariable=l, state='readonly')
# prioritychoosen['values']=('High','Low')
# #priority_engEntry = Entry(addtick,font='Arial 11',borderwidth=5)  
# #usernameEntry.grid(row=0, column=1)
# prioritychoosen.pack(pady=2)
# prioritychoosen.place(x=580,y=200)
# prioritychoosen.current()
# #prioritychoosen.bind("<<comboboxselected>>",addtickengr)



# des_eng = Label(addtick, text="Description",font='Arial 11',borderwidth=5,padx=8)
# des_eng.pack()
# des_eng.place(x=20,y=300)
# #age = StringVar()
# des_engEntry = Entry(addtick,font='Arial 11',borderwidth=5)  
# #usernameEntry.grid(row=0, column=1)
# des_engEntry.pack(pady=2)
# des_engEntry.place(x=150,y=300)


# t_idEntry.focus_set()
# ADDbutton = Button(addtick, text="ADD",font='Arial 20', command=addtickengr, padx=20,fg='blue',borderwidth=5) 
# #loginButton.grid(row=4, column=0) 
# ADDbutton.pack(pady=2)
# ADDbutton.place(x=50,y=400)

# backButton2 = Button(addtick, text="Back",font='Arial 20', command= back1, padx=30, fg='blue', borderwidth=5) 
# backButton2.pack(pady=2)
# backButton2.place(x=550,y=400)
