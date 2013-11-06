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

degree = 10 #округления для угла. Что-то надо с этим сделать...

def get_lines(im):
    im.load()
    #width,height = im.size
    img = tobits(list(im.getdata()),height,width)

    acc2  = Counter() 
    maxth = 180
    diag = int(math.sqrt(height*height + width*width))
    maxd = 2*diag

    def vote(th,d):
        acc2[(th,-d)] += 4
        acc2[(th-degree,-d-1)] += 2
        acc2[(th,-d-1)] += 2
        acc2[(th+degree,-d-1)] += 2
        acc2[(th-degree,-d)] += 2
        acc2[(th+degree,-d)] += 2
        acc2[(th-degree,-d+1)] += 2
        acc2[(th,-d+1)] += 2
        acc2[(th+degree,-d+1)] += 2
    
    #прямые заданы длиной перпендикуляра d к ней и углом th между этим перпендикуляром и горизонтальной осью
    for y in range(height):
        for x in range(width):
            #каждая ненулевая точка "голосует" за прямые, которым может принадлежать
            if img[y][x] > 0:
                for th in range(0,maxth,degree):
                    d = int(math.floor(x*math.cos(math.radians(th)) - y*math.sin(math.radians(th))))
                    acc2[(th,-d)] +=1
                    #vote(th,d)
                    


    return acc2

def filter_lines(acc):
    def is_local_max(x):
        count = 0
        if acc[x] > acc[(x[0]-degree),(x[1])]:
            count+=1
        if acc[x] > acc[(x[0]),(x[1]-1)]:
            count+=1
        if acc[x] > acc[(x[0]-degree),(x[1]-1)]:
            count+=1
        if acc[x] > acc[(x[0]+degree),(x[1])]:
            count+=1
        if acc[x] > acc[(x[0]),(x[1]+1)]:
            count+=1
        if acc[x] > acc[(x[0]+degree),(x[1]+1)]:
            count+=1
        if acc[x] > acc[(x[0]-degree),(x[1]+1)]:
            count+=1
        if acc[x] > acc[(x[0]+degree),(x[1]-1)]:
            count+=1
        return (count < 6) | (count == 0)
    return Counter({ k: v for k, v in acc.iteritems() if is_local_max(k) }) 




nmbLns = 0
window_height = 400
window_width = 400
root = Tk()


def line_to_drawable(d,th):
    sinth = math.sin(math.radians(th))
    startx = (window_width - width)/2
    starty = (window_height - height)/2
    if sinth == 0:
        return (startx-d,starty,startx-d,starty+height)
    y1 = int(math.floor(d / sinth))
    y2 = int(math.ceil((width * math.cos(math.radians(th)) + d)/sinth))
    return (startx,starty+y1,startx+width,starty+y2)

def Quit(ev):
    global root
    root.destroy()

def LoadFile(ev):
    global canvas,im,lines,width,height,nmbLns
    fn = tkFileDialog.Open(root, filetypes = [('*.bmp files', '.bmp')]).show()
    if fn == '':
        return
    im = Image.open(fn)
    width,height = im.size

    nmbLines.config(state = NORMAL)
    nmbLines.delete(1.0,"1."+str(len(str(nmbLns))))
    nmbLns = 0
    nmbLines.insert(1.0,nmbLns)
    nmbLines.config(state = DISABLED)

    canvas.delete(ALL)
    canvas.background = ImageTk.PhotoImage(im)
    canvas.create_image((window_width - width)/2, (window_height - height)/2,image = canvas.background, anchor = NW)
    saveBtn.config(state = NORMAL)
    #lines = filter_lines(get_lines(im))
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
imageFrame = Frame(root, width=window_width, height=window_height)

panelFrame.pack(side = 'bottom', fill = 'x')
imageFrame.pack(side = 'top', fill = 'both')

canvas = Canvas(imageFrame, width=window_width, height=window_height)
canvas.place(x = 0, y = 0,width = window_width, height=window_height)

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
