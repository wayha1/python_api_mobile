from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import * 
from app.extensions import db
from cloudinary.uploader import upload
from app.views.auth.form import CategoryForm, ProfileForm,AuthorForm

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

                flash('Profile created/updated successfully', 'success')
                return redirect(url_for('main.profile'))
            else:
                flash('Invalid profile image file extension', 'error')
        except Exception as e:
            flash('Error creating/updating profile: {}'.format(str(e)), 'error')

    profiles = Profile.query.all()

    # Handle edit operation
    if request.method == 'POST':
        if 'edit_profile' in request.form:
            profile_id = request.form.get('profile_id')
            new_username = request.form.get('new_username')
            new_email = request.form.get('new_email')
            new_gender = request.form.get('new_gender')
            new_role = request.form.get('new_role')
            new_profile_image = request.files.get('new_profile_image')

            if new_profile_image and allowed_file(new_profile_image.filename):
                cloudinary_response = upload(new_profile_image)
                new_cloudinary_url = cloudinary_response['secure_url']

                profile = Profile.query.get(profile_id)
                if profile:
                    profile.username = new_username
                    profile.email = new_email
                    profile.gender = new_gender
                    profile.role = new_role
                    profile.profile_image = new_cloudinary_url
                    db.session.commit()
                    flash('Profile updated successfully', 'success')
                    return redirect(url_for('main.profile'))
            else:
                flash('Invalid profile image file extension', 'error')

    return render_template('profile.html', form=form, profiles=profiles, username=username)

@main.route('/profile/delete/<int:id>', methods=['POST'])
@login_required
def delete_profile():
    profile = Profile.query.get_or_404(id)
    db.session.delete(profile)
    db.session.commit()
    flash('Profile deleted successfully', 'success')
    return redirect(url_for('main.profile'))


@main.route('/author', methods=['GET', 'POST'])
@login_required
def author():
    username= current_user.username
    form = AuthorForm()
    if form.validate_on_submit():
        author_name = form.author_name.data
        author_decs = form.author_decs.data
        gender = form.gender.data
        author_image = request.files['author_image']  # Access uploaded file
        
        # Upload image to Cloudinary
        cloudinary_response = upload(author_image)
        author_image_url = cloudinary_response['secure_url']

        new_author = Author(author_name=author_name, author_decs=author_decs, gender=gender, author_image=author_image_url)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully', 'success')
        return redirect(url_for('main.author'))
    
    authors = Author.query.all()
    return render_template('author.html', authors=authors, form=form, username=username)

@main.route('/author/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_author(id):
    author = Author.query.get_or_404(id)
    form = AuthorForm(obj=author)
    if form.validate_on_submit():
        form.populate_obj(author)
        db.session.commit()
        flash('Author updated successfully', 'success')
        return redirect(url_for('main.author'))
    return render_template('edit_author.html', form=form, author=author)

@main.route('/author/delete/<int:id>', methods=['POST'])
@login_required
def delete_author(id):
    author = Author.query.get_or_404(id)
    db.session.delete(author)
    db.session.commit()
    flash('Author deleted successfully', 'success')
    return redirect(url_for('main.author'))

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
