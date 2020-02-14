import os

from flask import Flask, render_template, request, jsonify, Response

from utils.yt_api_int import download_mp3

app = Flask(__name__, static_folder="./static", template_folder="./static")

# TODO https://developers.google.com/youtube/v3/getting-started 
# you can find instructions here to get a developer key to use youtube data api

devkey="AIzaSyBo8tOc2_oHekRMcZZ5Fxm2waHcx-mp_XM"

ydl_options = {
    'format' : 'bestaudio/best[ext=mp3]',
     'outtmpl' :"%(id)s.%(ext)s",
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
from googleapiclient.discovery import build

@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/yts_query/", methods=['GET'])
def youtube_search_results():
    qry_str = request.args.get('q')
    youtube = build("youtube", "v3", developerKey=devkey)
    search_response = youtube.search().list(
         q=qry_str,
         part="id,snippet",
         maxResults=10,
         type="video"
    ).execute()
    items = search_response.get('items',[])
    return jsonify(items)



@app.route("/dwnlo_mp3/", methods=['GET'])
def get_mp3_audio():
    vid=request.args.get('vid')
    download_mp3(vid, ydl_options)
    def generate():
        with open(vid+'.mp3', "rb") as af:
            data = af.read(1024)
            while data:
                yield data
                data = af.read(1024)
    return Response(generate(), mimetype="audio/mpeg")

if __name__ == "__main__":
    app.run()