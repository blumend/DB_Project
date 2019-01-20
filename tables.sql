
CREATE TABLE artists (
    artist_id VARCHAR(20) NOT NULL PRIMARY KEY,
    artist_name VARCHAR(105),
    artist_familiarity FLOAT(4,3)
);

CREATE TABLE songs (
    song_id VARCHAR(20) NOT NULL PRIMARY KEY,
    song_name VARCHAR(24),
    album_name VARCHAR(55),
    duration FLOAT(7,3),
    year INT,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

CREATE TABLE album (
    album_name VARCHAR(55) NOT NULL PRIMARY KEY,
    year INT,
    FOREIGN KEY (artist_id) REFERENCES artists(artist_id)
);

INSERT INTO artists (artist_id, artist_name, artist_familiarity)
SELECT artist_id, artist_name, artist_location FROM songs;

INSERT INTO songs (song_id, song_name, album_name, duration, year, artist_id)
SELECT song_id, title, album_name, duration, year, artist_id FROM songs;

INSERT INTO albums (album_name, year, artist_id)
SELECT album_name, year, artist_id FROM songs;

CREATE TABLE users(user_id INT(5) AUTO_INCREMENT PRIMARY KEY, highscore INT DEFAULT 0, user_name VARCHAR(12), user_pass VARCHAR(256));


CREATE TABLE artists
  AS (SELECT artist_id, artist_name, artist_familiarity
      FROM songs);

CREATE TABLE artist_locations
  AS (SELECT artist_id, artist_name, artist_location
      FROM artist_location);

CREATE TABLE songs
  AS (SELECT song_id, title as song_name, album_name, duration, year, artist_id
      FROM songs);

CREATE TABLE albums
  AS (SELECT album_name, year, artist_id
      FROM songs);

CREATE TABLE scores(game_id INT(5) AUTO_INCREMENT PRIMARY KEY, score INT(10))

CREATE TABLE high_scores
  AS (SELECT scores.game_id as game_id, scores.score as score, users.user_id as user_id
      FROM scores, users);



INDEXES:

CREATE INDEX idx_artist_id ON artists (artist_id, artist_name);
CREATE INDEX idx_familiarity ON artists (artist_id, artist_familiarity);
CREATE INDEX idx_song_id ON songs (song_id, song_name);
CREATE INDEX idx_song_name ON songs (song_name, artist_id, album_name);
CREATE INDEX idx_duration ON songs (song_name, duration);
CREATE INDEX idx_year ON songs (year ,artist_id, song_name);
CREATE INDEX idx_year2 ON songs (song_name, year);
CREATE INDEX idx_artist_locid ON artist_location (artist_id, artist_name);
CREATE INDEX idx_artist_loc ON artist_location (artist_name, location);