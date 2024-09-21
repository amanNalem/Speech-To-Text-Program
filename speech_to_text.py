import speech_recognition as sr
import openai

# Set up OpenAI API key
openai.api_key = "OPENAI_API_KEY"  # Replace with your actual OpenAI API key

# Initialize recognizer
r = sr.Recognizer()

def listen_and_recognize():
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening... (You can start speaking now)")
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)  # Increased timeout and phrase time limit
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Please speak again.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; check your network connection: {e}")
            return None
        except sr.WaitTimeoutError:
            print("Listening timed out. Please try again.")
            return None

def extract_key_points(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Extract the key points from the following text:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Summarize the following text in a concise manner:\n\n{text}"}
        ],
        temperature=0.5,
        max_tokens=150
    )
    return response['choices'][0]['message']['content'].strip()

def main():
    while True:
        transcript = listen_and_recognize()
        if transcript:
            print(f"Transcript: {transcript}")

            with open("recognized_speech.txt", "a") as f:  # Append to the file
                f.write(transcript + "\n")

            key_points = extract_key_points(transcript)
            print(f"Key Points: {key_points}")

            summary = summarize_text(transcript)
            print(f"Summary: {summary}")

            # Save key points and summary to files
            with open("keypoints.txt", "a") as f:  # Append to the file
                f.write(key_points + "\n")

            with open("summary.txt", "a") as f:  # Append to the file
                f.write(summary + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram exited by user.")
