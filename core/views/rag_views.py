from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class RagQueryAPIView(APIView):
    # DRF'e, kullanıcının kimliğini doğrulamak için tarayıcının oturum (session)
    # bilgisini kullanmasını söylüyoruz. Bu, en yaygın ve güvenli yöntemlerden biridir.
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from ..serializers import RagQuerySerializer
        
        # Frontend 'query' gönderiyor, serializer'ın beklemediği alanları filtreleyerek
        # sadece 'question' ve 'ders' alanlarını alıyoruz.
        request_data = {
            'question': request.data.get('query'), 
            'ders': request.data.get('ders', 'Genel') # Eğer ders belirtilmezse varsayılan olarak 'Genel' kullan
        }
        serializer = RagQuerySerializer(data=request_data)
        
        if serializer.is_valid():
            question = serializer.validated_data.get('question')
            ders = serializer.validated_data.get('ders')
            try:
                from ..calistir import rag_ile_cevap_ver
                answer = rag_ile_cevap_ver(kullanici_sorusu=question, ders_adi=ders)
                return Response({"answer": answer})
            except Exception as e:
                return Response({"error": f"RAG sisteminde hata: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
