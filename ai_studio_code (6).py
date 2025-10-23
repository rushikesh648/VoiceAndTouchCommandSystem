import speech_recognition as sr
import os
import time
from gtts import gTTS # For text-to-speech responses (optional)
# from playsound import playsound # For playing generated speech (optional, cross-platform issues can occur)

# --- Configuration ---
WAKE_WORD = "computer" # The word to trigger listening for a command
IOT_API_BASE_URL = "http://your-home-automation-server/api" # Replace with your actual IoT platform API
# For example, if using Home Assistant, this might be something like:
# IOT_API_BASE_URL = "http://localhost:8123/api"
# IOT_ACCESS_TOKEN = "YOUR_LONG_LIVED_ACCESS_TOKEN" # Required for Home Assistant API

# --- Text-to-Speech Function ---
def speak(text):
    print(f"Assistant: {text}")
    try:
        tts = gTTS(text=text, lang='en')
        tts.save("response.mp3")
        # Due to potential issues with playsound across different OS/environments,
        # you might need to use a different audio player here or just print the text.
        # Example using os.system for simple playback (might vary by OS):
        os.system("mpg321 response.mp3") # For Linux, install mpg321
        # os.system("afplay response.mp3") # For macOS
        # os.system("start response.mp3") # For Windows (might open in default player)
        # playsound("response.mp3") # If playsound works for you
    except Exception as e:
        print(f"Could not play speech: {e}. Just printing response.")

# --- IoT Interaction Functions (Simulated) ---
# Replace these with actual API calls or MQTT messages to your devices
def control_iot_device(device_name, action):
    # This is where you'd integrate with your actual IoT platform.
    # Examples:
    # 1. HTTP Request to a Home Assistant API:
    #    import requests
    #    headers = {"Authorization": f"Bearer {IOT_ACCESS_TOKEN}", "content-type": "application/json"}
    #    if action == "on":
    #        service = "turn_on"
    #    elif action == "off":
    #        service = "turn_off"
    #    else:
    #        print(f"Unknown action: {action}")
    #        return False
    #    data = {"entity_id": f"light.{device_name.replace(' ', '_')}"} # Assuming entity_id format
    #    response = requests.post(f"{IOT_API_BASE_URL}/services/light/{service}", json=data, headers=headers)
    #    if response.status_code == 200:
    #        print(f"Successfully sent command to {device_name}")
    #        return True
    #    else:
    #        print(f"Failed to send command to {device_name}: {response.status_code} - {response.text}")
    #        return False

    # 2. Publish MQTT message:
    #    import paho.mqtt.client as mqtt
    #    client = mqtt.Client("PythonVoiceAssistant")
    #    client.connect("your_mqtt_broker_ip", 1883, 60)
    #    topic = f"cmnd/{device_name.replace(' ', '_')}/POWER"
    #    payload = "ON" if action == "on" else "OFF"
    #    client.publish(topic, payload)
    #    client.disconnect()
    #    print(f"Published MQTT message to {device_name}")
    #    return True


    # --- SIMULATED IoT Interaction ---
    print(f"[SIMULATED] Controlling device: {device_name}, Action: {action}")
    if "light" in device_name:
        if action == "on":
            speak(f"Turning on the {device_name}.")
            return True
        elif action == "off":
            speak(f"Turning off the {device_name}.")
            return True
    elif "fan" in device_name:
        if action == "on":
            speak(f"Turning on the {device_name}.")
            return True
        elif action == "off":
            speak(f"Turning off the {device_name}.")
            return True
    
    speak(f"I don't know how to {action} the {device_name}.")
    return False

# --- Main Voice Command Loop ---
def listen_for_commands():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source) # Adjust for ambient noise once
        print("Listening for wake word...")
        speak(f"I am ready. Say '{WAKE_WORD}' to activate.")

        while True:
            try:
                audio = r.listen(source)
                command = r.recognize_google(audio).lower()
                print(f"You said (potential wake word): {command}")

                if WAKE_WORD in command:
                    speak("Yes?")
                    print("Listening for command...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio).lower()
                    print(f"You said: {command}")
                    
                    if "turn on" in command:
                        if "kitchen light" in command:
                            control_iot_device("kitchen light", "on")
                        elif "bedroom light" in command:
                            control_iot_device("bedroom light", "on")
                        elif "living room fan" in command:
                            control_iot_device("living room fan", "on")
                        else:
                            speak("Which device would you like to turn on?")
                    elif "turn off" in command:
                        if "kitchen light" in command:
                            control_iot_device("kitchen light", "off")
                        elif "bedroom light" in command:
                            control_iot_device("bedroom light", "off")
                        elif "living room fan" in command:
                            control_iot_device("living room fan", "off")
                        else:
                            speak("Which device would you like to turn off?")
                    elif "what time is it" in command:
                        speak(f"The current time is {time.strftime('%I:%M %p')}")
                    elif "hello" in command:
                        speak("Hello there!")
                    elif "goodbye" in command or "exit" in command:
                        speak("Goodbye!")
                        break # Exit the loop
                    else:
                        speak("I didn't understand that command. Can you please repeat it?")

            except sr.UnknownValueError:
                # This happens if speech_recognition can't understand the audio
                print("Could not understand audio")
            except sr.RequestError as e:
                # This happens if there's no internet connection for Google Speech Recognition
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
            time.sleep(1) # Small delay to prevent busy-waiting

if __name__ == "__main__":
    listen_for_commands()