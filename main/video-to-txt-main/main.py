# encoding=utf-8
import Tkinter
import time
import threading
import tkFont
import sys
import tkFileDialog
import tkMessageBox
import os
import Queue

ProgramPath=sys.argv[0][0:sys.argv[0].rfind('/')]#no final "/"
MainMatlabFilePath=ProgramPath+'/m-file/main.m'
MatlabPathDefault="/Applications/MATLAB/MATLAB_R2011a.app/bin/matlab"
VideoPathDefault=ProgramPath[0:ProgramPath.rfind('/')+1]+'test_file/test.mp4'
DataPathDefault=ProgramPath[0:ProgramPath.rfind('/')+1]+'data_file/'
MatlabFilePath=ProgramPath+'m-file/'
Waitingtime=1
ConvertState=Queue.Queue(maxsize=1)#0:stop,1:begin
ConvertState.put(0)
PlayState=Queue.Queue(maxsize=1)
PlayState.put(0)
DefaultMainText="""Thank you for using this program.

This program is used to convert the video file to TXT files. And then print TXT files one by one. Then you will see the ASCII text "video".

I use Matlab to convert the video to TXT files. And use Python to print TXT files. Therefore, if you want to use this program, you must have "Matlab" and "Python" at least.

Now, this program is only for Mac OS X system. Since the paths are difference, Windows users will have problems. But you can change the source file "main.py" a little to use this program in Windows or Linux.

I am pikipity. If you find any bugs or problems, please contact me through e-mail -- pikipityw@gmail.com. You also can go to my blog "pikipity.github.io" to find more interesting things.

Thank you very much.


*** User Guid: 3 steps for using this program.

1. Choose "Matlab Path" (choose the app file, like MATLAB_R2011a.app), "Video Path" (choose the video file that you want to convert) and "TXT file Path" (choose the location that you want to store the TXT files).
2. Click "Convert" Button and waiting. The Convert process will spend a lot of times.
3. Click "Start" Button. The ASCII text "video" will start.


*** Note:

1. Since there is the limitation of the Matlab function, it only can convert few types' file. The format supported is listed in http://support.apple.com/kb/HT3775
2. In the "Convert" and "Start" process, please don't close this program. Although you close this program, these processes will also be continued until they are finished.
3. TXT files are very large. Please make sure that you have enough space to store them.
"""

######## get and check fundamental function ######################################################################################
def CheckInput(MatlabPath,VideoPath,DataPath):
    MainText.insert("1.0","\nBegin to Check paths...\n")
    time.sleep(Waitingtime)
    if (not os.path.isfile(MatlabPath)):
        tkMessageBox.showwarning("Matlab Path Warning","The Matlab path is wrong. Please double check")
        MainText.insert("1.0","\nMatlab path is wrong. There is not this file. Please reset the Matlab path in the right side.\n")
        time.sleep(Waitingtime)
        return 0
    elif not os.path.exists(VideoPath):
        tkMessageBox.showwarning("Video Path Warning", "The video path is wrong. Please double check")
        MainText.insert("1.0","\nVideo Path is wrong. There is not this file. Please reset the video path in the right side.\n")
        time.sleep(Waitingtime)
        return 0
    elif not os.path.exists(DataPath):
        tkMessageBox.showwarning("TXT files storage warning","The TXT files pathes are wrong. Please double check")
        MainText.insert("1.0","\nThe path to store TXT files is wrong. There is not this path. Please reset the TXT files storage path in the right side.\n")
        time.sleep(Waitingtime)
        return 0
    elif not len(os.listdir(DataPath))-1<=0:
        tkMessageBox.showwarning("TXT files path warning","Since the number of TXT files will be very large, please give me a path of \"TXT files path\" in which there is nothing.")
        MainText.insert("1.0","\nSince the number of TXT files will be very large, please give me a path in which there is nothing.\n")
        time.sleep(Waitingtime)
        return 0
    MainText.insert("1.0","\nThe path checking has been finished. All paths exist.\n")
    time.sleep(Waitingtime)
    return 1

def GetAllPath():
    MainText.insert("1.0","\nBegin to get all paths...\n")
    time.sleep(Waitingtime)
    MatlabPathGet=MatlabPath.get("1.0","end")
    MatlabPathGet=MatlabPathGet[0:MatlabPathGet.rfind('\n')]
    VideoPathGet=VideoPath.get("1.0","end")
    VideoPathGet=VideoPathGet[0:VideoPathGet.rfind('\n')]
    DataPathGet=DataPath.get("1.0","end")
    DataPathGet=DataPathGet[0:DataPathGet.rfind('\n')]
    if not DataPathGet[len(DataPathGet)-1]=="/":
        DataPathGet=DataPathGet+"/"
        DataPath.delete("1.0","end")
        DataPath.insert("end",DataPathGet)
    MainText.insert("1.0","\nGet all paths\n")
    time.sleep(Waitingtime)
    return [MatlabPathGet,VideoPathGet,DataPathGet]

######################################################################################################################

############### Convert Button Function ##############################################################################
def StartConvert():
    StartConvertThreading=threading.Thread(target=StartConvertFunction)
    StartConvertThreading.start()

def StartConvertFunction():
    MainText.insert("1.0","\n\n\n")
    CheckPlayState=PlayState.get()
    PlayState.put(CheckPlayState)
    if CheckPlayState:
        tkMessageBox.showwarning("Waiting","Please wait for finishing the play.")
        MainText.insert("1.0","\nPlease wait for finishing this play.\n")
    else:
        MainText.insert("1.0","\nPlease don't close this program and wait.\n")
        time.sleep(Waitingtime)
        ConvertState.get()
        ConvertState.put(1)
        AllPath=GetAllPath()
        CheckResult=CheckInput(AllPath[0],AllPath[1],AllPath[2])
        if CheckResult:
            MainConvertFunction(AllPath[0],AllPath[1],AllPath[2])
        else:
            ConvertState.get()
            ConvertState.put(0)
            MainText.insert("1.0","\nPlease check your paths. There are something wrong. Try again after fix the path.\n")

def MainConvertFunction(MatlabPath,VideoPath,DataPath):
    MainText.insert("1.0","\nBegin to create matlab file\n")
    time.sleep(Waitingtime)
    MainMatlabFile=open(MainMatlabFilePath,'w')
    MainMatlabFile.write("""clear;
clc;
Video2Txt(\'%s\',\'%s\',3,3,3);
quit;"""%(VideoPath,DataPath))
    MainMatlabFile.close()
    MainText.insert("1.0","\nMatlab file has been created.\n")
    time.sleep(Waitingtime)
    MainText.insert("1.0","\nBegin to convert. Waiting...\n")
    time.sleep(Waitingtime)
    MatlabCommand='%s -nodesktop -nosplash -r "run(\'%s\')"'%(MatlabPath,MainMatlabFilePath)
    os.system(MatlabCommand)
    ConvertState.get()
    ConvertState.put(0)
    MainText.insert("1.0","\nConvert process has been finished. Click \"Start\" to play the \"TXT video\"\n")

#######################################################################################################################

######### Start Button Function #######################################################################################
def StartPlay():
    StartPlayThreading=threading.Thread(target=StartPlayFunction)
    StartPlayThreading.start()

def StartPlayFunction():
    MainText.insert("1.0","\n\n\n")
    CheckConvertState=ConvertState.get()
    ConvertState.put(CheckConvertState)
    if CheckConvertState:
        tkMessageBox.showwarning("Waiting","The convert process has not been finished. Please wait.")
        MainText.insert("1.0","\nWait for finishing the convert process.\n")
    else:
        DataPathGet=DataPath.get("1.0","end")
        DataPathGet=DataPathGet[0:DataPathGet.rfind('\n')]
        if os.path.isfile(DataPathGet+"1.txt"):
            MainPlayFunction(DataPathGet)
        else:
            tkMessageBox.showwarning("TXT Files Warning","Please check the convert process and \"TXT files path\". In the \"TXT files path\", there is not TXT files.")
            MainText.insert("1.0","\nPlease check the convert process and \"TXT files path\".\n\n")

def MainPlayFunction(DataPath):
    PlayState.get()
    PlayState.put(1)
    N=0
    M=0
    MainText.insert("1.0","\nGet All TXT Files.\n")
    time.sleep(Waitingtime)
    MaxN=len(os.listdir(DataPath))
    MaxM=(MaxN-2)*3+1
    MainText.insert("1.0","\nNow, begin to play!!.\n")
    time.sleep(Waitingtime)
    MainTextRemainder=MainText.get("1.0","end")
    MainText.delete("1.0","end")
    MainFont.config(size="3")
    fp=open(DataPath+"1.txt")
    line=fp.readline()
    fp.close()
    MainText.config(height=len(line)*2,width=len(line))
    while M<MaxM:
        M=3*N+1
        N=N+1
        fp=open(DataPath+"%d.txt"%M)
        lines=fp.readlines()
        fp.close()
        for line in lines:
            MainText.insert("end",line)
        if M==MaxM:
            time.sleep(Waitingtime*5)
            MainText.delete("1.0","end")
        else:
            time.sleep(0.12)
            MainText.delete(1.0,"end")
    MainText.config(height=40,width=70)
    MainFont.config(size="15")
    MainText.insert("1.0",MainTextRemainder)
    MainText.insert("1.0","\n\"TXT video play\" has been finished.\n")
    PlayState.get()
    PlayState.put(0)

######################################################################################################################

####### Choose Path Function #########################################################################################
def MatlabPathChoose():
    MatlabPathChoosing=tkFileDialog.askopenfilename(title="Choose Matlab Program",initialdir="/Application/",initialfile="/Applications/MATLAB/MATLAB_R2011a.app",filetypes=[("APP","*.app")])
    if MatlabPathChoosing:
        MatlabPath.delete("1.0","end")
        MatlabPath.insert("end",MatlabPathChoosing+'/bin/matlab')
    else:
        tkMessageBox.showwarning("Matlab Program Path Warning","Please choose your Matlab program path. Otherwise \"%s\" will be used"%MatlabPathDefault)

def VideoPathChoose():
    VideoPathChoosing=tkFileDialog.askopenfilename(title="Choose Video File",initialfile=VideoPathDefault,filetypes=[("AVI","*.avi"),("MPG","*.mpg"),("MP4","*.mp4"),("M4V","m4v"),("MOV","*.mov")])
    if VideoPathChoosing:
        VideoPath.delete("1.0","end")
        VideoPath.insert("end",VideoPathChoosing)
    else:
        tkMessageBox.showwarning("Video file warning","Please choose a video. Otherwise \"%s\" will be used"%VideoPathDefault)

def DataPathChoose():
    DataPathChoosing=tkFileDialog.askdirectory(title="Choose TXT files storage path",initialdir=DataPathDefault)
    if DataPathChoosing:
        DataPath.delete("1.0","end")
        DataPath.insert("end",DataPathChoosing+'/')
    else:
        tkMessageBox.showwarning("TXT files storage path warning","Please choose a location to store TXT files. Otherwise \"%s\" will be used"%DataPathDefault)

##########################################################################################################################

root=Tkinter.Tk()
root.title("Video2TXT")
root.iconbitmap("/icon/icon.icns")

MainFont=tkFont.Font(family="Courant",size="15",weight="normal")
MainText=Tkinter.Text(root,font=MainFont,height=40,width=70,relief="groove",bd=2)
MainText.pack(side="left")
MainText.insert("end",DefaultMainText)

ControlFrame=Tkinter.Frame(root)
ControlFrame.pack(side="left")

MatlabPathFrame=Tkinter.Frame(ControlFrame)
MatlabPathFrame.pack()
MatlabPathLabel=Tkinter.Label(MatlabPathFrame,text="Matlab Path: ")
MatlabPathLabel.pack(side="left")
MatlabPath=Tkinter.Text(MatlabPathFrame,width=40,height=1,relief="groove",bd=2)
MatlabPath.pack(side="left")
MatlabPath.delete("1.0","end")
MatlabPath.insert("end",MatlabPathDefault)
MatlabPathButton=Tkinter.Button(MatlabPathFrame,text="...",command=MatlabPathChoose)
MatlabPathButton.pack(side="left")

VideoPathFrame=Tkinter.Frame(ControlFrame)
VideoPathFrame.pack()
VideoPathFrameLabel=Tkinter.Label(VideoPathFrame,text="Video Path: ")
VideoPathFrameLabel.pack(side="left")
VideoPath=Tkinter.Text(VideoPathFrame,width=40,height=1,relief="groove",bd=2)
VideoPath.pack(side="left")
VideoPath.delete("1.0","end")
VideoPath.insert("end",VideoPathDefault)
VideoPathButton=Tkinter.Button(VideoPathFrame,text="...",command=VideoPathChoose)
VideoPathButton.pack(side="left")

DataPathFrame=Tkinter.Frame(ControlFrame)
DataPathFrame.pack()
DataPathFrameLabel=Tkinter.Label(DataPathFrame,text="TXT files Path: ")
DataPathFrameLabel.pack(side="left")
DataPath=Tkinter.Text(DataPathFrame,width=40,height=1,relief="groove",bd=2)
DataPath.pack(side="left")
DataPath.delete("1.0","end")
DataPath.insert("end",DataPathDefault)
DataPathButton=Tkinter.Button(DataPathFrame,text="...",command=DataPathChoose)
DataPathButton.pack(side="left")

ButtonFrame=Tkinter.Frame(ControlFrame)
ButtonFrame.pack()
ConvertButton=Tkinter.Button(ButtonFrame,text="Convert",command=StartConvert)
ConvertButton.pack(side="left")
StartButton=Tkinter.Button(ButtonFrame,text="Start",command=StartPlay)
StartButton.pack(side="left")

root.mainloop()