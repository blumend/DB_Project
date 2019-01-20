Queries to minimize the DATABASE:

DELETE FROM songs WHERE year=0;
DELETE FROM songs WHERE title in (SELECT title FROM (SELECT title, LENGTH(title) AS a from songs) AS b WHERE b.a > 22);
DELETE FROM songs WHERE artist_familiarity < 0.475;
DELETE FROM artist_location WHERE location="";



