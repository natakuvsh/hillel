from flask import Flask, render_template, request
from models import *
from spotify import *

app = Flask(__name__)

@app.route('/', methods=['get'])
def all_songs():
    context = {'songs': Song.select()}
    return render_template("song_list.html", **context)


@app.route('/add/song', methods=['get', 'post'])
def song_add():
    context = {'artists': Artist.select()}
    if request.method == 'POST':
        """
        Allowing user to enter new artist name.
        Adding it to the "Artist" table and using its id in "Song" table
        """
        try:
            artist = Artist.get(Artist.name == request.form['artist']).id
        except:
            Artist(name=request.form['artist']).save()
            artist = Artist.get(Artist.name == request.form['artist']).id
        # Saving data in "Song" table
        Song(
            name=request.form['name'],
            duration=request.form['duration'],
            artist=artist
        ).save()

    return render_template('add_song.html', **context)


@app.route('/delete/song', methods=['get', 'post'])
def song_delete():
    context = {'songs': Song.select()}
    if request.method == 'POST':
        Song.get(Song.name == request.form['name']).delete_instance()

    return render_template('delete_song.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
