from django.contrib.auth.models import User
from django.db import models
from django.core.validators import FileExtensionValidator, MaxValueValidator, MinValueValidator


class audiofile(models.Model):
    audio_file = models.FileField(upload_to="documents",validators=[FileExtensionValidator(allowed_extensions=('wav','mp3'))])
    session_name = models.CharField(max_length=255, blank=True)
    number_of_key_words = models.IntegerField(blank=True, null=True)
    percentage_of_key_words = models.IntegerField(validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ], blank=True, null=True)


class FreqList(models.Model):
    document_name = models.CharField(max_length=255, blank=True, default = "Key words",verbose_name='Session Name')
    creator = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE,
                                related_name='freqlists')
    words = models.ManyToManyField('Word')
    created_on = models.DateTimeField(auto_now_add=True)


class Word(models.Model):
    word_text = models.CharField(max_length=100, blank=False, unique=False)
    frequency = models.IntegerField(blank=False)
    p_o_s = models.CharField(max_length=15, blank=True, default="other")
