import google.generativeai as genai
import weather  # Assuming you have a `weather` module or library
import environ
import pywhatkit
import schedule
import time
import logging

# Set up logging for errors and success
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables
env = environ.Env()

# API and recipient details
API_KEY = env("geminiapi")
RECIPIENT_NUMBER = '+9779840408526'
# Configure Generative AI
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to fetch weather data
def get_weather_data():
    try:
        morning_condition = weather.morning_result()  # Assuming this fetches the weather data
        return {
            "current_condition_text": morning_condition['current_condition_text'],
            "current_temp": morning_condition['current_temp'],
            "sunrise": morning_condition['sunrise'],
            "sunset": morning_condition['sunset'],
        }
    except KeyError as e:
        logging.error(f"Missing key in weather data: {e}")
    except Exception as e:
        logging.error(f"Unable to fetch weather data: {e}")
    return None

# Function to generate romantic message
def generate_romantic_message(weather_data):
    if not weather_data:
        return "Unable to fetch weather data, but here's a lovely 'Good Morning'!"

    prompt = f'''
    Create a romantic "Good Morning" message with the following inputs:
    Weather Condition: "{weather_data['current_condition_text']}"
    Temperature: "{weather_data['current_temp']}°C"
    Sunrise Time: "{weather_data['sunrise']}"
    Sunset Time: "{weather_data['sunset']}"
    Include:

    - A poetic and romantic greeting.
    - Mention of the weather and temperature in a cozy, heartfelt way.
    - A reference to the sunrise that connects it to love and affection.
    - A sweet or flirty note to brighten the recipient's day.
    - A romantic song suggestion.

    Output: Provide only the romantic message in response, with no additional context or explanation.
    '''
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logging.error(f"Error generating romantic message: {e}")
        return "Good morning! Wishing you a beautiful day ahead filled with love and joy."

# Function to send WhatsApp message
def send_whatsapp_message(message):
    try:
        pywhatkit.sendwhatmsg_instantly(RECIPIENT_NUMBER, message)
        logging.info("Message sent successfully!")
    except Exception as e:
        logging.error(f"Error sending WhatsApp message: {e}")

# Scheduler job function
def scheduled_job():
    weather_data = get_weather_data()
    message = generate_romantic_message(weather_data)
    send_whatsapp_message(message)

# Set up the scheduler
schedule.every(20).seconds.do(scheduled_job)

logging.info("Scheduler started. Waiting to send messages...")

# Run the scheduler
if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
