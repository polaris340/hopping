#-*- coding: utf-8 -*-
from application import app, db

from flask import request, session, jsonify, render_template
from application.models.schema import Place, PlaceImage
from application.models.schema import User

from lib import login_required
from json import loads

from werkzeug import secure_filename

from google.appengine.api import files


from time import time

from PIL import Image
from StringIO import StringIO

THUMBNAIL_IMAGE_SIZE = 300
LARGE_IMAGE_WIDTH = 900

FILE_PATH = '/gs/hoppin-mvp-storage/user-upload-image/'
ORIGINAL_FILE_PATH = FILE_PATH + 'original/'
THUMBNAIL_FILE_PATH = FILE_PATH + 'thumbnail/'

PUBLIC_FILE_PATH = 'https://hoppin-mvp-storage.storage.googleapis.com/user-upload-image/'
PUBLIC_THUMBNAIL_FILE_PATH = PUBLIC_FILE_PATH + 'thumbnail/'

# EXTENSION_TYPE_MAP = {
#     'png':images.PNG, 
#     'jpg':images.JPEG, 
#     'jpeg':images.JPEG   
# }

ALLOWED_EXTENSIONS = ['png','jpg','jpeg']
IMAGE_FORMAT = {
    'png':'PNG',
    'jpg':'JPEG',
    'jpeg':'JPEG'
}


ORIENTATION_KEY = 274 # cf ExifTags

ROTATE_VALUES = {
    3: 180,
    6: 270,
    8: 90
}



def get_extension(filename):
    try:
        return filename.rsplit('.', 1)[1]
    except:
        return None

def allowed_extension(extension):
    return extension.lower() in ALLOWED_EXTENSIONS



@app.route('/image/<int:place_id>', methods=['POST'])
@login_required
def upload_image(place_id):

    uploaded_file = request.files['input-upload-image']

    if uploaded_file:
        img = Image.open(uploaded_file)

        try:
            exif = img._getexif()

            if ORIENTATION_KEY in exif:
                orientation = exif[ORIENTATION_KEY]
                if orientation in ROTATE_VALUES:
                    # Rotate picture
                    img = img.rotate(ROTATE_VALUES[orientation])
        except: pass

        extension = get_extension(uploaded_file.filename).lower()

        if not allowed_extension(extension):
            return jsonify(
                status = 400,
                message = "File extension not allowed : " + str(extension)
                ), 400

        mime_type = 'image/'+extension
        filename = str(int(time())) + secure_filename(uploaded_file.filename)

        image_url = PUBLIC_FILE_PATH + filename
        thumbnail_url = PUBLIC_THUMBNAIL_FILE_PATH + filename



        output = StringIO()
        #img.save(output, IMAGE_FORMAT[extension])

        # original image
        writable_file_name = files.gs.create(
            ORIGINAL_FILE_PATH + filename,
            mime_type = mime_type
            )
        with files.open(writable_file_name, 'ab') as f:
            img.save(f, IMAGE_FORMAT[extension])
            #f.write(output.getvalue())
            #output.close()
            

        files.finalize(writable_file_name)


        

        width, height = img.size
        large_image_width = LARGE_IMAGE_WIDTH if width > LARGE_IMAGE_WIDTH else width

        large_image_height = height * large_image_width / width


        if width < height:
            thumbnail_image_width = THUMBNAIL_IMAGE_SIZE if width > THUMBNAIL_IMAGE_SIZE else width
            thumbnail_image_height = height * thumbnail_image_width / width
        else:
            thumbnail_image_height = THUMBNAIL_IMAGE_SIZE if height > THUMBNAIL_IMAGE_SIZE else height
            thumbnail_image_width = width * thumbnail_image_height / height
        
        new_img = img.resize( (large_image_width, large_image_height) , Image.ANTIALIAS)

        # width 900
        writable_large_file_name = files.gs.create(
            FILE_PATH + filename,
            mime_type = mime_type,
            acl = 'public-read'
            )

        with files.open(writable_large_file_name, 'ab') as f:
            new_img.save(f, IMAGE_FORMAT[extension])
        

        files.finalize(writable_large_file_name)

        new_img = img.resize( (thumbnail_image_width, thumbnail_image_height) , Image.ANTIALIAS)
        output = StringIO()
        img.save(output, IMAGE_FORMAT[extension])

        writable_thumbnail_file_name = files.gs.create(
            THUMBNAIL_FILE_PATH + filename,
            mime_type = mime_type,
            acl = 'public-read'
            )

        with files.open(writable_thumbnail_file_name, 'ab') as f:
            new_img.save(f, IMAGE_FORMAT[extension])
        
        files.finalize(writable_thumbnail_file_name)

        target_place = Place.query.get(place_id)
        target_place.add_image(
            session['user_id'], 
            image_url,
            thumbnail_url
            )

        return jsonify(
            status = 200,
            message = "Successfully uploaded",
            response = {
                'imageUrl': image_url,
                'thumbnail_url': thumbnail_url
            }
            )

    else:
        return jsonify(
            status = 400,
            message = "Request does not contains image file"
            ), 400
        
        
    