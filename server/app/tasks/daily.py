# HomeMate/server/app/tasks/daily.py

from .celery import celery
from .template import send_email
from flask import render_template, current_app
from sqlalchemy import or_

@celery.task
def daily_reminder_professionals():
    from ..models import ServiceRequest
    pending_requests = ServiceRequest.query.filter(or_(ServiceRequest.status == 'Requested', ServiceRequest.status == 'In Progress')).distinct(ServiceRequest.service_professional_id).all()
    subject = 'Daily Reminder: Pending Service Requests'
    with current_app.app_context():
        visit_url = f"{current_app.config['FRONTEND_URL']}/dashboard/service-requests"
        for request in pending_requests:
            body = render_template('daily.html', name=request.service_professional.name, visit_url=visit_url)
            send_email(request.service_professional.user.email, subject, body, is_html=True)

@celery.task
def daily_rating_update():
    from ..models import ServiceProfessional
    from .. import db
    professionals = ServiceProfessional.query.all()
    for pro in professionals:
        rating = 0
        count = 0
        service_requests = [request for request in pro.service_requests if request.status == 'Completed']
        for request in service_requests:
            if len(request.review) > 0:
                rating += request.review[0].rating
                count += 1
        if count != 0:
            final_rating = (rating / count)
            pro.rating = final_rating
            db.session.commit()


    