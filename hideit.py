# pick a .png or .bmp file you have in the working directory
# or give full path name
original_image_file = "tsb.png"
img = Image.open(original_image_file)

# image mode needs to be 'RGB'
print(img, img.mode)  # test
# create a new filename for the modified/encoded image
encoded_image_file = "enc_" + original_image_file
# don't exceed 255 characters in the message
secret_msg = "don't you know who it is yet?"
print(len(secret_msg))  # test
img_encoded = encode_image(img, secret_msg)
if img_encoded:
    # save the image with the hidden text
    img_encoded.save(encoded_image_file)
    print("{} saved!".format(encoded_image_file))
    # get the hidden text back ...
    img2 = Image.open(encoded_image_file)
    hidden_text = decode_image(img2)
    print("Hidden text:\n{}".format(hidden_text))

from PIL import Image

png = Image.open('tsb.png')
png.load() # required for png.split()

background = Image.new("RGB", png.size, (255, 255, 255))
background.paste(png, mask=png.split()[3]) # 3 is the alpha channel

background.save('tsb.png', 'PNG', quality=80)    

