# AI Video Analysis with OpenAI GPT4o

I had an idea for a way to analize video B-Roll (non-talking clips) by creating storyboards and sending those to ChatGPT.
Anyway that was about 12 hours ago. It's currently 6am and I can't be bothered. 

Would love any and all feedback or thoughts on the aproach.
I only started coding a couple months ago so I'm really just winging it with Cursor.

it's seems to work supprisinly well.

I currently have it set up as a flask REST API with PythonAnywhere that takes direct the video url and returns timestamped analasys.

### Instuctions 

I guess get an OpenAI API KEY and slap it in a .env then try running the flask_app.py and go to this link..

http://127.0.0.1:5000?url={insert-direct-video-url}

