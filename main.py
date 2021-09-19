import os
from flask import *
from werkzeug.utils import secure_filename
from PIL import Image, ImageColor

app = Flask(__name__)

UPLOAD_FOLDER = "./pictures"
ALLOWED_EXTENSIONS =  {'png', 'jpg', 'jpeg'}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def bw_compare(filename):
    image = Image.open("./pictures/" + filename, "r").convert("RGB")
    black, white = 0, 0
    for p in image.getdata():
        if p == (0, 0, 0):
            black += 1
        if p == (255, 255, 255):
            white += 1
    if black > white:
        return 'черных'
    else:
        return 'белых'

def count_hex(filename, hex_code):
    image = Image.open("./pictures/" + filename, "r").convert("RGB")
    try:
        color = ImageColor.getcolor("#" + hex_code, "RGB")
    except:
        return 0
    amount = 0
    for pixel in list(image.getdata()):
        if pixel == color:
            amount += 1
    return amount

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        hex_code = request.form['text']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            m_pxl = bw_compare(filename)
            hex_am = count_hex(filename, hex_code)
            return render_template('index.html', m_pxl=m_pxl, hex_am=hex_am)
    return '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file>
                <input type=submit value=Upload></p>
            <p>hex code <input name=text type=text name=hex_code></p>    
            </form>
            '''

if __name__ == "__main__":
    app.run()

