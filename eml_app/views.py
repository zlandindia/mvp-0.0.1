import email
import os
import re
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserDetailForm, EmlUploadForm, FeedbackForm
from .models import UserDetail
import google.generativeai as genai

def user_details(request):
    if request.method == 'POST':
        form = UserDetailForm(request.POST)
        if form.is_valid():
            user_detail = form.save()
            return redirect('upload_eml', user_id=user_detail.id)
    else:
        form = UserDetailForm()
    return render(request, 'user_details.html', {'form': form})

def extract_text_from_email(msg):
    text = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                payload = part.get_payload(decode=True)
                if payload:
                    text += payload.decode('utf-8')
    else:
        payload = msg.get_payload(decode=True)
        if payload:
            text = payload.decode('utf-8')
    return text

def final_ai_response(clean_text_01):
    os.environ["API_KEY"] = "AIzaSyBlUF9y20Hr5gerkBYHTeaODaVpPd4EK9o"  # Replace with your actual API key
    genai.configure(api_key=os.environ["API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # Ai instructions
    instruction = "give me two line suggestions from the following to make a decision like an instructor "
    response = model.generate_content(instruction + "{" + clean_text_01 + "}")

    return response.text
    # return instruction

def clean_text(input_text):
    # Remove extra spaces, newlines, and symbols
    cleaned_lines = []
    for line in input_text.splitlines():
        stripped_line = re.sub(r'[^\w\s]', '', line).strip()
        if stripped_line:  # Avoid adding empty lines
            cleaned_lines.append(stripped_line)

    return ' '.join(cleaned_lines)

def upload_eml(request, user_id):
    user_detail = get_object_or_404(UserDetail, id=user_id)
    if request.method == 'POST':
        form = EmlUploadForm(request.POST, request.FILES)
        if form.is_valid():
            eml_file = request.FILES['eml_file']
            msg = email.message_from_bytes(eml_file.read())
            text = extract_text_from_email(msg)
            cleaned_text_output = clean_text(text)
            ai_response = final_ai_response(cleaned_text_output)

            # Create feedback form
            feedback_form = FeedbackForm(instance=user_detail)
            return render(request, 'result.html', {'user_detail': user_detail, 'email_text': ai_response, 'feedback_form': feedback_form})
    else:
        form = EmlUploadForm()
    return render(request, 'upload_eml.html', {'form': form, 'user_detail': user_detail})

def submit_feedback(request, user_id):
    user_detail = get_object_or_404(UserDetail, id=user_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=user_detail)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = FeedbackForm(instance=user_detail)
    return render(request, 'feedback.html', {'form': form, 'user_detail': user_detail})

def thank_you(request):
    return render(request, 'thank_you.html')
