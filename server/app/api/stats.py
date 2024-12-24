# HomeMate/server/app/api/stats.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User, Customer, ServiceProfessional, ServiceRequest, Service
from ..custom import IndianZone
from sqlalchemy import extract, func

class StatsApi(Resource):
    @jwt_required()
    def get(self):
        page = request.args.get('page')
        if page:
            try:
                current_user = get_jwt_identity()
                user = User.query.filter_by(username=current_user).first()
                if user:
                    role = user.role
                    if role == 'Admin':
                        return self.admin_stats(page)
                    elif role == 'Customer':
                        return self.other_user_stats(page, user.customer)
                    elif role == 'Professional':
                        return self.other_user_stats(page, user.service_professional)
                    else:
                        return {'message': 'Invalid user identity!'}, 400
                else:
                    return {'message': 'User not found!'}, 400
            except Exception as e:
                return f"{e}"
        else:
            return {'message': 'Illegal request!'}, 400
        

    def admin_stats(self, page):
        if page == 'home':
            now = IndianZone()
            current_month, current_year = now.month, now.year
            previous_month = current_month - 1 if current_month > 1 else 12
            previous_year = current_year if current_month > 1 else current_year - 1

            # Total counts
            total_customers = Customer.query.count()
            total_professionals = ServiceProfessional.query.count()
            total_requests = ServiceRequest.query.count()
            

            # Progress calculations for customers
            this_month_customers = Customer.query.join(Customer.user).filter(
                extract('month', User.created_at) == current_month,
                extract('year', User.created_at) == current_year
            ).count()

            previous_month_customers = Customer.query.join(Customer.user).filter(
                extract('month', User.created_at) == previous_month,
                extract('year', User.created_at) == previous_year
            ).count()

            customer_progress = (
                (this_month_customers - previous_month_customers) /
                max(1, this_month_customers)
            ) * 100

            # Progress calculations for professionals
            this_month_professionals = ServiceProfessional.query.join(ServiceProfessional.user).filter(
                extract('month', User.created_at) == current_month,
                extract('year', User.created_at) == current_year
            ).count()

            previous_month_professionals = ServiceProfessional.query.join(ServiceProfessional.user).filter(
                extract('month', User.created_at) == previous_month,
                extract('year', User.created_at) == previous_year
            ).count()

            professional_progress = (
                (this_month_professionals - previous_month_professionals) /
                max(1, this_month_professionals)
            ) * 100

            # Progress calculations for requests
            this_month_requests = ServiceRequest.query.filter(
                extract('month', ServiceRequest.request_date) == current_month,
                extract('year', ServiceRequest.request_date) == current_year
            ).count()

            previous_month_requests = ServiceRequest.query.filter(
                extract('month', ServiceRequest.request_date) == previous_month,
                extract('year', ServiceRequest.request_date) == previous_year
            ).count()

            request_progress = (
                (this_month_requests - previous_month_requests) /
                max(1, this_month_requests)
            ) * 100

            # Revenue progress
            this_month_completed_requests = ServiceRequest.query.filter(
                extract('month', ServiceRequest.completion_date) == current_month,
                extract('year', ServiceRequest.completion_date) == current_year,
                ServiceRequest.status == 'Completed'
            ).all()

            previous_month_completed_requests = ServiceRequest.query.filter(
                extract('month', ServiceRequest.completion_date) == previous_month,
                extract('year', ServiceRequest.completion_date) == previous_year,
                ServiceRequest.status == 'Completed'
            ).all()

            def calculate_revenue(requests):
                total_revenue = 0
                for request in requests:
                    fee = request.service_professional.fee
                    time_required = request.service.time_required
                    time_unit = time_required.split(' ')[1]
                    time_value = float(time_required.split(' ')[0])
                    
                    if time_unit == 'hours':
                        total_revenue += float(fee) * time_value
                    elif time_unit == 'minutes':
                        total_revenue += float(fee) * (time_value / 60)
                return total_revenue

            this_month_revenue = calculate_revenue(this_month_completed_requests)
            previous_month_revenue = calculate_revenue(previous_month_completed_requests)

            if this_month_revenue > 0:
                revenue_progress = (
                    (this_month_revenue - previous_month_revenue) /
                    max(1, this_month_revenue)
                ) * 100
            else:
                revenue_progress = 0

            # Count Distributed Requests
            completed_requests = ServiceRequest.query.filter(ServiceRequest.status == 'Completed').count()
            pending_requests = ServiceRequest.query.filter(ServiceRequest.status.in_(['In Progress', 'Requested'])).count()
            rejected_requests = ServiceRequest.query.filter(ServiceRequest.status.in_(['Cancelled', 'Rejected'])).count()


            # Compile stats
            stats = {
                'customers': total_customers,
                'professionals': total_professionals,
                'requests': total_requests,
                'revenue': this_month_revenue,
                'customer_progress': round(customer_progress, 2),
                'professional_progress': round(professional_progress, 2),
                'request_progress': round(request_progress, 2),
                'revenue_progress': round(revenue_progress, 2),
                'completed': completed_requests,
                'pending': pending_requests,
                'rejected': rejected_requests
            }

            return stats, 200
        
        elif page == 'services':
            requests = ServiceRequest.query.count()
            completed = ServiceRequest.query.filter(ServiceRequest.status == 'Completed').count()
            pending = ServiceRequest.query.filter(ServiceRequest.status.in_(['Requested', 'In Progress'])).count()
            failed = ServiceRequest.query.filter(ServiceRequest.status.in_(['Rejected', 'Cancelled'])).count()

            def calculate_progress(types):
                now = IndianZone()
                current_month, current_year = now.month, now.year
                previous_month = current_month - 1 if current_month > 1 else 12
                previous_year = current_year if current_month > 1 else current_year - 1

                completed_this_month = ServiceRequest.query.filter(
                extract('month', ServiceRequest.request_date) == current_month,
                extract('year', ServiceRequest.request_date) == current_year,
                ServiceRequest.status.in_(types)).count()

                completed_previous_month = ServiceRequest.query.filter(
                extract('month', ServiceRequest.request_date) == previous_month,
                extract('year', ServiceRequest.request_date) == previous_year,
                ServiceRequest.status.in_(types)).count()

                return ((completed_this_month - completed_previous_month) / max(1, completed_this_month)) * 100
            
            requests_progress = calculate_progress(['Completed', 'Requested', 'In Progress', 'Rejected', 'Cancelled'])
            completed_progress = calculate_progress(['Completed'])
            pending_progress = calculate_progress(['Requested', 'In Progress'])
            failed_progress = calculate_progress(['Rejected', 'Cancelled'])

            stats = {
                'requests': requests,
                'requests_progress': round(requests_progress, 2),
                'completed': completed,
                'pending': pending,
                'failed': failed,
                'completed_progress': round(completed_progress, 2),
                'pending_progress': round(pending_progress, 2),
                'failed_progress': round(failed_progress, 2),
            }

            return stats, 200
        
    def other_user_stats(self, page, user):
        if page == 'services':
            requests = user.service_requests
            total = len(requests)
            completed = sum(1 for req in requests if req.status == 'Completed')
            pending = sum(1 for req in requests if req.status in ['Requested', 'In Progress'])
            failed = sum(1 for req in requests if req.status in ['Rejected', 'Cancelled'])


            def calculate_progress(types):
                now = IndianZone()
                current_month, current_year = now.month, now.year
                previous_month = current_month - 1 if current_month > 1 else 12
                previous_year = current_year if current_month > 1 else current_year - 1

                def is_in_month_year(request, month, year):
                    return request.request_date.month == month and request.request_date.year == year
                
                completed_this_month = sum(1 for req in requests if is_in_month_year(req, current_month, current_year) and req.status in types)
                completed_previous_month = sum(1 for req in requests if is_in_month_year(req, previous_month, previous_year) and req.status in types)

                return ((completed_this_month - completed_previous_month) / max(1, completed_this_month)) * 100
            
            total_progress = calculate_progress(['Completed', 'Requested', 'In Progress', 'Rejected', 'Cancelled'])
            completed_progress = calculate_progress(['Completed'])
            pending_progress = calculate_progress(['Requested', 'In Progress'])
            failed_progress = calculate_progress(['Rejected', 'Cancelled'])

            stats = {
                'total': total,
                'total_progress': round(total_progress, 2),
                'completed': completed,
                'pending': pending,
                'failed': failed,
                'completed_progress': round(completed_progress, 2),
                'pending_progress': round(pending_progress, 2),
                'failed_progress': round(failed_progress, 2),
            }

            return stats, 200
        
        elif page == 'home':
            now = IndianZone()
            current_month, current_year = now.month, now.year
            previous_month = current_month - 1 if current_month > 1 else 12
            previous_year = current_year if current_month > 1 else current_year - 1
            
            # Income
            requests = user.service_requests
            completed_requests = sum(1 for req in requests if req.status in ['Completed'])
            pending_requests = sum(1 for req in requests if req.status in ['Requested', 'In Progress'])
            failed_requests = sum(1 for req in requests if req.status in ['Rejected', 'Cancelled'])

            service_type = user.service_type
            time_required = Service.query.filter_by(name=service_type).first().time_required
            time_unit = time_required.split(' ')[1]
            time_value = float(time_required.split(' ')[0])
            
            if time_unit == 'hours':
                total_income = float(user.fee) * time_value * completed_requests
            elif time_unit == 'minutes':
                total_income = float(user.fee) * (time_value / 60) * completed_requests

            def is_in_month_year(request, month, year):
                return request.request_date.month == month and request.request_date.year == year

            completed_this_month = sum(1 for req in requests if is_in_month_year(req, current_month, current_year) and req.status in ['Completed'])
            completed_previous_month = sum(1 for req in requests if is_in_month_year(req, previous_month, previous_year) and req.status in ['Completed'])

            income_progress = ((completed_this_month - completed_previous_month) / max(1, completed_this_month)) * 100

            # Unique Customer
            unique_customers = len(set(req.customer_id for req in requests if req.status == 'Completed'))
            unique_customers_this_month = len(set(req.customer_id for req in requests if is_in_month_year(req, current_month, current_year) and req.status == 'Completed'))
            unique_customers_previous_month = len(set(req.customer_id for req in requests if is_in_month_year(req, previous_month, previous_year) and req.status == 'Completed'))

            customer_progress = ((unique_customers_this_month - unique_customers_previous_month) / max(1, unique_customers_this_month)) * 100

            # Reviews
            total_reviews = sum(1 for req in requests if req.status == 'Completed' and len(req.review) != 0)
            total_reviews_this_month = sum(1 for req in requests if is_in_month_year(req, current_month, current_year) and req.status == 'Completed' and len(req.review) != 0)
            total_reviews_previous_month = sum(1 for req in requests if is_in_month_year(req, previous_month, previous_year) and req.status == 'Completed' and len(req.review) != 0)

            review_progress = ((total_reviews_this_month - total_reviews_previous_month) / max(1, total_reviews_this_month)) * 100

            # Total requests 
            total_requests = len(user.service_requests)
            total_requests_this_month = len([req for req in requests if is_in_month_year(req, current_month, current_year)])
            total_requests_previous_month = len([req for req in requests if is_in_month_year(req, previous_month, previous_year)])

            requests_progress = ((total_requests_this_month - total_requests_previous_month) / max(1, total_requests_this_month)) * 100

            stats = {
                'earning': total_income,
                'earning_progress': round(income_progress, 2),
                'customer': unique_customers,
                'customer_progress': round(customer_progress, 2),
                'review': total_reviews,
                'review_progress': round(review_progress, 2),
                'request': total_requests,
                'request_progress': round(requests_progress, 2),
                'completed': completed_requests,
                'pending': pending_requests,
                'failed': failed_requests
            }

            return stats, 200











        
    
            