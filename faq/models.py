from django.db import models
from ckeditor.fields import RichTextField
from googletrans import Translator

translator = Translator()

class FAQ(models.Model):
    question = models.TextField()
    answer = RichTextField()

    question_bn = models.TextField(blank=True, null=True)  
    question_es = models.TextField(blank=True, null=True)  
    question_te = models.TextField(blank=True, null=True)  
    question_hi = models.TextField(blank=True, null=True)  
    question_sa = models.TextField(blank=True, null=True)  

    answer_hi = RichTextField(blank=True, null=True)  
    answer_bn = RichTextField(blank=True, null=True)  
    answer_es = RichTextField(blank=True, null=True)  
    answer_te = RichTextField(blank=True, null=True)  
    answer_sa = RichTextField(blank=True, null=True)  

    def get_translated_question(self, lang='en'):
        return getattr(self, f'question_{lang}', self.question)

    def get_translated_answer(self, lang='en'):
        return getattr(self, f'answer_{lang}', self.answer)

    def save(self, *args, **kwargs):
        languages = ['hi', 'bn', 'es', 'te', 'sa']  
        for lang in languages:
            if not getattr(self, f'question_{lang}'):
                setattr(self, f'question_{lang}', self.translate_text(self.question, lang))
            if not getattr(self, f'answer_{lang}'):
                setattr(self, f'answer_{lang}', self.translate_text(self.answer, lang))
        super().save(*args, **kwargs)

    @staticmethod
    def translate_text(text, dest_lang):
        try:
            return translator.translate(text, dest=dest_lang).text
        except:
            return text  

    def __str__(self):
        return self.question