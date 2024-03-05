import random
import time

# Dummy function
# TODO: This should return the reponse by our RAG modeö


def response_generator(prompt, delay=0.05):
    # Chose random response from a list
    response = random.choice(
        [
            f"Hallo! Was willst du über die Europa Wahl 2024 wissen?",
            f"Guten Tag menschlicher Wähler! Wie kann ich dir helfen?",
            f"Hi! Ich bin ein Politik Chatbot. Frag mich etwas über die Europa Wahl!",
        ]
    )
    # Streaming response: delay is dely between words in seconds
    for word in response.split():
        yield word + " "
        time.sleep(delay)
