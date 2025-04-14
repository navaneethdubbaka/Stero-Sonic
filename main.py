import datetime
import os
import smtplib
import time
import webbrowser
import cv2
import speech_recognition as sr
import wikipedia
import pyttsx3
import psutil
import pyautogui
import pywhatkit as kit
import spacy
import google.generativeai as genai
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import tkinter as tk
import pandas as pd

# Initialize the recognizer, engine, and camera objects
camera = cv2.VideoCapture(0)
r = sr.Recognizer()
engine = pyttsx3.init()
nlp = spacy.load("en_core_web_sm")

def commandcheck():
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                r.energy_threshold = 300
                r.pause_threshold = 0.5
                audio = r.listen(source)
                print("hi")
                print("Audio captured, recognizing...")

                # Use Google Speech Recognition to transcribe the user's speech
                text = r.recognize_google(audio)
                print("You said: " + text)

                # Check if the command was heard
                if text.lower() == command:
                    say_hello()
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

# Define the command to listen for
command = "sonic"
query_global = ""

# Defining a command to speak text
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Define the action to perform when the command is heard
def say_hello():
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    def wish_me():
        speak("waiting for your command")

    def take_command():
        # It takes microphone input from the user and returns string output
        global query_global
        with sr.Microphone() as source:
            print("WAITING FOR YOUR COMMAND")
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            print("Recognizing the Command")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            query_global = query
        except Exception as e:
            print("I didn't get it. Please say it again, sir.")
            return "None"

        return query

    def send_email(to, content, attachment_path=None):
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.base import MIMEBase
        from email import encoders

        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        # Login to the email account
        server.login('', '')

        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = "your_email@gmail.com"
        message['To'] = to
        message['Subject'] = "Automated Email"

        # Attach the body with the msg instance
        message.attach(MIMEText(content, 'plain'))

        # Attach the file
        if attachment_path:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f"attachment; filename= {os.path.basename(attachment_path)}")
                message.attach(part)

        # Send the message
        text = message.as_string()
        server.sendmail('72011084@sasi.ac.in', to, content)

        # Terminate the SMTP session
        server.quit()

    def windows_search():
        app_name = query_global
        # Split the input string into words
        words = app_name.split()
        # Remove the first word
        if len(words) > 1:
            app_name = ' '.join(words[1:])
        pyautogui.press('winleft')
        time.sleep(1)
        pyautogui.typewrite(app_name)
        time.sleep(1)
        pyautogui.press('enter')

    def close_specific_exe_processes(exe_list):
        try:
            # Iterate through all running processes
            for process in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    # Check if the process is associated with an exe file in the specified list
                    if process.info['exe'] and any(process.info['exe'].endswith(exe) for exe in exe_list):
                        pid = process.info['pid']
                        process_name = process.info['name']
                        # Terminate the process
                        psutil.Process(pid).terminate()
                        print(f"Closed process: {process_name} (PID: {pid})")
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass
            print("All specified exe processes closed successfully.")
        except Exception as e:
            print(f"Error closing specified exe processes: {e}")

    def record_and_save_voice(file_path="C:\\Users\\sushu\\OneDrive\\Desktop\\LETS CODE\\python projects by navaneeth\\noted data by stero.txt"):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Say something...")
                audio_data = recognizer.listen(source, timeout=5)
                print("Recording complete. Converting to text...")
                text = recognizer.recognize_google(audio_data)
                print("Text: {}".format(text))
                with open(file_path, "w") as file:
                    file.write(text)
                print("Text saved to {}".format(file_path))
        except sr.UnknownValueError:
            print("Google Web Speech API could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Web Speech API; {0}".format(e))

    stored_data_path = "C:\\Users\\sushu\\OneDrive\\Desktop\\LETS CODE\\python projects by navaneeth\\stored data.txt"
    def store_data(key, value):
        with open(stored_data_path, 'a+') as file:
            file.seek(0)
            existing_data = file.read()
            file.seek(0, 2)
            if existing_data:
                file.write("\n")
            file.write(f"{key},{value}")

    def retrieve_value(key):
        value = None
        filepath = stored_data_path
        with open(filepath, 'r') as file:
            for line in file:
                k, v = line.strip().split(',')
                if k == key:
                    value = v
                    break
        return value

    def find_and_click_image(image_path, confidence=0.8, timeout=10):
        start_time = time.time()

        while True:
            # Try to locate the image on the screen
            location = pyautogui.locateOnScreen(image_path, confidence=confidence)

            # If the image is found, click it
            if location is not None:
                center = pyautogui.center(location)
                pyautogui.click(center)
                print(f"Image found and clicked at position: {center}")
                return True

            # Check if the timeout has been reached
            if time.time() - start_time > timeout:
                print(f"Image not found within {timeout} seconds.")
                return False

            # Sleep briefly to avoid high CPU usage during the loop
            time.sleep(0.5)

    def capture_screenshot():
        print("capturing the screen")
        root = tk.Tk()
        root.withdraw()

        # Get screen dimensions
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Create a fullscreen window
        selection_window = tk.Toplevel(root)
        selection_window.attributes('-fullscreen', True)


        selection_window.attributes('-alpha', 0.3)  # Semi-transparent
        selection_window.configure(bg='gray')

        start_x = start_y = end_x = end_y = 0
        screenshot_path_var = tk.StringVar()

        def on_button_press(event):
            nonlocal start_x, start_y
            start_x, start_y = event.x, event.y
            canvas.coords(rect, start_x, start_y, start_x, start_y)

        def on_mouse_move(event):
            nonlocal end_x, end_y
            end_x, end_y = event.x, event.y
            canvas.coords(rect, start_x, start_y, end_x, end_y)

        def on_button_release(event):
            nonlocal start_x, start_y, end_x, end_y
            root.quit()
            root.destroy()
            region = (start_x, start_y, end_x - start_x, end_y - start_y)
            screenshot_path = take_screenshot(region)
            screenshot_path_var.set(screenshot_path)

        canvas = tk.Canvas(selection_window, cursor="cross", bg='gray')
        canvas.pack(fill=tk.BOTH, expand=True)
        rect = canvas.create_rectangle(0, 0, 0, 0, outline='red', width=2)

        canvas.bind("<ButtonPress-1>", on_button_press)
        canvas.bind("<B1-Motion>", on_mouse_move)
        canvas.bind("<ButtonRelease-1>", on_button_release)

        root.mainloop()

        return screenshot_path_var.get()

    def take_screenshot(region):
        image_path = r"C:\Users\sushu\OneDrive\Pictures\Screenshots\screenshot.png"
        screenshot = pyautogui.screenshot(region=region)
        screenshot.save(image_path)
        print(f"Screenshot saved to: {image_path}")
        return image_path

    def capture_image_from_camera():
        image_path = r"C:\Users\sushu\OneDrive\Pictures\Screenshots\camera_image.png"
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return False

        ret, frame = cap.read()
        if ret:
            cv2.imwrite(image_path, frame)
            print(f"Image captured and saved to: {image_path}")
            cap.release()
            return image_path
        else:
            print("Error: Could not capture image.")
            cap.release()
            return False

    def upload_image_to_google_lens(image_path):
        try:
            # Setup Chrome WebDriver with keep_alive option
            print("image being uploaded")
            chrome_options = Options()
            chrome_options.add_experimental_option("detach", True)
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # Open Google Lens
            driver.get("https://lens.google.com/")
            print("Opened Google Lens")

            # Allow time for the page to load
            time.sleep(5)

            # Locate and click the "Search by image" button using PyAutoGUI
            button_image_path = r'C:\Users\sushu\PycharmProjects\pythonProject36\img.png'  # Replace with the path to the button image file
            if find_and_click_image(button_image_path):
                # Allow time for the file dialog to open
                time.sleep(3)
                # Use PyAutoGUI to type the file path and press Enter
                pyautogui.write(image_path)
                pyautogui.press('enter')
                print("Uploaded the image")
            else:
                print("Button image not found. Exiting.")
                return

            # Allow time for the image to upload and results to appear
            time.sleep(10)

            print("Image upload completed. Browser will remain open.")
        except Exception as e:
            print(f"An error occurred: {e}")
        # No driver.quit() to keep the browser open

    def use_lens():
        path = capture_image_from_camera()
        upload_image_to_google_lens(path)

    def scan_screen():
        time.sleep(3)
        path = capture_screenshot()
        upload_image_to_google_lens(path)


    def chatbot_bard(prompt):
        genai.configure(api_key="api")
        generation_config = {
            "temperature": 0.9,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 2048,
        }
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]
        model = genai.GenerativeModel(model_name="gemini-1.0-pro", generation_config=generation_config,
                                      safety_settings=safety_settings)
        convo = model.start_chat(history=[
            {"role": "user", "parts": [
                "YOU ARE A CHAT BOT YOURS NAME IS \"STERO SONIC\" YOU WERE CREATED BY NAVANEETH. YOU NEED TO ANSWER ALL THE GENERAL QUESTIONS ASKED BY THE USERS."]},
            {"role": "model", "parts": [
                "Sure, I am STERO SONIC, a chatbot created by Navaneeth. I am here to answer your general questions to the best of my ability."]}
        ])
        convo.send_message(prompt)
        return convo.last.text

    def analyze_dataframe():
        genai.configure(api_key="api")

        # Define the generation configuration
        generation_config = {
            "temperature": 1,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Initialize the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start the chat session
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        "You will be provided with a DataFrame containing specific column names in a Pandas dataset. Based on the operations I want to perform on the DataFrame, you should provide the corresponding Pandas code to achieve those tasks. Also when user asks for visualization you will use NumPy and Matplotlib for better visualization, The code should be clean, well-commented, and optimized for readability.",
                    ],
                },
                {
                    "role": "model",
                    "parts": [
                        "Please provide me with the following information:\n\n1. **DataFrame column names:** A list of the column names in your Pandas DataFrame.\n2. **Desired operations:** Describe the operations you want to perform on the DataFrame. Be specific about:\n    * **Data manipulation:** What transformations do you want to apply to the data (e.g., filtering, sorting, grouping, aggregating, renaming, etc.)?\n    * **Column selection:** Which specific columns are involved in each operation?\n    * **Output:** What kind of output do you expect (e.g., a new DataFrame, a specific value, a visualization)?\n\nOnce you provide this information, I can write the corresponding Pandas code with clear comments and best practices.",
                    ],
                },
            ]
        )

        # Load your DataFrame
        speak("enter the path of the dataset : ")
        path = input("Enter the path of dataset")
        df = pd.read_csv(path)
        columns = df.columns

        # Prompt the user for a task
        speak("what task you want to perform on the dataset: ")
        x = take_command()

        # Construct the message for the model
        y = f"The dataframe contains the columns {columns}. Now, {x},if result was a dataframe dont forget to print the dataframe,Please provide only the code lines, nothing extra."

        # Send the message to the model
        chat_session.send_message(y)
        response = chat_session.last.text
        # print(response)
        # Clean the response to remove any unnecessary formatting
        cleaned_code = response.replace("```python", "").replace("```", "").strip()
        print(cleaned_code)
        # Execute the cleaned code
        try:
            exec(cleaned_code)
        except Exception as e:
            print(f"An error occurred while executing the code: {e}")

    def search_wikipedia():
        speak('what do you want me browse for ')
        query = take_command()
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    def open_youtube():
        speak("What do you want me to search for on YouTube?")
        query = take_command()
        url = f"https://www.youtube.com/search?q={query}"
        webbrowser.open(url)

    def note_down():
        speak("What do you want me to note down")
        record_and_save_voice("noted_data.txt")

    def open_stackoverflow():
        webbrowser.open("https://stackoverflow.com")

    def play_music():
        music_dir = r"E:\Music"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))

    def get_time():
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {str_time}")

    def open_mirror():
        while True:
            ret, frame = camera.read()
            cv2.imshow('Camera Feed', frame)
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()

    def Switch_win():
        pyautogui.keyDown('alt')
        pyautogui.press('tab')
        time.sleep(1)
        pyautogui.keyUp('alt')


    def get_contact_number(name):
        try:
            with open('C:\\Users\\sushu\\PycharmProjects\\pythonProject36\\contacts.txt', 'r') as file:
                contacts = dict(line.strip().split(',') for line in file)
                return contacts.get(name)
        except FileNotFoundError:
            print("Contacts file not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return None


    def send_whatsapp_message():
        try:
            # Prompt the user for the necessary information
            speak("whom you want to send message")
            name = take_command().lower()
            phone_number = get_contact_number(name)
            print(phone_number)
            speak("What should I text ")
            message = take_command()
            # Send the message instantly (appear in the text field)
            kit.sendwhatmsg_instantly(phone_number, message, 10, tab_close=False)

            # Wait for the message to be typed out
            time.sleep(15)

            # Press Enter to send the message
            pyautogui.press('enter')
            print("Message sent successfully.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")



    def store_data_command():
        speak("TELL ME THE KEY")
        key = take_command()
        speak("TELL ME THE VALUE")
        value = take_command()
        store_data(key, value)
        speak("Data stored successfully.")

    def retrieve_data_command():
        speak("tell me the key")
        key = take_command()
        result = retrieve_value(key)
        if result:
            speak(result)
        else:
            speak("value does not exist")

    def send_mail_command():
        try:
            speak("Enter the email address (without @gmail.com)")
            email_prefix = input("Enter the email address (without @gmail.com): ")

            if not email_prefix:
                speak("The email address cannot be empty.")
                return

            to = f"{email_prefix}@gmail.com"

            speak("What should I say?")
            content = take_command()

            if not content:
                speak("The email content cannot be empty.")
                return

            speak("Do you want to attach a file? Say yes or no.")
            attach_file_response = take_command().lower()

            attachment_path = None
            if 'yes' in attach_file_response:
                speak("Please provide the file path of the attachment.")
                attachment_path = input("Enter the file path of the attachment: ")

                if not os.path.isfile(attachment_path):
                    speak("The provided file path is invalid. No attachment will be sent.")
                    attachment_path = None

            send_email(to, content, attachment_path)
            speak("Email sent successfully.")
        except Exception as e:
            speak(f"An error occurred: {str(e)}")

    def take_selfie():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open webcam.")
            return
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not capture frame.")
            cap.release()
            return
        image_filename = "captured_image.jpg"
        cv2.imwrite(image_filename, frame)
        print(f"Image saved as {image_filename}")
        cap.release()
        cv2.destroyAllWindows()

    def open_google():
        speak("What do you want me to search for on Google?")
        query = take_command()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)

    def close_all_windows():
        exe_to_close = ['notepad.exe', 'chrome.exe', 'WhatsApp.exe']
        close_specific_exe_processes(exe_to_close)

    def help_me_research():
        speak("What do you need help with?")
        prompt = take_command()
        response = chatbot_bard(prompt)
        print(response)
        speak(response)

    def who_are_you():
        speak("I am Stereo Sonic, created by Navaneeth. I can help you with daily tasks.")

    def switch_to_chatbot_mode():
        speak("Activating Chatbot mode.")
        chatbot_mode()

    def intent_mapping(command):
        doc = nlp(command.lower())

        patterns = {
            "wikipedia": [("search", "VERB"), ("wikipedia", "PROPN")],
            "youtube": [("search", "VERB"), ("youtube", "PROPN")],
            "note down": [("note", "NOUN"), ("down", "PART")],
            "stackoverflow": [("search", "VERB"), ("stackoverflow", "PROPN")],
            "music": [("play", "VERB"), ("music", "NOUN")],
            "time": [("time", "NOUN")],
            "mirror": [("open", "VERB"), ("mirror", "NOUN")],
            "store": [("store", "VERB"), ("data", "NOUN")],
            "retrieve": [("retrieve", "VERB"), ("data", "NOUN")],
            "email": [("send", "VERB"), ("email", "NOUN")],
            "selfie": [("take", "VERB"), ("selfie", "NOUN")],
            "Google": [("search", "VERB"), ("Google", "PROPN")],
            "close windows": [("close", "VERB"), ("windows", "NOUN")],
            "research": [("help", "VERB"), ("research", "NOUN")],
            "who are you": [("who", "PRON"), ("are", "VERB"), ("you", "PRON")],
            "send message": [("send", "VERB"), ("message", "NOUN")],
            "activate chatbot": [("activate", "VERB"), ("chatbot", "NOUN")],
            "switch windows": [("switch", "VERB"), ("windows", "NOUN")],
            "open lens": [("open", "VERB"), ("lens", "NOUN")],
            "scan the screen": [("scan", "VERB"), ("screen", "NOUN")],
            "open": [("open", "VERB")],
            "analyse data": [("analyse", "VERB"), ("data", "NOUN")]
        }

        for intent, key_parts in patterns.items():
            if all(keyword in [token.text for token in doc] and
                   any(tag == pos for _, pos in key_parts for token in doc if token.text == keyword)
                   for keyword, tag in key_parts):
                return intent

        return None

    def handle_commands():
        intent_functions = {
            "wikipedia": search_wikipedia,
            "youtube": open_youtube,
            "note down": note_down,
            "stackoverflow": open_stackoverflow,
            "music": play_music,
            "time": get_time,
            "mirror": open_mirror,
            "store": store_data_command,
            "retrieve": retrieve_data_command,
            "email": send_mail_command,
            "selfie": take_selfie,
            "Google": open_google,
            "close windows": close_all_windows,
            "research": help_me_research,
            "who are you": who_are_you,
            "send message": send_whatsapp_message,
            "activate chatbot": switch_to_chatbot_mode,
            "switch windows": Switch_win,
            "open lens": use_lens,
            "scan the screen": scan_screen,
            "open": windows_search,
            "analyse data": analyze_dataframe,
        }

        while True:
            query = take_command()
            if query:
                print(f"Processing command: {query}")
                intent = intent_mapping(query)
                if intent and intent in intent_functions:
                    intent_functions[intent]()
                else:
                    print("Command not recognized. Please try again.")

    def chatbot_mode():
        while True:
            query = take_command()
            if query == "activate general mode":
                speak("switching to general mode")
                commandcheck()
            else:
                response = chatbot_bard(query)
                print(response)
                speak(response)

    handle_commands()
commandcheck()




