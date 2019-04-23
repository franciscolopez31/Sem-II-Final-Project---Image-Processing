"""
Francisco Lopez 
4/22/19
Sem II Final Project 
I will modify different bmp images and give them certain image effects. They
will either get a regular or reverse outline effect, a vertical or horizontal
mirror effect or a static effect. 
On my honor, I have neither given nor received any unacknowledged aid on this
assignment.
Francisco Lopez
"""
import os
import random

"""
Description: Calls the methods that are typed by the user.
Parameter: None
Return: Nothing
Plan: Variable will ask user for the certain effect they want to see. 
"""
def main():
    bin_file = bin_file_setup()
    print "The effects you can choose are outline, mirror or static."
    effect = raw_input("Which effect would you like to do? ")
    if effect == "outline":
        outline(bin_file)
    elif effect == "mirror":
        mirror(bin_file)
    elif effect == "static":
        static(bin_file)
    else:
        effect = raw_input("Which effect would you like? ")

"""
Description: Gets the users file and checks if it is a file in the folder. 
Parameter: None
Return:
    file_name = binary file for upcoming methods.
Plan: Asks the user for a file and uses os.path.exists to check if the file is
in the folder with the code.
"""   
def bin_file_setup():
    #Picks the appropriate file for the certain image the user wants
    image = raw_input("Do you want to use a lion, flower or class pic? ")
    if image == "flower":
        file_name = "testforoutline.bmp"
    if image == "lion":
        file_name = "lion.bmp"
    if image == "class pic":
        file_name = "class_pic.bmp"
    
    #Checks if the file is in the folder
    while os.path.exists(file_name) == False:
        print "This file does not exist. Input another one"
        file_name = raw_input("What binary file do you want to run? ")
    bin_file = open(file_name, "r+b")
    return bin_file

"""
Description: Gets integer of an offset for the binary file and uses it to see
the characteristics of the file.
Parameter:
    bin_file - the binary file from get_file
    offset - chooses the column that is going to be read 
Return:
    integer - the value of the chosen offsets 
Plan:
    I will set the file marker for bin_file on the value of offset to get the
certain info needed from the file. A for loop will run 4 times, read a ch and
make it the byte variable. Then I will get the value of the byte using ord and
multiplying it by 256 since that's the max it can be and it can go up depending
on how many bytes are read. Adding them to integer which gives me the offset's
value. 
"""
def get_integer(bin_file,offset):
    #Sets the file marker
    bin_file.seek(offset)
    integer = 0
    #Goes through each bite to calculate integer 
    for i in range(4):
        byte = bin_file.read(1)
        #Multiplies the byte number by 256 depending on what pixel it is in
        integer += ord(byte)*(256**i)
    return integer

"""
Description: Gets the header of the binary file to copy it to the output. 
Parameter:
    bin_file - the binary file from get_file
    output - the output file for the effect
Return: Nothing
Plan: Gets the offset of the header and reads every pixel until that number.
Then the pixels are written into the output file. 
"""
def copy_header(bin_file,output):
    header = get_integer(bin_file,10)
    bin_file.seek(0)
    for i in range(header):
        ch = bin_file.read(1)
        output.write(ch)

"""
Description: Sets up output file for the methods that need one.
Parameter:
    bin_file - the binary file from get_file
Return: None
Plan: Asks the usre for an output name and opens it up. Then the input file's
header is copied to that output file. 
"""
def set_up_output(bin_file):
    #Asks for the output name and opens it
    #output_name = raw_input("What is the output file? ")
    output_name = "outline.bmp"
    output = open(output_name, "w+b")
    copy_header(bin_file, output)
    return output

"""
Description: Sets up the variables used in the effects methods.
Parameter:
    bin_file - the binary file containing the image
Return: Nothing
Plan: Uses get_integer to get each appropriate variable for the following
methods.
"""
def set_up_size(bin_file):
    #Variables to help flip image and set file_marker
    w = get_integer(bin_file,18)
    h = get_integer(bin_file,22)
    offset = get_integer(bin_file,10)
    bin_file.seek(offset)
    return w, h, offset

"""
Description: Sets the outline of a certain figures by turning the dark colors to
black and the opposite for lighter colors.
Parameter:
    bin_file - the binary file from get_file
Return: Nothing
Plan:
    Have an if statement checking to see if the rgb levels in a byte are under
a certain number to either turn them into black or white colors. Creating the
figures into outlines of themselves. 
"""
def outline(bin_file):
    w, h, offset = set_up_size(bin_file)
    outline_type = raw_input("Do you want a reverse or regular outline? ")
    with set_up_output(bin_file) as outline:
        for i in range(w*h):
            ch = bin_file.read(3)
            if outline_type == "regular":
                #Looks at the rgb levels to see whether they should become a
                #black or a white color
                if ord(ch[0]) < 140 and ord(ch[1]) < 130 and ord(ch[2]) < 120:
                    outline.write(chr(0) + chr(0) + chr(0))
                else:
                    outline.write(chr(255) + chr(255) + chr(255))
                    
            if outline_type == "reverse":
                #Looks at the rgb levels but changes the rgb levels to the
                #opposite of the regular outline
                if ord(ch[0]) < 140 and ord(ch[1]) < 130 and ord(ch[2]) < 120:
                    outline.write(chr(255) + chr(255) + chr(255))
                else:
                    outline.write(chr(0) + chr(0) + chr(0))
    print "Finished"

"""
Description: Mirrors an image vertically. 
Parameter:
    bin_file - binary file containing the original image
Return: Nothing
Plan: Has a loop that reads each pixel from the first half of each row and the
pixel is written down normally on the outline file. Then another for loop will
take the row of pixels from the first half of the line, and write them in
reverse. Creating the mirror effect for one line and th eloop will continue to
go until it reaches the last line. 
"""
def mirror(bin_file):
    #Set varialbes for 
    w, h, offset = set_up_size(bin_file)
    row = []
    choice = raw_input("Would you want a horiontal or vertical mirror effect? ")
    
    with set_up_output(bin_file) as mirror:
        if choice == "vertical":
            for i in range(h):
                #Reads the first half of each line and appends it to a list 
                for i in range(w/2): 
                    pixel = bin_file.read(3)
                    row.append(pixel)
                    mirror.write(pixel)
                #Writes down the list from above but in reverse
                for i in range(w/2):
                    pixel = bin_file.read(3)
                    mirror.write(row[(w/2-1)-i])
                #Resets the row variable for the next line
                row = []
                
        if choice == "horizontal":
            #Reads half of the files lines  
            for i in range(h/2+1):
                pixel = bin_file.read(w*3)
                row.append(pixel)
                mirror.write(pixel)
            #Writes the lines in reverse at the half way mark
            for i in range(h/2):
                mirror.write(row[(h/2-1)-i])
            
        print "Finished"
        
"""             
Description: Creates a static effect on an image. 
Parameter:
    bin_file - the binary file containing the image
Return: Nothing
Plan: Will go through each pixel in the binary file and alter the rgb lvls to
make the effect lighter or normal in brightness. Once the rgb lvls are set, they
will be inputed into a list where it will be randomly chosen to be written down
in the static file. 
"""
def static(bin_file):
    w, h, offset = set_up_size(bin_file)
    #Level of brightness for the effect
    static_lvl = raw_input("Would you want a lighter or normal static effect? ")
    with set_up_output(bin_file) as static:
        for i in range(w*h):
            #Pixels and bytes to alter
            pixel = bin_file.read(3)
            b1 = ord(pixel[0])
            b2 = ord(pixel[1]) 
            b3 = ord(pixel[2])

            #Increases the brightness of the effect
            if static_lvl == "lighter":
                if 100 < b1 < 200:
                    b1 += 50
                if 100 < b2 < 200:
                    b2 += 50
                if 100 < b3 < 200:
                    b3 += 50 
                    
            bytes = [b1,b2,b3]
            #Chooses a rgb level randomly from bytes to write them as a pixel
            static.write(chr(random.choice(bytes)) +\
                        chr(random.choice(bytes))+ chr(random.choice(bytes)))
    print "Finished"
    
if __name__ == "__main__":
    main()
