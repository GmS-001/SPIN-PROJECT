from flask import Blueprint, render_template, redirect, request, url_for, flash
from ...models import *
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import time

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/images/uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/signup_i', methods=['GET', 'POST'])
def signup_i():
        if request.method=="POST":
            name = request.form.get('name')
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            phone_number = request.form.get('phone_number')
            dob = request.form.get('dob')
            niche = request.form.get('niche')
            gender = request.form.get('gender')
            dob = datetime.strptime(dob, '%Y-%m-%d').date()
            
            picture = request.files['picture']
            picture_filename = None
            if picture and picture.filename != '':
              filename = secure_filename(picture.filename)
              picture_filename = f"{username}_{int(time.time())}_{filename}"
              picture_path = os.path.join(UPLOAD_FOLDER, picture_filename)
              picture.save(picture_path)
        

            useri=Influencer.query.filter_by(username=username).first()
            users=Sponsor.query.filter_by(username=username).first()
            mail = Influencer.query.filter_by(email=email).first()
            phone = Influencer.query.filter_by(phone_number=phone_number).first()
            if useri :
                  flash(f"Username {username} is currently taken!")
                  influencers = Influencer.query.all()
                  return redirect(url_for('user.display_influencers', influencers=influencers))
            if users :
                  flash(f"Username {username} is currently taken!")
                  sponsors = Sponsor.query.all()
                  return redirect(url_for('user.display_sponsors', sponsors=sponsors))
            if phone :
                  print('phone number taken')
                  flash(f"phone number {phone_number} is currently taken!")
                  influencers = Influencer.query.all()
                  return redirect(url_for('user.display_influencers', influencers=influencers))
            if mail :
                  print('mail taken')
                  flash(f"mail {email} is currently taken!")
                  influencers = Influencer.query.all()
                  return redirect(url_for('user.display_influencers', influencers=influencers))
            else :
                  new_user = Influencer(name = name,username = username, picture = picture_filename ,email = email, password = password,phone_number = phone_number, dob = dob, niche = niche, gender = gender)
                  db.session.add(new_user)
                  db.session.commit() 
                  flash(f"Successfully registered as {username} !")
                  return redirect(url_for("profiles.influencer_dashboard",username = username))
        return render_template('signup_i.html', title='Influencers Sign Up')

@auth_bp.route('/signup_s', methods=['GET', 'POST'])
def signup_s():
        if request.method=="POST":
            username = request.form.get('username')
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            phone_number = request.form.get('phone_number')
            industry = request.form.get('industry')

            picture = request.files['picture']
            picture_filename = None
            if picture and picture.filename != '':
              filename = secure_filename(picture.filename)
              picture_filename = f"{username}_{int(time.time())}_{filename}"
              picture_path = os.path.join(UPLOAD_FOLDER, picture_filename)
              picture.save(picture_path)

            useri=Influencer.query.filter_by(username=username).first()
            users=Sponsor.query.filter_by(username=username).first()
            mail = Sponsor.query.filter_by(email=email).first()
            phone = Sponsor.query.filter_by(phone_number=phone_number).first()
            if useri :
                  flash(f"Username {username} is currently taken!")
                  influencers = Influencer.query.all()
                  return redirect(url_for('user.display_influencers', influencers=influencers))
            if users :
                  flash(f"Username {username} is currently taken!")
                  sponsors = Sponsor.query.all()
                  return redirect(url_for('user.display_sponsors', sponsors=sponsors))
            if phone :
                  print('phone number taken')
                  flash(f"phone number {phone_number} is currently taken!")
                  sponsors = Sponsor.query.all()
                  return redirect(url_for('user.display_sponsors', sponsors=sponsors))
            if mail :
                  print('mail taken')
                  flash(f"mail {email} is currently taken!")
                  sponsors = Sponsor.query.all()
                  return redirect(url_for('user.display_sponsors', sponsors=sponsors))
            else :
                  new_user = Sponsor(name = name,username = username , picture = picture_filename ,email = email,industry = industry, password = password,phone_number = phone_number)
                  db.session.add(new_user)
                  db.session.commit() 
                  flash(f"Successfully Registered {name}!")
                  return redirect(url_for("profiles.sponsor_dashboard",username = username))
        return render_template('signup_s.html')