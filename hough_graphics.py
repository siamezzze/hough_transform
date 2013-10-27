# -*- coding: cp1251 -*-
from Tkinter import *
from PIL import Image, ImageTk
import tkFileDialog
import math
from collections import Counter


#transform
def tobit(pix, v = 126):
    if pix > v:
        return 0
    return 1

def tobits(lst, height, width):
    result = []
    for i in range(height):
        result.append(map(tobit,(lst[i*width:(i+1)*width])))
    return result


def get_lines(im):
    im.load()
    #width,height = im.size
    img = tobits(list(im.getdata()),height,width)

    acc2  = Counter() 
    maxth = 180
    diag = int(math.sqrt(height*height + width*width))
    maxd = 2*diag
    
    #прямые заданы длиной перпендикуляра d к ней и углом th между этим перпендикуляром и горизонтальной осью
    for y in range(height):
        for x in range(width):
            #каждая ненулевая точка "голосует" за прямые, которым может принадлежать
            if img[y][x] > 0:
                for th in range(0,maxth):
                    d = int(x*math.cos(math.radians(th)) - y*math.sin(math.radians(th)))
                    acc2[(th,-d)] +=1



    return acc2


def line_to_drawable(d,th):
    sinth = math.sin(math.radians(th))
    if sinth == 0:
        return (d,0,d,height)
    y1 = int(d / sinth)
    y2 = int((width * math.cos(math.radians(th)) + d)/sinth)
    return (0,y1,width,y2)


nmbLns = 0
root = Tk()

def Quit(ev):
    global root
    root.destroy()

def LoadFile(ev):
    global canvas,im,lines,width,height
    fn = tkFileDialog.Open(root, filetypes = [('*.bmp files', '.bmp')]).show()
    if fn == '':
        return
    im = Image.open(fn)
    width,height = im.size

    canvas.background = ImageTk.PhotoImage(im)
    canvas.create_image(0, 0,image = canvas.background, anchor = NW)
    saveBtn.config(state = NORMAL)
    lines = get_lines(im)

    
    
def SaveFile(ev):
    fn = tkFileDialog.SaveAs(root, filetypes = [('*.bmp files', '.bmp')]).show()
    if fn == '':
        return
    if not fn.endswith(".bmp"):
        fn+=".bmp"
    im.save(fn)

drawable_lines = []

def MoreLines(ev):
    global nmbLns,canvas
    nmbLines.config(state = NORMAL)
    nmbLns += 1
    nmbLines.delete(1.0,"1."+str(len(str(nmbLns))))
    nmbLines.insert(1.0,nmbLns)
    nmbLines.config(state = DISABLED)
    newln = list(lines.most_common(nmbLns))[nmbLns-1]
    print newln
    print line_to_drawable(newln[0][1],newln[0][0])
    drawable_lines.append(
        canvas.create_line(line_to_drawable(newln[0][1],newln[0][0]),
                           fill = "red"))



panelFrame = Frame(root, height = 60, bg = 'gray')
imageFrame = Frame(root, width=300, height=300)

panelFrame.pack(side = 'bottom', fill = 'x')
imageFrame.pack(side = 'top', fill = 'both')

canvas = Canvas(imageFrame, width=300, height=300)
canvas.place(x = 0, y = 0,width = 300, height=300)

loadBtn = Button(panelFrame, text = 'Load')
saveBtn = Button(panelFrame, text = 'Save', state = DISABLED)
quitBtn = Button(panelFrame, text = 'Quit')

loadBtn.bind("<Button-1>", LoadFile)
saveBtn.bind("<Button-1>", SaveFile)
quitBtn.bind("<Button-1>", Quit)

loadBtn.place(x = 10, y = 10, width = 40, height = 40)
#saveBtn.place(x = 60, y = 10, width = 40, height = 40)
quitBtn.place(x = 110, y = 10, width = 40, height = 40)

nmbLines = Text(panelFrame,font=('times',12))
nmbLines.insert(1.0,'0')
nmbLines.config(state = DISABLED)
moreBtn = Button(panelFrame, text = ">")
moreBtn.bind("<Button-1>", MoreLines)

nmbLines.place(x = 210, y = 10, width = 40, height = 40)
moreBtn.place(x = 260, y = 10, width = 40, height = 40)



root.mainloop()
