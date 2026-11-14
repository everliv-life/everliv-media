import sys, numpy as np
sys.argv=['x','tinL.jpg','tinLplate.jpg','collagen-front-cutout-v2.png','tin12','--ring']
import cp_composite as C
def det(img, grey=False, hint=None):
    m=np.zeros(img.shape[:2],np.uint8); m[1064:1690,616:1224]=1
    return m,(612,1062,1228,1694)
C.detect_standin=det
C.run(sys.argv[1],sys.argv[2],sys.argv[3],'tin12',shape='flat')
