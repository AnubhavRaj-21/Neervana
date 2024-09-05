from django.shortcuts import render
import os
import re

from word2number import w2n
from django.http import JsonResponse
import speech_recognition as sr
from googletrans import Translator
#from langdetect import detect, DetectorFactory
from django.views.decorators.csrf import csrf_exempt
from langdetect import detect

import json
from .models import Product_details
# Create your views here.



# Initialize Google Translate client
translator = Translator()


# @csrf_exempt
# def audio(request):
#     if request.method == 'POST' and request.FILES.get('audio'):
#         audio_file = request.FILES['audio']
#         language = request.POST.get('language', 'en-US')  # Default to English

#         # Convert audio to text using a speech-to-text service
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(audio_file) as source:
#             audio = recognizer.record(source)
#             try:
#                 text = recognizer.recognize_google(audio, language=language)
#                 return JsonResponse({'text': text})
#             except sr.UnknownValueError:
#                 return JsonResponse({'error': 'Could not understand audio'}, status=400)
#             except sr.RequestError as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': 'Invalid request'}, status=400)

# def translate_text(text, target_language='en'):
#     result = translator.translate(text, dest=target_language)
#     return result.text

# @csrf_exempt
# def audio(request):
#     if request.method == 'POST' and request.FILES.get('audio'):
#         audio_file = request.FILES['audio']
#         language = request.POST.get('language', 'en-US')  # Default to English

#         # Convert audio to text using a speech-to-text service
#         recognizer = sr.Recognizer()
#         with sr.AudioFile(audio_file) as source:
#             audio = recognizer.record(source)
#             try:
#                 text = recognizer.recognize_google(audio, language=language)
                
#                 # Detect the language of the transcribed text
#                 detected_language = detect(text)
                
#                 # Translate to English if the detected language is not English
#                 if detected_language != 'en':
#                     text = translate_text(text, target_language='en')
                
#                 return JsonResponse({'text': text})
#             except sr.UnknownValueError:
#                 return JsonResponse({'error': 'Could not understand audio'}, status=400)
#             except sr.RequestError as e:
#                 return JsonResponse({'error': str(e)}, status=500)
#     return JsonResponse({'error': 'Invalid request'}, status=400)



def extract_product_and_quantity(text):
    # First, try to find a numeric quantity (e.g., "5 apples")
    quantity_match = re.search(r'\d+', text)
    
    if quantity_match:
        quantity = int(quantity_match.group())
        product_name = text.replace(str(quantity), '').strip()
    else:
        # If no numeric quantity, try to convert spelled-out numbers (e.g., "five apples")
        try:
            # Convert spelled-out number to numeric using w2n
            words = text.split()
            for i, word in enumerate(words):
                try:
                    # Attempt to convert the word to a number
                    quantity = w2n.word_to_num(word)
                    # If successful, remove that word from the product name
                    product_name = " ".join(words[:i] + words[i+1:]).strip()
                    return product_name, quantity
                except ValueError:
                    continue
            # If no valid number is found, consider the entire text as product_name
            return text, None
        except ValueError:
            return text, None
    
    return product_name, quantity







def translate_text(text, target_language='en'):
    # Use googletrans to translate text (correct argument is 'dest' not 'target_language')
    result = translator.translate(text, dest=target_language)
    return result.text

@csrf_exempt
def audio(request):
    if request.method == 'POST' and request.FILES.get('audio'):
        audio_file = request.FILES['audio']
        language = request.POST.get('language', 'en-US')  # Default to English

        # Convert audio to text using a speech-to-text service
        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio, language=language)
                
                # Detect the language of the transcribed text
                detected_language = detect(text)
                
                # Translate to English if the detected language is not English
                if detected_language != 'en':
                    text = translate_text(text, target_language='en')
                
                return JsonResponse({'text': text})
            except sr.UnknownValueError:
                return JsonResponse({'error': 'Could not understand audio'}, status=400)
            except sr.RequestError as e:
                return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)




@csrf_exempt
def Product_details(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_name = data.get('product_name')
        quantity = data.get('quantity')
        product_category = data.get('product_category')

        Product_details = Product_details(product_name=product_name,quantity=quantity,product_category=product_category)
        Product_details.save()

        return JsonResponse({'message': 'Product created successfully!'}, status=201)
    
    else:
        return JsonResponse({"Invalid request"},status=400)