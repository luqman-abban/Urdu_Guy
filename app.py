import torch
from transformers import SpeechT5ForTextToSpeech, SpeechT5Processor, SpeechT5HifiGan
import soundfile as sf
import gradio as gr
import scipy.io.wavfile as wav
import numpy as np
import wave
from datasets import load_dataset, Audio, config
from IPython.display import Audio
import streamlit as st

# Load the TTS model from the Hugging Face Hub
checkpoint = "TheUpperCaseGuy/Guy-Urdu-TTS"  # Replace with your actual model name
processor = SpeechT5Processor.from_pretrained(checkpoint)
model = SpeechT5ForTextToSpeech.from_pretrained(checkpoint)
tokenizer = processor.tokenizer
vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")

# Buckwalter to Unicode mapping
buck2uni = {
            u"\u0627":"A",
            u"\u0627":"A",
            u"\u0675":"A",

            u"\u0673":"A",
            u"\u0630":"A",
            u"\u0622":"AA",
            u"\u0628":"B",
            u"\u067E":"P",
            u"\u062A":"T",
            u"\u0637":"T",
            u"\u0679":"T",

            u"\u062C":"J",
            u"\u0633":"S",
            u"\u062B":"S",
            u"\u0635":"S",
            u"\u0686":"CH",
            u"\u062D":"H",
            u"\u0647":"H",
            u"\u0629":"H",

            u"\u06DF":"H",
            u"\u062E":"KH",
            u"\u062F":"D",
            u"\u0688":"D",
            u"\u0630":"Z",
            u"\u0632":"Z",
            u"\u0636":"Z",
            u"\u0638":"Z",
            u"\u068E":"Z",

            u"\u0631":"R",
            u"\u0691":"R",
            u"\u0634":"SH",
            u"\u063A":"GH",
            u"\u0641":"F",
            u"\u06A9":"K",
            u"\u0642":"K",
            u"\u06AF":"G",

            u"\u0644":"L",
            u"\u0645":"M",
            u"\u0646":"N",
            u"\u06BA":"N",
            u"\u0648":"O",
            u"\u0649":"Y",
            u"\u0626":"Y",
            u"\u06CC":"Y",

            u"\u06D2":"E",
            u"\u06C1":"H",
            u"\u064A":"E"  ,
            u"\u06C2":"AH"  ,
            u"\u06BE":"H"  ,
            u"\u0639":"A"  ,
            u"\u0643":"K" ,
            u"\u0621":"A",

            u"\u0624":"O",
            u"\u060C":"" #seperator ulta comma
}

def transString(string, reverse=0):
    """Given a Unicode string, transliterate into Buckwalter.
    To go from
    Buckwalter back to Unicode, set reverse=1"""
    for k, v in buck2uni.items():
        if not reverse:
            string = string.replace(k, v)
        else:
            string = string.replace(v, k)
    return string

def generate_audio(text):
    # Convert input text to Roman Urdu
    roman_urdu = transString(text)

    # Tokenize the input text

    inputs = processor(text=roman_urdu, return_tensors="pt")

    # Generate audio from the SpeechT5 model
    speaker_embeddings = torch.tensor(np.load("speaker_embeddings.npy"))
    speech = model.generate_speech(inputs["input_ids"], speaker_embeddings, vocoder=vocoder)

    return speech

def text_to_speech(text):
    # Generate audio
    audio_output = generate_audio(text)

    output_path = "output.wav"
    sf.write(output_path, audio_output.numpy(), 16000, "PCM_16")

    return output_path

examples = [
    ['میں ٹھیک ہوں، شکریہ! اور آپ؟'],
    ['آپ سَے ملکر خوشی ہوًی!'],
]

# Streamlit app
st.title("Urdu TTS")
st.write("A simple Urdu Text to Speech Application.")

text_input = st.text_input("Enter Urdu text:")
if st.button("Generate Audio"):
    if text_input:
        audio_file = text_to_speech(text_input)
        st.audio(audio_file, format="audio/wav")
    else:
        st.warning("Please enter some text.")
