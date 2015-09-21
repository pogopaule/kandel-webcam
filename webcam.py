import numpy
import cv2
import urllib
from matplotlib import pyplot as plt
import pytz
from datetime import datetime

timezone = pytz.timezone('Europe/Berlin')
now = datetime.now(timezone)

def is_webcam_running():
    today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    today8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
    return (today8am > now) & (now < today8pm)

def webcam_url():
    hour = str(now.hour)
    minute = str(now.minute / 15 * 15).zfill(2)
    return 'http://www.dgfc-suedschwarzwald.de/webcam2/image-%(hour)-%(minute).jpg'

def url_to_image(url):
    resp = urllib.urlopen(url)
    image = numpy.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def mask_image(image):
    mask = numpy.zeros(image.shape, dtype=numpy.uint8)
    region_of_interest = numpy.array([[(300, 940), (515, 850), (980, 780), (910, 1030), (805, 1015), (620, 1100), (545, 1060), (350, 1130)], [(1060, 780), (1360,750), (1500, 900), (1450, 1000), (1300, 1010), (1300, 885), (1220, 900), (1180, 975)]], dtype=numpy.int32)
    white = (255, 255, 255)
    cv2.fillPoly(mask, region_of_interest, white)
    return cv2.bitwise_and(image, mask)

def number_of_keypoints(image):
    masked_image = mask_image(image)
    ff_detector = cv2.FastFeatureDetector(40)

    keypoints = ff_detector.detect(masked_image,None)
    return len(keypoints)

if is_webcam_running():
    if number_of_keypoints(url_to_image(webcam_url())) > 70:
        print 'something is going on'
    else:
        print 'nope, no one there'
else:
    print 'webcam is not running'
