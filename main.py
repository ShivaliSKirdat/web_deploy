from flask import Flask
from flask import sessions
from flask import request
from flask import render_template
from flask import redirect, url_for
from werkzeug.utils import secure_filename
import json
import os
from modules.Login import Login
from modules.Gallery import Gallery
from modules.Photos import Photos
from definition import *
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

app = Flask(__name__)
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])
session = {}

'''
for int routes
@app.route('/<int:id>')
def func(id):
    print(id)
'''
photos_obj = Photos()


@app.route('/')
@app.route('/index')
def index():
    if 'type' in session:
        return redirect(url_for('galleries'))

    return render_template("index.html")

def get_secrets_from_keyvault():
    vault_url = 'https://demo-web-key-vault.vault.azure.net/'  # Replace with your Key Vault URL

    credential = DefaultAzureCredential()
    secret_client = SecretClient(vault_url=vault_url, credential=credential)

    username = secret_client.get_secret('admin').value
    password = secret_client.get_secret('https://demo-web-key-vault.vault.azure.net/secrets/admin/2a81d20f0195456da01101212990f85a').value

    return username, password

@app.route('/login', methods=['POST'])
def do_login():
    # Get the username and password from the request
    request_data = request.get_json()
    input_username = request_data['username']
    input_password = request_data['password']

    # Retrieve the username and password from Azure Key Vault
    secret_username, secret_password = get_secrets_from_keyvault()

    # Compare the input username and password with the secrets
    if input_username == secret_username and input_password == secret_password:
        # Successful login
        return jsonify({'message': 'Login successful'})
    else:
        # Failed login
        return jsonify({'message': 'Invalid credentials'})

# Other routes and application logic here

# if __name__ == '__main__':
#     app.run()


# @app.route('/login', methods=['POST'])
# def do_login():
#     if request.method == "POST":
#         user_name = request.form['username']
#         password = request.form['password']
        
#         login_obj = Login()
#         result = login_obj.login(user_name, password)
#         print(result['type'])

#         if result['result']:
#             session['type'] = result['type']

#         response = {'success': result}
#         return json.dumps(response)


@app.route('/logout')
def do_logout():
    session.pop('type', None)
    return redirect(url_for('index'))


# -------------- Gallery Routes ----------------
@app.route('/galleries')
def galleries():
    if 'type' in session:
        gallery_obj = Gallery()
        galleries = gallery_obj.get_all_gallery()
        return render_template("gallery.html", galleries=galleries, session=session)
    else:
        return redirect(url_for("index"))


@app.route('/galleries/add', methods=['POST'])
def add_galleries():
    if 'type' in session:
        if request.method == "POST":
            gallery_name = request.form['galleryName']

            gallery_obj = Gallery()
            result = gallery_obj.add_gallery(gallery_name)

            response = {'success':result}
            return json.dumps(response)
    else:
        response = {'success': False}
        return json.dumps(response)


@app.route('/galleries/edit', methods=['POST'])
def edit_galleries():
    if request.method == "POST":
        new_name = request.form['newName']
        gallery_name = request.form['galleryName']

        gallery_obj = Gallery()
        result = gallery_obj.edit_gallery_name(gallery_name, new_name)

        response = {'success': result}
        return json.dumps(response)


@app.route('/galleries/delete', methods=['POST'])
def delete_galleries():
    if request.method == "POST":
        gallery_name = request.form['galleryName']

        gallery_obj = Gallery()
        result = gallery_obj.delete_gallery(gallery_name)

        response = {'success': result}
        return json.dumps(response)

# -------------- Gallery Routes ----------------


# -------------- Gallery Photos Routes ----------------
@app.route('/galleries/album/<gallery_name>', methods=['GET'])
def gallery(gallery_name):
    if 'type' in session:
        photos_obj = Photos()
        photos = photos_obj.get_all_gallery_photos(gallery_name)
        return render_template("photos.html", photos=photos, gallery_folder=Gallery_Folder,gallery_name=gallery_name, session=session)
    else:
        return redirect(url_for("index"))


@app.route('/galleries/album/photos/delete', methods=['POST'])
def delete_gallery_photo():
    if request.method == "POST":
        gallery_name = request.form['galleryName']
        photo_name = request.form['photoName']

        result = photos_obj.delete_gallery_photos(gallery_name, photo_name)

        response = {'success': result}
        return json.dumps(response)


@app.route('/galleries/album/<gallery_name>/upload', methods=['GET','POST'])
def upload_gallery_photo(gallery_name):
    app.config['UPLOAD_FOLDER'] = Gallery_Folder+gallery_name

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(url_for('gallery', gallery_name=gallery_name))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            msg = 'No selected file'
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('gallery', gallery_name=gallery_name))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# -------------- Gallery Photos Routes ----------------


#if __name__  == "__main__":
#    app.run(debug=True)

if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5000))
   app.run(debug=True, host='0.0.0.0', port=port)


