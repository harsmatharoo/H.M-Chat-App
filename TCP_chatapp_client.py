import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
from datetime import datetime
from tkinter import *
from tkinter.ttk import *


HOST='127.0.0.1'
PORT= 9090

#THis is the client class, for which all methods have been derived for the chat and the gui
class Client:

        

    def __init__(self,host,port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg=tkinter.Tk()
        msg.withdraw()

        #THe following set of code below is aimed at creating a pop up box to attain the username of the user.
        self.name=simpledialog.askstring("Name","Enter your Personal Login Name in the input box",parent=msg)

        #only enter the next chat GUI portion after username entered and cleared off
        self.gui_donee=False
        self.running=True

        #multiple things happening at once reqire threading so therefore the following statement
        gui_thread=threading.Thread(target=self.gui_loop)
        receive_thread=threading.Thread(target=self.receive)

        gui_thread.start()
        
        receive_thread.start()




    def text_title_reset(self,message):#resets the input text area for new input and puts the message to text area

        self.text_title.config(state='normal')
        self.text_title.insert('end', message)
        self.text_title.yview('end')
        self.text_title.config(state='disabled')

    def clear(self):#diminish the client window completely, and end all processes
        self.input_area.delete('0.0', END)
 

    def gui_loop(self):#This function makes UI including text areas,input_area and button
        
        self.wndow=tkinter.Tk()
        self.wndow.title('H.M Chat App')
        self.wndow.configure(bg="pink")
        

        self.chat_logo = tkinter.Label(self.wndow, text="💬📧 H.M Chat App©️", bg="yellow")
        self.chat_logo.config(font=("Bodoni MT Poster Compressed", 20))
        self.chat_logo.pack(padx=0, pady=0, side=tkinter.LEFT)
        
        
        self.chat_label = tkinter.Label(self.wndow, text=self.name.upper(), bg="yellow")
        self.chat_label.config(font=("Times New Roman", 14))
        self.chat_label.pack(padx=29, pady=5)
         
        self.host_lbl = tkinter.Label(self.wndow, text="Connection Host - 127.0.0.1", bg="brown", fg="green")
        self.host_lbl.config(font=("Times New Roman", 10))
        self.host_lbl.pack(padx=89, pady=0)
        
        self.port_lbl = tkinter.Label(self.wndow, text="Connection Port - 9090", bg="black", fg="white")
        self.port_lbl.config(font=("Times New Roman", 10))
        self.port_lbl.pack(padx=99, pady=0)

     

    
        self.text_title = tkinter.scrolledtext.ScrolledText(self.wndow, bg="pink",height=15, width = 90)
        self.text_title.pack(padx=20, pady=5)
        currtime = datetime.now()
        current_time = currtime.strftime("%H:%M:%S")

        message=f"SERVER : you have joined the H.M Chat server at {current_time}!\n"
        self.text_title_reset(message)

        self.msg_label=tkinter.Label(self.wndow,text="Type your message into the input box below:\t\t\t\t\t\t\t      ",bg="lightgreen")
        self.msg_label.config(font=("Times New Roman",16))
        self.msg_label.pack(padx=20,pady=5)

        self.credit_l=tkinter.Label(self.wndow,text="By- Harsahib Matharoo",bg="white")
        self.credit_l.config(font=("Times New Roman",16, "italic"))
        self.credit_l.pack(padx=500,pady=30)


        self.input_area=tkinter.Text(self.wndow,height=1,width=60)
        self.input_area.config(font=("Times New Roman", 16))
        self.input_area.pack(padx=20,pady=5)
        self.input_area.bind('<Return>', lambda _: self.write())#This function tends to call self.write if user press enter

        self.send_button = tkinter.Button(self.wndow, text=" [[ ▶️ ]] ", bg='#531', fg='White', command=self.write)
       
        self.send_button.config(font=("Times New Roman", 26))
        self.send_button.pack(padx=20, pady=0)
        
        self.help_button = tkinter.Button(self.wndow, text="  ❓  ", bg='#211', fg='red', command=self.help)
       
        self.help_button.config(font=("Times New Roman", 16))
        self.help_button.pack(padx=40, pady=0)
        
        self.settings_button = tkinter.Button(self.wndow, text="  ⚙️  ", bg='#131', fg='lightblue', command=self.settings)
       
        self.settings_button.config(font=("Arial", 22))
        self.settings_button.pack(padx=2, pady=0)

        self.gui_donee=True
        self.wndow.protocol("WM_DELETE_wndowDOW",self.killcode)
        self.clr_button = tkinter.Button(self.wndow, text=" [[ Clear ]] ", bg='#567', fg='White', command=self.clear)
        self.clr_button.config(font=("Times New Roman", 26))
        self.clr_button.pack(padx=30, pady=0)
#mainloop reprsents continuous and ever so going loop

        self.wndow.mainloop()


    def write(self):#This function forwards the input text by client to server.
        message=f"{self.name.upper()}: {self.input_area.get('1.0','end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0','end')

    def killcode(self):#diminish the client window completely, and end all processes
        self.running=False
        self.wndow.destroy()
        self.sock.close()
        exit(0)
    
    def help(self):#diminish the client window completely, and end all processes
        self.wndow2=tkinter.Tk()
        self.wndow2.title('Help')
        self.wndow2.configure(bg="yellow")
        self.help_lbl = tkinter.Label(self.wndow2, text="Use the input box to type your message \n \n", bg="red", fg="green")
        self.help_lbl.config(font=("Times New Roman", 10))
        self.help_lbl.pack(padx=89, pady=0)
        self.help_lbl2 = tkinter.Label(self.wndow2, text="Then click the send button to send, or the clear button to clear the input box, for a new message \n", bg="yellow", fg="green")
        self.help_lbl2.config(font=("Times New Roman", 10))
        self.help_lbl2.pack(padx=89, pady=3)

    def settings(self):#diminish the client window completely, and end all processes
        self.wndow3=tkinter.Tk()
        self.wndow3.title('Settings')
        self.wndow3.configure(bg="yellow")
        self.stg_lbl1 = tkinter.Label(self.wndow3, text="Change Chat Colour \n",)
        self.stg_lbl1.config(font=("Times New Roman", 25))
        self.stg_lbl1.pack(padx=30, pady=20)
        self.chngbg_button = tkinter.Button(self.wndow3, text=" Red ", bg='#567', fg='red', command=self.red)
        self.chngbg_button.config(font=("Times New Roman", 26))
        self.chngbg_button.pack(padx=30, pady=0)
        self.chngbg_button2 = tkinter.Button(self.wndow3, text=" Green ", bg='white', fg='green', command=self.green)
        self.chngbg_button2.config(font=("Times New Roman", 26))
        self.chngbg_button2.pack(padx=30, pady=0)
        self.chngbg_button3 = tkinter.Button(self.wndow3, text=" Blue ", bg='white', fg='blue', command=self.blue)
        self.chngbg_button3.config(font=("Times New Roman", 26))
        self.chngbg_button3.pack(padx=30, pady=0)
        self.chngbg_button4 = tkinter.Button(self.wndow3, text=" White ", bg='black', fg='white', command=self.white)
        self.chngbg_button4.config(font=("Times New Roman", 26))
        self.chngbg_button4.pack(padx=30, pady=0)
        self.canvas=Canvas(self.wndow3, width=1800, height=20)
        self.canvas.pack()
        self.canvas.configure(bg='cyan')

        self.stg_lbl2 = tkinter.Label(self.wndow3, text="Input Type Box Font Size \n",)
        self.stg_lbl2.config(font=("Times New Roman", 25))
        self.stg_lbl2.pack(padx=30, pady=20)
        self.chngbg2_button = tkinter.Button(self.wndow3, text=" Large ", bg='black', fg='cyan', command=self.largefont)
        self.chngbg2_button.config(font=("Times New Roman", 36))
        self.chngbg2_button.pack(padx=30, pady=0)
        self.chngbg3_button2 = tkinter.Button(self.wndow3, text=" Normal ", bg='black', fg='cyan', command=self.normalfont)
        self.chngbg3_button2.config(font=("Times New Roman", 22))
        self.chngbg3_button2.pack(padx=30, pady=0)
        self.chngbg4_button3 = tkinter.Button(self.wndow3, text=" Small ", bg='black', fg='cyan', command=self.smallfont)
        self.chngbg4_button3.config(font=("Times New Roman", 10))
        self.chngbg4_button3.pack(padx=30, pady=0)

    def red(self):
        self.wndow.configure(bg="red")
      
    def green(self):

        self.wndow.configure(bg="green")


    def blue(self):

        self.wndow.configure(bg="blue")


    def white(self):

        self.wndow.configure(bg="white")

    def largefont(self):


        self.input_area.config(font=("Times New Roman", 30))
        
    def normalfont(self):


        self.input_area.config(font=("Times New Roman", 22))
    def smallfont(self):

      
        self.input_area.config(font=("Times New Roman", 10))
     
   #The function below receives all possible messages that have been in the past sent by server.

    def receive(self):
        while self.running:
            try:
                message=self.sock.recv(1024).decode('utf-8')
                if message=='SERVER_CHECK':#try statement to ensure server is correctly working
                    self.sock.send(self.name.encode('utf-8'))

                else:
                    if self.gui_donee:#This is neccesary because both receive and gui_loop are running in different threads
                        self.text_title_reset(message)
            except ConnectionAbortedError:
                break
            except:
                print("Unwanted Error for the connection")
                self.sock.close()
                break


client=Client(HOST,PORT)#finally an object of the class client is created here according to the relevant port and its host