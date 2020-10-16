from language_capture import transcribeFile
from language_capture import keyWorder as kW
from language_capture.models import FreqList, Word, User
import os


def speech_to_freq_list(wavfilename, percent, num,  request_user, session_name):
    speech, extrafile = transcribeFile.transcribe_file(wavfilename)
    mykeyworder = kW.KeyWorder(text=speech)
    word_freqs, pos_list = mykeyworder.top_words(pos=True, percent=percent, num=num)
    creator = User.objects.get(id=request_user)
    flist = FreqList(document_name=session_name, creator=creator)
    flist.save()
    for i in range(len(word_freqs)):
        tup = word_freqs[i]
        word_pos = pos_list[i]
        w = Word(word_text=tup[0], frequency=tup[1], p_o_s=word_pos)
        w.save()
        flist.words.add(w)
    os.remove(extrafile)
    return


