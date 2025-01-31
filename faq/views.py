from rest_framework import viewsets
from django.core.cache import cache
from .models import FAQ
from .serializers import FAQSerializer

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer

    def get_queryset(self):
        lang = self.request.query_params.get('lang', 'en')
        cache_key = f'faqs_{lang}'
        queryset = cache.get(cache_key)

        if not queryset:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, timeout=60 * 15)  # Cache for 15 minutes
        return queryset

    def get_serializer_context(self):
        # Pass the request context to the serializer
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        instance = serializer.save()
        self.clear_cache()

    def perform_update(self, serializer):
        instance = serializer.save()
        self.clear_cache()

    def clear_cache(self):
        languages = ['en', 'hi', 'bn']  # Add all supported languages here
        for lang in languages:
            cache_key = f'faqs_{lang}'
            cache.delete(cache_key)