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

# Separate page for exclusive
@app.route("/exclusive_library")
def exclusive_library():
    manuals = Manuals.get_all_info()
    return render_template("library_exclusive.html", manuals = manuals)

# Instruction manual page
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
    # checks if the file type is allowed
    if not allowed_file(file.filename):
        flash("Invalid file type. Only PDF files are allowed.")
        return redirect('/upload')
    # checks if a file with the same name already exists in a specific folder
    filename = secure_filename(file.filename)
    if os.path.exists("/static/images/manual/" + filename):
        return redirect('/library')
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # converts pdf file to jpg and saves it to a folder
    file_basename = os.path.splitext(filename)[0]
    image_file = file_basename + '.jpg'
    f_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    images = convert_from_path(f_path, fmt='jpeg')
    images[0].save(os.path.join(COVER_ART_FOLDER, image_file))
    # check if kit is exclusive
    exclusive = request.form.get('exclusive', False)
    # create to database
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
    # render the correct page
    if exclusive:
        return redirect('/exclusive_library')
    else:
        return redirect('/library')

@app.route('/edit_manual/<int:id>', methods=['GET', 'POST'])
def edit_manual(id):
    if 'user_id' not in session:
        session.clear()
        return redirect('/logout')
    manual = Manuals.get_one_id(id)
    if request.method == 'POST':
        data = {
            'id': id,
            'kit_name': request.form['kit_name'],
            'series': request.form['series'],
            'release_year': request.form['release_year'],
            'exclusive': request.form.get('exclusive', False)
        }
        Manuals.update(data)
        flash("Manual updated successfully!")
        return redirect(f'/edit_manual/{id}')
    return render_template('edit_manual.html', manual=manual)

@app.route('/delete_manual/<int:id>')
def delete_manual(id):
    if 'user_id' not in session:
        session.clear()
        return redirect('/logout')
    Manuals.delete(id)
    return redirect('/library')
