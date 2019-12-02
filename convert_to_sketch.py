from PIL import Image
import numpy as np
import os
import time

def image(sta,end,depths=10):
    a = np.asarray(Image.open(sta).convert('L')).astype('float')
    depth = depths  #the range of depth is between 0 to 100, the standard is 10
    grad = np.gradient(a)  # take the gradient of all pixales of the picture
    grad_x, grad_y = grad  # split the gradient to x and y axis
    grad_x = grad_x * depth / 100. # take the norm of the gradient x
    grad_y = grad_y * depth / 100. # take the norm of gradient y
    A = np.sqrt(grad_x ** 2 + grad_y ** 2 + 1.)
    uni_x = grad_x / A
    uni_y = grad_y / A
    uni_z = 1. / A
    vec_el = np.pi / 2.2  # elevation angle of the light source
    vec_az = np.pi / 4.  # azimuth angle of the light source
    dx = np.cos(vec_el) * np.cos(vec_az)  # shade on x axis
    dy = np.cos(vec_el) * np.sin(vec_az)  # shade on y axis
    dz = np.sin(vec_el)  # shade on z axis
    b = 255 * (dx * uni_x + dy * uni_y + dz * uni_z)  #
    b = b.clip(0, 255)# give a bound of the pixel
    im = Image.fromarray(b.astype('uint8'))  # reconstruct the image
    im.save(end)

def main():
    xs=20
    start_time = time.perf_counter()
    startss = os.listdir("./images")
    time.sleep(2)
    for starts in startss:
        start = ''.join(starts)
        sta = './images/' + start
        end = './images/' + 'SK_' + start
        try:
            image(sta=sta,end=end,depths=xs)
        except IOError:
            print("{} is not a picture file".format(start))
            print(IOError)

    end_time = time.perf_counter()
    print('total time for producing the picture: ----' + str(end_time - start_time) + '   seconds')
    time.sleep(3)

main()
