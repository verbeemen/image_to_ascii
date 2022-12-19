
# import libraries
import os
import torch
import numpy as np
from html2image import Html2Image
from PIL import (Image, ImageDraw, ImageFont)
import torchvision.transforms as transforms

# define a torch to pill transformer
TORCH_TO_PIL = transforms.ToPILImage()
PIL_TO_TORCH = transforms.PILToTensor()
GAUSSIAN_BLUR = transforms.GaussianBlur(5, sigma=(1.3, 1.7))

def load_image_from_string(image_path):
    """Load image from path and return a numpy array

    Args:
        image_path (str): path of the image
    """
    # load the image
    image = Image.open(image_path)

    # convert the image to grayscale
    image = image.convert('L')

    # convert the image to torch array
    image = PIL_TO_TORCH(image)[0,:,:].to(torch.float32)

    # return the image
    return image



def show_image_from_tensor(image):
    """Show image from numpy array

    Args:
        image (numpy array): numpy array of the image
    """
    # convert the image to PIL image
    image = TORCH_TO_PIL(image)

    # show the image
    image.show()
 


def create_an_alphabet(font_size = 9, 
                       alphabet = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*().,?-_+=`'~^'\"\/|"
                       ):
    """
        In general, we want to split the image into a grid of X by Y cells.
        Each cell will be a character in the alphabet.
        But first of all, we don't know the size of each cell because,
        the size of each character is different and they are dependent on the font and font size.

        Therefore, we will create an numpy array of the letters in our alphabet.
        And then we will find the maximum width and height of the biggest character.

    """
    #alphabet = ".:*|#/\\ _-≃^\"'"
    #
    # Create, Estimate the size of each letter by creating a fake html page
    # Cut out the letters from the fake html page
    # In theory, this estimation should generate us a good result
    #
    # get a random id
    id = np.random.randint(1e8)

    ## prepare a fake html page
    hti = Html2Image()
    css = "body {font-family: monospace; background: #000000; color:#ffffff; margin:0; padding:0; font-size: "+ str(font_size) +"px;}"
 
    #
    # Height
    #

    html = alphabet

    # Store the fake html page as an image
    hti.screenshot(html_str= html, css_str=css, save_as=f'img_{id}.png', size=((len(alphabet) *(font_size+10), font_size+20) ))

    # load the image as a numpy array
    img = load_image_from_string(f'img_{id}.png')
    os.remove(f'img_{id}.png')

    # get the amount of filled int pixels as the height of the letters
    height = np.array(img.numpy() > 3).max(axis=1).sum()

    #
    # Width : transpose the alphabet
    #
    html = '<br/>'.join([char for char in list(alphabet)])

    # Store the fake html page as an image
    hti.screenshot(html_str= html, css_str=css, save_as=f'img_{id}.png', size=((font_size+20), len(alphabet) *(font_size+10) ))

    # load the image as a numpy array
    img = load_image_from_string(f'img_{id}.png')
    os.remove(f'img_{id}.png')

    # get the amount of filled int pixels as the width of the letters
    width = np.array(img.numpy() > 3 ).max(axis=0).sum()


    #
    # Loop over the alphabet
    #
    letters = []
    pattern = []
    # convolute over the image to get the edges
    kernel = torch.tensor([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=torch.float32)
    kernel = torch.stack([kernel, kernel.T], dim=0)[:,None,:,:]
    for char in alphabet:

        # Store the fake html page as an image
        hti.screenshot(html_str= char, css_str=css, save_as=f'img_{id}.png', size=((width), (height) ))

        # load the image as a numpy array
        img = load_image_from_string(f'img_{id}.png')
        os.remove(f'img_{id}.png')


        letters.append(char)
        pattern.append(img)
        #show_image_from_tensor(img.to(torch.uint8))
    
        

    return np.array(letters), pattern, width, height



def preprocess_image(img, height, width):


    # convolute over the image to get the edges
    kernel = torch.tensor([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], dtype=torch.float32)
    kernel = torch.stack([kernel, kernel.T], dim=0)[:,None,:,:]

    # Bur the image
    img = GAUSSIAN_BLUR(img[None,:,:])

    # get the edges
    img = torch.nn.functional.conv2d(img[None, :, :, :], kernel, padding=1)
    img = img.min(dim=1)[0][0]
   
    # resize the image
    img = img[:height*int(img.shape[0]/height), :width*int(img.shape[1]/width)]
    
    # normalize: between 0 and 255 per dimension
    #img = 255 - ((img - img.min()) / (img.max() - img.min()) * 255)
    # normalize: zero mean
    img = (img - img.mean()) / img.std()

    #img = (img > 55)*255
    quantiles = torch.quantile(img.to(torch.float32), torch.tensor([0.075, 0.925]))
    img = ((img < quantiles[0]) | (img > quantiles[1]))*255

    #show_image_from_tensor(img.to(torch.uint8))

    # reshape the image
    return img.unfold(0, height, height).unfold(1, width, width).reshape(-1, height, width)



def main():

    # load the image
    img = load_image_from_string('data/photo_cat.jpg')
    img = load_image_from_string('data/dieter.jpeg')
    img = load_image_from_string('data/lena.jpg')
    show_image_from_tensor(img.to(torch.uint8))

    #img = load_image_from_string('data/test.jpg')
    #show_image_from_numpy_array(img)

    # get the alphabet
    letters, patterns, width, height = create_an_alphabet()

    # Create a convolution kernel with the patterns of our alphabet
    kernel = torch.stack(patterns, dim=0)[:,None,:,:]

    # get lines and edges
    processed_image = preprocess_image(img, height, width) 
    letter_index = ((processed_image - kernel)**2).mean(dim=(-2,-1)).argmin(dim=0).view(int(img.shape[0]/height), int(img.shape[1]/width)).numpy()

    # create a txt file and print each row
    with open('readme.txt', 'w') as f:
        f.write('\n'.join([''.join(row)for row in letters[letter_index]]))


if "__main__" == __name__:
    main()

