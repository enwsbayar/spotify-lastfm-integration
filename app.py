from flask import Flask, render_template, request, session, redirect
import webbrowser
import json, base_file

app = Flask(__name__)

app.secret_key = 'th1s 1s  4 v3ry s3cure 4pp'

obj = base_file.last_fm_spotify()
songs_data = obj.fetch_songs_from_last_fm()  

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/top', methods=['GET', 'POST'])
def top_songs():  
    if request.method == 'GET':
        return render_template("index.html", top_songs=songs_data, template='top') 
    else:
        if 'id' in session.keys():
          uri = obj.get_uri_from_spotify(songs_data)  
          id = session['id']
          ans = obj.add_songs_to_playlist(id, uri)
          return redirect('/view')
        return redirect('/create')

@app.route('/view')
def view_songs():
    if 'id' in session.keys():
      songs = obj.list_songs_in_playlist(session['id'])
      return render_template("index.html", songs=songs, template='view') 
    return redirect('/create')  

@app.route('/create', methods=['GET', 'POST'])
def create_playlist():
    if request.method == 'GET':
      return render_template("index.html", template='create')
    if request.method == 'POST':
      name = request.form['playlist_name'].strip()
      desc = request.form['playlist_desc'].strip()
      session['id'] = obj.create_spotify_playlist(name, desc)
      return redirect('/top')

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5000')
    app.run()