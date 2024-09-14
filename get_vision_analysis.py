import base64
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
openai_api_key = os.getenv('OPENAI_API_KEY')


# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Function to create payload
def create_payload(base64_image, number_of_frames, video_path):
  return {
    "model": "gpt-4o",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": """
            this is a storyboard of the video with 1 frame == 1 second.

            break the video down into sections that describe whats happening on screen so an editer can edit the video using only the clip descriptions
            
            the video is broken down into """ + f"""{number_of_frames}"""+ """ frames

            mark the in and out frames of each section 

            keep the descriptions brief

            never use single quotes in the json, always use double quotes e.g. "NOBS"
            output valid json only. output in one line with no spetial characters
            output only the json, no other text

            output a list, the list must be in this format

            EXAMPLE:
            [{"clip_1": {"in_frame": 0, "out_frame": 5, "description": "A man in a dark red room"}},{"clip_2": {"in_frame": 6, "out_frame": 10, "description": "The man stands up and walks to the door"}}]
            """
          },
          {
            "type": "image_url",
            "image_url": {
              "url": f"data:image/jpeg;base64,{base64_image}"
            }
          }
        ]
      }
    ],
    "max_tokens": 2048
  }

# Function to get vision analysis
def get_vision_analysis(api_key, image_path, number_of_frames, video_path):
  base64_image = encode_image(image_path)
  headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
  }
  payload = create_payload(base64_image, number_of_frames, video_path)
  response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
  
  response_json = response.json()  # Convert response to JSON
  response_content = response_json['choices'][0]['message']['content']
  return response_content

# Function to sterilize JSON
def sterilize_json(raw_string):
    # Replace escape characters and remove unnecessary formatting
    clean_string = raw_string.replace('\\n', '').replace('\\', '').replace('\'', '"')
    
    # Convert the cleaned string into a JSON object
    try:
        json_data = json.loads(clean_string)
        return json_data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None


def main(tile_num):
  analysis = get_vision_analysis(api_key=openai_api_key, image_path="storyboard.png", number_of_frames=tile_num, video_path="video.mp4")
  analysis = sterilize_json(analysis)
  # print('AI Analysis:', analysis)
  with open('storyboard_analysis.json', 'w') as f:
      json.dump(analysis, f, indent=4)
  return analysis


if __name__ == "__main__":
    try:
        print("TESTING GET VISION ANALYSIS")
        main()
        print("PASSED")
    except Exception as e:
        print(f"An error occurred: {e}")



