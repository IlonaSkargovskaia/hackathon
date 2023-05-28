
CREATE TABLE movies (
	id serial PRIMARY KEY,
	movie_id INTEGER NOT NULL UNIQUE,
	title VARCHAR ( 100 ) NOT NULL,
	genres VARCHAR ( 200 ) NOT NULL,
	overview TEXT NOT NULL,
	popularity VARCHAR(50),
	poster_path VARCHAR (200),
	release_date DATE
);
