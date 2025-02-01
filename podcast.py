import os
from gtts import gTTS
from pydub import AudioSegment
from google.colab import files

# ✅ Default Voice Settings (Different TLDs for Accents)
DEFAULT_VOICE_TLDS = ["com", "co.uk", "com.au", "ca"]

# ✅ Function to Assign Voice Based on Speaker
def assign_voice(speaker_name):
    speaker_hash = sum(ord(char) for char in speaker_name)  # Generate a consistent hash
    tld = DEFAULT_VOICE_TLDS[speaker_hash % len(DEFAULT_VOICE_TLDS)]
    return tld

# ✅ Function to Generate Podcast Audio from Script
def generate_audio_from_script(script_file_path):
    if not os.path.exists(script_file_path):
        raise FileNotFoundError("❌ Podcast script file not found!")

    with open(script_file_path, "r", encoding="utf-8") as f:
        script_lines = f.readlines()

    audio_segments = []
    line_number = 1

    for line in script_lines:
        line = line.strip()

        if ':' in line:
            speaker, dialogue = line.split(':', 1)
            speaker = speaker.strip()
            dialogue = dialogue.strip()

            if dialogue:  # Only process non-empty dialogues
                print(f"🎙️ Generating audio for {speaker}: {dialogue}")

                # ✅ Assign Voice Based on Speaker
                tld = assign_voice(speaker)

                # ✅ Generate Speech Audio
                tts = gTTS(text=dialogue, lang='en', tld=tld)
                temp_filename = f"temp_audio_{line_number}.mp3"
                tts.save(temp_filename)

                # ✅ Load Audio with Pydub
                audio_segment = AudioSegment.from_mp3(temp_filename)
                audio_segments.append(audio_segment + AudioSegment.silent(duration=300))  # Add short pause

                # Cleanup temporary file
                os.remove(temp_filename)

                line_number += 1

    # ✅ Merge All Audio Segments into a Final Podcast
    final_podcast = AudioSegment.silent(duration=1000)  # Start with a short silence
    for segment in audio_segments:
        final_podcast += segment

    # ✅ Export Final Podcast
    output_filename = "final_podcast.mp3"
    final_podcast.export(output_filename, format="mp3")
    print(f"🎧 Podcast successfully generated as '{output_filename}'!")

    # ✅ Download the Audio File Automatically
    files.download(output_filename)

# ✅ Upload the Generated Podcast Script
uploaded = files.upload()
script_file_path = list(uploaded.keys())[0]  # Get the uploaded script file name

# ✅ Generate Podcast Audio
generate_audio_from_script(script_file_path)
