from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.core.cache import cache
from .models import FAQ

class FAQTests(APITestCase):
    def setUp(self):
        cache.clear()

        self.faq_data = {
            "question": "What is Django?",
            "answer": "<p>Django is a web framework.</p>"
        }
        self.faq = FAQ.objects.create(**self.faq_data)

    def test_create_faq(self):
        """
        Ensure we can create a new FAQ.
        """
        url = reverse('faq-list')
        data = {
            "question": "What is Python?",
            "answer": "<p>Python is a programming language.</p>"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FAQ.objects.count(), 2)
        self.assertEqual(response.data['question'], data['question'])
        self.assertEqual(response.data['answer'], data['answer'])

    def test_retrieve_faq(self):
        """
        Ensure we can retrieve an existing FAQ.
        """
        url = reverse('faq-detail', args=[self.faq.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], self.faq_data['question'])
        self.assertEqual(response.data['answer'], self.faq_data['answer'])

    def test_update_faq(self):
        """
        Ensure we can update an existing FAQ.
        """
        url = reverse('faq-detail', args=[self.faq.id])
        updated_data = {
            "question": "What is Django?",
            "answer": "<p>Django is a high-level Python web framework.</p>"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], updated_data['question'])
        self.assertEqual(response.data['answer'], updated_data['answer'])

    def test_delete_faq(self):
        """
        Ensure we can delete an existing FAQ.
        """
        url = reverse('faq-detail', args=[self.faq.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FAQ.objects.count(), 0)

    def test_list_faqs(self):
        """
        Ensure we can list all FAQs.
        """
        url = reverse('faq-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], self.faq_data['question'])
        self.assertEqual(response.data[0]['answer'], self.faq_data['answer'])

    def test_translation_fallback(self):
        """
        Ensure the API falls back to English if translation is unavailable.
        """
        url = reverse('faq-list')
        response = self.client.get(url, {'lang': 'hi'})  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['question'], self.faq.get_translated_question('hi'))
        self.assertEqual(response.data[0]['answer'], self.faq.get_translated_answer('hi'))

    def test_caching(self):
        """
        Ensure the API uses caching for improved performance.
        """
        url = reverse('faq-list')
        response1 = self.client.get(url)
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        response2 = self.client.get(url)
        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        self.assertEqual(response1.data, response2.data)

    def test_cache_invalidation_on_create(self):
        """
        Ensure the cache is invalidated when a new FAQ is created.
        """
        url = reverse('faq-list')
        self.client.get(url)

        data = {
            "question": "What is Redis?",
            "answer": "<p>Redis is an in-memory data store.</p>"
        }
        self.client.post(url, data, format='json')
    
        response = self.client.get(url)
        self.assertEqual(len(response.data), 2)  

    def test_cache_invalidation_on_update(self):
        """
        Ensure the cache is invalidated when an FAQ is updated.
        """
        url = reverse('faq-detail', args=[self.faq.id])
        self.client.get(url)

        updated_data = {
            "question": "What is Django?",
            "answer": "<p>Django is a high-level Python web framework.</p>"
        }
        self.client.put(url, updated_data, format='json')

        response = self.client.get(url)
        self.assertEqual(response.data['answer'], updated_data['answer'])

    def test_cache_invalidation_on_delete(self):
        """
        Ensure the cache is invalidated when an FAQ is deleted.
        """
        list_url = reverse('faq-list')
        detail_url = reverse('faq-detail', args=[self.faq.id])

        self.client.get(list_url)
        self.client.delete(detail_url)

        response = self.client.get(list_url)
        self.assertEqual(len(response.data), 0) 

    def test_translation_spanish(self):
        """
        Ensure the API returns FAQs translated into Spanish.
        """
        url = reverse('faq-list')
        response = self.client.get(url, {'lang': 'es'})  # Spanish
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['question'], self.faq.get_translated_question('es'))
        self.assertEqual(response.data[0]['answer'], self.faq.get_translated_answer('es'))

    def test_translation_telugu(self):
        """
        Ensure the API returns FAQs translated into Telugu.
        """
        url = reverse('faq-list')
        response = self.client.get(url, {'lang': 'te'})  # Telugu
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['question'], self.faq.get_translated_question('te'))
        self.assertEqual(response.data[0]['answer'], self.faq.get_translated_answer('te'))

    def test_translation_sanskrit(self):
        """
        Ensure the API returns FAQs translated into Sanskrit.
        """
        url = reverse('faq-list')
        response = self.client.get(url, {'lang': 'sa'})  # Sanskrit
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['question'], self.faq.get_translated_question('sa'))
        self.assertEqual(response.data[0]['answer'], self.faq.get_translated_answer('sa'))