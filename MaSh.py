from flask import Flask, render_template, request
import speech_recognition as sr
import pyttsx3
import webbrowser

app = Flask(__name__)

Build = "0.2"
Name = "MaSh"
datedon = "25/05/2023"
# Initialize the recognizer
r = sr.Recognizer()

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Get available voices
voices = engine.getProperty('voices')

# Set the voice (change the index according to the desired voice)
engine.setProperty('voice', voices[0].id)
#Function to describe the AI
def desc_bot():
    say = f"My name is {Name} i was created on {datedon} and my build is {Build}. I have no feelings yet"
    speak_text(say)

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to process the AI logic
@app.route('/process', methods=['POST'])
def process():
    # Get the speech input from the frontend
    speech = request.form['speech']

    # Perform speech recognition
    text = recognize_speech(speech)

    # Perform AI processing based on the recognized text
    # Add your AI logic and code here
    
    # Return the processed result back to the frontend
    return text

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
            text = text.lower() #to optimize the code
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

# Function to handle math calculations
def handle_math():
    speak_text("Sure! You can provide a mathematical expression.")
    user_input = recognize_speech()
    while user_input != "stop":
        try:
            result = eval(user_input)
            response = "The result is: " + str(result)
        except Exception:
            response = "Sorry, I couldn't compute the expression."

        print(response)
        speak_text(response)

        speak_text("Please provide another mathematical expression or say 'stop' to pause math calculations.")
        user_input = recognize_speech()

    speak_text("Paused math calculations.")

# Function to handle task processing
def handle_tasks():
    speak_text("Alright! I will process tasks.")
    speak_text("Please provide a task to be completed or say 'stop' to pause tasks.")
    user_input = recognize_speech()
    is_on_youtube = False
    while user_input != "stop":
        if user_input.startswith("open"):
            website = user_input.split("open", 1)[1].strip()
            if website == "youtube":
                url = "https://www.youtube.com"
                webbrowser.get().open(url)
                speak_text("Opening YouTube...")
                is_on_youtube = True
            elif website == "email":
                url = "https://www.example.com/email"  # Replace with your desired email URL
                webbrowser.get().open(url)
                speak_text("Opening Email...")
            else:
                speak_text("Sorry, I don't know how to open that website.")
        elif user_input.startswith("search"):
            query = user_input.split("search", 1)[1].strip()
            if is_on_youtube:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.get().open(url)
                speak_text(f"Searching for {query} on YouTube...")
            else:
                speak_text("Sorry, you can only search on YouTube when you are on the YouTube website.")
        else:
            speak_text("Sorry, I couldn't understand the task.")

        speak_text("Please provide another task or say 'stop' to pause tasks.")
        user_input = recognize_speech()

    speak_text("Paused task processing.")

# Main function
def main():
    starting = "Hello, my name is MaSh! I can perform various tasks. Say 'math' for math calculations, 'speech' for regular speech processing, or 'task' to assign me a new task."
    speak_text(starting)
    print(starting)
    running = False
    while True:
        if not running:

            user_input = recognize_speech()
            if user_input == "math":
                running = True
                handle_math()
            elif user_input == "speech":
                running = False
                speak_text("Alright! I will continue processing speech input.")
            elif user_input == "task":
                running = False
                handle_tasks()
            elif user_input == "about":
                running = False
                desc_bot()
            else:
                speak_text("Sorry, I didn't understand. Please say 'math', 'speech', or 'task'.")

# Run the main function
if __name__ == "__main__":

    user_input = recognize_speech()

    if user_input == "mash":
        main()
    else:
        speak_text("Sorry, I didn't understand. Please say 'mash' to begin.")
    
