import tkinter
import os
import random
from platform import system
import easygui
import configparser

import weather
import chat


config = configparser.ConfigParser()
config.read('./config.ini')
print(config["Options"])



class Pet():
    def __init__(self) -> None:
        self.root=tkinter.Tk()#window
        self.delay=200#delay time
        self.pfr=int(config["Options"]["pfr"])#*pixels from right (location in window)
        self.pfb=int(config["Options"]["pfb"])#*pixes from bottom
        self.move_speed=int(config["Options"]["move_speed"])#move speed

        self.x = 100#no need to change this, it's just the image dimensions
        self.y = 100

        self.animation = dict(\
            idle=[tkinter.PhotoImage(file=os.path.abspath('assets/idle.gif'),format='gif -index %i' % i)for i in range(5)],\
                 idle_to_sleep = [tkinter.PhotoImage(file=os.path.abspath('assets/idle-to-sleep.gif'), format = 'gif -index %i' % i) for i in range(8)],\
                    sleep = [tkinter.PhotoImage(file=os.path.abspath('assets/sleep.gif'), format = 'gif -index %i' % i) for i in range(3)]*3,\
                        sleep_to_idle = [tkinter.PhotoImage(file=os.path.abspath('assets/sleep-to-idle.gif'), format = 'gif -index %i' % i) for i in range(8)],\
                            walk_left = [tkinter.PhotoImage(file=os.path.abspath('assets/walk-left.gif'), format = 'gif -index %i' % i) for i in range(8)],\
                                walk_right = [tkinter.PhotoImage(file=os.path.abspath('assets/walk-right.gif'),format = 'gif -index %i' % i) for i in range(8)])
                                #import idle gif img (idle.gif has 5 frames, so "for in range(5)")
                                #(sleep)times 3 to repeat gif for a few times
        
        self.root.overrideredirect(True)#remove tkinter UI
        if system() == 'Windows':#if OS is Windows
            self.root.wm_attributes('-transparent','black')
        else:#if OS is Mac or Linux
            self.root.wait_visibility(self.root)
            self.root.wm_attributes('-alpha',1.0)#Mac executes this, but the backgroud is black
            #self.root.config(bg='systemTransparent')#remove the black background


        self.root.bind("<Button-1>",self.onLeftClick)#left click
        self.root.bind("<Button-2>",self.onRightClick)#right click
        self.root.bind("<Button-3>",self.onRightClick)#scroll  uses the same func as right key
        self.root.bind("<Key>",self.onKeyPress)#Other key presses

        self.root.attributes('-topmost', True)#pin window on topmost layer
        self.label = tkinter.Label(self.root, bd=0, bg='black')#set endless border for window
        if system()!='Windows':#for mac/linux
            #self.label.config(bg='systemTransparent')
            pass
        self.label.pack()

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.min_width = 110
        self.max_width = screen_width - 110 #disallow pet to move out of window

        self.curr_width = screen_width - self.pfr#get current x pos(dont ask me why it is called"curr_width")
        self.curr_height = screen_height - self.pfb#get current y pos
        self.root.geometry('%dx%d+%d+%d'%(self.x,self.y,self.curr_width,self.curr_height))#100,100 is position
    


    def update(self,curr_frame,curr_animation):
        self.root.attributes('-topmost',True)#pin to top
        animation_arr = self.animation[curr_animation]#load animation
        frame = animation_arr[curr_frame]
        self.label.configure(image=frame)

        if curr_animation in ('walk_left','walk_right'): 
            self.move_window(curr_animation)#move the thing
        
        curr_frame += 1
        if curr_frame == len(animation_arr):#if at the end of animation, move to next animation
            next_animation = self.getNextAnimation(curr_animation)
            self.root.after(self.delay,self.update,0,next_animation)
        else:
            self.root.after(self.delay,self.update,curr_frame,curr_animation)
    

    def move_window(self,curr_animation):
        if curr_animation == 'walk_left':
            if self.curr_width > self.min_width:
                self.curr_width -= self.move_speed#reverse movement
        
        elif curr_animation == 'walk_right':
            if self.curr_width < self.max_width:
                self.curr_width += self.move_speed#reverse movement
        
        self.root.geometry('%dx%d+%d+%d'%(self.x,self.y,self.curr_width,self.curr_height))#update window stuff


    def getNextAnimation(self,curr_animation):
        if curr_animation == 'idle':
            return random.choice(['idle','idle_to_sleep','walk_left','walk_right'])
        elif curr_animation == 'idle_to_sleep':
            return 'sleep'
        elif curr_animation == 'sleep':
            return random.choice(['sleep','sleep_to_idle'])
        elif curr_animation == 'sleep_to_idle':
            return 'idle'
        elif curr_animation == 'walk_left':
            return random.choice(['idle','walk_left','walk_right'])
        elif curr_animation == 'walk_right':
            return random.choice(['idle','walk_left','walk_right'])


    def onRightClick(self,event):
        self.quit()


    def onLeftClick(self,event):
        chatContent = ""
        choice = easygui.buttonbox(msg="天气：\n"+weather.get_weather(),title="",choices=["刷新","智能对话"])#pop up a selection window
        if choice == "刷新":
            self.onLeftClick(event)
        elif choice == "智能对话":
            input = easygui.enterbox(msg=chatContent,title="智能对话")
            while True:
                if input:
                    chatContent += "你："+str(input)+"\n猫咪：Miao~ "+chat.chat(str(input))+"\n"
                    input = easygui.enterbox(msg=chatContent,title="智能对话")
                else:
                    break

    def onKeyPress(self,event):
        if event.char in ('q','Q'):
            self.quit()


    def run(self):
        self.root.after(self.delay,self.update,0,'idle')#start state should be idle
        self.root.mainloop()
    

    def quit(self):
        if str(config["Options"]["closeOnClick"]) == "True":
            self.root.destroy()
            quit()#terminate program



if __name__ == '__main__':
    print("Initializing your desktop pet...")
    print('To quit, right click on your pet')
    pet = Pet()
    pet.run()