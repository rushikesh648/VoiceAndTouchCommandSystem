import speech_recognition as sr
import os
import requests
from gtts import gTTS
# from playsound import playsound # Consider alternative audio playback for cross-platform reliability

# --- Configuration ---
GOOGLE_MAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY" # <--- REPLACE WITH YOUR ACTUAL API KEY
WAKE_WORD = "navigator" # Optional wake word

# --- Text-to-Speech Function ---
def speak(text):
    print(f"Assistant: {text}")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        # Adjust audio playback based on your OS/setup
        # For Linux (install mpg321):
        os.system("mpg321 response.mp3")
        # For macOS:
        # os.system("afplay response.mp3")
        # For Windows (might open in default player or use a specific player like 'start' command):
        # os.system("start response.mp3")
        # If playsound works:
        # playsound("response.mp3")
    except Exception as e:
        print(f"Could not play speech: {e}. Just printing response.")

# --- Geocoding (getting coordinates from an address) ---
def get_coordinates(address):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["status"] == "OK":
            location = data["results"][0]["geometry"]["location"]
            return f"{location['lat']},{location['lng']}"
        else:
            speak(f"Could not find coordinates for {address}. Status: {data['status']}")
            print(f"Geocoding Error: {data['error_message'] if 'error_message' in data else data['status']}")
            return None
    except requests.exceptions.RequestException as e:
        speak("I'm having trouble connecting to the mapping service.")
        print(f"Request Error during geocoding: {e}")
        return None

# --- Get Walking Directions ---
def get_walking_directions(origin, destination):
    base_url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": "walking", # Specify walking mode
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        if data["status"] == "OK":
            route = data["routes"][0]
            legs = route["legs"]
            
            speak(f"Getting walking directions from {legs[0]['start_address']} to {legs[0]['end_address']}.")
            speak(f"The total distance is {legs[0]['distance']['text']} and it will take approximately {legs[0]['duration']['text']}.")
            speak("Here are the steps:")

            directions_text = []
            for i, step in enumerate(legs[0]["steps"]):
                # Clean up HTML tags from instructions
                instruction = step["html_instructions"].replace("<b>", "").replace("</b>", "").replace("<div style=\"font-size:0.9em\">", " ").replace("</div>", "")
                directions_text.append(f"Step {i+1}: {instruction}. Distance: {step['distance']['text']}.")
                speak(f"Step {i+1}: {instruction}. Distance: {step['distance']['text']}.")
            
            # Optionally, open Google Maps in a browser
            # import webbrowser
            # map_url = f"https://www.google.com/maps/dir/?api=1&origin={origin}&destination={destination}&travelmode=walking"
            # webbrowser.open(map_url)
            # speak("I've also opened the directions in your web browser.")

            return "\n".join(directions_text)

        elif data["status"] == "ZERO_RESULTS":
            speak("I couldn't find any walking directions for that route. Please check the addresses.")
            return None
        else:
            speak(f"An error occurred while getting directions. Status: {data['status']}")
            print(f"Directions API Error: {data['error_message'] if 'error_message' in data else data['status']}")
            return None

    except requests.exceptions.RequestException as e:
        speak("I'm having trouble connecting to the mapping service.")
        print(f"Request Error during directions lookup: {e}")
        return None

# --- Main Voice Command Loop ---
def listen_for_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        speak(f"Hello! I am ready. Say '{WAKE_WORD}' to ask for directions.")

        while True:
            try:
                audio = r.listen(source)
                command = r.recognize_google(audio).lower()
                print(f"You said (potential wake word): {command}")

                if WAKE_WORD in command:
                    speak("Yes? Where would you like to go?")
                    print("Listening for destination command...")
                    audio = r.listen(source)
                    destination_command = r.recognize_google(audio).lower()
                    print(f"You said: {destination_command}")

                    if "directions to" in destination_command:
                        destination = destination_command.split("directions to", 1)[1].strip()
                        speak(f"Okay, I'll get walking directions to {destination}.")
                        
                        # For simplicity, let's assume current location or a default starting point
                        # In a real app, you'd get actual GPS coordinates for 'origin'
                        origin = "current location" # Placeholder, replace with actual current location if available
                        # Or for testing, use a fixed address:
                        # origin = "1600 Amphitheatre Parkway, Mountain View, CA" 
                        
                        # First, try to geocode the destination (if it's not already coordinates)
                        # For a real app, you'd handle "current location" more robustly
                        
                        # Let's try to get directions with the string addresses first,
                        # the Google Directions API is usually good at resolving these.
                        
                        get_walking_directions(origin, destination)

                    elif "stop" in destination_command or "exit" in destination_command:
                        speak("Goodbye!")
                        break
                    else:
                        speak("I didn't understand the destination. Please try again, starting with 'directions to...'")

            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")

            time.sleep(1) # Small delay to prevent busy-waiting

if __name__ == "__main__":
    listen_for_commands()
