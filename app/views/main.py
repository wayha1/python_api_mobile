from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import ImageModel,Profile
from app.extensions import db
from cloudinary.uploader import upload

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            gender = request.form['gender']
            role = request.form['role']
            profile_image = request.files['profile_image']

            # Check if profile image is provided and allowed
            if profile_image and allowed_file(profile_image.filename):
                cloudinary_response = upload(profile_image)
                cloudinary_url = cloudinary_response['secure_url']

                profile = Profile(
                    username=username,
                    email=email,
                    gender=gender,
                    role=role,
                    profile_image=cloudinary_url
                )
                db.session.add(profile)
                db.session.commit()

                flash('Profile created successfully', 'success')
                return redirect(url_for('main.dashboard'))
            else:
                flash('Invalid profile image file extension', 'error')
        except Exception as e:
            flash('Error creating profile: {}'.format(str(e)), 'error')

    return render_template('profile.html')
@main.route('/dashboard')
@login_required
def dashboard():
    username = current_user.username
    return render_template('dashboard.html', username=username)

@main.route('/dash', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        try:
            file = request.files['file']

            if file and allowed_file(file.filename):
                cloudinary_response = upload(file)
                cloudinary_url = cloudinary_response['secure_url']

                image = ImageModel(file_path=cloudinary_url)
                db.session.add(image)
                db.session.commit()

                return redirect(url_for('main.home'))
            else:
                flash('Invalid file extension', 'error')
        except Exception as e:
            flash('Error uploading the image: {}'.format(str(e)), 'error')

    images = ImageModel.query.all()
    return render_template('home.html', images=images)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt','png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
