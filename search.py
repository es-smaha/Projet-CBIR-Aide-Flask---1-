from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from datetime import datetime




from datetime import datetime


def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def get_colors(image , number_of_colors , show_chart = True):
    
    modified_image = cv2.resize(image, (600, 400), interpolation = cv2.INTER_AREA)
    modified_image = modified_image.reshape(modified_image.shape[0]*modified_image.shape[1], 3)
    
    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)

    counts = Counter(labels)

    center_colors = clf.cluster_centers_
  # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb_colors = [ordered_colors[i] for i in counts.keys()]

    if (show_chart):
        plt.figure(figsize = (8, 6))
        plt.pie(counts.values(), labels = hex_colors, colors = hex_colors)
        plt.savefig("./static/plot2.png",dpi = 300)


    return rgb_colors



def match_image_by_color(image, color, threshold = 40, number_of_colors = 3): 
    
    image_colors = get_colors(image, number_of_colors, False)
    selected_color = rgb2lab(np.uint8(np.asarray([[color]])))
    
    select_image = False
    for i in range(number_of_colors):
        curr_color = rgb2lab(np.uint8(np.asarray([[image_colors[i]]])))
        diff = deltaE_cie76(selected_color, curr_color)
        if (diff < threshold):
            select_image = True
    
    return select_image


def show_selected_images(color, threshold, colors_to_match):
    
    IMAGE_DIRECTORY = 'images'

    images = []
    

    for file in os.listdir(IMAGE_DIRECTORY):
        if not file.startswith('.'):
            images.append(get_image(os.path.join(IMAGE_DIRECTORY, file)))

    index = 1
    
    result = []
    names = []
      
    for i in range(len(images)):
        selected= []
        for j in range(3):
            selected.append(match_image_by_color(images[i], color[j], threshold, colors_to_match))
        if (all(selected)):
            result.append(images[i]) 
    print(result)
          


    for file in os.listdir(IMAGE_DIRECTORY):
        im = get_image(os.path.join(IMAGE_DIRECTORY, file))
        for i in range(len(result)):
            if result[i].shape == im.shape:
                difference = cv2.subtract(im, result[i])
                b, g, r = cv2.split(difference)
                if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                    print("The images are completely Equal")
                    names.append(file)
    return names