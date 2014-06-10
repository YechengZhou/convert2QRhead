# -*- coding: utf-8 -*-
__author__ = 'Yecheng'
__doc__ ="""

Usage: convert2QRhead.py <imgfile> [--target=<target>]

"""

from PIL import Image
from docopt import docopt
import ImageEnhance

dct = docopt(__doc__)

imgname = dct['<imgfile>']

target = dct['--target']

print "source: ", imgname

print "target: ", target

try:
    img = Image.open(imgname)
except IOError:
    exit("File not found: " + imgname, ". This is the source file need to be converted")

try:
    template_img = Image.open('template.jpg')  # use this as template # TODO need to change the template
except IOError:
    exit("Please copy the template.jpg to the source code files folder")

#img = Image.open("jordan.jpg")

template_img.save(target)
target_img = Image.open(target)

# use 3*3 black and white jpg as a pixel in 2-dimension head pic

# if img size is 180*180  corner is 36 * 36, means 0.2 * height(width)

rate = 600.0 / 2557650  # converted sum 2557650, 1-bit pixels, black and white, stored with one pixel per byte
print rate

width, height = img.size

if width != height:
    #raise BaseException, "the raw pic should be a square"
    pass
img = img.resize(template_img.size)
width, height = img.size



def get_this_pivot(this_img): # rgb, have 3 values for each pixel, x means has been converted to single value for each pixel
    this_sum_rgb = 0
    #width, height = img.size
    this_pixel = this_img.load()
    for i in range(width):
        for j in range(height):
            try:
                this_sum_rgb += sum(this_pixel[i,j])
            except TypeError:
                this_sum_rgb += this_pixel[i,j]
    return this_sum_rgb


raw_pic_total_rgb = get_this_pivot(img)

print "raw pic sum rgb is:", raw_pic_total_rgb

#pivot = 600.00 / 7518351350 * raw_pic_total_rgb

#print "pivot is:", pivot
#region = template_img.crop((88,42,91,45))
#r,g,b = img.split()

# enhance the pic
enhancer = ImageEnhance.Sharpness(img)
img = enhancer.enhance(2)
#img.show()

new_img = img.convert('1') # (1-bit pixels, black and white, stored with one pixel per byte)
#new_img = img.filter(ImageFilter.CONTOUR)
#new_img.show()

converted_pic_total_rgb = get_this_pivot(new_img)

print "converted pic sum rgb is:", converted_pic_total_rgb


pixel = new_img.load()


# go through raw pic and determine every 383 block should replace by black or white block

def get_average_rgb(pixel,box): # box is (a,b,c,d) like (88,42,91,45)， diagonal(88，42), (91,45)
    sum_box = 0
    counter = 0
    for i in range(box[0],box[2]):
        for j in range(box[1],box[3]):
            sum_box += sum(pixel[i,j])
            counter += 1
    return sum_box/( (box[2]-box[0]) * (box[3]-box[1]) * 3 )

def get_average_x(pixel,box):
    sum_box = 0
    for i in range(box[0],box[2]):
        for j in range(box[1],box[3]):
            sum_box += pixel[i,j]

    return sum_box/(box[2]-box[0]) * (box[3]-box[1])


def if_in_corner(box_tuple):
    x = box_tuple[0]
    y = box_tuple[1]
    if x < 36 and y < 36:
        return True
    elif x < 36 and y > 180 - 36 - 3: # template size is 180, 36 is corner length, 3 is the size of every paste
        return True
    elif x > 180 - 36 - 3 and y < 36:
        return True
    else:
        return False

for h in range(3,height,3): # interval is 3
    for w in range(3,width,3):
        if if_in_corner((h-3,w-3,h,w)):
            continue
        temp_avg = get_average_x(pixel,(h-3,w-3,h,w))
        #print rate * converted_pic_total_rgb
        if temp_avg > rate * converted_pic_total_rgb:
            paste_item = Image.open('white.jpg')
        else:
            paste_item = Image.open('black.jpg')
        target_img.paste(paste_item,(h-3,w-3,h,w))


"""
# handle edges
# decide if the edge need to be changed

white_tuple = (255,255,255)
black_tuple = (0,0,0)

after_convert_pixel = target_img.load()

# decoration

for h in range(3,height,3): # interval is 3
    white_marker = 0
    black_marker = 0
    for w in range(3,width,3):
        if if_in_corner((h-3,w-3,h,w)):
            continue
        print after_convert_pixel[h-3,w-3]
        temp_avg = get_average_rgb(after_convert_pixel,(h-3,w-3,h,w))
        print "average rgb:", temp_avg
        #print rate * converted_pic_total_rgb
        if temp_avg == 255:  # white block
            print "white"
            white_marker += 1
            #paste_item = Image.open('white.jpg')
        elif temp_avg == 0: # black block
            print "black"
            black_marker += 1
            #paste_item = Image.open('black.jpg')
        print "w,b", white_marker, black_marker

        if abs(white_marker - black_marker) >= 5: #  judge it as successive blank area
            if white_marker > black_marker:
                paste_item = Image.open('black.jpg')
            else:
                paste_item = Image.open('white.jpg')
            x = h + 3 * (black_marker + white_marker)
            y = w + 3 * (black_marker + white_marker)
            target_img.paste(paste_item,(x-3,y-3,x,y))

"""

"""
for w in range(36,180-36-3):
    white_marker = 0
    black_marker = 0
    for h in range(36,180-36-3):
        if after_convert_pixel[h,w] == white_tuple: # white
            white_marker += 1
        elif after_convert_pixel[h,w] == black_tuple: # black
            black_marker += 1
        print "black and white marker are:", black_marker, white_marker
        if abs(white_marker - black_marker) >= 18: # successive 18 pixel determines a pure line
            # change mass up this line
            # chose 3 point and revers
            for k in range(3):
                random_index = random.randint(0,17)
                if after_convert_pixel[w, random_index] == white_tuple:
                    after_convert_pixel[w, random_index] = black_tuple
                    print "reverse pixel is :", w
                else:
                    after_convert_pixel[w, random_index] = white_tuple

"""

target_img.save(target)
target_img.show()


print "Done"





