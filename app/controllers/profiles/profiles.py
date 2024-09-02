from flask import Blueprint, render_template, redirect, request, url_for, flash
from ...models import *
from datetime import datetime

prof_bp = Blueprint('profiles', __name__, template_folder='templates')

@prof_bp.route('/influencer_dashboard', methods=['GET', 'POST'])
def influencer_dashboard(): 
    username = request.args.get('username')
    influencer = Influencer.query.filter_by(username=username).first()

    campaign = Campaign.query.filter_by(influencer_id=influencer.id).filter(Campaign.posts > 0).all()
    campaigns = []
    for camp in campaign:
        sponsor = Sponsor.query.filter_by(id=camp.sponsor_id).first()
        if sponsor:
            combined_entry = {
                'id' : camp.id,
                'description': camp.description,
                'goal': camp.goal,
                'camp_name': camp.name,
                'name': sponsor.name,
                'end_date': camp.end_date,
                'budget' : camp.budget,
                'picture' : camp.picture,
                'posts' : int(camp.posts),
                'visibility' : camp.visibility
            }
            campaigns.append(combined_entry)

    ad_req = AdRequest.query.filter_by(initiated_for=username).all()
    ad_reqs = []
    for ad in ad_req:
        sponsor = Sponsor.query.filter_by(username=ad.initiator).first()
        campaign = Campaign.query.get(ad.campaign_id)
        if sponsor:
            combined_entry = {
                'id': ad.id, 
                'posts': ad.posts,
                'message': ad.message,
                'payment': ad.payment,
                'name': sponsor.name,
                'campaign_id': ad.campaign_id,
                'camp_name': campaign.name
            }
            ad_reqs.append(combined_entry)
            
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = 'Good Morning'
    elif 12 <= current_hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'
    return render_template('influencer_dashboard.html', 
                           greeting=greeting,
                           campaigns = campaigns,
                           ad_reqs = ad_reqs,
                           picture = influencer.picture,
                           username = influencer.username ,
                           is_flagged = influencer.is_flagged,
                           ongoing = influencer.ongoing_campaigns,
                           successful = influencer.successful_campaigns)
        

@prof_bp.route('/influencer_profile', methods=['GET', 'POST'])
def influencer_profile():
     username = request.args.get('username')
     influencer = Influencer.query.filter_by(username = username).first()
     data = {}
     data['username'] = influencer.username
     data['name'] = influencer.name
     data['gender'] = influencer.gender
     data['picture'] = influencer.picture
     data['niche'] = influencer.niche
     data['is_flagged'] = influencer.is_flagged
     data['ongoing_campaigns'] = influencer.ongoing_campaigns
     data['successful_campaigns'] = influencer.successful_campaigns
     today = datetime.today().date()
     data['age'] = today.year - influencer.dob.year - ((today.month, today.day) < (influencer.dob.month, influencer.dob.day))
     return render_template('influencer_profile.html',data = data)



@prof_bp.route('/sponsor_profile', methods=['GET', 'POST'])
def sponsor_profile():
     username = request.args.get('username')
     sponsor = Sponsor.query.filter_by(username = username).first()
     data = {}
     data['username'] = sponsor.username
     data['is_flagged'] = sponsor.is_flagged
     data['name'] = sponsor.name
     data['picture'] = sponsor.picture
     data['industry'] = sponsor.industry
     data['ongoing_campaigns'] = sponsor.ongoing_campaigns
     data['successful_campaigns'] = sponsor.successful_campaigns
     return render_template('sponsor_profile.html',data = data)


@prof_bp.route('/sponsor_dashboard', methods=['GET', 'POST'])
def sponsor_dashboard():
    username = request.args.get('username')
    sponsor = Sponsor.query.filter_by(username=username).first()
    campaign = Campaign.query.filter_by(sponsor_id = sponsor.id).filter(Campaign.posts>0).all()
    campaigns = []
    for camp in campaign:
        influencer = Influencer.query.filter_by(id=camp.influencer_id).first()
        if influencer:
            combined_entry = {
                'id' : camp.id,
                'description': camp.description,
                'goal': camp.goal,
                'camp_name': camp.name,
                'name': influencer.name,
                'end_date': camp.end_date,
                'picture' : camp.picture,
                'budget' : camp.budget,
                'posts' : int(camp.posts),
                'visibility' : camp.visibility
            }
            campaigns.append(combined_entry)

    ad_req = AdRequest.query.filter_by(initiated_for=username).all()
    ad_reqs = []
    for ad in ad_req:
        influencer = Influencer.query.filter_by(id = ad.influencer_id).first()
        campaign = Campaign.query.get(ad.campaign_id)
        if influencer:
            combined_entry = {
                'id': ad.id, 
                'posts': ad.posts,
                'message': ad.message,
                'payment': ad.payment,
                'name': influencer.name,
                'campaign_id': ad.campaign_id,
                'camp_name': campaign.name
            }
            ad_reqs.append(combined_entry)


    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = 'Good Morning'
    elif 12 <= current_hour < 18:
        greeting = 'Good Afternoon'
    else:
        greeting = 'Good Evening'

    return render_template('sponsor_dashboard.html',greeting=greeting,
                           username = sponsor.username ,
                           ongoing = sponsor.ongoing_campaigns,
                           successful = sponsor.successful_campaigns,
                           picture = sponsor.picture,
                           is_flagged = sponsor.is_flagged,
                           campaigns = campaigns,
                           ad_reqs = ad_reqs)    


@prof_bp.route('/accept_ad_request/<int:ad_id>', methods=['POST'])
def accept_ad_request(ad_id):
    ad_request = AdRequest.query.get(ad_id)
    campaign = Campaign.query.get(ad_request.campaign_id)
    if ad_request:
        influencer = Influencer.query.get(ad_request.influencer_id)
        sponsor = Sponsor.query.get(ad_request.sponsor_id)
        if influencer:
            campaign.influencer_id = ad_request.influencer_id
            campaign.posts = ad_request.posts
            campaign.total_posts = ad_request.posts
            influencer.ongoing_campaigns += 1
            sponsor.ongoing_campaigns += 1
            db.session.delete(ad_request)
            db.session.commit()
            flash('Ad request accepted and campaign started.', 'success')

    return redirect(request.referrer)


@prof_bp.route('/reject_ad_request/<int:ad_id>', methods=['POST'])
def reject_ad_request(ad_id):
    ad_request = AdRequest.query.get(ad_id)
    if ad_request:
        db.session.delete(ad_request)
        db.session.commit()
    return redirect(request.referrer)


@prof_bp.route('/decrease_posts/<int:campaign_id>')
def decrease_posts(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign.posts > 1:
        campaign.posts -= 1
        db.session.commit()
        flash(f'Well done! {campaign.posts} posts left. Keep Promoting...')
    else :
        influencer = Influencer.query.get(campaign.influencer_id)
        sponsor = Sponsor.query.get(campaign.sponsor_id)
        influencer.successful_campaigns += 1
        influencer.ongoing_campaigns -= 1
        sponsor.successful_campaigns += 1
        sponsor.ongoing_campaigns -= 1
        campaign.posts -= 1
        db.session.commit()
        flash(f'Congratulations on finishing campaign {campaign.name}...')
    return redirect(request.referrer)

@prof_bp.route('/delete_campaign/<int:campaign_id>', methods=['GET'])
def delete_campaign(campaign_id):
    campaign = Campaign.query.get(campaign_id)
    if campaign:
        flash(f'Campaign {campaign.name} deleted successfully')
        db.session.delete(campaign)
        db.session.commit()
       
    else:
        flash('Campaign not found', 'error')

    return redirect(request.referrer)