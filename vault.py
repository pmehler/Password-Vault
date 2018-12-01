#Vault program stub
from tkinter import *
#from PIL import ImageTk, Image
import os
import sys, getopt
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util import Counter

class Vault(Frame):

    #if program is already set up
    def start_screen(self):
        # start_screen GUI #
        self.frame = Frame(self.master, bg="dark grey")
        self.headLbl = Label(self.frame, text="Vault Password Manager", 
                             bg="black", fg="white", font=("Courier New", 20))
        self.headLbl.pack(side=TOP, fill=X)
        self.pswd_frame = Frame(self.frame, bg="dark grey")
        self.pswd_label = Label(self.pswd_frame, height=2, bg="dark grey",
                                text="Please enter your password", fg="white",
                                font=("Courier New", 18))
        self.pswd_label.pack(side=TOP, fill=X)
        self.password_box = Entry(self.pswd_frame, show='*')
        self.password_box.bind('<Return>', self.login)
        self.password_box.pack(side=TOP)
        self.pswd_frame.pack(expand=YES, fill=BOTH, pady=100)
        self.frame.pack(expand=YES, fill=BOTH)

    def setup_screen(self):
        self.frame = Frame(self.master, bg="#282828")
        self.headLbl = Label(self.frame, bg="black", fg="white",
                             text="Vault Password Manager Setup", 
                             font=("Courier New", 20))
        self.headLbl.pack(side=TOP, fill=X)
        self.pswd_frame = Frame(self.frame, bg="#282828")
        self.pswd_label = Label(self.pswd_frame, height=2, bg="#282828",
                                text="Please enter a password", fg="white", 
                                font=("Courier New", 18))
        self.pswd_label.pack(side=TOP, fill=X)
        self.password_one = StringVar()
        self.password1_box = Entry(self.pswd_frame,
                                   textvariable=self.password_one, show='*')
        self.password1_box.pack(side=TOP)
        self.repeat_label = Label(self.pswd_frame, height=2, bg="#282828",
                                  text="Enter password again" fg="white", 
                                  font=("Courier New", 18))
        self.repeat_label.pack(side=TOP)
        self.password_two = StringVar()
        self.password2_box = Entry(self.pswd_frame, 
                                   textvariable=self.password_two, show='*')
        self.password2_box.bind('<Return>', self.password_setup)
        self.password2_box.pack(side=TOP)
        self.pswd_frame.pack(expand=YES, fill=BOTH, pady=100)
        self.frame.pack(expand=YES, fill=BOTH)

    def password_setup(self, event):
        pass_1 = self.password_one.get()
        pass_2 = self.password_two.get()

        if (pass_1 != pass_2):
            print("passwords don't match")
        else:
            print("passwords match!")

    def login(self, event):
        print("test")
 
    def create_derived_key(self, master_pass, password_file):
        master_pass = master_pass.encode('utf-8')   #MAY NEED DIFFERENT ENCODING .hex()
        salt = Random.get_random_bytes(8)    #Create random salt
        master_iv = Random.get_random_bytes(AES.block_size)    
        derived_key = PBKDF2(master_pass, salt, count=1000)  #use PBKDFS with salt to make master password to derived key
        cipher = AES.new(derived_key, AES.MODE_CBC, master_iv)
        enc_master_pass = cipher.encrypt(master_pass)   #Encrypt master password with AES.CTR
        iv_cipher = AES.new(derived_key, AES.MODE_ECB)
        enc_master_iv = iv_cipher.encrypt(master_iv)
        ofile = open(password_file, 'wb')
        ofile.write(salt + enc_master_iv + enc_master_pass)     #write out to file
        ofile.close()
    #** Make sure plaintext of master password not in memory for
    #too long!! **

    #take password file, parse salt, nonce, encrypted master password and stores those, they will be passed to a function that validates them

    def parse_file(self, password_file):
        ifile = open.(password_file, 'rb')
        file_contents = ifile.read()
        self.salt = file_content[:8]
        self.enc_iv = file_content[8:40]
        self.enc_master_pass = file_content[40:(40+AES.block_size)]

    def validate_login(self, password_input):
        derived_key = PBKDF2(password_input, self.salt, count=1000)
        iv_cipher = AES.new(derived_key, AES.MODE_ECB)
        master_iv = iv_cipher.decrypt(self.enc_iv)
        cipher = AES.new(derived_key, AES.MODE_CBC, master_iv)
        master_pass = cipher.decrypt(self.enc_master_pass)
        if(master_pass == password_input):
            master_pass = "" # to reduce time master password is in memory
            return True
        else:
            return False


    def __init__(self, master):
        # a test comment :)
        Frame.__init__(self, master)               
        self.master = master
        self.pack()

        #check if setup is needed
        if (os.path.isfile("./passwords.txt")):
            self.start_screen()
        else:
            self.setup_screen()

 
root = Tk()
app = Vault(root)
root.title("Password Manager")
root.minsize(width=500, height=500)
root.maxsize(width=500, height=500)
root.mainloop()



'''    Program setup:
        - Detect if theres a current encrypted password file, if so, move on
        Function: 
            Takes in the user's new master password with restrictions
            Read and validate
        Function:
            Create random salt
            Make a random IV
            use PBKDFS with salt to make master password to derived key
            Encrypt master password and IV with ECB
            write out to file
            ** Make sure plaintext of master password not in memory for
                too long!! **

        Function:
            reads in and parses encrypted file so that we have
            the salt, the iv, and the stored ENC master password

    Program start:
        Function:
            Takes in password
            Uses salt to generate derived password P
            Uses derived password P to decrypt IV with AES_ECB
            Uses IV and P to decrypt master password with AES_CBC
            Sees if password = master password
        Repeat if wrong, if rejected 3 times, send email?

        Function:
            Opens the program window for searching/adding new things

    Program options:
        Create new account (enter username, url, password)
        Create new password for account
        Search for account password
            - copy to clipboard '''
