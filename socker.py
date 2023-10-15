import socket
from googletrans import Translator
import google.generativeai as palm
import re

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Define the host and port to listen on
host = "127.0.0.1"
port = 12344

# Bind the socket to the host and port
server_socket.bind((host, port))

# Start listening for incoming connections
server_socket.listen()
translator = Translator()
language_codes = {
    'Afrikaans': 'af',
    'Albanian': 'sq',
    'Arabic': 'ar',
    'Armenian': 'hy',
    'Azerbaijani': 'az',
    'Bengali': 'bn',
    'Bosnian': 'bs',
    'Bulgarian': 'bg',
    'Chinese (Simplified)': 'zh-cn',
    'Chinese (Traditional)': 'zh-tw',
    'Croatian': 'hr',
    'Czech': 'cs',
    'Danish': 'da',
    'Dutch': 'nl',
    'Estonian': 'et',
    'Finnish': 'fi',
    'German': 'de',
    'Greek': 'el',
    'Haitian Creole': 'ht',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Hungarian': 'hu',
    'Icelandic': 'is',
    'Indonesian': 'id',
    'Italian': 'it',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Latvian': 'lv',
    'Lithuanian': 'lt',
    'Macedonian': 'mk',
    'Malay': 'ms',
    'Maltese': 'mt',
    'Norwegian': 'no',
    'Persian': 'fa',
    'Polish': 'pl',
    'Portuguese': 'pt',
    'Romanian': 'ro',
    'Russian': 'ru',
    'Serbian': 'sr',
    'Slovak': 'sk',
    'Slovenian': 'sl',
    'Swahili': 'sw',
    'Swedish': 'sv',
    'Tamil': 'ta',
    'Thai': 'th',
    'Turkish': 'tr',
    'Ukrainian': 'uk',
    'Urdu': 'ur',
    'Vietnamese': 'vi',
    'Welsh': 'cy',
    'Xhosa': 'xh',
    'Yoruba': 'yo',
    'Zulu': 'zu',
    'Kannada': 'kn',
    'Telugu': 'te',
    'Punjabi': 'pa',
    'Gujarati': 'gu',
    'Marathi': 'mr',
    'Oriya': 'or',
    'Bengali': 'bn',
    'Assamese': 'as',
    'Kashmiri': 'ks',
    'Sindhi': 'sd',
    'Nepali': 'ne',
    'Pashto': 'ps',
    'Dari': 'fa-af',
    'Tajik': 'tg',
    'Kazakh': 'kk',
    'Tatar': 'tt',
    'Bashkir': 'ba',
    'Kyrgyz': 'ky',
    'Turkmen': 'tk',
    'Uighur': 'ug',
    'Chuvash': 'cv',
    'Buryat': 'bxr',
    'Mongolian': 'mn',
    'Tibetan': 'bo',
    'Korean': 'ko',
}
def remove_special_chars(text):
    pattern = r'[*#]'
    return re.sub(pattern, '', text)
print(f"Server listening on {host}:{port}")
palm.configure(api_key='AIzaSyAeVEziX5SVO5xC1qg0Riif3MzzXWVsUMc')
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
while True:
    # Accept incoming connections
    client_socket, addr = server_socket.accept()
    # print(f"Accepted connection from {addr}")

    while True:
        # Receive and print messages from the client
        data = client_socket.recv(1024).decode('utf-8')
        if not data:
            # Client disconnected
            # print(f"Client {addr} disconnected")
            break

        # Split the received message into components
        components = data.split('#')
        if len(components) == 3:
            action, language, text = components
            response=""+data
            print(data)
            client_socket.send(response.encode('utf-8'))
            cleaned_string = re.sub(r'\s+', ' ', text)
            text = cleaned_string.strip()

            # Now you can process the received data:
            # - action contains "Correct" or "Translate"
            # - language contains the selected language
            # - text contains the text to be corrected or translated
            # print(f"Action: {action}, Language: {language}, Text: {text}")
            if action=="Correct":
                input_para = text
                prompt = f'Correct the grammar of the text making sure there is meaning of the corrected text given in the source language. The text is: {input_para}'
                fixedprompt = translator.translate(prompt, dest='en').text
                completion = palm.generate_text(
                model=model,
                prompt=fixedprompt,
                temperature=0.7,  # Adjust the temperature as needed
                max_output_tokens=2000,)
                corrected_text = remove_special_chars(completion.result)
                print("\nCORRECTION ACTIVATED\n")
                hoho=corrected_text
                print(hoho)
            elif action=="Translate":
                print("\nTRANSLATE ACTIVATED\n")
                text_to_translate = text
                target_language_name = language
                target_language_code = language_codes.get(target_language_name.title(), 'en')
                hoho = translator.translate(text_to_translate, dest=target_language_code)
                print(hoho.text)
        # You can send a response back to the client if needed
        # response = "Received: " + data

# Close the client socket - This code will not be reached as the outer loop is infinite
client_socket.close()
