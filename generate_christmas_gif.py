import dlib
from PIL import Image
import argparse
from imutils import face_utils
import numpy as np
import moviepy.editor as mpy
import cv2


def showImgae(img, imgname="imge"):
    cv2.imshow(imgname, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


parser = argparse.ArgumentParser()
parser.add_argument("-img", required=True, help="path to input image")
args = parser.parse_args()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68.dat')

# resize to a max_width to keep gif size small
max_width = 500

# open our image, convert to rgba
img = Image.open(args.img).convert('RGBA')

# two images we'll need, glasses and deal with it text
hat = Image.open('image/hat.png')
text = Image.open('image/text.png')
if img.size[0] > max_width:
    scaled_height = int(max_width * img.size[1] / img.size[0])
    img.thumbnail((max_width, scaled_height))

img_gray = np.array(img.convert('L'))  # need grayscale for dlib face detection

# rects = detector(img_gray, 0)
rects = detector(img_gray, 1)

if len(rects) == 0:
    print("No faces found, exiting.")
    exit()

print("%i faces found in source image. processing into gif now." % len(rects))

faces = []

for rect in rects:
    face = {}
    facearray = [rect.left(), rect.top(), rect.right(), rect.bottom()]
    shades_width = rect.right() - rect.left()
    print(shades_width)
    # shades_top = rect.top - rect.bottom

    # predictor used to detect orientation in place where current face is
    shape = predictor(img_gray, rect)
    for index, pt in enumerate(shape.parts()):
        pt_pos = (pt.x, pt.y)
        cv2.circle(img_gray, pt_pos, 2, (0, 0, 0), 1)
    showImgae(img_gray)
    shape = face_utils.shape_to_np(shape)
    # grab the outlines of each eye from the input image
    leftEye = shape[36:42]
    print("leftEye:", leftEye)
    rightEye = shape[42:48]
    print("rightEye:", rightEye)

    # compute the center of mass for each eye
    leftEyeCenter = leftEye.mean(axis=0).astype("int")
    rightEyeCenter = rightEye.mean(axis=0).astype("int")
    print("leftEyeCenter:", leftEyeCenter)
    print("rightEyeCenter:", rightEyeCenter)
    # compute the angle between the eye centroids
    dY = leftEyeCenter[1] - rightEyeCenter[1]
    dX = leftEyeCenter[0] - rightEyeCenter[0]
    angle = np.rad2deg(np.arctan2(dY, dX))

    # resize hat to fit face width
    factor = 1.2
    hat_w = int(round(shades_width * factor))
    hat_h = int(round(shades_width * hat.size[1] / hat.size[0] * factor))
    current_hat = hat.resize(
        (hat_w, hat_h),
        resample=Image.LANCZOS)
    # rotate and flip to fit eye centers
    current_hat = current_hat.rotate(angle, expand=True)
    current_hat = current_hat.transpose(Image.FLIP_TOP_BOTTOM)

    # mid of hat needs shift
    shit_hat_x = int(round(1 / 4 * hat_w))
    # add the scaled image to a list, shift the final position to the
    # left of the leftmost eye
    face['hat_image'] = current_hat
    left_eye_x = leftEye[0, 0] - shades_width // 4
    left_eye_y = leftEye[0, 1] - shades_width // 6
    face['final_pos'] = (left_eye_x - shit_hat_x, left_eye_y - 80)
    faces.append(face)

# how long our gif should be
duration = 3


def make_frame(t):
    draw_img = img.convert('RGBA')  # returns copy of original image

    if t == 0:  # no glasses first image
        return np.asarray(draw_img)

    for face in faces:
        if t <= duration - 2:
            current_x = int(face['final_pos'][0])
            current_y = int(face['final_pos'][1] * t / (duration - 2))
            draw_img.paste(face['hat_image'], (current_x, current_y), face['hat_image'])
        else:
            draw_img.paste(face['hat_image'], face['final_pos'], face['hat_image'])
            draw_img.paste(text, (75, draw_img.height // 2 - 32), text)


    return np.asarray(draw_img)


animation = mpy.VideoClip(make_frame, duration=duration)
animation.write_gif("image/deal.gif", fps=4)
