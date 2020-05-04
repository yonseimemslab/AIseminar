import sys
import random as rnd

if sys.version_info[0] == 3:
    from urllib.request import urlopen
    import urllib.request
else:
    from urllib import urlopen
    import urllib

# get random number with specified minimum and amplitude value
def get_random(minimum=0.0, amplitude=1.0):
    return minimum + amplitude * rnd.random()