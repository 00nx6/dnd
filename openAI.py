import urllib.request
from openai import OpenAI # `poetry add openai`

# Configure the OpenAI API to work through our server (for payment credits)
openai = OpenAI(
    api_key="YOUR_TOKEN_GOES_HERE", # dldr7bh6dp55
    base_url="https://openai.sd42.nl/api/providers/openai/v1"
)

# Ask the LLM for a joke
response = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Tell a short joke."}
    ],
)
joke = response.choices[0].message.content
print(joke)

# Convert the joke to spoken audio and save it as an MP3 file
response = openai.audio.speech.create(model="tts-1", voice="alloy", input=joke)
response.stream_to_file("joke.mp3")

# Create a DALL-E image for the joke
response = openai.images.generate(model="dall-e-3", prompt=joke, quality="standard", n=1, size="1024x1024")
urllib.request.urlretrieve(response.data[0].url, 'joke.png')
