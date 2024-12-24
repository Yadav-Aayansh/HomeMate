# HomeMate/server/app/tasks/trigger.py

from .celery import celery
import csv
import io
from .template import send_email_with_csv
from flask import render_template

@celery.task
def export_to_csv():
    from ..models import ServiceRequest, User
    service_requests = ServiceRequest.query.filter_by(status='Completed').all()
    subject = 'HomeMate: Export of Completed Service Requests'
    output = io.StringIO()
    fieldnames = ['service_request_id','service_id','customer_id','service_professional_id','request_date','completion_date','status','remarks','priority','address','pincode',]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for request in service_requests:
        writer.writerow({
            'service_request_id': request.service_request_id,
            'service_id': request.service_id,
            'customer_id': request.customer_id,
            'service_professional_id': request.service_professional_id,
            'request_date': request.request_date.strftime('%Y-%m-%d %H:%M:%S'),
            'completion_date': request.completion_date.strftime('%Y-%m-%d %H:%M:%S') if request.completion_date else 'N/A',
            'status': request.status,
            'remarks': request.remarks or 'N/A',
            'priority': request.priority,
            'address': request.address,
            'pincode': request.pincode,
        })
    csv_content = output.getvalue()
    output.close()
    body = render_template('csv_export.html')
    admins = User.query.filter_by(role='Admin').all()
    for admin in admins:
        send_email_with_csv(admin.email, subject, body, csv_content)
    