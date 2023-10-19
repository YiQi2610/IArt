import librosa
import librosa.display
import os
import numpy as np
from pydub import AudioSegment
import torch
from torch import nn


os.chdir(os.path.dirname(os.path.realpath(__file__)))

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

EMOTIONS = ["ANG", "DIS", "FEA", "HAP", "NEU", "SAD"]

def extract_features(data, sample_rate):
    # ZCR
    result = np.array([])
    zcr = np.mean(librosa.feature.zero_crossing_rate(y=data).T, axis=0)
    result=np.hstack((result, zcr)) # stacking horizontally

    # Chroma_stft
    stft = np.abs(librosa.stft(data))
    chroma_stft = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
    result = np.hstack((result, chroma_stft)) # stacking horizontally

    # MFCC
    mfcc = np.mean(librosa.feature.mfcc(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mfcc)) # stacking horizontally

    # Root Mean Square Value
    rms = np.mean(librosa.feature.rms(y=data).T, axis=0)
    result = np.hstack((result, rms)) # stacking horizontally

    # MelSpectogram
    mel = np.mean(librosa.feature.melspectrogram(y=data, sr=sample_rate).T, axis=0)
    result = np.hstack((result, mel)) # stacking horizontally
    
    return result

def listOfCouples(file_length,file_number,out_file_length):

    a = (file_length-out_file_length)/(file_number-1)
    LC = [(round(a*k), round(a*k) + out_file_length) for k in range(file_number)]

    return LC

def decouper_audio(audioPath,file_number,out_file_length):
    audio = AudioSegment.from_file(audioPath)

    audio_length = len(audio)
    intervals = listOfCouples(audio_length,file_number,out_file_length)
    segments = []

    for start_time, end_time in intervals:
        segment = audio[start_time:end_time]
        segments.append(segment)

    return segments

def get_emotion(audioPath):
    N = 50
    out_file_length = 3500

    audioParts = decouper_audio(audioPath,N,out_file_length)

    for i, part in enumerate(audioParts):
        part.export(f"audios/audioPart{i+1}.wav",format="wav")


    model = torch.jit.load("model/model_scripted.pt", map_location=device)
    model.eval()
    
    audios = os.listdir("audios/")
    model.to(device)

    all_X = []
    for file in audios:
        if(file!=".gitkeep"):
            audio, sr = librosa.load(os.path.join("audios/", file))
            X = np.array(extract_features(audio, sr))
            mean, std  = np.mean(X), np.std(X)
            X = (X-mean)/std
            X = X.astype("float32")
            all_X.append(np.array(X))

    prompt = np.vstack(all_X)
    prompt = np.expand_dims(prompt,axis=1)
    X_torch = torch.from_numpy(prompt)
    X_torch = X_torch.to(device)
    res = model(X_torch)
    res = torch.transpose(res, 0, 1)
    res = torch.mean(res, 1)
    id = torch.argmax(res)
    return EMOTIONS[id]
    