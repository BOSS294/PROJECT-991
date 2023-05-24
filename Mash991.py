import speech_recognition as sr
import pyttsx3

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Function to perform speech recognition
def recognize_speech():
    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise levels
        r.adjust_for_ambient_noise(source)

        # Capture the audio
        audio = r.listen(source)

        print("Recognizing...")

        try:
            # Convert speech to text
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            print("Speech recognition could not understand audio.")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))

    # If an error occurred or no speech was recognized, return an empty string
    return ""

# Function to generate speech from text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# Main function
def main():
    running = False
    while True:
        if not running:
            speak_text("Hello! I can perform math calculations. Say 'math' for math calculations or 'speech' for regular speech processing.")
            user_input = recognize_speech()
            if user_input.lower() == "1":
                running = True
                speak_text("Sure! You can provide a mathematical expression.")
            elif user_input.lower() == "speech":
                running = False
                speak_text("Alright! I will continue processing speech input.")
            else:
                speak_text("Sorry, I didn't understand. Please say 'math' or 'speech'.")
        else:
            speak_text("Please provide a mathematical expression or say 'stop' to pause math calculations.")
            user_input = recognize_speech()
            if user_input.lower() == "stop":
                running = False
                speak_text("Paused math calculations.")
            else:
                try:
                    result = eval(user_input)
                    response = "The result is: " + str(result)
                except Exception:
                    response = "Sorry, I couldn't compute the expression."

                print(response)
                speak_text(response)

# Run the main function
if __name__ == "__main__":
    main()
