from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .parser import analyze_webpage

class ScanWebpageView(APIView):
    def post(self, request):
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Run real semantic scraping analysis
        analysis_result = analyze_webpage(url)
        
        if 'error' in analysis_result:
            return Response({'error': analysis_result['error']}, status=status.HTTP_400_BAD_REQUEST)
            
        # Optional: Save result safely into Database (PostgreSQL via Docker)
        try:
            from .models import ScanResult
            ScanResult.objects.create(
                url=analysis_result['url'],
                score=analysis_result['score'],
                issues_payload=analysis_result['issues']
            )
        except Exception as db_err:
            print(f"Warning: Could not save to DB (Migrations might not be applied): {db_err}")
            
        return Response(analysis_result, status=status.HTTP_200_OK)
