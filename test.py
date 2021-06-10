
""" Program by Denise Rushing
    for Code in Place 2021 Final Project
    video location is here:
    Vimeo: https://vimeo.com/555444517
    youtube: https://youtu.be/D6JQ6Qj9Iq8
    This program accepts user input for elements of an award badge:
    the shape, color, inner shape, icon and the text to display
    then creates an image by first creating the base then layering the elements and the user text
    It both displays the image and saves it in a file"""

# import PIL module
from PIL import Image, ImageFont, ImageDraw
from simpleimage import SimpleImage

N_ROWS = 1
N_COLS = 1
BADGE_SIZE = 300  #assumes a square
WIDTH = N_COLS * BADGE_SIZE
HEIGHT = N_ROWS * BADGE_SIZE
R_OLD, G_OLD, B_OLD = (242, 172, 79)  #this is the orange base color for each badge

#Constants include lists of shapes and icons --to be used in user selection
#badge is layered -- base, added, icon, banner
BADGE_SHAPES = ['square', 'circle', 'heart', 'star', 'burst', 'flag', 'shield']
INNER_SHAPES = ['square', 'circle', 'heart', 'star', 'blotch', 'karel']
ICON_TYPES = ['trophy', 'threestars', 'star', 'karel', 'first', 'stardog', 'millie', 'walnut', 'frog']
BADGE_COLORS = ['orange', 'gray', 'tan', 'teal']
BANNERFILE = 'images/banner_300.png'  #transparent banners to place on badge
COLOR0 = 'orange' #Default color for badge
color_1 = 255 #text color for year
color_2 = 0 #text color for name and award
CH_SIZE = 38 #This font size fits in the badge space
CH_W = 9 #width of characters in pixels for centering functions

#Constants if needed for RGB validation - a future feature
LOWNUM = 0
HIGHNUM = 255

def main():
    #accepts user input for elements - text elements, shapes, icon
    #return a badge file and displays the image

    #user text input for badge
    title_text = input('Enter the award text- 14 characters max: ')
    name_text = input('Enter name - 14 characters max: ')
    year = input('Enter award date to display (year is best): ')

    #user selects color from allowed pallette
    user_color = input('input desired badge color: '  + str(BADGE_COLORS) + ': ')
    #function returns the RGB for the user-selected color
    r_new, g_new, b_new = color_picker(user_color)

    #Next, user selects an outer and inner shape and an icon
    print('')
    print('Next you will select shapes and an icon for your badge.')
    input('press any key when ready...')

    #calls function to get user inputs and puts the element filenames in a list (passes in the one selection already made)
    user_list = user_elements(user_color)

    """ Now the program builds the badge"""
    #calls function to convert base image to correct color
    new_path = colorizer(r_new, g_new, b_new, BADGE_SHAPES[int(user_list[4])])
    user_list[0] = new_path

    #function layers badge base and inner shape
    add_to_image(user_list[3], user_list[0]) #adds user selection of inner shape to main shape
    nextimage = 'images/new_image.png'

    #function layers user selection of icon to badge
    add_to_image(user_list[2], nextimage)  # adds user selection of icon to created file

    #layers user text and banners to badge
    banner = put_text(year, title_text, name_text)
    badge = add_to_image(banner, nextimage)

    # reveals completed badge!
    badge.save("images/badge_result.png", format="png")
    print('Your badge is stored in file: badge_result.png')
    message = input('press return to reveal your badge...')
    badge.show()


def user_elements(user_color):
    #creates the list of badge shape file names
    badge_shape_files = []
    print('')
    print('BADGE SHAPES')
    for i in range(len(BADGE_SHAPES)):
        filenamex = str('images/' + BADGE_SHAPES[i] + '1.png')
        badge_shape_files.append(filenamex)
        print(str(i+1) + ' ---> '+ BADGE_SHAPES[i])
    # gets badge shape choice from user
    #shape1 = input('input number of shape (1 - ' + str(len(badge_shape_files)) + '): ')
    #need to validate the input
    #if shape1.type is not int:
        #input('stop here')
    #shape_num = shape1
    shape_num = int(input('input number of shape (1 - ' + str(len(badge_shape_files)) + '): '))-1
    user_base = badge_shape_files[shape_num] #creates new user base file.

    #creates the list of inner shape file names
    inner_shape_files = []
    print('')
    print('INNER SHAPES')
    for i in range(len(INNER_SHAPES)):
        filenamez = str('images/' + INNER_SHAPES[i] + '_150.png')
        inner_shape_files.append(filenamez)
        print(str(i+1) + ' ---> '+ INNER_SHAPES[i])
    #gets shape choice from user
    x = int(input('input number of inner element (1 - ' + str(len(inner_shape_files)) + '): '))
    user_shape2 = inner_shape_files[x - 1]

    #creates the list of icon file names
    icon_files = []
    print('')
    print('ICON TYPES')
    for i in range(len(ICON_TYPES)):
        filenamey = str('images/icon_' + ICON_TYPES[i] + '.png')
        icon_files.append(filenamey)
        print(str(i+1) + ' ---> '+ ICON_TYPES[i])
    #gets icon choice from user
    x = int(input('input number of icon (1 - ' + str(len(icon_files)) + '): '))
    user_icon = icon_files[x - 1]

    #returns a list that stores the user selections
    user_list = [user_base, user_color, user_icon, user_shape2, shape_num] #list of user prefernces, + main shape number x
    return user_list

#this function adds one image to another preserving pransparnecy
def add_to_image(filename, filename1): 

    # Open Front Image
    frontImage = Image.open(filename)
  
    # Open Background Image
    background = Image.open(filename1)
  
    # Convert image to RGBA
    frontImage = frontImage.convert("RGBA")
  
    # Convert image to RGBA
    background = background.convert("RGBA")
  
    # Calculate width to be at the center
    width = (background.width - frontImage.width) // 2
  
    # Calculate height to be at the center
    height = (background.height - frontImage.height) // 2
  
    # Paste the frontImage at (width, height)
    background.paste(frontImage, (width, height), frontImage)
  
    # Save this image
    background.save("images/new_image.png", format="png")
    return background
    #background.show() for debugging

#This function gets text input from user and places on transparent banner image
def put_text(year, title_text, name_text):
    #gets text input from user
    #places test on banner image
    my_image = Image.open(BANNERFILE)
    title_font = ImageFont.truetype('trebuchet.ttf', CH_SIZE)
    image_editable = ImageDraw.Draw(my_image)
    txtlength = len(title_text)
    namelength = len(name_text)
    datelength = len(year)
    #determines horizontal center point for each type of text
    x1 = int(centertext_x(txtlength))
    x2 = int(centertext_x(namelength))
    x3 = int(centertext_x(datelength))
    #places text at x,y coordinates on the banner
    image_editable.text((x1, 0.617 * BADGE_SIZE), title_text, (color_2, color_2, color_2), font=title_font)
    image_editable.text((x2, 0.067 * BADGE_SIZE), name_text, (color_2, color_2, color_2), font=title_font)
    image_editable.text((x3,int(0.767 * BADGE_SIZE)), year, (color_1, color_1, color_1), font=title_font)
    my_image.save("images/banner_result.png", format="png")
    banner = 'images/banner_result.png'
    return banner

#This function centers the text
def centertext_x(string_length):
    center_pt = BADGE_SIZE/2
    if ((string_length % 2) != 0):
        pad = int(CH_W/2)
    else: pad = 0
    start_pt = int(pad + center_pt - (string_length*CH_W)) #text starting point, x-axis
    return start_pt

#This function translates user color choice to RGB (for our select pallette)
#In the future - add a RGB input option
def color_picker(user_color):
    #gets color choice for base image
    #returns r_new, g_new, b_new for the selected color and user_color name
    if user_color not in BADGE_COLORS:
        print('Using default color ' + str(COLOR0))
    if user_color == 'orange':
        r = 242
        g = 172
        b = 79
    elif user_color == 'gray':
        r = 125
        g = 125
        b = 125
    elif user_color == 'tan':
        r = 170
        g = 140
        b = 100
    elif user_color == 'teal':
        r = 0
        g = 128
        b = 128
    else: #makes sure that stray inputs use default color
        r = 242
        g = 172
        b = 79
    # print(r,g,b)
    # pause = input('paused at colorpicker - RGB ')
    return r,g,b

# The following creates a new file--replacing one color and preserving transparency
# replaces main color in the base file image
#saves a file for the program to use in the layering
def colorizer(r_new, g_new, b_new, shape):
    old_path = ('images/' + str(shape) + '1.png')
    new_path = ('images/' + str(shape) + '2.png')
    #print(old_path)
    #print(new_path)
    #pause = input('paused at colorizer')
    #r_new, g_new, b_new = (0, 174, 239)
    im = Image.open(old_path)
    pixels = im.load()

    width, height = im.size
    for x in range(width):
        for y in range(height):
            r, g, b, a = pixels[x, y]
            if (r, g, b) == (R_OLD, G_OLD, B_OLD):
                pixels[x, y] = (r_new,g_new,b_new, a)
    im.save(new_path)
    #im.show()
    return new_path


if __name__ == '__main__':
    main()