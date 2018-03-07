import PIL.Image
import colorsys
from tkinter import *
from tkinter.filedialog import askopenfilenames 
import random

###########################
#Color Suggest
###########################

def gatherColorData(string):
    height = 500
    width = 500
    picture = PIL.Image.open(string)
    picture.show()
    picture = picture.resize((width, height), PIL.Image.BICUBIC)
    picture = picture.convert('RGB')
    pixelList = []
    sampleSpace = 5
    for pixel in range(sampleSpace):
        horizontal = random.randint(0, 499)
        vertical = random.randint(0, 499)
        r,g,b = picture.getpixel((horizontal,vertical))
        pixelList.append((r,g,b))
    return pixelList

def constructColorScheme(pixelList):
    maxSat = 0
    rd = 0
    gn = 0
    bl = 0
    for color in pixelList:
        r = color[0]
        g = color[1]
        b = color[2]
        saturation = (max(r,g,b) - min(r,g,b))/max(r,g,b)
        if saturation > maxSat:
            maxSat = saturation
            rd, gn, bl = r, g, b
    h,s,v = colorsys.rgb_to_hsv(rd,gn,bl)
    #This converts our most saturated color to HSV
    color1 = colorsys.hsv_to_rgb(colorOffset(h,-36), s, v)
    color2 = colorsys.hsv_to_rgb(colorOffset(h,-18), .75*s, v)
    color3 = colorsys.hsv_to_rgb(h,s,v)
    color4 = colorsys.hsv_to_rgb(colorOffset(h,18), .75*s, v)
    color5 = colorsys.hsv_to_rgb(colorOffset(h,36), s, v)
    return [color1, color2, color3, color4, color5]

def colorOffset(h, offset):
    return (((h*360)+offset)%360)/360

def getImage():
    file = askopenfilenames()
    imageString = file[0]
    return imageString

def suggestColors():
    imageString = getImage()
    pixelList = gatherColorData(imageString)
    colorList = constructColorScheme(pixelList)
    """
    for color in colorList:
        square = "rgb(" + str(int(color[0])) + "," + str(int(color[1])) + "," + str(int(color[2])) + ")"
        #print(color)
        im = PIL.Image.new("RGB", (100, 100), square)
        im.show()
    """
    ####Takes suggesed colors and an additional black and white image to create overlay 
    color = random.choice(colorList)
    photo1 = PIL.Image.open(imageString)
    photo2 = ProcessOverlay(color)
    width, height = photo1.size
    photo2 = photo2.resize((width, height), PIL.Image.BICUBIC)
    finalPhoto = PIL.Image.blend(photo1,photo2, .5)
    finalPhoto.show()

#####################
#Overlay
#####################

def ProcessOverlay(color):
    imageString2 = getImage()
    photo2 = PIL.Image.open(imageString2)
    photo2 = photo2.convert('RGB')
    pixelsMap2 = photo2.load()
    for width in range(photo2.size[0]):
        for height in range(photo2.size[1]):
            if (pixelsMap2[width, height] != (255,255,255)):
                pixelsMap2[width, height] = (int(color[0]),int(color[1]),int(color[2]))
    photo2.show()
    return photo2


#####################
#Desaturate Filter
#####################

#Future work in progress
#Muted colors filter
def Filter():
    imageString = getImage()
    photo = PIL.Image.open(imageString)
    photo = photo.convert('RGB')
    photo.show()
    pixelsMap = photo.load()
    for width in range(photo.size[0]):
        for height in range(photo.size[1]):
            r,g,b = pixelsMap[width,height]
            r,g,b = desaturate(r,g,b)
            pixelsMap[width,height] = (r, g, b)
    photo.show()

def desaturate(r,g,b):
    r /= 255
    g /= 255
    b /= 255
    h,s,v = colorsys.rgb_to_hsv(r,g,b)
    s = s/2
    r,g,b = colorsys.hsv_to_rgb(h,s,v)
    r *= 255
    b *= 255
    g *= 255
    return int(r),int(g),int(b)


#####################
#Tkinter Stuff#######
#####################

def init(data):
    # load data.xyz as appropriate
    pass

def mousePressed(event, data):
    suggestColors()

def keyPressed(event, data):
    # use event.char and event.keysym
    if (event.keysym == "m"):
        Filter()

def redrawAll(canvas, data):
    # draw in canvas
    pass

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    root = Tk()
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)
