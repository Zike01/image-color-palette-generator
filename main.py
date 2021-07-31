from flask import Flask, render_template, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from forms import ImageForm, EditForm
from palette_generator import PaletteGenerator
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
Bootstrap(app)
Base = declarative_base()

# CONFIGURE DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL_1', 'sqlite:///images.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# # IMAGE DB TABLE
class Image(db.Model, Base):
    __tablename__ = 'image'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    
    # Establish a bidirectional one-to-many relationship 
    # between each image and colors
    colors = relationship('Colors', back_populates='image')
     
    
# # COLORS DB TABLE
class Colors(db.Model, Base):
    __tablename__ = 'colors'
    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.Integer, ForeignKey('image.id'))
    image = relationship('Image', back_populates='colors')
    rgb_color = db.Column(db.String(100), nullable=False)


db.create_all()


@app.route("/")
def home():
    return render_template("index.html", images=Image.query.all(), colors=Colors.query.all())


# # ADD IMAGE
@app.route("/add", methods=["GET", "POST"])
def add_image():
    form = ImageForm()
    if form.validate_on_submit():
        new_image = Image(name=form.name.data,
                          img_url=form.img_url.data)
        db.session.add(new_image)
        db.session.commit()
        
        # Use the PaletteGenerator class to save and grab the color palette of the new image
        generator = PaletteGenerator(image_name=new_image.name, 
                                     image_url=new_image.img_url, 
                                     num_colors=form.num_colors.data)
        color_palette = generator.generate_palette()
        
        for color in color_palette:
            new_color = Colors(image_id = new_image.id,
                                rgb_color=color)
            db.session.add(new_color)
            db.session.commit()
  
        return redirect(url_for("home"))
        
    return render_template("add.html", form=form)


# # EDIT IMAGE
@app.route("/edit", methods=["GET", "POST"])
def edit_image():
    id = request.args.get('id')
    image_to_edit = Image.query.get(id)
    num_colors = len(Colors.query.filter_by(image_id=id).all())
    
    edit_form = EditForm(name=image_to_edit.name,
                          img_url=image_to_edit.img_url,
                          num_colors=num_colors)
    
    if edit_form.validate_on_submit():
        if edit_form.num_colors.data != num_colors or edit_form.img_url.data != image_to_edit.img_url:
            # Generate a new color palette
            generator = PaletteGenerator(image_name=image_to_edit.name, 
                                        image_url=edit_form.img_url.data, 
                                        num_colors=edit_form.num_colors.data)
            color_palette = generator.generate_palette()
            
            # Delete existing color palette
            Colors.query.filter_by(image_id=id).delete()
            
            # Add new color palette to image
            for color in color_palette:
                new_color = Colors(image_id = image_to_edit.id,
                                    rgb_color=color)
                db.session.add(new_color)
                
        # Update image name and img_url
        image_to_edit.name = edit_form.name.data
        image_to_edit.img_url = edit_form.img_url.data
        db.session.commit()
        return redirect(url_for('home'))
    
    return render_template("edit.html", form=edit_form)


# # DELETE IMAGE
@app.route("/delete")
def delete_image():
    id = request.args.get('id')
    image_to_delete = Image.query.get(id)
    Colors.query.filter_by(image_id=id).delete()
    
    db.session.delete(image_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__=="__main__":
    app.run(debug=True)
