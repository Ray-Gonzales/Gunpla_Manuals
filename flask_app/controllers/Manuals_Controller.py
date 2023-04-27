from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.manual_model import Manuals
from flask_app.models.user_model import Users
from flask_bcrypt import Bcrypt
from pdf2image import convert_from_path
bcrypt = Bcrypt(app) 
from werkzeug.utils import secure_filename
import os

# Homepage
@app.route("/")
def homepage():
    return render_template("index.html")

# Display library
@app.route("/library")
def library():
    manuals = Manuals.get_all_info()
    return render_template("library.html", manuals = manuals)

# Search library
@app.route("/search_library")
def search_library():
    search_manual = request.args.get('search_manual')
    manuals = Manuals.search(search_manual)
    return render_template("library.html", manuals=manuals)

# Separate path for 
@app.route("/exclusive_library")
def exclusive_library():
    manuals = Manuals.get_all_info()
    return render_template("library_exclusive.html", manuals = manuals)

@app.route("/instructions/<int:id>")
def instructions(id):
    instructions = Manuals.get_one_kit(id)
    return render_template("instructions.html", instructions = instructions)

# Display Upload page
@app.route("/upload")
def upload():
    if 'user_id' not in session:
        session.clear()
        return redirect('/logout')
    return render_template("upload.html")

# Define the allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}
def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set the path to the upload folder
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'images', 'manuals')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set the path to the cover art folder
COVER_ART_FOLDER = os.path.join(app.root_path, 'static', 'images', 'cover_art')
if not os.path.exists(COVER_ART_FOLDER):
    os.makedirs(COVER_ART_FOLDER)
app.config['COVER_ART_FOLDER'] = COVER_ART_FOLDER

# Upload route
@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['ins_manual']
    if not allowed_file(file.filename):
        flash("Invalid file type. Only PDF files are allowed.")
        return redirect('/upload')
    filename = secure_filename(file.filename)
    print(filename)
    if os.path.exists("/static/images/manual/" + filename):
        return redirect('/library')
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_basename = os.path.splitext(filename)[0]
    print(file_basename)
    image_file = file_basename + '.jpg'
    print(image_file)
    f_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    images = convert_from_path(f_path, fmt='jpeg', size=800)
    images[0].save(os.path.join(COVER_ART_FOLDER, image_file))
    exclusive = request.form.get('exclusive', False)
    data = {
        'kit_name': request.form['kit_name'],
        'series': request.form['series'],
        'release_year': request.form['release_year'],
        'ins_manual': filename,
        'cover_art': image_file,
        'exclusive': request.form['exclusive'],
        'user_id': session['user_id']
    }
    Manuals.create(data)
    if exclusive:
        return redirect('/exclusive_library')
    else:
        return redirect('/library')

@app.route('/delete_manual/<int:id>')
def delete_manual(id):
    Manuals.delete(id)
    return redirect('/library')

