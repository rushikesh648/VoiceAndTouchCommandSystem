import speech_recognition as sr
import os
import requests # For directions API
from gtts import gTTS
import time

# --- Configuration ---
# You'd need a way to determine or let the user select these
CURRENT_LANGUAGE_CODE_ASR = "en-US" # Example: "es-ES", "fr-FR", "de-DE", "ja-JP", "zh-CN"
CURRENT_LANGUAGE_CODE_TTS = "en"    # Example: "es", "fr", "de", "ja", "zh-cn"

# For the navigation example, the API key is still needed
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY" # <--- REPLACE WITH YOUR ACTUAL API KEY
WAKE_WORD = "navigator" # Wake word is also language-specific now!

# --- Text-to-Speech Function (Language Aware) ---
def speak(text, lang=CURRENT_LANGUAGE_CODE_TTS):
    print(f"Assistant ({lang}): {text}")
    try:
        tts = gTTS(text=text, lang=lang)
        tts.save("response.mp3")
        os.system("mpg321 response.mp3") # Or your preferred audio player
    except Exception as e:
        print(f"Could not play speech in {lang}: {e}. Just printing response.")

# --- Geocoding and Directions (Language can affect result display, but API generally works internationally) ---
# (Keeping these simplified from previous example for brevity, they mostly pass through to Google API)
def get_walking_directions(origin, destination, language=CURRENT_LANGUAGE_CODE_ASR):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "walking",
        "key": GOOGLE_MAPS_API_KEY,
        "language": language # Request directions in the specified language
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            route = data["routes"][0]
            legs = route["legs"]
            
            # These strings would need to be translated for actual multi-language NLU/TTS
            speak(f"Getting walking directions from {legs[0]['start_address']} to {legs[0]['end_address']}.")
            speak(f"The total distance is {legs[0]['distance']['text']} and it will take approximately {legs[0]['duration']['text']}.")
            speak("Here are the steps:")

            for i, step in enumerate(legs[0]["steps"]):
                instruction = step["html_instructions"].replace("<b>", "").replace("</b>", "").replace("<div style=\"font-size:0.9em\">", " ").replace("</div>", "")
                speak(f"Step {i+1}: {instruction}. Distance: {step['distance']['text']}.")
            return True
        elif data["status"] == "ZERO_RESULTS":
            speak("I couldn't find any walking directions for that route. Please check the addresses.")
            return False
        else:
            speak(f"An error occurred while getting directions. Status: {data['status']}")
            return False
    except requests.exceptions.RequestException as e:
        speak("I'm having trouble connecting to the mapping service.")
        print(f"Request Error during directions lookup: {e}")
        return False


# --- Main Voice Command Loop (Language Aware for ASR, but NLU is still English-centric) ---
def listen_for_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        speak(f"Hello! I am ready. Say '{WAKE_WORD}' to ask for directions.", lang=CURRENT_LANGUAGE_CODE_TTS)

        while True:
            try:
                audio = r.listen(source)
                # Specify language for Google Speech Recognition
                command = r.recognize_google(audio, language=CURRENT_LANGUAGE_CODE_ASR).lower()
                print(f"You said (potential wake word): {command}")

                # NLU part here is still in English. For true multi-language,
                # you'd need to detect language or have separate NLU for each.
                if WAKE_WORD.lower() in command: # Ensure wake word matches expected language
                    speak("Yes? Where would you like to go?", lang=CURRENT_LANGUAGE_CODE_TTS)
                    print("Listening for destination command...")
                    audio = r.listen(source)
                    destination_command = r.recognize_google(audio, language=CURRENT_LANGUAGE_CODE_ASR).lower()
                    print(f"You said: {destination_command}")

                    # These keywords ("directions to", "stop", "exit") need to be translated
                    # if CURRENT_LANGUAGE_CODE_ASR is not English.
                    # This is where the NLU challenge for multi-language really shows up.
                    if "directions to" in destination_command:
                        destination = destination_command.split("directions to", 1)[1].strip()
                        speak(f"Okay, I'll get walking directions to {destination}.", lang=CURRENT_LANGUAGE_CODE_TTS)
                        origin = "current location" # Placeholder
                        get_walking_directions(origin, destination, language=CURRENT_LANGUAGE_CODE_ASR) # Pass language to API
                    elif "stop" in destination_command or "exit" in destination_command:
                        speak("Goodbye!", lang=CURRENT_LANGUAGE_CODE_TTS)
                        break
                    else:
                        speak("I didn't understand the destination. Please try again, starting with 'directions to...'", lang=CURRENT_LANGUAGE_CODE_TTS)

            except sr.UnknownValueError:
                speak("Could not understand audio.", lang=CURRENT_LANGUAGE_CODE_TTS)
                print("Could not understand audio")
            except sr.RequestError as e:
                speak(f"Could not connect to speech recognition service: {e}", lang=CURRENT_LANGUAGE_CODE_TTS)
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                speak("An unexpected error occurred.", lang=CURRENT_LANGUAGE_CODE_TTS)
                print(f"An unexpected error occurred: {e}")

            time.sleep(1)

if __name__ == "__main__":
    # Example of how you might change the language:
    # CURRENT_LANGUAGE_CODE_ASR = "es-ES"
    # CURRENT_LANGUAGE_CODE_TTS = "es"
    # WAKE_WORD = "navegador" # Translate wake word too!

    listen_for_commands()