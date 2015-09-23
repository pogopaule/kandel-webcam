import numpy
import cv2
import urllib
import pytz
from datetime import datetime
from twitter import *
import os

timezone = pytz.timezone('Europe/Berlin')
now = datetime.now(timezone)

def webcam_url():
    hour = str(now.hour)
    minute = str(now.minute / 15 * 15).zfill(2)
    return "http://www.dgfc-suedschwarzwald.de/webcam2/image-%s-%s.jpg" % (hour, minute)

def send_tweet():
    t = Twitter(auth=OAuth(os.environ['TOKEN'], os.environ['TOKEN_KEY'], os.environ['CON_SECRET'], os.environ['CON_SECRET_KEY']))
    message = 'Auf dem Kandel scheint was los zu sein! %s' % webcam_url()
    t.statuses.update(status=message)

def webcam_on():
    today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
    today8pm = now.replace(hour=20, minute=0, second=0, microsecond=0)
    return (today8am < now) and (now < today8pm)

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

def activity():
    return number_of_keypoints(url_to_image(webcam_url())) > 70

def run():
    if webcam_on() and activity(): send_tweet()
