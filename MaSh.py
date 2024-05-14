import pyttsx3
import speech_recognition as sr
import random
import time
import psutil
import re
import datetime
from plyer import notification

# Function to change voice of the assistant
def change_voice():
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    # Change index to choose a different voice
    engine.setProperty('voice', voices[1].id)
    return engine

welcome_message1= [
    "Welcome back, sir. It's great to have you here!",
    "Hey there! Welcome back, my friend.",
    "Good day, sir! Your presence always brightens my day.",
    "Hello! It's a pleasure to see you again.",
    "Welcome back Sir! Your visit is always appreciated.",
    "Hi there! I hope you're ready for some delightful conversation.",
    "Greetings, sir! Your return brings joy to this place.",
    "Ahoy! Welcome back, captain. Smooth sailing ahead!",
    "Salutations Sir! Your presence makes this place feel like home.",
    "Welcome back, Sir! Your company is cherished here."
]

# Function to create notifications
def create_notification(title, message, timeout=5):
    notification.notify(
        title=title,
        message=message,
        timeout=timeout
    )

def process_user_query(user_input):
    if "battery" in user_input.lower():
        return get_battery_percentage()
    elif "cpu" in user_input.lower():
        return get_cpu_usage()
    elif "system information" in user_input.lower():
        return get_system_info()
    elif "date" in user_input.lower():
        return get_date()
    elif "time" in user_input.lower():
        return get_time()
    elif any(question in user_input.lower() for question, _ in casual_talks):
        return get_random_casual_talk()
    else:
        return get_ai_response(user_input)


def get_time():
    current_time = datetime.datetime.now().strftime("%H:%M")

    return f"The current time is {current_time}."

def get_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return f"Today's date is {current_date}."

def get_battery_percentage():
    try:
        battery_percentage = psutil.sensors_battery().percent
        return f"Your current battery percentage is {battery_percentage}%."
    except Exception as e:
        return f"Sorry, I couldn't retrieve the battery information. Error: {e}"

def get_cpu_usage():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        return f"Your current CPU usage is {cpu_usage}%."
    except Exception as e:
        return f"Sorry, I couldn't retrieve the CPU information. Error: {e}"

def get_appreciation_response(user_input):
    appreciation_keywords = ["very good", "good job", "well done", "nice work", "impressive", "good"]

    for keyword in appreciation_keywords:
        if keyword in user_input.lower():
            # Return a random thank you response
            thank_you_responses = [
                "Thank you, sir!",
                "I appreciate your kind words.",
                "It's my pleasure to assist you!",
                "Thank you for your appreciation!",
                "I'm here to help. Thank you!",
            ]
            return random.choice(thank_you_responses)

    # If no specific appreciation, return None
    return None


def get_system_info():
    try:
        # Get CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)
        cpu_info = f"Your current CPU usage is {cpu_usage}%."

        # Get memory usage
        memory_info = psutil.virtual_memory()
        memory_used = memory_info.used / (1024 ** 3)  # Convert to gigabytes
        memory_total = memory_info.total / (1024 ** 3)  # Convert to gigabytes
        memory_usage = f"Your current memory usage is {memory_used:.2f} GB out of {memory_total:.2f} GB."

        # Get disk usage
        disk_info = psutil.disk_usage("/")
        disk_used = disk_info.used / (1024 ** 3)  # Convert to gigabytes
        disk_total = disk_info.total / (1024 ** 3)  # Convert to gigabytes
        disk_usage = f"Your current disk usage is {disk_used:.2f} GB out of {disk_total:.2f} GB."

        return f"{cpu_info} {memory_usage} {disk_usage}"

    except Exception as e:
        return f"Sorry, I couldn't retrieve the system information. Error: {e}"
def get_ai_response(user_input):
    # Basic NLP-based responses
    responses = {
        "hello": "Hello! How can I help you today?",
        "how are you": "I'm doing well, thank you for asking.",
        "your name": "I'm MASH your virtual assistant created by Bo$$ .",
        "bye": "Goodbye! Take care.",
        "version": "VERSION MAB3CM",

    }
  # Check for health-related responses
    health_response = get_health_response(user_input)
    if health_response:
        return health_response
    
    # Keyword detection for custom responses
    for keyword in responses:
        if keyword in user_input.lower():
            return responses[keyword]

    # If no specific response, generate a generic one
    return generate_generic_response()

def repeat_user_input():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Say something to copy...")
        audio = recognizer.listen(source)

    try:
        user_input = recognizer.recognize_google(audio)
        print(f"You: {user_input}")
        speak_and_print(f"You said: {user_input}")
        return user_input

   # except sr.UnknownValueError:
       # speak_and_print("Sorry, I could not understand what you said.")

    except sr.RequestError as e:
        print(f"Error connecting to Google Speech Recognition service: {e}")
        speak_and_print("I'm sorry, but there was an error connecting to the speech recognition service.")

    return ""

def monitor_battery():
    battery = psutil.sensors_battery()
    last_percent = battery.percent

    while True:
        battery = psutil.sensors_battery()
        current_percent = battery.percent

        if current_percent < last_percent:
            message = f"Your battery percentage has decreased to {current_percent}%."
            speak_and_print(message)
            last_percent = current_percent

        time.sleep(10)  # Check battery every minute
def generate_generic_response():
    generic_responses = [
        "The best error message is the one that never shows up.",
        "Code is like humor. When you have to explain it, it’s bad.",
        "The only way to learn a new programming language is by writing programs in it.",
        "Programming isn’t about what you know; it’s about what you can figure out.",
        "Code is where the real magic happens.",
        "A good programmer is someone who always looks both ways before crossing a one-way street.",
        "The only way to do great work is to love what you do.",
        "Your limitation—it's only your imagination.",
        "Code is like a poem; it's meant to be read by humans.",
        "Quality is not an act, it is a habit.",
        "The best time to plant a tree was 20 years ago. The second best time is now.",
        "The only place where success comes before work is in the dictionary.",
        "The only true wisdom is in knowing you know nothing.",
        "Success is not final, failure is not fatal: It is the courage to continue that counts.",
        "Do not wait to strike till the iron is hot, but make it hot by striking.",
        "Don't watch the clock; do what it does. Keep going.",
        "Believe you can and you're halfway there.",
        "The future belongs to those who believe in the beauty of their dreams.",
        "The only limit to our realization of tomorrow will be our doubts of today.",
        "If you want to lift yourself up, lift up someone else.",

    ]
    return random.choice(generic_responses)

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

def speak_and_print(text):
    print(f"MASH: {text}")
    speak(text)
    
# Function to get weather updates
def get_weather_update():
    # Code to fetch weather information from an API
    # Example: weather_info = fetch_weather_info()
    # Here, weather_info contains the weather details
    weather_info = "Today's weather: Sunny, with a high of 25°C."
    create_notification("Weather Update", weather_info)
# health_responses.py
def get_health_response(user_input):
    health_responses = {
        "headache": "To relieve a headache, you can try drinking plenty of water, getting some rest, or taking over-the-counter pain relievers.",
        "cough": "For a persistent cough, consider drinking warm tea with honey, using a humidifier, or taking cough syrup.",
        "fever": "If you have a fever, it's essential to rest, stay hydrated, and take fever-reducing medications as recommended by your doctor.",
        "sore throat": "For a sore throat, you might find relief by gargling with warm saltwater, staying hydrated, and using throat lozenges.",
        "fatigue": "If you're feeling fatigued, make sure to get enough sleep, eat a balanced diet, and engage in regular physical activity.",
        "stomachache": "For a stomachache, consider avoiding heavy or spicy foods, drinking peppermint tea, and using a heating pad.",
        "insomnia": "If you're having trouble sleeping, establish a regular sleep schedule, create a relaxing bedtime routine, and avoid stimulants before bedtime.",
        # Add more health-related responses as needed
    }

    # Keyword detection for health responses
    for keyword in health_responses:
        if keyword in user_input.lower():
            return health_responses[keyword]

    # If no specific health response, return a generic message
    return None


casual_talks = [
    ("How's the weather today?", [
        "It's sunny outside!",
        "It's a bit cloudy, but not too bad.",
        "Looks like rain is on the way.",
        "I heard it's going to be a hot day!",
        "It's perfect weather for a picnic!"
    ]),
    ("What did you do over the weekend?", [
        "I relaxed and caught up on some reading.",
        "I went hiking with friends.",
        "I watched a movie marathon.",
        "I visited some family members.",
        "I explored a new city."
    ]),
    ("Have you watched any good movies lately?", [
        "Yes, I watched a comedy film that was really funny.",
        "I saw a gripping thriller that kept me on the edge of my seat.",
        "I watched a heartwarming drama that made me cry.",
        "I enjoyed a classic movie from the 80s.",
        "I watched a documentary that was really informative."
    ]),
    ("Do you have any plans for the evening?", [
        "I'm thinking of going for a walk in the park.",
        "I'm meeting up with friends for dinner.",
        "I have a yoga class scheduled.",
        "I'm staying in and catching up on some work.",
        "I'm planning to try out a new recipe."
    ]),
    ("What's your favorite food?", [
        "I love pizza! What about you?",
        "I'm a big fan of sushi.",
        "My favorite food is definitely pasta.",
        "I can't resist a good burger.",
        "I enjoy trying new dishes from different cuisines."
    ]),
    # Add more casual talks with their replies here
]

def get_random_casual_talk():
    question, replies = random.choice(casual_talks)
    return f"{question} {random.choice(replies)}"

unheard_responces = ["\033[31mYour last command could\'t be heard...\033[0m", "\033[31mPlease say that again?\033[0m", "\033[31mPlease speak louder!\033[0m", "\033[31mSpeak clearly sir!\033[0m", "\033[31mPardon?\033[0m"]

def listen_to_user():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    
    try:
        print("Recognizing.....")
        user_input = recognizer.recognize_google(audio)
        print(f"You said: {user_input}")

        # Check for affirmative gestures
        if re.match(r"^(can you|will you|could you|would you)", user_input.lower()):
            response = "Yes, of course! "
            response += process_user_query(user_input)
            return response

        # Check for the copy command
        if "copy me" in user_input.lower():
            repeat_user_input()

        # Check for appreciation keywords
        appreciation_response = get_appreciation_response(user_input)
        if appreciation_response:
            return appreciation_response

        # Process specific queries and trigger corresponding functions
        return process_user_query(user_input)
    except Exception:
        RandomResponce = unheard_responces[random.randint(0, len(unheard_responces)-1)]
        print(RandomResponce)
        #speak(RandomResponce)
        return "None"


def welcome_message():
    speak_and_print(random.choice(welcome_message1))
    create_notification("MaSh","MaSh is now online & functioning")
    
def main():
    try:
        # Initialize pyttsx3 engine with a different voice
        engine = change_voice()

        # Deliver a welcome message with a notification
        welcome_message()

        while True:
            # Listen to user input
            user_input = listen_to_user()

            # Process user input and generate response
            response = process_user_query(user_input)

            # Speak and print the response
            speak_and_print(response)

            # Check for weather update feature
            if "weather" in user_input.lower():
                get_weather_update()
            
            elif 'sleep' in query or 'sleep now' in query or 'take a break' in query or 'rest now' in query or 'you can sleep now' in query or "keep quite" in query or 'rest' in query:
                speak("Okay sir, don\'t forget to call me again if required.")
                speak("Sleep mode activated...")
                create_notification("MaSh","Sleep mode activated.")
                break #for exiting command loop, wake up or shutdown now...

    except Exception as e:
        print(f"Unexpected error: {e}")
        speak_and_print("I'm sorry, but an unexpected error occurred. Please try again later.")
    monitor_battery()


if __name__ == "__main__":

    UnlockCounter = 0
    speak("Hey there, My access is password protected to restrict any unknown guy to use me. ")
    speak("If you're verified person then you probably be having the password, please write it down.")
    
    while UnlockCounter<3:
        password = input("Enter the password: ")
        if password=="test":
            speak("Welcome back sir, initiating the start protocol")
            UnlockCounter=3

        else:
            speak("You dumbass!! get the fuck out of here, don't do hit and trial to get my access")
            speak("Don\'t you dare to open me back again until you have the password.")
            UnlockCounter+=1
            print("You have", 3-UnlockCounter, "attempt(s) remaining")
    

    while True:
        speak("Initializing the workspace....")
        speak("Successfully initiated, waiting for your orders to start... ")

        user_input = listen_to_user()
        permission = user_input.lower()
        if ('wake up' in permission) or ('start' in permission) or ('work' in permission) or ('working' in permission) or ('workspace' in permission):
            create_notification("MaSh","MaSh is now activated. waiting for orders to start")
            main()
        
        elif ('goodbye' in permission) or ('shutdown' in permission) or ('shut' in permission) or ('down' in permission):
           speak("Do You want me to shutdown sir")
           query = user_input.lower()

           if ('no' in query) or ('cancel' in query) or ('nah' in query):
               speak("Process cancelled")

           if ('yes' in query) or ('yep' in query) or ('shutdown' in query) or ('down' in query) or ('shut' in query):
                
                hour = int(datetime.datetime.now().hour)
                if hour>=0 and hour<18:
                    speak("Alright, Have a nice day ahead sir!")
                    speak("Shutting down...")
                    create_notification("MaSh","MaSh is now de-activated")
                    exit()

                elif hour>=18 and hour<24:
                    speak("Ok, good night sir")
                    speak("Shutting down...")
                    create_notification("MaSh","MaSh is now deactivated")
                    exit()
