#This works by salting the password before hashing it.
#A random numbers are generated which is salt
#The password is salted before being hashed to make this work.
#However, bcrypt utilizes the salt from the previously stored hashed password to hash the user-entered password. This is how verification works.
#It has to be matched with a new password

import bcrypt

#passwordHashing function is used to hashing the password entered by user and the hashed password will be stored into the DB
def passwordHashing(pin):
	bits_pin=pin.encode() #converting the entered password to bits using encoding
	salting = bcrypt.gensalt(15) #the process of producing the salt for the password
	bcrypt_hashpassword = bcrypt.hashpw(bits_pin, salting) #With the help of bcrypt combing both the password and salt
	decode_password = bcrypt_hashpassword.decode() #decoding the pin from  bits to a string
	return decode_password

#checkPassword function is used to check the password during login which matches with the hashed password which is already present in the data base
def checkPassword(pin,pin_hasshing):
	bits_pin = pin.encode() #converting the password from string to bits using encoding
	encode_password = pin_hasshing.encode() #converting the password stored in DB to bits using encoding
	check_match = bcrypt.checkpw(bits_pin, encode_password) #check whether the password entered by the user and password present in the DB matches are not
	return check_match