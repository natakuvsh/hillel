import peewee

db = peewee.SqliteDatabase('songs_library.sqlite3')


class Artist(peewee.Model):
    name = peewee.CharField()

    class Meta:
        database = db


class Song(peewee.Model):
    name = peewee.CharField()
    duration = peewee.IntegerField()
    artist = peewee.ForeignKeyField(Artist)

    class Meta:
        database = db


if __name__ == '__main__':
    db.create_tables([Artist, Song])