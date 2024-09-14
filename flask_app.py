from flask import Flask, request, jsonify, Response, after_this_request
import os
import time
import json
import requests
import urllib.request
from create_storyboard import main as create_storyboard
from get_vision_analysis import main as get_vision_analysis


app = Flask(__name__)

current_status = "fready"

@app.route('/')
def home():
    return "Welcome to the Flask app!"

@app.route('/debug', methods=['POST', 'GET'])
def debug():
    message = str(request.args.get('input'))
    data = {'response': message}
    return jsonify(data)



@app.route('/status')
def get_status():

    global current_status
    data = json.dumps({'status': current_status})
    return Response(data)



@app.route('/analize_video')
def analize_video():

    # deconstruct the request
    url = request.args.get('url', default='no url')
    video_name = request.args.get('video_name', default='no-video-name')
    # clean the name
    video_name = video_name.replace(' ', '-')
    
    def download_video(url):
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response, open('video.mp4', 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        return 'video.mp4'
    
    def is_valid_json(json_string):
        try:
            json.loads(json_string)
            return True
        except ValueError:
            return False
    
    video_path = download_video(url)
    print('video downloaded')

    tile_num = create_storyboard(video_path, 'storyboard.png')

    analysis = get_vision_analysis(tile_num)

    data = json.dumps(analysis)
    
    @after_this_request
    def cleanup(response):
        print('cleaning up...')
        try:
            os.remove('video.mp4')
            os.remove('video.mp4_reduced.mp4')
            os.remove('storyboard_analysis.json')
            os.remove('storyboard.png')
            print('removed: video.mp4, video.mp4_reduced.mp4, storyboard_analysis.json, storyboard.png')
        except Exception as e:
            print(f"Error during cleanup: {e}")
        return response

    return Response(data)




if __name__ == '__main__':
    app.run(debug=True)