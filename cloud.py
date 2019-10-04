#-*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import nltk
from konlpy.tag import Kkma
# 리뷰자료는 공개불가자료로 kolaw 로 대체
from konlpy.corpus import kolaw
import matplotlib.pyplot as plt
import platform
from matplotlib import font_manager, rc
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator


def gen_cloud():

    kkma = Kkma()

    # stopwords = set(STOPWORDS)    
    # text = open("musical.txt","r").read()
    text = kolaw.open('constitution.txt').read()
    tokens_ko = kkma.nouns(unicode(text))
    # tokens_ko = [each_word for each_word in tokens_ko if each_word not in stopwords]

    ko = nltk.Text(tokens_ko, name='musical review')    
    data = ko.vocab().most_common(1000)
    tmp_data = dict(data)

    logo_coloring = Image.open("flipper_logo.png")
    np_logo_coloring = np.array(Image.open("flipper_logo.png"))
    mask = Image.new("RGB", logo_coloring.size, (255,255,255))
    mask.paste(logo_coloring,logo_coloring)
    mask = np.array(mask)
    

    wc = WordCloud(
        font_path='/Library/Fonts/AppleGothic.ttf',
        relative_scaling=0.2,
        background_color="white",
        max_words=1000,
        mask=mask,
        min_font_size=10,
        max_font_size=500,
        random_state=42)
    wc.generate_from_frequencies(tmp_data)
    image_colors = ImageColorGenerator(np_logo_coloring)

    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(12,12))
    plt.imshow(wc.recolor(color_func=image_colors), interpolation='bilinear')
    plt.axis("off")
    plt.savefig('result.png')
    plt.show()
    

if __name__ == "__main__":
    gen_cloud()