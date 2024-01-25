from PIL import Image
import openai 
import os 
import requests 
from ip import BytesIO

# Import libraries for openai API, os funcionality, http requests and image manipulation

API_KEY_PATH = "api_key.txt"

def save_api_key(api_key):
  api_key = input("Enter your OpenAI api key: ")
  with open(API_KEY_PATH, "w") as f:
    f.write(api_key)

#saves api key to text file

def load_api_key():
  if not os.path.exists(API_KEY_PATH):
    save_api_key()
  with open(API_KEY_PATH, "r") as f:
    return f.read().strip()

#loads api key from text file

def generate_image(api_key, prompt):
  openai.api_key = api_key

  response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="256x256"
  )
  image_url = response['data'][0]['url']

  #download the image from the url
  response = request.get(image_url)
  img_data = BytesIO(response.content)

  return Image.open(img_data)

#from openai documentation:API reference, create image variation

def image_to_ascii(image_path, output_width):
  #list of ascii characters to use for different brightness levels.
  ascii_chars = ["@", "#", "S", "%", "?", "*", "+", ";", ":" ,",","."]

  #convert image to grayscale
  image = Image.open(image_path).convert('L')

  #get aspect ratio
  width, height = image.size
  aspect_ratio = height / float(width)
  output_height = int(output_width * aspect_ratio)

  #resize image to width and height
  image = image.resize((output_width, output_height))

  # Create the ASCII representation
  pixels = list(image.getdata())
  ascii_str = ""
  for pixel_value in pixels:
    ascii_str += ascii_chars[pixel_value // 256]
  ascii_str_len = len(ascii_str)
  ascii_img = ""
  for i in range(0, ascii_str_len, output_width):
    ascii_img += ascii_str[i:i + output_width] + "\n"

  return ascii_img


if __name__ =="__main__": 
  print("for the best experience, set terminal to fullscreen and/or zoom out")
  api_key = load_api_key()
  prompt = input("Enter a prompt for the image: ")
  image = generate_image(api_key, prompt)
  image_path = "temp_image.jpg"
  image.save(image_path)
  ascii_result = image_to_ascii(image_path, 200)
  print(ascii_result)

  #deletes the temporary image
  os.remove(image_path)
  