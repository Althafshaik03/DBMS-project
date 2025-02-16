from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import sqlite3
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from . import forms, models
from insurance import models as CMODEL
from insurance import forms as CFORM

# PDF Report Generation
from django.http import HttpResponse
from django.template.loader import render_to_string
import sqlite3
from weasyprint import HTML

from django.shortcuts import render
from . import models
from django.http import JsonResponse
import random
from django.shortcuts import render
from django.http import JsonResponse

from insurance.models import Category,Policy,Claim  # Replace 'other_app' with the correct app name

def recommend_policy(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        category = data.get('category')
        premium = float(data.get('premium'))
        sum_assured = float(data.get('sum_assured'))
        tenure = int(data.get('tenure'))

        # Query policies based on input
        recommendations = Policy.objects.filter(
            category__icontains=category,
            premium__lte=premium,
            sum_assured__gte=sum_assured,
            tenure__gte=tenure
        )

        # Prepare recommendation message
        if recommendations.exists():
            message = "I recommend the following policies:\n"
            for policy in recommendations:
                message += f"- {policy.name} (Premium: {policy.premium}, Sum Assured: {policy.sum_assured}, Tenure: {policy.tenure} years)\n"
        else:
            message = "Sorry, I couldn't find a suitable policy for you based on your preferences."

        return JsonResponse({'recommendation': message})


    
from django.shortcuts import render
from django.http import JsonResponse
from insurance.models import Policy,Category,Claim
from django.views.decorators.csrf import csrf_exempt

# Chatbot view for handling user queries
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from insurance.models import Policy  # Ensure you import your models

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from insurance.models import Policy  # Ensure you import your models

from django.shortcuts import render
from django.http import JsonResponse
from insurance.models import Policy
import json

def chatbot_view(request):
    if request.method == 'POST':
        # Handle the POST request with the message from the chatbot
        data = json.loads(request.body)
        message = data.get('message')

        # Process the message and get a response based on the policy
        response_message = process_message(message)

        # Return a JsonResponse with the chatbot's message
        return JsonResponse({'message': response_message})

    # Render the chatbot.html template when the page is accessed with a GET request
    return render(request, 'chatbot.html')


def process_message(message):
    # Define the keywords and corresponding policies (You can adjust this logic to use real database values)
    keywords_to_policies = {
        'health': ['Health Insurance', 'Medical Coverage', 'Health Care Plans'],
        'car': ['Car Insurance', 'Vehicle Coverage', 'Auto Protection'],
        'home': ['Home Insurance', 'Property Coverage', 'Homeowner Protection'],
    }

    # Default response if no keywords match
    response = "I'm sorry, I couldn't find any policies related to that."

    # Match the message with keywords and generate the response
    for keyword, policies in keywords_to_policies.items():
        if keyword.lower() in message.lower():
            response = f"Here are some policies related to '{keyword}':\n"
            response += "\n".join(policies)
            break

    return response

def generate_pdf_report(request, customer_id):
    # Fetch data from the database
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    # Initial query to get the customer, policies, claims, etc.
    cursor.execute("""
        SELECT 
            c.id AS customer_id, 
            c.address, 
            c.mobile, 
            u.username AS customer_name,
            p.id AS policy_id, 
            p.policy_name, 
            p.sum_assurance, 
            p.premium AS policy_premium, 
            p.tenure, 
            p.creation_date AS policy_creation_date,
            pr.status AS policy_status,
            cl.id AS claim_id, 
            cl.claim_name, 
            cl.claim_amount, 
            cl.premium AS claim_premium, 
            cl.claim_date,
            cr.status AS claim_status,
            q.description AS question, 
            q.admin_comment, 
            q.asked_date
        FROM 
            customer_customer c
        JOIN 
            auth_user u ON c.user_id = u.id
        LEFT JOIN 
            insurance_policyrecord pr ON c.id = pr.customer_id
        LEFT JOIN 
            insurance_policy p ON pr.Policy_id = p.id
        LEFT JOIN 
            insurance_claimrecord cr ON c.id = cr.customer_id
        LEFT JOIN 
            insurance_claim cl ON cr.Claim_id = cl.id
        LEFT JOIN 
            insurance_question q ON c.id = q.customer_id
        WHERE 
            c.id = ?;
    """, (customer_id,))

    data = cursor.fetchall()

    # Organize data for the template
    customer_name = data[0][3]
    address = data[0][1]
    mobile = data[0][2]

    # Create dictionaries to avoid duplication
    policies = {}
    claims = {}
    questions = set()  # Using a set to avoid duplicate questions

    # Step 1: Deduct the claim premium if the claim is approved
    for row in data:
        claim_id = row[11]

        if claim_id is not None:
            claim = {
                'claim_name': row[12],
                'claim_amount': row[13],
                'claim_premium': row[14],
                'claim_date': row[15],
                'claim_status': row[16]
            }

            if claim['claim_status'] == 'Approved':
                if claim['claim_premium'] >= claim['claim_amount']:
                    # Deduct claim premium and update in the database
                    new_claim_premium = claim['claim_premium'] - claim['claim_amount']
                    cursor.execute("""
                        UPDATE insurance_claim 
                        SET premium = ? 
                        WHERE id = ?
                    """, (new_claim_premium, claim_id))
                    conn.commit()  # Commit the changes to the database

                    claim['status'] = "Claim Approved and Deducted"
                else:
                    claim['status'] = "Insufficient Claim Premium for Claim"
            claims[claim_id] = claim

        # Add policies to the policies dictionary
        policy_id = row[4]
        if policy_id not in policies and policy_id is not None:
            policies[policy_id] = {
                'policy_name': row[5],
                'sum_assurance': row[6],
                'premium': row[7],  # Original premium before deduction
                'tenure': row[8],
                'policy_creation_date': row[9],
                'policy_status': row[10]
            }

        # Add questions to the set (set automatically avoids duplicates)
        if row[17] and row[18]:
            questions.add((row[17], row[18], row[19]))

    # Step 2: Re-fetch the updated claim data (to ensure premium is deducted)
    cursor.execute("""
        SELECT 
            cl.id AS claim_id, 
            cl.claim_name, 
            cl.claim_amount, 
            cl.premium AS updated_claim_premium
        FROM 
            insurance_claim cl
        WHERE 
            cl.id IN ({})
    """.format(','.join(str(claim_id) for claim_id in claims.keys())))

    updated_claims_data = cursor.fetchall()

    # Update the claims dictionary with the new premium values
    for claim_row in updated_claims_data:
        claim_id = claim_row[0]
        remaining_claim_premium = claim_row[3]
        if claim_id in claims:
            claims[claim_id]['claim_premium'] = remaining_claim_premium

    # Convert dictionaries to lists
    policies_list = list(policies.values())
    claims_list = list(claims.values())
    questions_list = [{'question': q[0], 'admin_comment': q[1], 'asked_date': q[2]} for q in questions]

    # Render HTML template
    html_string = render_to_string('customer/report_template.html', {
        'customer_name': customer_name,
        'address': address,
        'mobile': mobile,
        'policies': policies_list,
        'claims': claims_list,
        'questions': questions_list
    })

    # Generate PDF
    pdf = HTML(string=html_string).write_pdf()

    # Close the database connection after generating the PDF
    conn.close()

    # Return PDF as a response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="insurance_report_{customer_id}.pdf"'
    return response




# Other views (unchanged)
def customerclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'customer/customerclick.html')

def customer_signup_view(request):
    userForm = forms.CustomerUserForm()
    customerForm = forms.CustomerForm()
    mydict = {'userForm': userForm, 'customerForm': customerForm}

    if request.method == 'POST':
        userForm = forms.CustomerUserForm(request.POST)
        customerForm = forms.CustomerForm(request.POST, request.FILES)
        if userForm.is_valid() and customerForm.is_valid():
            user = userForm.save(commit=False)
            user.set_password(userForm.cleaned_data['password'])  # Hash the password
            user.save()

            customer = customerForm.save(commit=False)
            customer.user = user
            customer.save()

            my_customer_group, created = Group.objects.get_or_create(name='CUSTOMER')
            my_customer_group.user_set.add(user)

            return redirect('customerlogin')
        else:
            # If forms are invalid, re-render the page with errors
            mydict['userForm'] = userForm
            mydict['customerForm'] = customerForm

    return render(request, 'customer/customersignup.html', context=mydict)

def is_customer(user):
    return user.groups.filter(name='CUSTOMER').exists()

@login_required(login_url='customerlogin')
def customer_dashboard_view(request):
    dict = {
        'customer': models.Customer.objects.get(user_id=request.user.id),
        'available_policy': CMODEL.Policy.objects.all().count(),
        'applied_policy': CMODEL.PolicyRecord.objects.all().filter(
            customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'available_claim': CMODEL.Claim.objects.all().count(),
        'applied_claim': CMODEL.ClaimRecord.objects.all().filter(
            customer=models.Customer.objects.get(user_id=request.user.id)).count(),
        'total_category': CMODEL.Category.objects.all().count(),
        'total_question': CMODEL.Question.objects.all().filter(
            customer=models.Customer.objects.get(user_id=request.user.id)).count(),
    }
    return render(request, 'customer/customer_dashboard.html', context=dict)

def apply_policy_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.Policy.objects.all()
    return render(request, 'customer/apply_policy.html', {'policies': policies, 'customer': customer})

def apply_view(request, pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policy = CMODEL.Policy.objects.get(id=pk)
    policyrecord = CMODEL.PolicyRecord()
    policyrecord.Policy = policy
    policyrecord.customer = customer
    policyrecord.save()
    return redirect('history')

def apply_claim_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    claims = CMODEL.Claim.objects.all()
    return render(request, 'customer/apply_claim.html', {'claims': claims, 'customer': customer})

def apply_Claims_view(request, pk):
    customer = models.Customer.objects.get(user_id=request.user.id)
    claim = CMODEL.Claim.objects.get(id=pk)
    claimrecord = CMODEL.ClaimRecord()
    claimrecord.Claim = claim
    claimrecord.customer = customer
    claimrecord.save()
    return redirect('claim_history')

def history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    policies = CMODEL.PolicyRecord.objects.all().filter(customer=customer)
    return render(request, 'customer/history.html', {'policies': policies, 'customer': customer})

def claim_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    claims = CMODEL.ClaimRecord.objects.all().filter(customer=customer)
    return render(request, 'customer/claim_history.html', {'claims': claims, 'customer': customer})

def ask_question_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questionForm = CFORM.QuestionForm()

    if request.method == 'POST':
        questionForm = CFORM.QuestionForm(request.POST)
        if questionForm.is_valid():
            question = questionForm.save(commit=False)
            question.customer = customer
            question.save()
            return redirect('question-history')
    return render(request, 'customer/ask_question.html', {'questionForm': questionForm, 'customer': customer})

def question_history_view(request):
    customer = models.Customer.objects.get(user_id=request.user.id)
    questions = CMODEL.Question.objects.all().filter(customer=customer)
    return render(request, 'customer/question_history.html', {'questions': questions, 'customer': customer})