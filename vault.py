#Vault program stub
from tkinter import *
import os
import sys, getopt
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util import Counter
from Crypto.Util import Padding
from Crypto.Random import random
import re
import subprocess

class Vault(Frame):

    #Start Screen - if program is already set up #
    def start_screen(self):
        self.parse_file("passwords.hex")
        self.line_count = self.count_accounts()
        self.pass_count = self.line_count
        self.attempts = 0
        self.frame = Frame(self.master, bg="#282828")
        self.headLbl = Label(self.frame, text="Vault Password Manager", 
                             bg="black", fg="white", font=("Courier New", 20))
        self.headLbl.pack(side=TOP, fill=X)
        self.pswd_frame = Frame(self.frame, bg="#282828")
        self.pswd_label = Label(self.pswd_frame, height=2, bg="#282828",
                                text="Please enter your password", fg="white",
                                font=("Courier New", 18))
        self.pswd_label.pack(side=TOP, fill=X)
        self.password_input = StringVar()
        self.password_box = Entry(self.pswd_frame, show='*',
                                  textvariable=self.password_input)
        self.password_box.bind('<Return>', self.login)
        self.password_box.pack(side=TOP)
        self.validated = StringVar()
        self.repeat_label = Label(self.pswd_frame, height=2, bg="#282828",
                                  textvariable=self.validated, fg="light blue", 
                                  font=("Courier New", 18))
        self.repeat_label.pack(side=TOP)
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
                                  text="Enter password again", fg="white", 
                                  font=("Courier New", 18))
        self.repeat_label.pack(side=TOP)
        self.password_two = StringVar()
        self.password2_box = Entry(self.pswd_frame, 
                                   textvariable=self.password_two, show='*')
        self.password2_box.bind('<Return>', self.password_setup)
        self.password2_box.pack(side=TOP)

        self.accepted = StringVar()
        self.accepted.set("")
        self.accepted_label = Label(self.pswd_frame, height=2, bg="#282828",
                                    textvariable=self.accepted, fg="light blue", 
                                    font=("Courier New", 15))
        self.accepted_label.pack(side=TOP)
        self.repeat_label.pack(side=TOP)
        self.pswd_frame.pack(expand=YES, fill=BOTH, pady=100)
        self.frame.pack(expand=YES, fill=BOTH)

    def main_screen(self):
        self.frame = Frame(self.master, bg="#282828")
        self.headLbl = Label(self.frame, bg="black", fg="white",
                             text="Vault - Home", 
                             font=("Courier New", 20))
        self.headLbl.pack(side=TOP, fill=X)
        self.frame.pack(expand=YES, fill=BOTH)
        self.options_frame = Frame(self.frame, bg="#282828")
        self.search_label = Label(self.options_frame, height=2, bg="#282828",
                                  text="Search for an account password",
                                  fg="white",font=("Courier New", 18))
        self.search_label.pack(side=TOP, fill=X)
        self.username_input = StringVar()
        self.url_input = StringVar()
        self.username_input.set("")
        self.url_input.set("")
        self.username_search = Entry(self.options_frame, 
                                     textvariable=self.username_input)
        self.url_search = Entry(self.options_frame, textvariable=self.url_input)
        self.username_label = Label(self.options_frame, height=2, bg="#282828",
                                    text="Search by username", fg="#F0F0F0",
                                    font=("Courier New", 18))
        self.username_label.pack(side=TOP)
        self.username_search.pack(side=TOP)
        self.url_label = Label(self.options_frame, height=2, bg="#282828",
                               text="Search by URL", fg="#F0F0F0",
                               font=("Courier New", 18))
        self.url_label.pack(side=TOP)
        self.url_search.pack(side=TOP)
        self.search_button = Button(self.options_frame, height=2, bg="#282828",
                                    text="Retrieve Password", fg="black", 
                                    highlightbackground="#282828",
                                    font=("Courier New", 18), 
                                    command=self.search_for_password)
        self.search_button.pack(side=TOP)
        self.search_result = StringVar()
        self.search_result.set("")
        self.result_label = Label(self.options_frame, height=2, bg="#282828",
                                  textvariable=self.search_result, 
                                  fg="light blue", font=("Courier New", 18))
        self.result_label.pack(side=TOP)
        self.options_frame.pack(expand=YES, fill=BOTH, pady=70)
        self.add_account_button = Button(self.options_frame, height=2, 
                                         bg="#282828", text="Add an account", 
                                         fg="black", font=("Courier New", 18),
                                         highlightbackground="#282828",
                                         command=self.add_account_screen)
        self.add_account_button.pack(side=TOP)


    def add_account_screen(self):
        self.frame.destroy()
        self.frame = Frame(self.master, bg="#282828")
        self.headLbl = Label(self.frame, bg="black", fg="white",
                             text="Vault - Add account", 
                             font=("Courier New", 20))
        self.headLbl.pack(side=TOP, fill=X)
        self.frame.pack(expand=YES, fill=BOTH)
        self.options_frame = Frame(self.frame, bg="#282828")
        self.new_account_label = Label(self.options_frame, height=2,bg="#282828",
                                       text="New Account Information", 
                                       fg="white", font=("Courier New", 20))
        self.new_account_label.pack(side=TOP, fill=X)
        self.new_username = StringVar()
        self.new_url = StringVar()
        self.new_username.set("")
        self.new_username.set("")
        self.new_user = Entry(self.options_frame, 
                                     textvariable=self.new_username)
        self.new_url_entry = Entry(self.options_frame,textvariable=self.new_url)
        self.new_user_label = Label(self.options_frame,height=2, bg="#282828",
                                    text="Username", fg="#F0F0F0",
                                    font=("Courier New", 18))
        self.new_user_label.pack(side=TOP)
        self.new_user.pack(side=TOP)
        self.new_url_label = Label(self.options_frame, height=2, bg="#282828",
                                   text="URL [ex: gmail.com]", fg="#F0F0F0",
                                   font=("Courier New", 18))
        self.new_url_label.pack(side=TOP)
        self.new_url_entry.pack(side=TOP)
        self.password_frame = Frame(self.options_frame, bg="#282828")
        self.password_frame.pack(expand=YES, fill=BOTH)
        self.new_password = StringVar()
        self.new_password.set("")
        self.new_password = Entry(self.password_frame, show="*",
                                  textvariable=self.new_password)
        self.new_pass_label = Label(self.password_frame, height=2, bg="#282828",
                                    text="Enter new password", fg="#F0F0F0",
                                    font=("Courier New", 18))
        self.new_pass_label.pack(side=TOP)
        self.new_password.pack(side=TOP)
        self.gen_password = Button(self.password_frame, text="Generate password",
                                   font=("Courier New", 18), fg="black",
                                   command=self.gen_new_password,
                                   highlightbackground="#282828")
        self.gen_password.pack(side=TOP)
        self.add_account_button = Button(self.options_frame, text="Add account",
                                         font=("Courier New", 18),fg="black",
                                         command=self.new_account_entries,
                                         highlightbackground="#282828")
        self.add_account_button.pack(side=TOP, pady=10)
        self.add_result = StringVar()
        self.add_result.set("")
        self.result_label = Label(self.options_frame, height=2, bg="#282828",
                                  textvariable=self.add_result, fg="light blue", 
                                  font=("Courier New", 18))
        self.result_label.pack(side=TOP)
        self.back_home_button = Button(self.options_frame,height=1,bg="#282828",
                                       text="Back home", fg="black",
                                       highlightbackground="#282828",
                                       font=("Courier New", 18), 
                                       command=self.go_home)
        self.back_home_button.pack(side=BOTTOM, pady=5)
        self.options_frame.pack(expand=YES, fill=BOTH, pady=20)

    def go_home(self):
        self.frame.destroy()
        self.main_screen()

    def count_accounts(self):
        count = 0
        if os.path.isfile("./accounts.txt"):
            ifile = open("accounts.txt", 'r')

            for line in ifile:
                count += 1
            return count

        else:
            return count



    def new_account_entries(self):
        new_usr = self.new_username.get()
        new_url = self.new_url.get()
        new_pass = self.new_password.get()
        
        if new_usr == "":
            self.add_result.set("Please add a username")
        elif new_url == "":
            self.add_result.set("Please add a URL")
        elif new_pass == "":
            self.add_result.set("Please add a password")
        else:
            self.add_result.set("New account added.")
            self.new_password.delete(0, END)
            self.new_url_entry.delete(0, END)
            self.new_user.delete(0, END)
            self.add_username_url_password(new_url, new_usr, new_pass,
                                           "passwords.hex", "accounts.txt")

    def strength_validated(self, password):
        SpecialSym = ['$','@','#','!','%','^','*','(',')','+','-','[',']']
        if any(char in SpecialSym for char in password):
            if len(password) > 11 and len(password) < 33:
                if re.search(r'[0-9]', password):
                    return "Success"
                else:
                    return "Password must have at least 1 number"
            else:
                return "Password must be between 12 and 32 characters"
        else:
            return "Password must have at least 1 special character"

    def password_setup(self, event):
        pass_1 = self.password_one.get()
        pass_2 = self.password_two.get()

        if (pass_1 != pass_2):
            self.accepted.set("Passwords don't match")
            return
        else:
            result = self.strength_validated(pass_2)
            if result == "Success":
                self.create_derived_key(pass_2, "passwords.hex")
                self.frame.destroy()
                self.start_screen()
            else:
                self.accepted.set(result)

    def login(self, event):
        success = False
        self.password_attempt = self.password_input.get()

        if (self.attempts >= 3):
            self.validated.set("3 attempts exceeded. Account locked.")
        else:
            success = self.validate_login(self.password_attempt)
            if (not success):
                self.validated.set("Invalid password.")
                self.attempts = self.attempts + 1
            else:
                self.validated.set("Success")
                self.frame.destroy()
                self.main_screen()

    def search_for_password(self):

        if os.path.isfile("./accounts.txt"):
            username = self.username_input.get()
            url = self.url_input.get()

            if username == "":
                self.search_result.set("Please enter the username")
            elif url == "":
                self.search_result.set("Please enter the URL")
            else:
                result = self.search_username_or_url("accounts.txt", username, url, 
                                                     "passwords.hex")
                self.search_result.set(result)
        else:
            self.search_result.set("No accounts yet - Add one!")


    def create_derived_key(self, master_pass, password_file):
        master_pass = master_pass.encode('utf-8')   
        padded_master_pass = Padding.pad(master_pass, AES.block_size)
        salt = Random.get_random_bytes(8)    
        master_iv = Random.get_random_bytes(AES.block_size)   
        #use PBKDFS with salt to make master password to derived key 
        derived_key = PBKDF2(master_pass, salt, count=1000)  
        cipher = AES.new(derived_key, AES.MODE_CBC, master_iv)
        enc_padded_master_pass = cipher.encrypt(padded_master_pass)
        iv_cipher = AES.new(derived_key, AES.MODE_ECB)
        enc_master_iv = iv_cipher.encrypt(master_iv)
        ofile = open(password_file, 'wb')
        length_enc_padded_master_pass = len(enc_padded_master_pass).to_bytes(2, 'big')

        ofile.write(salt + enc_master_iv + length_enc_padded_master_pass + enc_padded_master_pass)     #write out to file
        ofile.write(b'\n')
        ofile.close()

    
    def parse_file(self, password_file):
        ifile = open(password_file, 'rb')
        file_content = ifile.read()
        ifile.close()

        self.salt = file_content[:8]
        self.enc_iv = file_content[8:24]
        length_enc_padded_master_pass = int.from_bytes(file_content[24:26], byteorder='big')
        self.enc_master_pass = file_content[26:(26+length_enc_padded_master_pass)]


    def validate_login(self, password_input):
        self.derived_key = PBKDF2(password_input, self.salt, count=1000)
        iv_cipher = AES.new(self.derived_key, AES.MODE_ECB)
        self.master_iv = iv_cipher.decrypt(self.enc_iv)
        cipher = AES.new(self.derived_key, AES.MODE_CBC, self.master_iv)
        padded_master_pass = cipher.decrypt(self.enc_master_pass)

        try:
            master_pass = Padding.unpad(padded_master_pass, AES.block_size)
        except ValueError:
            return False
        else:
            master_pass = master_pass.decode('ascii')
            if(master_pass == password_input):
                master_pass = "" # to reduce time master password is in memory
                return True
            else:
                return False
            
    def copy_pass_to_clipboard(self, password):
        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        p.stdin.write(password)
        p.stdin.close()
        retcode = p.wait()
        password=""
        return "Password copied to clipboard!"

    def enc_and_add_password(self, new_password, password_file, derived_key):
        self.pass_count += 1
        new_password = new_password.encode('utf-8')
        padded_new_password = Padding.pad(new_password, AES.block_size)     
        iv = Random.get_random_bytes(AES.block_size)
        cipher = AES.new(derived_key, AES.MODE_CBC, iv)
        enc_padded_new_password = cipher.encrypt(padded_new_password)
        length = len(enc_padded_new_password)
        with open(password_file, "ab") as myfile: 
            flag = b'#'+((self.pass_count).to_bytes(3, byteorder='big'))+b'#'
            myfile.write(flag)
            myfile.write(length.to_bytes(2, byteorder='big'))
            myfile.write(iv+enc_padded_new_password)
     
    def add_username_url_password(self, url, username, password, password_file, account_file): 
        self.line_count += 1
        self.enc_and_add_password(password, password_file, self.derived_key)
        with open(account_file, "a") as myfile:
            myfile.write(str(self.line_count)+" USERNAME:"+username+" | URL:"+url)
            myfile.write('\n')

    def gen_new_password(self):
        self.new_password.delete(0, END)
        password = ""
        for i in range(0, 24):
            password += random.choice("!#$%&'()*+,-./:;<=>?@[]^_`{|}~ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890")
        self.new_password.insert(0,password)

    def search_username_or_url(self, username_file, username, url, password_file):
        account_line_num = 1
        ifile = open(username_file, 'r')
        for line in ifile:
            if username not in line or url not in line:
                account_line_num += 1
            else: 
                return self.copy_searched_password_to_clipboard(account_line_num, password_file)

        return "That account was not found"

    def copy_searched_password_to_clipboard(self, account_line_num, password_file):
        password_line_num = 0
        ifile = open(password_file, 'rb')
        passwords = ifile.read()

        for byte in range(0, len(passwords)):
            if passwords[byte:byte+1] == b'#':
                num_in_bytes = passwords[byte+1:byte+4]
                num = int.from_bytes(num_in_bytes, byteorder='big')
                if num == account_line_num and passwords[byte+4:byte+5] == b'#':
                    length_in_bytes = passwords[byte+5:byte+7]
                    length = int.from_bytes(length_in_bytes, byteorder='big')
                    iv = passwords[byte+7:byte+23]
                    enc_pass_padded = passwords[byte+23:byte+23+length]
                    cipher = AES.new(self.derived_key, AES.MODE_CBC, iv)
                    plaintext_password = cipher.decrypt(enc_pass_padded)
                    plaintext_password = Padding.unpad(plaintext_password, AES.block_size)
                    return self.copy_pass_to_clipboard(plaintext_password)
        return "An error occured"


    def __init__(self, master):
        Frame.__init__(self, master)               
        self.master = master
        self.pack()

        #check if setup is needed - go to appropriate screen
        if (os.path.isfile("./passwords.hex")):
            self.start_screen()
        else:
            self.setup_screen()

root = Tk()
app = Vault(root)
root.title("Password Manager")
root.minsize(width=500, height=500)
root.maxsize(width=500, height=500)
root.configure(bg="#282828")
root.mainloop()