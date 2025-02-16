from TTS.api import TTS

# Load the model
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False).to("cuda")

# Generate speech and save to file
tts.tts_to_file(text="Hello Hoe", file_path="output.wav")