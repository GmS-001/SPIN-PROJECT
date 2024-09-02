from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.models import *
from datetime import datetime

user_bp = Blueprint('user', __name__, template_folder='templates')


@user_bp.route('/')
@user_bp.route('/home')
def home():
    return render_template('home.html')


@user_bp.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    completed_campaign = Campaign.query.filter(Campaign.posts == 0,Campaign.influencer_id != 0).count()
    sponsor_number = Sponsor.query.count()
    influencer_number = Influencer.query.count()
    adRequest_number = AdRequest.query.count()
    flaggd_users = Sponsor.query.filter(Sponsor.is_flagged == True).count() + Influencer.query.filter(Influencer.is_flagged == True).count()
    live_campaign = Campaign.query.filter(Campaign.posts != 0,Campaign.influencer_id != 0).count()
    return render_template('admin_dashboard.html',flaggd_users = flaggd_users,completed_campaign = completed_campaign,adRequest_number = adRequest_number, influencer_number = influencer_number,live_campaign = live_campaign,sponsor_number = sponsor_number)

@user_bp.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method=="POST":
        username = request.form.get('username') 
        password = request.form.get('password')
        if username == 'admin' and password == '0000' :
            return redirect(url_for('user.admin_dashboard')) 
        else :
            user_type = request.form.get('user_type')
            if user_type == 'influencer':
               check_influencer = Influencer.query.filter_by(username = username).first()
               if check_influencer :
                   if check_influencer.password == password :
                       return redirect(url_for('profiles.influencer_dashboard',username = username))
                   else :
                       flash('Incorrect Password.Please check again!')
               else :
                   flash("Username does not exist. Try Sign in..")
            if user_type == 'sponsor':
               check_sponsor = Sponsor.query.filter_by(username = username).first()
               if check_sponsor :
                   if check_sponsor.password == password:
                      return redirect(url_for('profiles.sponsor_dashboard',username = username))
                   else :
                      flash('Incorrect Password.Please check again!')
               else :
                    flash("Username does not exist. Try Sign in..")
    return render_template('login.html',title = 'Login Page')


@user_bp.route('/display_influencers', methods=['GET', 'POST'])
def display_influencers():
    influencers = Influencer.query.all()
    return render_template('display_influencers.html',influencers = influencers)

@user_bp.route('/display_sponsors', methods=['GET', 'POST'])
def display_sponsors():
    sponsors = Sponsor.query.all()
    return render_template('display_sponsors.html',sponsors = sponsors)


@user_bp.route('/display_database', methods=['GET', 'POST'])
def display_database():
    sponsors = Sponsor.query.all()
    influencers = Influencer.query.all()
    campaigns = Campaign.query.all()
    add_reqs = AdRequest.query.all()
    return render_template('display_database.html',sponsors = sponsors,
                           influencers = influencers,
                           campaigns = campaigns,
                           add_reqs = add_reqs)

@user_bp.route('/flag_user', methods=['POST'])
def flag_user():
    username = request.form.get('username')
    action = request.form.get('action')

    influencer = Influencer.query.filter_by(username=username).first()
    sponsor = Sponsor.query.filter_by(username=username).first()
    if influencer:
        if action == 'flag':
            influencer.is_flagged = True
            flash(f'{username} flagged !')
        elif action == 'unflag':
            influencer.is_flagged = False
            flash(f'{username} unflagged !')
        db.session.commit()
    elif sponsor:
        if action == 'flag':
            sponsor.is_flagged = True
            flash(f'{username} flagged !')
        elif action == 'unflag':
            sponsor.is_flagged = False
            flash(f'{username} unflagged !')
        db.session.commit()
    else : 
        flash("This username does not exist.")
    
    return redirect(request.referrer)



@user_bp.route('/live_campaign', methods=['GET', 'POST'])
def live_campaign():
    live_campaign = Campaign.query.filter(Campaign.posts > 0)
    return render_template('live_campaign.html',live_campaign = live_campaign)


@user_bp.route('/display_adrequest', methods=['GET', 'POST'])
def display_adrequest():
    add_reqs = AdRequest.query.all()
    return render_template('display_adrequest.html',add_reqs = add_reqs)



@user_bp.route('/completed_campaigns', methods=['GET', 'POST'])
def completed_campaigns():
    completed_campaigns = Campaign.query.filter(Campaign.posts == 0,Campaign.influencer_id != 0).all()
    return render_template('completed_campaigns.html',completed_campaigns = completed_campaigns)

@user_bp.route('/flaggd_users', methods=['GET', 'POST'])
def flaggd_users():
    flagged_sponsors = Sponsor.query.filter(Sponsor.is_flagged == True).all()
    flagged_influencers = Influencer.query.filter(Influencer.is_flagged == True).all()
    return render_template('flaggd_users.html',flagged_sponsors = flagged_sponsors,flagged_influencers = flagged_influencers)