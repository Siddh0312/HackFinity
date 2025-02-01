import os
import random
from groq import Groq
from google.colab import files

# ✅ Set the GROQ API key (Ensure it's securely stored in your environment)
os.environ["GROQ_API_KEY"] = "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"

# ✅ Initialize GROQ client
groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

# ✅ Available Podcast Tones
PODCAST_TONES = [
    "Casual Conversational",
    "Inquisitive and Thoughtful",
    "Witty and Light-Hearted",
    "Professional and Analytical",
    "Friendly Storytelling",
    "Insightful and Reflective",
    "Dynamic and Engaging",
    "Laid-back and Relatable",
    "Motivational and Uplifting",
    "Balanced - Mix of Informative and Fun"
]

# ✅ Audience Types
AUDIENCE_TYPES = [
    "General Audience",
    "Students/Academics",
    "Professionals/Experts",
    "Youth/Gen Z"
]

# ✅ Podcast Styles
PODCAST_STYLES = [
    "Interview Style",
    "Panel Discussion",
    "Narrative Storytelling",
    "Debate Format"
]

# ✅ Function to Generate Podcast Script
def generate_podcast_script(summarized_text, guest_names, tone, audience, style, target_word_count=10000, host_name="CHRIS BUMSTEAD AKA CBUM"):
    guest_roles = "\n".join([
        f"{i+1}. {guest_names[i]}, who is a domain expert in the research topic with profound understanding."
        for i in range(len(guest_names))
    ])

    dynamic_segments = "\n- Hot Takes: Quickfire opinions from each guest.\n- Fact Check: Surprising stats thrown by the host.\n- Audience Questions: Simulated listener questions.\n- Rapid Fire Round: Quick, humorous Q&A."

    prompt = [
        {"role": "system", "content":
            f"You are an expert podcast script writer specializing in engaging content.\n"
            f"Generate a podcast script featuring:\n"
            f"1. The HOST, {host_name}.\n"
            f"{guest_roles}\n"
            f"Tone: '{tone}', Audience: '{audience}', Style: '{style}'.\n"
            "Include engaging segments like Hot Takes, Fact Check, Audience Questions, and Rapid Fire Rounds.\n"
            "Break down key statistics in simple terms and add fun facts where relevant.\n"
            "Ensure the script flows naturally with light-hearted moments, realistic dialogue, and dynamic transitions."
        },
        {"role": "user", "content":
            f"Convert the following research paper summary into an engaging podcast script:\n\n{summarized_text}\n"
            "Ensure natural interactions and approximately 10000 words."
        }
    ]

    response = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=prompt,
        max_tokens=32768
    )

    return response.choices[0].message.content

# ✅ Function to Upload and Process Research Paper
def upload_and_generate_script():
    uploaded = files.upload()
    for filename in uploaded.keys():
        with open(filename, 'r') as file:
            summarized_text = file.read()
            host_name = input("Enter the host's name: ")
            num_guests = int(input("Enter the number of guests: "))
            guest_names = [input(f"Enter the name of guest {i+1}: ") for i in range(num_guests)]

            # ✅ Select Tone
            print("\n🎙️ Choose the tone for the podcast:")
            for idx, tone in enumerate(PODCAST_TONES, 1):
                print(f"{idx}. {tone}")
            tone_choice = int(input("Enter the number for the tone: "))
            selected_tone = PODCAST_TONES[tone_choice - 1]

            # ✅ Select Audience
            print("\n👥 Choose the target audience:")
            for idx, audience in enumerate(AUDIENCE_TYPES, 1):
                print(f"{idx}. {audience}")
            audience_choice = int(input("Enter the number for the audience: "))
            selected_audience = AUDIENCE_TYPES[audience_choice - 1]

            # ✅ Select Podcast Style
            print("\n🎧 Choose the podcast style:")
            for idx, style in enumerate(PODCAST_STYLES, 1):
                print(f"{idx}. {style}")
            style_choice = int(input("Enter the number for the style: "))
            selected_style = PODCAST_STYLES[style_choice - 1]

            # ✅ Generate Podcast Script
            script = generate_podcast_script(
                summarized_text, guest_names, selected_tone, selected_audience, selected_style, host_name=host_name
            )

            # ✅ Save Script to File
            output_filename = f"podcast_script_{filename.replace(' ', '_')}.txt"
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(script)

            # ✅ Download File Automatically
            files.download(output_filename)
            print(f"🎙️ Podcast script saved and downloaded as '{output_filename}'!")

# ✅ Run the Script
upload_and_generate_script()
