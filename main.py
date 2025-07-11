import speech_recognition as sr
import pyttsx3
import pywhatkit
import requests
import random

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Function to make Luna speak and print
def talk(text):
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to listen and convert voice to text
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)  # Helps reduce noise impact
            voice = listener.listen(source, timeout=10, phrase_time_limit=10)  # Increased listening time
            command = listener.recognize_google(voice)
            command = command.lower()
            print(f"You said: {command}")
            return command
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that. Could you repeat?")
        return ""
    except sr.RequestError:
        talk("Sorry, there seems to be an issue with the speech recognition service.")
        return ""

# Function to get the meaning of a word using an API
def get_word_meaning(word):
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if response.status_code == 200:
            data = response.json()
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            return definition
        else:
            return None
    except:
        return None

# List of jokes Luna can tell
jokes = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "I told my computer I needed a break, and now it won’t stop sending me Kit-Kats!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "I'm reading a book on anti-gravity. It's impossible to put down!",
    "Why don't skeletons fight each other? They don't have the guts!"
]

# List of phrases Luna can say
phrases = [
    "Believe in yourself!",
    "You are doing great, keep going!",
    "Every day is a new opportunity to be better!",
    "Success starts with self-belief!",
    "The only way to do great work is to love what you do."
]

# Improved conversational assistant logic
def run_assistant():
    command = take_command()

    if 'play' in command:
        song = command.replace('play', '').replace('a', '').replace('music', '').replace('song', '').strip()
        if not song:
            song = "music"
        talk(f"Sure Sir! Playing {song} for you. Enjoy!")
        pywhatkit.playonyt(song)
        talk("I'm going silent now. Let me know if you need anything else.")

    elif 'what is your name' in command:
        talk("My name is Luna.")

    elif 'thank you' in command or 'thanks' in command:
        talk("You're welcome! It was a pleasure helping you. Goodbye!")
        return False  # Exit loop gracefully

    elif 'who are you' in command:
        talk("I am your personal assistant. You can call me Luna.")

    elif 'how are you' in command:
        talk("I'm doing great, thanks for asking! How about you?")

    elif 'i am good' in command or 'i am fine' in command:
        talk("That's great!")

    elif 'who is your creator' in command:
        talk("My creator is Hrushikesh Harde. He is super awesome!")

    elif 'what can you do' in command or 'help' in command:
        talk("I can play songs, tell jokes, search the web, tell meanings of words, and share positive phrases with you. Just ask!")

    elif 'meaning of' in command:
        word = command.replace('meaning of', '').strip()
        if word:
            meaning = get_word_meaning(word)
            if meaning:
                talk(f"The meaning of {word} is: {meaning}")
            else:
                talk(f"Sorry, I couldn't find the meaning of {word}. Maybe try another word?")
        else:
            talk("I didn't quite catch the word. Can you say the word again after 'meaning of'?")

    elif 'tell a joke' in command:
        joke = random.choice(jokes)  # Pick a random joke
        talk(f"Here's a joke for you: {joke}")

    elif 'tell a phrase' in command:
        phrase = random.choice(phrases)  # Pick a random phrase
        talk(f"Here's a phrase: {phrase}")

    elif ' Ok Thank You For Your help' in command or 'exit' in command:
        talk("Goodbye! I'm always here if you need me!")
        return False  # Exit loop gracefully

    else:
        talk("Oops, I didn't quite get that. Can you say it again?")

    return True  # Keep listening

# Start listening loop
while True:
    if not run_assistant():
        break  # Exit the loop when 'thank you'
