from rest_framework import serializers
from .models import FAQ

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer']

    def to_representation(self, instance):
        # Get the language from the request
        lang = self.context['request'].query_params.get('lang', 'en')
        
        # Override the question and answer fields with the translated values
        representation = super().to_representation(instance)
        representation['question'] = instance.get_translated_question(lang)
        representation['answer'] = instance.get_translated_answer(lang)
        
        return representation