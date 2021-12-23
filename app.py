from flask import Flask, render_template, redirect, url_for, request
from dominatcolor import *

import cv2
import os
from PIL import Image
from search import *



STATIC_FOLDER = './static'



app = Flask(__name__)


@app.route('/')
def home():
    return render_template('input.html')
 
@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if request.method == 'POST':
        if request.files:            
            # Lecture des paramètres 
            image = request.files["image"]
            imageName = image.filename
            image.save(os.path.join(STATIC_FOLDER, imageName))            
            
            # Lecture et traitement
            imagePath = os.path.join(STATIC_FOLDER, imageName)
            img = cv2.imread(imagePath)
            
            image2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            get_pie(image2)
            
        
            # Sauvegarde du résultat                   
            cv2.imwrite(os.path.join(STATIC_FOLDER, "ct_"+imageName), image2)

            return redirect(url_for('output',name=imageName))
            
    else :
        return redirect(url_for('/'))

@app.route('/output')
def output():
    
    local_url1= './static/'+request.args.get('name')
    local_url2= './static/plot2.png'
    return render_template('output.html',url1 = local_url1, url2 = local_url2)




@app.route('/search')
def search():
    return render_template('search.html')


@app.route("/search_image", methods=["GET", "POST"])
def search_image():
    if request.method == 'POST':
        if request.files:            
            # Lecture des paramètres 
            image = request.files["image"]
            imageName = image.filename
            image.save(os.path.join(STATIC_FOLDER, imageName))            
            
            # Lecture et traitement
            imagePath = os.path.join(STATIC_FOLDER, imageName)
            img = cv2.imread(imagePath)
            
            image2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            col = get_colors(image2 , 3 , False)
            names = show_selected_images(col, 40, 3)

        return  render_template('search.html', list = names , name = imageName)
            
    else :
        return redirect(url_for('/'))






if __name__ == '__main__':
   app.run()