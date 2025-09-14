import cv2
from pix2text import Pix2Text, merge_line_texts


p2t = Pix2Text.from_config()
outs2 = p2t.recognize("image.png", file_type='text_formula', return_text=True, save_analysis_res='mixed-out.jpg')