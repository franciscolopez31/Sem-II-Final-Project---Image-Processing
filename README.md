# Sem-II-Final-Project---Image-Processing
"""

Francisco Lopez 

4/16/19

Sem II Final

Any help recieved: 

Description: I will modify a binary image with different effects, like outline, fisheye and glass.

On my honor, I have neither given nor recieved any unacknowledged aid on this assignment.

Francisco Lopez

"""

import os 

"""

Description:Calls all methods to help create the new image effects.

Parameter: None

Return: Nothing

Plan: Calls all methods.

"""

def main():

    bin_file = bin_file_setup()
    
    outline(bin_file)
    
"""

Description: Gets the users file and checks if it is a file in the folder. 

Parameter: None

Return:
    file_name = binary file for upcoming methods.
    
Plan: Asks the user for a file and uses os.path.exists to check if the file is
in the folder with the code.

"""  

def bin_file_setup():

    #file_name = raw_input("What binary file do you want to run? ")
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
    
    #Goes through each byte to calculate integer 
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

    #Variables to help flip image and set file_marker
    
    w = get_integer(bin_file,18)
    
    h = get_integer(bin_file,22)
    
    offset = get_integer(bin_file,10)
    
    bin_file.seek(offset)
    
    with set_up_output(bin_file) as outline:
    
        for i in range(w*h):
        
            ch = bin_file.read(3)
            
            if ord(ch[0]) < 140 and ord(ch[1]) < 130 and ord(ch[2]) < 140:
                outline.write(chr(0) + chr(0) + chr(0))
                
            else:
                outline.write(chr(255) + chr(255) + chr(255))
                
    print "done"
   
if __name__ == "__main__":
    main()
