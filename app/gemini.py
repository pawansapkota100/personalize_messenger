import google.generativeai as genai
import weather  # Assuming you have a 'weather' module or library
import environ

# Load environment variables
env = environ.Env()
environ.Env.read_env()  # Load from .env file
api_key = env('geminiapi')
print(f"API Key Loaded: {api_key}")

# Configure Generative AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash") 

# Function to create a romantic good morning message
def morning_message_response():
    # Fetch weather data
    try:
        morning_condition = weather.morning_result()  # Adjust method name as needed
        current_condition_text = morning_condition['current_condition_text']
        current_temp = morning_condition['current_temp']
        sunrise = morning_condition['sunrise']
        sunset = morning_condition['sunset']
    except KeyError as e:
        return f"Error: Missing key in weather data - {e}"
    except Exception as e:
        return f"Error: Unable to fetch weather data - {e}"

    # Generate the prompt
    prompt = f'''
    Create a romantic "Good Morning" message with the following inputs:
    Weather Condition: "{current_condition_text}"
    Temperature: "{current_temp}"°C
    Sunrise Time: "{sunrise}"
    Sunset Time: "{sunset}"
    Include:

    - A poetic and romantic greeting.
    - Mention of the weather and temperature in a cozy, heartfelt way.
    - A reference to the sunrise that connects it to love and affection.
    - A sweet or flirty note to brighten the recipient's day.
    - A romantic song suggestion.

    Output: Provide only the romantic message in response, with no additional context or explanation.
    '''

    # Generate content using the AI model
    try:
        response = model.generate_content(prompt)
        return response.text 
    except Exception as e:
        return f"Error: Unable to generate romantic message - {e}"

# Generate and display the message
message = morning_message_response()


import pywhatkit
pywhatkit.sendwhatmsg_instantly("+9779840408526", message)
