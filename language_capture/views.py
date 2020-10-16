from django.shortcuts import render, redirect
import os
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from language_capture.models import FreqList
from language_capture.forms import DocumentForm
from language_capture.tasks import speech_to_freq_list
from KeySpeech.settings import MEDIA_ROOT
import django_filters
from django.utils import timezone
from datetime import timedelta

# after python manage.py runserver run this in terminal:
# celery worker -A keyspeech --loglevel=debug --concurrency=4

DOC_ROOT = os.path.join(MEDIA_ROOT,"documents")


class WordlistFilter(django_filters.FilterSet):

    date_between = django_filters.DateFromToRangeFilter(
        field_name='created_on',
        label='Date range (format MM/DD/YYYY)')
    session_name = django_filters.CharFilter(field_name='document_name',lookup_expr='icontains')
    days = django_filters.NumberFilter(field_name='created_on', method='get_past_n_days', label="Past n days")

    def get_past_n_days(self, queryset, field_name, value):
        time_threshold = timezone.now() - timedelta(days=int(value))
        return queryset.filter(created_on__gte=time_threshold)

    class Meta:
        model = FreqList
        fields = ('days',)


class SignUp(generic.CreateView):

    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def form_valid(self, form):
        if self.request.POST.get('agree'):
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


def tandc(request):
    return render(request,'tandc.html')


def home(request):
    if request.user.is_authenticated:
        f = WordlistFilter(request.GET, queryset=request.user.freqlists.all())
        merge = request.GET.get('merge')
        allwords_sorted = []
        if merge:
            allwords = {}
            for wordlist in f.qs:
                for word in wordlist.words.all():
                    if word.word_text in allwords:
                        allwords[word.word_text][0]+=word.frequency
                    else:
                        allwords[word.word_text] = [word.frequency,word.p_o_s]
            allwords_sorted = sorted(allwords.items(),key = lambda x: x[1][0], reverse=True)
        return render(request, 'language_capture/userhome.html', {'filter': f,'merge':merge, 'mergewords':allwords_sorted})
    else:
        return redirect('mainhome')


def freqlists(request, freqlist_id):
    flist = FreqList.objects.get(pk=freqlist_id)
    if flist.creator == request.user:
        return render(request, 'language_capture/freqlists.html', {'flist':flist})
    else:
        return redirect('home')


def model_form_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save()
                afile = form.cleaned_data['audio_file']
                fname = form.cleaned_data['session_name']
                percent = form.cleaned_data['percentage_of_key_words']
                keynum = form.cleaned_data['number_of_key_words']
                filename = os.path.join(DOC_ROOT, afile.name)
                current_user_id = request.user.id
                speech_to_freq_list(wavfilename=filename, percent=percent, num=keynum, request_user=current_user_id, session_name=fname)
                obj.delete()
                return redirect('home')
        else:
            form = DocumentForm()
        return render(request, 'language_capture/model_form_upload.html', {
            'form': form
        })
    else:
        return redirect('mainhome')


def delete_freqlist(request,pk):
    if request.method == "POST":
        flist = FreqList.objects.get(pk=pk)
        if flist.creator == request.user:
            flist.delete()
    return redirect('home')


