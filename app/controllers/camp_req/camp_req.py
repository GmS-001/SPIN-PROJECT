from flask import Blueprint, render_template, redirect, request, url_for, flash
from ...models import *
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import time

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/images/uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


camp_req= Blueprint('camp_req', __name__, template_folder='templates')

@camp_req.route('/campaign', methods=['GET', 'POST'])
def campaign():
     campaign_id = request.args.get('campaign_id')
     campaign = Campaign.query.get(campaign_id)
     sponsor = Sponsor.query.get(campaign.sponsor_id)
     sponsor_name = sponsor.name
     sponsor_username = sponsor.username
     sponsor_industry = sponsor.industry
     influencer = Influencer.query.filter_by(id = campaign.influencer_id).first()
     if not influencer :
          influencer_data = None
     else :
          influencer_data = {}
          today = datetime.today().date()
          age = today.year - influencer.dob.year - ((today.month, today.day) < (influencer.dob.month, influencer.dob.day))
          influencer_data['name'] = influencer.name
          influencer_data['username'] = influencer.username
          influencer_data['age'] = age
          influencer_data['niche'] = influencer.niche
          influencer_data['picture'] = influencer.picture
          
     today = datetime.today().date() 
     days_left = (campaign.end_date - today).days       
     camp_name = campaign.name
     st_date = campaign.start_date
     end_date = campaign.end_date
     goal = campaign.goal
     budget = campaign.budget
     picture = campaign.picture
     description = campaign.description
     visibility = campaign.visibility
     posts = campaign.posts
     return render_template('campaign.html',camp_name = camp_name,
                            st_date = st_date,
                            end_date = end_date,
                            goal = goal,
                            picture = picture,
                            posts = posts,
                            budget = budget,
                            description = description,
                            visibility = visibility,
                            influencer_data = influencer_data,
                            sponsor_name = sponsor_name,
                            sponsor_username = sponsor_username,
                            sponsor_industry = sponsor_industry,
                            days_left = days_left)

@camp_req.route('/campaign_list', methods=['GET', 'POST'])
def campaign_list():
     username = request.args.get('username')
     campaigns = Campaign.query.filter_by(influencer_id = 0,visibility = 'Public').all()
     return render_template('campaign_list.html',campaigns = campaigns, username = username)

@camp_req.route('/add_campaign', methods=['GET', 'POST'])
def add_campaign():
     username = request.args.get('username')
     if request.method == 'POST':
          username = request.form.get('username')
          sponsor = Sponsor.query.filter_by(username = username).first()
          camp_name = request.form.get('camp_name')
          description = request.form.get('description')
          start_date = request.form.get('start_date')
          end_date = request.form.get('end_date')
          goal = request.form.get('goal')
          budget = request.form.get('budget')
          visibility = request.form.get('visibility')
          
          picture = request.files['picture']
          picture_filename = None
          if picture and picture.filename != '':
              filename = secure_filename(picture.filename)
              picture_filename = f"{username}_{int(time.time())}_{filename}"
              picture_path = os.path.join(UPLOAD_FOLDER, picture_filename)
              picture.save(picture_path)

          start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
          end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
     
          new_campaign = Campaign(name = camp_name, picture = picture_filename, sponsor_id = sponsor.id,description = description,visibility= visibility,budget= budget,start_date = start_date,end_date = end_date,goal = goal)
          db.session.add(new_campaign)
          db.session.commit()
          flash('Your Campaign is added...')
          return redirect(url_for('profiles.sponsor_dashboard', username=username))
     return render_template('add_campaign.html', username=username)


@camp_req.route('/add_request', methods=['GET', 'POST'])
def add_request():
    username = request.args.get('username')
    campaign_name = request.args.get('campaign_name')
    influencer_name = request.args.get('influencer_name')
    if request.method == 'POST':
        username = request.form.get('username')
        campaign_name = request.form.get('campaign_name')
        influencer_name = request.form.get('influencer_name')
        message = request.form.get('message')
        posts = request.form.get('posts')
        payment = request.form.get('payment')
        influencer = Influencer.query.filter_by(username=username).first()
        if not influencer :
             print('yes sponsor is there!')
             sponsor = Sponsor.query.filter_by(username = username).first()
             campaign = Campaign.query.filter_by(name=campaign_name).first()
             influencer = Influencer.query.filter_by(username=influencer_name).first()
             new_req = AdRequest(message = message, posts = posts,initiator = username,initiated_for = influencer.username, payment = payment, influencer_id = influencer.id, campaign_id=campaign.id, sponsor_id = sponsor.id)
             db.session.add(new_req)
             db.session.commit()
             flash('Sit back & Relax . Your Request is sent!')
             return redirect(url_for('profiles.sponsor_dashboard', username=username))
        
        else :
             print('yes influencer is there!')
             campaign = Campaign.query.filter_by(name=campaign_name).first()
             sponsor = Sponsor.query.filter_by(id = campaign.sponsor_id).first()
             new_req = AdRequest(message = message, posts = posts,initiator = username,initiated_for = sponsor.username, payment = payment, influencer_id = influencer.id, campaign_id=campaign.id, sponsor_id = campaign.sponsor_id)
             db.session.add(new_req)
             db.session.commit()
             return redirect(url_for('profiles.influencer_dashboard', username=username))
        
    return render_template('add_request.html', username=username, campaign_name = campaign_name,influencer_name = influencer_name)


@camp_req.route('/prev_campaign', methods=['GET', 'POST'])
def prev_campaign():
     username = request.args.get('username')
     sponsor = Sponsor.query.filter_by(username = username).first()
     influencer = Influencer.query.filter_by(username = username).first()
     if sponsor :
          campaigns = Campaign.query.filter_by(sponsor_id = sponsor.id, posts = 0).filter(Campaign.influencer_id != 0).all()
          campaign_list = []
          for campaign in campaigns :
               data = {}
               influencer = Influencer.query.get(campaign.influencer_id)
               data['id'] = campaign.id
               data['name'] = campaign.name
               data['goal'] = campaign.goal
               data['visibility'] = campaign.visibility
               data['description'] = campaign.description
               data['budget'] = campaign.budget
               data['partner'] = influencer.name
               data['picture'] = campaign.picture
               data['total_posts'] = campaign.total_posts
               campaign_list.append(data)

          return render_template('prev_campaign.html',campaign_list = campaign_list)
     else :
          campaigns = Campaign.query.filter_by(influencer_id = influencer.id, posts = 0).all()
          campaign_list = []
          for campaign in campaigns :
               data = {}
               sponsor = Sponsor.query.get(campaign.sponsor_id)
               data['id'] = campaign.id
               data['name'] = campaign.name
               data['goal'] = campaign.goal
               data['description'] = campaign.description
               data['budget'] = campaign.budget
               data['partner'] = sponsor.name
               data['picture'] = campaign.picture
               data['total_posts'] = campaign.total_posts
               campaign_list.append(data)

          return render_template('prev_campaign.html',campaign_list = campaign_list)

@camp_req.route('/sponsor_campaign_list', methods=['GET', 'POST'])
def sponsor_campaign_list():
     username = request.args.get('username')
     sponsor = Sponsor.query.filter_by(username = username).first()
     campaigns = Campaign.query.filter_by(sponsor_id=sponsor.id, influencer_id=0).all()
     return render_template('sponsor_campaign_list.html',username = username,campaigns = campaigns)


@camp_req.route('/influencers_list', methods=['GET', 'POST'])
def influencers_list():
     username = request.args.get('username')
     campaign_name = request.args.get('campaign_name')
     influencers = Influencer.query.all()
     influencer_data = []
     for influencer in influencers:
        today = datetime.today().date()
        age = today.year - influencer.dob.year - ((today.month, today.day) < (influencer.dob.month, influencer.dob.day))
        influencer_data.append({
            'name': influencer.name,
            'age': age,
            'niche': influencer.niche,
            'username': influencer.username,
            'picture': influencer.picture,
            'username': influencer.username
         })
     
     return render_template('influencers_list.html',username = username,campaign_name = campaign_name,influencer_data = influencer_data)