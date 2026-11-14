import sys, numpy as np
sys.argv=['x','serumL.jpg','serumLplate.jpg','/home/claude/everliv-media-repo/library/peptide-eye-serum/peptide-eye-serum--front-cutout.png','serum15','--cyl','--wrap','--ring','--grad']
import cp_composite as C
def det(img, grey=False, hint=None):
    m=np.zeros(img.shape[:2],np.uint8); m[856:1694,505:872]=1   # measured stand-in body (base ~1700)
    return m,(499,850,878,1700)
C.detect_standin=det
C.run(sys.argv[1],sys.argv[2],sys.argv[3],'serum15',shape='cyl',product_shrink=float(sys.argv_shrink) if False else 1.04)
