from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import * 
from app.extensions import db
from cloudinary.uploader import upload
from app.views.auth.form import CategoryForm, ProfileForm

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/category', methods=['GET', 'POST'])
@login_required
def category():
    username = current_user.username
    form = CategoryForm()
    
    # Create operation
    if form.validate_on_submit():
        name = form.name.data
        
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        
        flash('Category added successfully', 'success')
        return redirect(url_for('main.category'))
    
    # Read operation
    categories = Category.query.all()
    
    # Update operation
    if request.method == 'POST':
        if 'edit_category' in request.form:
            category_id = request.form.get('category_id')
            new_name = request.form.get('new_name')
            category = Category.query.get(category_id)
            if category:
                category.name = new_name
                db.session.commit()
                flash('Category updated successfully', 'success')
                return redirect(url_for('main.category'))
        
        # Delete operation
        elif 'delete_category' in request.form:
            category_id = request.form.get('category_id')
            category = Category.query.get(category_id)
            if category:
                db.session.delete(category)
                db.session.commit()
                flash('Category deleted successfully', 'success')
                return redirect(url_for('main.category'))
    
    return render_template('category.html', form=form, username=username, categories=categories)

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    username = current_user.username
    form = ProfileForm()

    if form.validate_on_submit():
        try:
            username = form.username.data
            email = form.email.data
            gender = form.gender.data
            role = form.role.data
            profile_image = form.profile_image.data

            if profile_image and allowed_file(profile_image.filename):
                cloudinary_response = upload(profile_image)
                cloudinary_url = cloudinary_response['secure_url']

                profile = Profile.query.filter_by(username=username).first()
                if profile:
                    profile.email = email
                    profile.gender = gender
                    profile.role = role
                    profile.profile_image = cloudinary_url
                else:
                    profile = Profile(
                        username=username,
                        email=email,
                        gender=gender,
                        role=role,
                        profile_image=cloudinary_url
                    )
                db.session.add(profile)
                db.session.commit()
                
                profiles = Profile.query.all()  
                
                flash('Profile created/updated successfully', 'success')
                return redirect(url_for('main.profile'))
            else:
                flash('Invalid profile image file extension', 'error')
        except Exception as e:
            flash('Error creating/updating profile: {}'.format(str(e)), 'error')
            
    profiles = Profile.query.all()  
    
    return render_template('profile.html', form=form, username=username, profiles=profiles)

@main.route('/profile/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    profile = Profile.query.get_or_404(id)
    form = ProfileForm(obj=profile)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            form.populate_obj(profile)
            profile_image = request.files['profile_image']
            if profile_image and allowed_file(profile_image.filename):
                cloudinary_response = upload(profile_image)
                profile.profile_image = cloudinary_response['secure_url']
            db.session.commit()
            flash('Profile updated successfully', 'success')
            return redirect(url_for('main.profile'))
        except Exception as e:
            flash('Error updating profile: {}'.format(str(e)), 'error')

    return render_template('edit_profile.html', form=form, profile=profile)

@main.route('/profile/delete/<int:id>', methods=['POST'])
@login_required
def delete_profile(id):
    profile = Profile.query.get_or_404(id)
    db.session.delete(profile)
    db.session.commit()
    flash('Profile deleted successfully', 'success')
    return redirect(url_for('main.profile'))

@main.route('/author', methods=['GET', 'POST'])
@login_required
def author():
    username = current_user.username
    return render_template('author.html', username=username)

@main.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    username = current_user.username
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
    return render_template('book.html', images=images,username=username)

@main.route('/dashboard')
@login_required
def dashboard():
    username = current_user.username
    return render_template('dashboard.html', username=username)

    
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt','png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
