import glob
from deepspeech import Model
from timeit import default_timer as timer
import os
import numpy as np
from language_capture import wavSplit
import webrtcvad
from pydub import AudioSegment
from datetime import date
from KeySpeech.settings import MEDIA_ROOT

DEFAULT_SAMPLE_RATE = 16000

def load_model(models, scorer):
    model_load_start = timer()
    ds = Model(models)
    model_load_end = timer() - model_load_start
    print("Loaded model in %0.3fs." % (model_load_end))
    scorer_load_start = timer()
    ds.enableExternalScorer(scorer)
    scorer_load_end = timer() - scorer_load_start
    print('Loaded external scorer in %0.3fs.' % (scorer_load_end))
    return [ds, model_load_end, scorer_load_end]


def stt(ds, audio, fs):
    inference_time = 0.0
    audio_length = len(audio) * (1 / fs)
    print('Running inference...')
    inference_start = timer()
    output = ds.stt(audio)
    inference_end = timer() - inference_start
    inference_time += inference_end
    print('Inference took %0.3fs for %0.3fs audio file.' % (inference_end, audio_length))

    return [output, inference_time]

def resolve_models(dirName):
    pb = glob.glob(dirName + "/*.pbmm")[0]
    print("Found Model: %s" % pb)
    scorer = glob.glob(dirName + "/*.scorer")[0]
    print("Found scorer: %s" % scorer)
    return pb, scorer

def vad_segment_generator(wavFile, aggressiveness):
    audio, sample_rate, audio_length = wavSplit.read_wave(wavFile)
    vad = webrtcvad.Vad(int(aggressiveness))
    frames = wavSplit.frame_generator(30, audio, DEFAULT_SAMPLE_RATE)
    frames = list(frames)
    segments = wavSplit.vad_collector(DEFAULT_SAMPLE_RATE, 30, 300, vad, frames)
    return segments, DEFAULT_SAMPLE_RATE

def transcribe_file(waveFile):
    waveFile = waveFile.replace(" ","_")
    head, tail = os.path.split(waveFile)
    oldname, ext = os.path.splitext(tail)
    if ext == ".wav":
        sound = AudioSegment.from_wav(waveFile)
        os.remove(waveFile)
    elif ext == ".mp3":
        sound = AudioSegment.from_mp3(waveFile)
        os.remove(waveFile)
    else:
        os.remove(waveFile)
        return
    sound = sound.set_frame_rate(16000)
    sound = sound.set_sample_width(2)
    sound = sound.set_channels(1)
    name = date.today().strftime("%s%m%d%m%Y")+oldname+"audio.wav"
    newfile = os.path.join(MEDIA_ROOT, "documents/" + name)
    sound.export(newfile, format="wav")
    output_graph, scorer = resolve_models(os.path.abspath("language_capture/static"))
    model = load_model(output_graph, scorer)
    segments, sample_rate = vad_segment_generator(wavFile = newfile, aggressiveness=1)
    text = " "
    inference_time = 0
    for i, segment in enumerate(segments):
        audio = np.frombuffer(segment, dtype=np.int16)
        output = stt(model[0],audio,sample_rate)
        inference_time += output[1]
        text+= str(output[0])
        text+= " "
    print("transcribed text: "+text)
    return text, newfile

