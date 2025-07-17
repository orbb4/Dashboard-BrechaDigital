import os
from PIL import Image

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_gradient_magnitude
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, ImageColorGenerator



stopwords = stopwords.words("spanish") + ["si", "mas"]
text = open("../Dataset/Wordcloud/Brecha Digital e Inclusion.txt", "r", encoding="utf-8").read()


image_color = np.array(Image.open("../Dataset/Wordcloud/internet2.png"))

image_color = image_color[::3, ::3]

image_mask = image_color.copy()
image_mask[image_mask.sum(axis=2) == 0] = 255
edges = np.mean([gaussian_gradient_magnitude(image_color[:, :, i] / 255., 2) for i in range(3)], axis=0)
image_mask[edges > .08] = 255
wc = WordCloud(max_words=400, background_color="navy", mask=image_mask, max_font_size=40, random_state=42, relative_scaling=0,
                contour_color="yellow", contour_width=2, colormap="Wistia", stopwords=stopwords)
wc.generate(text)
plt.imshow(wc)
plt.show()
wc.to_file("wordcloud.png")