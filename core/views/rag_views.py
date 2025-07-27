from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RagQueryAPIView(APIView):
    def post(self, request):
        from ..serializers import RagQuerySerializer
        serializer = RagQuerySerializer(data=request.data)
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
