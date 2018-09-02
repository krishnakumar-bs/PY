

from Tkinter import *
from threading import * 
import time
import tkMessageBox


class Board:
	def __init__(self,w,h):
		self.width=w
		self.height=h
		self.rw=30
		self.cl=20
		self.cel=20
		self.t=Tk()
		self.can=Canvas(self.t,width=self.width,height=self.height,bg="black")
		self.can.pack()
		self.can.bind("<Button-1>",self.liveNode)
		self.can.bind("<Button-3>",self.deadNode)
		self.can.bind("<Return>",self.play)	
		self.can.bind("<Key>",self.pause)			
		self.t.title("Game_Of_Life")
		self.t.resizable(0,0)
		self.t.geometry("600x400")	
		self.matrix={}
		self.active={}
		

	def getCanvas(self):
		return self.can
		
	def drawRect(self):
		for i in range(0,self.rw+1):
			for j in range(0,self.cl+1):
				if(i!=0):
					self.can.create_rectangle(i*self.cel,self.cel*j,0,0,outline="gray")
					self.matrix[str(i*self.cel)+":"+str(self.cel*j)]=0
				else:	
					self.matrix[str(i*self.cel)+":"+str(self.cel*j)]=-1
					
			
	def liveNode(self,event):
		self.setPoints(event.x,event.y)
		if(self.x!=None):
			self.rect=self.can.create_rectangle(self.x,self.y,self.xx,self.yy,fill='red',outline="gray")
			self.matrix[str(self.x)+":"+str(self.y)]=1
		return

	def deadNode(self,event):
		self.setPoints(event.x,event.y)
		if(self.x!=None):
			self.rect=self.can.create_rectangle(self.x,self.y,self.xx,self.yy,fill='black',outline="gray")
			self.matrix[str(self.x)+":"+str(self.y)]=0
		return

	def setPoints(self,x,y):
		if(self.cel<x<self.width-self.cel and self.cel<y<self.height-self.cel):
			self.x=(x/self.cel)*self.cel
			self.y=(y/self.cel)*self.cel
			self.xx = self.x+self.cel
			self.yy = self.y+self.cel 
		else:
			self.x=None
			self.y=None
			self.xx = None
			self.yy = None
		 
		
	def nextGen(self,rw,cl):
		for i in range(1,rw):
			for j in range(1,cl):				
				_x=i*self.cel
				_y=j*self.cel
				_xx=_x+self.cel
				_yy=_y+self.cel
				_val=self.matrix[str(_x)+":"+str(_y)]		
				_cnt=self.getCountActive(_x,_y)
				if (self.isLive(_val,_cnt)):
					self.active[str(_x)+":"+str(_y)]=1
				else:
					if self.matrix[str(_x)+":"+str(_y)]==1:
						self.active[str(_x)+":"+str(_y)]=0
		self.update()
		
	def update(self):
		for st in self.active.keys():
			_ts=st.split(":")
			_x=int(_ts[0])
			_y=int(_ts[1])
			if(self.active[st]==1):
				self.can.create_rectangle(_x,_y,_x+self.cel,_y+self.cel,outline="gray",fill='red')
			else:
				self.can.create_rectangle(_x,_y,_x+self.cel,_y+self.cel,outline="gray",fill='black')
			self.matrix[st]=self.active.get(st)
			del self.active[st]

	def getCountActive(self,r,c):
		self.count=0
		for i in [r-self.cel,r,r+self.cel]:
			for j in [c-self.cel,c,c+self.cel]:
				if(i==r and j==c):
					continue
				else:
					try:
						if self.matrix[str(i)+":"+str(j)]==1:
							self.count +=1
					except:
						continue
		return self.count


	def isLive(self,val,cnt):
		live=False
		if (val==1 and (cnt==2 or cnt==3)):
			live=True
		elif (val==1 and (cnt<2 or cnt>3)):
			 live=False
		elif (val==0 and (cnt==3)):
			 live=True
		return live
			 

	def play(self,event):
		self.et=event
		self.nextGen(self.rw,self.cl)
		self.active={}
		self.a=self.t.after(200,self.play,self.et)

	def pause(self,event):
		self.t.after_cancel(self.a)
		
	
b=Board(600,400)
ss="""
Short-cut keys
1. Mouse - Left : cell active state selection
2. Mouse - Right : cell inactive state selection
3. Play  - 1st click Tab+Enter and after Enter only
4. Pause - click Tab key
5. Speed - Enter key[+]: Tab Key[-]
"""
tkMessageBox.showinfo("Game Rules",ss)

b.drawRect()
mainloop()
		































































