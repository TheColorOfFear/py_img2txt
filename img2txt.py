from PIL import Image
import os
if __name__ == '__main__':
    import sys

e = "\033["
fc = [e+"97m",e+"90m",e+"30m"]
bc = [e+"107m",e+"100m",e+"40m"]
c = e+"0m"
#chars= ["@", "J", "D", "%", "*", "P", "+", "Y", "$", ",", "."]
#chars= ["█", "█", "█", "▓", "▓", "▒", "▒", "▒", " ", " ", " "]
#chars= ["█", "▇", "▆", "▅", "▄", "▃", "▂", "▁", " ", " ", " "]
#chars= [fc[0]+"█"+c, bc[1]+fc[0]+"▓"+c, bc[1]+fc[0]+"▒"+c, bc[0]+fc[1]+"░"+c, bc[1]+fc[0]+"░"+c, bc[0]+fc[1]+"▒"+c, bc[0]+fc[1]+"▓"+c, bc[0]+fc[1]+"█"+c, " "+c, " "+c]
chars= [" "+c, bc[0]+fc[1]+"█"+c, bc[0]+fc[1]+"▓"+c, bc[0]+fc[1]+"▒"+c, bc[1]+fc[0]+"░"+c, bc[0]+fc[1]+"░"+c, bc[1]+fc[0]+"▒"+c, bc[1]+fc[0]+"▓"+c, fc[0]+"█"+c, fc[0]+"█"+c]

#for i in range(len(chars)):
#    chars[i] = chars[i]
#    print(chars[i], end="")

def print_img_bw(imgName, wid=80):
    img = Image.open(imgName, mode='r')
    width, height = img.size
    aspect_ratio = height/width
    new_width = wid
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')
    pixels = img.getdata()
    ascii_image = "\n"
    for i in range(len(pixels)//new_width):
        for j in range(new_width):
            try:
                ascii_image += chars[min( (pixels[j + (i*new_width)]//25),(len(chars) - 1))]
            except:
                print(pixels[j + (i*new_width)]//25)
        ascii_image += "\n"
    '''
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    
    # split string of chars into multiple strings of length equal to new width and create a list
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    '''
    print(ascii_image)

def print_img_ld(imgName, wid=80):
    img = Image.open(imgName, mode='r')
    width, height = img.size
    aspect_ratio = height/width
    new_width = wid
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    pixels = img.getdata()
    ascii_image = "\n"
    for i in range(len(pixels)//new_width):
        for j in range(new_width):
            ascii_image += e + "38;2;"
            ascii_image += str(pixels[j + (i*new_width)][0]) + ";"
            ascii_image += str(pixels[j + (i*new_width)][1]) + ";"
            ascii_image += str(pixels[j + (i*new_width)][2]) + "m"
            ascii_image += "█"
        ascii_image += "\n"
    print(ascii_image)

def print_img_col(imgName, wid=80):
    img = Image.open(imgName, mode='r')
    width, height = img.size
    aspect_ratio = height/width
    new_width = wid
    new_height = (aspect_ratio * new_width * 0.55) * 2
    img = img.resize((new_width, int(new_height)))
    pixels = img.getdata()
    ascii_image = "\n"
    for i in range(0,len(pixels)//(new_width),2):
        for j in range(new_width):
            try:
                ascii_image += e + "38;2;"
                ascii_image += str(pixels[j + (i*new_width)][0]) + ";"
                ascii_image += str(pixels[j + (i*new_width)][1]) + ";"
                ascii_image += str(pixels[j + (i*new_width)][2]) + "m"
                ascii_image += e + "48;2;"
                ascii_image += str(pixels[j + ((i + 1)*new_width)][0]) + ";"
                ascii_image += str(pixels[j + ((i + 1)*new_width)][1]) + ";"
                ascii_image += str(pixels[j + ((i + 1)*new_width)][2]) + "m"
                ascii_image += "▀" + c
            except IndexError:
                pass
        ascii_image += "\n"
    print(ascii_image)

def print_img_256_ld(imgName, wid=80):
    img = Image.open(imgName, mode='r')
    width, height = img.size
    aspect_ratio = height/width
    new_width = wid
    new_height = (aspect_ratio * new_width * 0.55) * 2
    img = img.resize((new_width, int(new_height)))
    pixels = img.getdata()
    ascii_image = "\n"
    for i in range(0,len(pixels)//(new_width), 2):
        for j in range(new_width):
            try:
                ascii_image += e + "38;5;"
                r = ((pixels[j + (i*new_width)][0]) * 5) // 256
                g = ((pixels[j + (i*new_width)][1]) * 5) // 256
                b = ((pixels[j + (i*new_width)][2]) * 5) // 256
                ascii_image += str( ( (b ) + (g * 6) + (r * 36) ) + 16) + "m"
                ascii_image += "█" + c
            except IndexError:
                pass
        ascii_image += "\n"
    print(ascii_image)

def print_img_256(imgName, wid=80):
    img = Image.open(imgName, mode='r')
    width, height = img.size
    aspect_ratio = height/width
    new_width = wid
    new_height = (aspect_ratio * new_width * 0.55) * 2
    img = img.resize((new_width, int(new_height)))
    pixels = img.getdata()
    ascii_image = "\n"
    for i in range(0,len(pixels)//(new_width), 2):
        for j in range(new_width):
            try:
                ascii_image += e + "38;5;"
                r = ((pixels[j + (i*new_width)][0]) * 5) // 256
                g = ((pixels[j + (i*new_width)][1]) * 5) // 256
                b = ((pixels[j + (i*new_width)][2]) * 5) // 256
                ascii_image += str( ( (b ) + (g * 6) + (r * 36) ) + 16) + "m"
                ascii_image += e + "48;5;"
                r = ((pixels[j + ((i + 1)*new_width)][0]) * 5) // 256
                g = ((pixels[j + ((i + 1)*new_width)][1]) * 5) // 256
                b = ((pixels[j + ((i + 1)*new_width)][2]) * 5) // 256
                ascii_image += str( ( (b ) + (g * 6) + (r * 36) ) + 16) + "m"
                ascii_image += "▀" + c
            except IndexError:
                pass
        ascii_image += "\n"
    print(ascii_image)

def print_img(imgName, printType="colour", imgres="high", wid=80):
    if wid == "max":
        wid = os.get_terminal_size()[0]
    else:
        wid = int(wid)
    if printType.lower() == "colour":
        if imgres.lower() == "high":
            print_img_col(imgName, wid)
        else:
            print_img_ld(imgName, wid)
    elif printType.lower() == "256":
        if imgres.lower() == "high":
            print_img_256(imgName, wid)
        else:
            print_img_256_ld(imgName, wid)
    elif printType.lower() == "bw":
        print_img_bw(imgName, wid)
    else:
        print_img_256_ld(imgName, wid)

if __name__ == '__main__':
    print_type = "256"
    img_res = "high"
    img_width = "max"
    if len(sys.argv) > 1:
        img_name = sys.argv[1]
        if len(sys.argv) > 2:
            print_type = sys.argv[2]
            if len(sys.argv) > 3:
                img_res = sys.argv[3]
                if len(sys.argv) > 4:
                    img_width = int(sys.argv[2])
    else:
        img_name = input("file name? : ")
    print_img(img_name, print_type, img_res, img_width)
