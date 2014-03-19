# -*- coding: cp1251 -*-
from Tkinter import *
from PIL import Image, ImageTk
import tkFileDialog
import math
from collections import Counter

img = []

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


def clear_circles(circles,circle,width,height):
    x = circle[0]
    y = circle[1]
    r = circle[2]
    points = set()
    for th in range(360):
        x0 = int(round(x + r*math.cos(math.radians(th))))
        y0 = int(round(y + r*math.sin(math.radians(th))))
        points.add((x0,y0))
    points = list(points)
    for point in points:
        x0 = point[0]
        y0 = point[1]
        if img[y0][x0] == 0:
            continue
        for y1 in range(height):
                for x1 in range(width):
                    r1 = int(round(math.sqrt(math.pow(x0 - x1,2) + math.pow(y0 - y1,2))))

                    circles[(x1,y1,r1)] -= 1
    return circles

def get_circles(im):
    global img
    im.load()
    width,height = im.size
    img = tobits(list(im.getdata()),height,width)

    acc2  = Counter() 
    maxth = 180
    diag = int(math.sqrt(height*height + width*width))
    maxd = 2*diag

    
    
    for y in range(height):
        for x in range(width):
            
            if img[y][x] > 0:
                for y0 in range(height):
                    for x0 in range(width):
                        r0 = math.sqrt(math.pow(x - x0,2) + math.pow(y - y0,2))
                        r = int(round(r0))
                        acc2[(x0,y0,r)] += 1

    return acc2


window_height = 400
window_width = 400
root = Tk()
nmbC = 0

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
Canvas.create_circle = _create_circle



def Quit(ev):
    global root
    root.destroy()

def LoadFile(ev):
    global canvas,im,circles,listcircles,width,height,nmbC
    fn = tkFileDialog.Open(root, filetypes = [('*.bmp files', '.bmp')]).show()
    if fn == '':
        return
    im = Image.open(fn)
    width,height = im.size


    canvas.delete(ALL)
    canvas.background = ImageTk.PhotoImage(im)
    canvas.create_image((window_width - width)/2, (window_height - height)/2,image = canvas.background, anchor = NW)
    saveBtn.config(state = NORMAL)
    circles = get_circles(im)

    nmbC = 0
    
    print circles.most_common(5)
    
    

    
    
def SaveFile(ev):
    fn = tkFileDialog.SaveAs(root, filetypes = [('*.bmp files', '.bmp')]).show()
    if fn == '':
        return
    if not fn.endswith(".bmp"):
        fn+=".bmp"
    im.save(fn)


def MoreCircles(ev):
    global nmbCircles,canvas,nmbC,circles
    nmbCircles.config(state = NORMAL)
    nmbC += 1
    nmbCircles.delete(1.0,"1."+str(len(str(nmbC))))
    nmbCircles.insert(1.0,nmbC)
    nmbCircles.config(state = DISABLED)

    newcircle = list(circles.most_common(1))[0][0]
    print newcircle

    width,height = im.size
    circles = clear_circles(circles,newcircle,width,height)
    canvas.create_circle((window_width - width)/2 + newcircle[0],(window_height - height)/2 + newcircle[1],newcircle[2],
                           outline="red")

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


nmbCircles = Text(panelFrame,font=('times',12))
nmbCircles.insert(1.0,'0')
nmbCircles.config(state = DISABLED)
moreBtn = Button(panelFrame, text = ">")
moreBtn.bind("<Button-1>", MoreCircles)

nmbCircles.place(x = 210, y = 10, width = 40, height = 40)
moreBtn.place(x = 260, y = 10, width = 40, height = 40)



root.mainloop()

