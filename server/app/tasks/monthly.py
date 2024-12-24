# HomeMate/server/app/tasks/monthly.py

from .celery import celery
from .template import send_email_with_doc
from flask import render_template, current_app
from ..custom import IndianZone
import weasyprint
from datetime import datetime

@celery.task
def monthly_report_customer():
    from ..models import Customer
    customers = Customer.query.all()
    subject = 'HomeMate: Monthly Report For Your Account'
    with current_app.app_context():
        now = IndianZone()
        month, year = now.month, now.year
        previous_month = month - 1 if month > 1 else 12
        previous_year = year if month > 1 else year - 1
        subject = 'HomeMate: Monthly Report For Your Account'
        for customer in customers:
            service_requests = [
                request for request in customer.service_requests
                if request.updated_at.month == previous_month and request.updated_at.year == previous_year
            ]
            if len(service_requests) > 0:
                previous_month = datetime(previous_year, previous_month, 1).strftime('%B')
                report = render_template('monthly_report.html', service_requests=service_requests, customer=customer, month=previous_month, year=previous_year)
                pdf = weasyprint.HTML(string=report, base_url=f"{current_app.config['BACKEND_URL']}").write_pdf()
                body = render_template('monthly.html', name=customer.name)
                send_email_with_doc(customer.user.email, subject, body, pdf)


