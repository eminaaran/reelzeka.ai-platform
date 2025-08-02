
# core/views/chat_views.py

import os
from dotenv import load_dotenv
import google.generativeai as genai
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

load_dotenv()

# Gemini modelini yapılandır
try:
    genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
except Exception as e:
    print(f"!!! GEMINI YAPILANDIRMA HATASI: {e}")
    model = None

class ChatbotView(APIView):
    permission_classes = [IsAuthenticated] # SADECE GİRİŞ YAPANLAR KULLANABİLİR

    def post(self, request, *args, **kwargs):
        user_query = request.data.get('query')

        if not user_query:
            return Response({"error": "Sorgu ('query') alanı boş olamaz."}, status=400)
        
        if not model:
            return Response({"error": "AI modeli yapılandırılamadı."}, status=500)

        try:
            # Sunumda hızlı olması için prompt'u basit tutuyoruz
            prompt = f"Bir YKS öğrencisine yardımcı olan bir asistansın. Şu soruyu kısa ve net bir şekilde cevapla: {user_query}"
            response = model.generate_content(prompt)
            
            response_data = {
                "answer": response.text
            }
            return Response(response_data)

        except Exception as e:
            return Response({"error": f"AI model hatası: {e}"}, status=500)
