"""Script for Tkinter GUI chat client."""
import sys
import os.path
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter
#import vlc
import subprocess

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")

            if(msg=="1"):
                nes_thread = Thread(target=openjar)
                nes_thread.start()
            if(msg=="2"):
                print("Kill")
                bsnes.kill()
        except OSError:  # Possibly client has left the chat.
            msg_list.insert(tkinter.END, 'endchat')
            break

def openjar():
    global bsnes
    print("Nintaco")
    bsnes = subprocess.Popen(['wine','wine /Users/Ashot/Desktop/snes9x-rr-1.60-win32-x64/snes9x-x64.exe -fullscreen /Users/Ashot/Desktop/Space\ Megaforce\ \(USA\).zip'],stdout=subprocess.PIPE)
    output = bsnes.communicate()[0]
    print(output)


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = my_msg.get()
    my_msg.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        top.quit()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    my_msg.set("{quit}")
    send()


def play_video():
    return


top = tkinter.Tk()

top.title("Chatter")
top.resizable(0,0)

top.attributes('-fullscreen', True)
top.attributes('-topmost', True)
top.overrideredirect(True)

def quitApp():
    # mlabel = Label (root, text = 'Close').pack()
    top.destroy()

# placing the button on my window
messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()  # For the messages to be sent.
my_msg.set("Type your messages here.")
scrollbar = tkinter.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

button = tkinter.Button(text = 'QUIT', command = quitApp).pack()

top.protocol("WM_DELETE_WINDOW", on_closing)

#----Now comes the sockets part----
HOST = '192.168.10.112'#input('Enter host: ')
PORT = 2000#input('Enter port: ')


BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
tkinter.mainloop()  # Starts GUI execution.