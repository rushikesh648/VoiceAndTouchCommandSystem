# Voice and Touch Command System

A collection of Python and JavaScript code examples demonstrating various voice command and touch gesture functionalities for daily tasks, IoT control, and interactive web experiences.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Voice Command Examples](#voice-command-examples)
  - [General Voice Commands](#general-voice-commands)
  - [IoT Device Control](#iot-device-control)
  - [Walking Directions](#walking-directions)
  - [Multi-Language Support (Concept)](#multi-language-support-concept)
- [Touch Command Examples](#touch-command-examples)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## About the Project

This repository serves as a practical demonstration and boilerplate code for building interactive systems controlled by both voice and touch. It explores various applications from simple task automation to smart home integration and web-based gesture control. The goal is to provide foundational code snippets and a clear understanding of how these modern input methods can enhance user experience and interact with the digital and physical world.

## Features

*   **Voice-to-Text Transcription:** Utilizes Google's Speech Recognition API (via `speech_recognition` library) for accurate voice input.
*   **Text-to-Speech Output:** Provides spoken feedback using Google Text-to-Speech (`gTTS`).
*   **IoT Device Control (Simulated/Integrable):** Demonstrates how to parse voice commands to control smart home devices (with placeholders for actual API/MQTT integration).
*   **Walking Directions:** Integrates with Google Maps Directions API to provide turn-by-turn walking instructions via voice.
*   **Basic Touch Gesture Recognition (Web):** Implements common touch interactions like tap, long press, and swipes for web applications using JavaScript.
*   **Conceptual Multi-Language Support:** Outlines how to integrate different languages for ASR and TTS.

## Voice Command Examples

### General Voice Commands

*(Refer to `your_python_voice_script.py` or similar file in the project)*
A basic script that listens for a wake word and responds to simple queries like asking for the time or greetings.

**Commands:**
*   `"Computer, what time is it?"`
*   `"Computer, hello"`
*   `"Computer, goodbye"`

### IoT Device Control

*(Refer to `your_python_iot_script.py` or similar file)*
Extends the general voice command system to include control over simulated (or real, with configuration) IoT devices.

**Configuration:**
*   You will need to replace the simulated IoT interaction with actual API calls (e.g., to Home Assistant, Philips Hue, MQTT broker) in the `control_iot_device` function.
*   Update `IOT_API_BASE_URL` and potentially `IOT_ACCESS_TOKEN` with your specific smart home platform details.

**Commands:**
*   `"Computer, turn on the kitchen light"`
*   `"Computer, turn off the bedroom light"`
*   `"Computer, turn on the living room fan"`

### Walking Directions

*(Refer to `your_python_directions_script.py` or similar file)*
Leverages the Google Maps Directions API to provide voice-guided walking directions.

**Configuration:**
*   **Google Maps API Key:** You **must** obtain a Google Maps API key and enable the "Directions API" in your Google Cloud Project. Replace `"YOUR_GOOGLE_MAPS_API_KEY"` in the script with your actual key. **Keep this key secure.**

**Commands:**
*   `"Navigator, directions to the nearest park"`
*   `"Navigator, directions to Times Square New York"`

### Multi-Language Support (Concept)

*(Refer to `your_python_multi_lang_script.py` or similar file)*
Demonstrates how `speech_recognition` and `gTTS` can be configured for different languages. The core Natural Language Understanding (NLU) logic still requires adaptation for each language (e.g., translating keywords).

**Configuration:**
*   Set `CURRENT_LANGUAGE_CODE_ASR` and `CURRENT_LANGUAGE_CODE_TTS` variables to your desired language codes (e.g., "es-ES" and "es" for Spanish).
*   Remember to translate your `WAKE_WORD` and command keywords if switching NLU to a new language.

## Touch Command Examples

*(Refer to `index.html` and `script.js` in the project)*
A simple web-based demonstration of detecting and responding to fundamental touch gestures on an HTML element.

**Gestures Detected:**
*   **Tap:** A quick touch and release.
*   **Long Press:** Touching and holding for a duration (e.g., 500ms).
*   **Swipe (Left, Right, Up, Down):** Touching and dragging a finger across the element.

**How to Use:**
1.  Open `index.html` in a web browser on a touchscreen device.
2.  Interact with the green box to see the recognized gestures in the "Action" output.

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

*   **Python 3.x:** Installed on your system.
*   **`pip`:** Python package installer.
*   **Git:** For cloning the repository.
*   **Microphone:** For voice commands.
*   **Internet Connection:** Required for Google Speech Recognition and Google Maps APIs.
*   **Speakers/Headphones:** For spoken responses.
*   **Google Maps API Key:** (For Walking Directions example)

### Installation

1.  **Clone the repo:**
    ```bash
    git clone https://github.com/rushikesh648/VoiceAndTouchCommandSystem.git
    cd VoiceAndTouchCommandSystem
    ```
  

2.  **Install Python packages:**
    ```bash
    pip install SpeechRecognition gTTS requests
    ```

3.  **Install `PyAudio` (for microphone input):**
    This can be platform-specific.
    *   **Windows:**
        ```bash
        pip install pipwin
        pipwin install PyAudio
        ```
    *   **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt-get update
        sudo apt-get install python3-pyaudio
        pip install PyAudio
        ```
    *   **macOS:**
        ```bash
        brew install portaudio
        pip install PyAudio
        ```

4.  **Install an audio player (for `gTTS` output):**
    The `os.system()` calls in `speak()` function depend on command-line audio players.
    *   **Linux:** `sudo apt-get install mpg321` (if using `mpg321`)
    *   **macOS:** `afplay` is usually built-in.
    *   **Windows:** The `start` command might work, or you might need to configure a specific player. Alternatively, you can use `pygame` or `playsound` (though `playsound` can have cross-platform issues).

### Configuration

1.  **Google Maps API Key:**
    Edit the Python files (`your_python_directions_script.py` and potentially others) and replace `"YOUR_GOOGLE_MAPS_API_KEY"` with your key.

2.  **IoT API Configuration:**
    If you're integrating with real IoT devices, modify the `control_iot_device` function in your IoT script to make actual API calls or MQTT messages to your devices. Update relevant URLs and tokens.

## Usage

*   **For Voice Commands:**
    Run the respective Python script:
    ```bash
    python your_python_iot_script.py
    # or
    python your_python_directions_script.py
    ```
    Then, speak the specified wake word and commands.

*   **For Touch Commands:**
    Open `index.html` in a web browser on a touch-enabled device.

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/rushikesh648/VoiceAndTouchCommandSystem](https://github.com/rushikesh648/VoiceAndTouchCommandSystem)
