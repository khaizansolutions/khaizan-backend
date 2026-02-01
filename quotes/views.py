from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import QuoteRequest
from .serializers import QuoteRequestSerializer


class QuoteRequestViewSet(viewsets.ModelViewSet):
    """
    API endpoint for quote requests
    POST /api/quotes/ - Create new quote request
    """
    queryset = QuoteRequest.objects.all()
    serializer_class = QuoteRequestSerializer
    http_method_names = ['post']  # Only allow POST
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'success': True,
            'message': 'Quote request submitted successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)