import google.generativeai as genai
import os


API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("API Key not found, exiting...")
    exit()

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")


def gen_general_answer(text):
    try:
        response = model.generate_content(f"Please provide the answers for this {text}, try parsing as much as you can.  in a direct fashion, do not say anything else other than the answer in a format of 1- answer, 2- etc...")
        ai_response = response.text  
        print(ai_response) # debugging
        return ai_response
    except Exception as e:
        print(f"Unexpected error occured while checking if the answer is a graphing or math question, {e}")
        return f"Unexpected error occured while generating the answer, {e}"

def if_graphing_or_math(text):
    try:
        response = model.generate_content(f"Are these questions graphing related? {text}, If they are, reply with 'True', or reply with 'False', DO NOT USE ANY PUNCTUATION!")
        ai_response = response.text
        if ai_response == "True":
            return True
        elif ai_response == "False":
            return False
        else:
            return None
    except Exception as e:
        print(f"Unexpected error occured while checking if the answer is a graphing or math question, {e}")
        return f"Unexpected error occured while checking if the answer is a graphing or math question, {e}"
    

