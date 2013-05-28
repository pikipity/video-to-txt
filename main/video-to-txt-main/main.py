# encoding=utf-8
import Tkinter
import time
import threading
import tkFont

def StartNow():
    StartThreading=threading.Thread(target=StartFunction)
    StartThreading.start()


def StartFunction():
    N=0
    M=0
    while M<3283:
        M=3*N+1
        N=N+1
        fp=open("/Users/wangze/Documents/Git/video-to-txt/m-file/%d.txt"%M)
        lines=fp.readlines()
        fp.close()
        for line in lines:
            MainText.insert("end",line)
        time.sleep(0.12)
        MainText.delete(1.0,"end")

root=Tkinter.Tk()
root.title("Video2TXT")
root.iconbitmap("/icon/icon.icns")

MainFont=tkFont.Font(family="Courant",size="3",weight="normal")
MainText=Tkinter.Text(root,font=MainFont,height=200,width=300,relief="groove",bd=2)
MainText.pack(side="left")

ControlFrame=Tkinter.Frame(root)
ControlFrame.pack(side="left")

MatlabPathFrame=Tkinter.Frame(ControlFrame)
MatlabPathFrame.pack()
MatlabPathLabel=Tkinter.Label(MatlabPathFrame,text="Matlab Path: ")
MatlabPathLabel.pack(side="left")
MatlabPath=Tkinter.Text(MatlabPathFrame,width=20,height=1,relief="groove",bd=2)
MatlabPath.pack(side="left")
MatlabPathButton=Tkinter.Button(MatlabPathFrame,text="...")
MatlabPathButton.pack(side="left")

VideoPathFrame=Tkinter.Frame(ControlFrame)
VideoPathFrame.pack()
VideoPathFrameLabel=Tkinter.Label(VideoPathFrame,text="Video Path: ")
VideoPathFrameLabel.pack(side="left")
VideoPath=Tkinter.Text(VideoPathFrame,width=20,height=1,relief="groove",bd=2)
VideoPath.pack(side="left")
VideoPathButton=Tkinter.Button(VideoPathFrame,text="...")
VideoPathButton.pack(side="left")

DataPathFrame=Tkinter.Frame(ControlFrame)
DataPathFrame.pack()
DataPathFrameLabel=Tkinter.Label(DataPathFrame,text="TXT files Path: ")
DataPathFrameLabel.pack(side="left")
DataPath=Tkinter.Text(DataPathFrame,width=20,height=1,relief="groove",bd=2)
DataPath.pack(side="left")
DataPathButton=Tkinter.Button(DataPathFrame,text="...")
DataPathButton.pack(side="left")

ButtonFrame=Tkinter.Frame(ControlFrame)
ButtonFrame.pack()
ConvertButton=Tkinter.Button(ButtonFrame,text="Convert")
ConvertButton.pack(side="left")
StartButton=Tkinter.Button(ButtonFrame,text="Start")
StartButton.pack(side="left")

root.mainloop()