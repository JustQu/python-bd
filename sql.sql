CREATE TABLE `users` (
  `id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `login` VARCHAR(20) UNIQUE NOT NULL,
  `group` ENUM ('admin', 'editor', 'user') NOT NULL DEFAULT('user'),
  `created_at` TIMESTAMP NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `user_passwd` (
  `user_id` INT,
  `user_passwd` VARCHAR(255),
  `auth_tok` VARCHAR(255)
);

CREATE TABLE `games` (
  `game_id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `game_name` VARCHAR(255) NOT NULL UNIQUE,
  `release_date` DATE,
  `rating` FLOAT NOT NULL,
  `description` TEXT
);

CREATE TABLE `genres` (
  `genre_id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `genre_name` VARCHAR(255) UNIQUE
);

CREATE TABLE `developers` (
  `developer_id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `developer_name` VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE `publishers` (
  `publisher_id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `publisher_name` VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE `platforms` (
  `platform_id` INT UNIQUE PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `platform_name` VARCHAR(255) UNIQUE
);

CREATE TABLE `rewiews` (
  `user_id` INT NOT NULL,
  `game_id` INT NOT NULL,
  `user_rating` FLOAT NOT NULL,
  `text` VARCHAR(2000) NOT NULL
);

CREATE TABLE `game_platform` (
  `game_id` INT NOT NULL,
  `platform_id` INT
);

CREATE TABLE `game_genre` (
  `game_id` INT NOT NULL,
  `genre_id` INT
);

CREATE TABLE `game_developer` (
  `game_id` INT,
  `developer_id` INT
);

CREATE TABLE `game_publisher` (
  `game_id` INT NOT NULL,
  `publisher_id` INT
);

CREATE TABLE `pictures` (
  `game_id` INT,
  `source` blob
);

ALTER TABLE `rewiews` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

ALTER TABLE `rewiews` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE;

ALTER TABLE `game_platform` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE;

ALTER TABLE `game_platform` ADD FOREIGN KEY (`platform_id`) REFERENCES `platforms` (`platform_id`);

ALTER TABLE `game_publisher` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE;

ALTER TABLE `game_publisher` ADD FOREIGN KEY (`publisher_id`) REFERENCES `publishers` (`publisher_id`);

ALTER TABLE `game_genre` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE;

ALTER TABLE `game_genre` ADD FOREIGN KEY (`genre_id`) REFERENCES `genres` (`genre_id`);

ALTER TABLE `pictures` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE;

ALTER TABLE `user_passwd` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `game_developer` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`) ON DELETE CASCADE;

ALTER TABLE `game_developer` ADD FOREIGN KEY (`developer_id`) REFERENCES `developers` (`developer_id`);

INSERT INTO `users` (`login`, `group`)
	VALUES
	('dmelessa', 'admin'),
	('xxx_xxx', 'user');

INSERT INTO `user_passwd`(`user_id`, `user_passwd`, `auth_tok`)
	VALUES
	(1, '4d9dfca096f6b6cc672707a80f3a42a96ddcf488972e61163858348b69b747df48462c58db26afb82a84dbf1f5073065d5d9083e3c8e114a112dd45cf887f099', NULL);

INSERT INTO `genres` (`genre_name`)
	VALUES
	('rpg'),
	('action'),
	('adventure'),
	('fighting'),
	('platform'),
	('puzzle'),
	('racing'),
	('shooter'),
	('simulation'),
	('sports'),
	('strategy'),
	('misc');

INSERT INTO `platforms` (`platform_name`)
	VALUES
	('PC'),
	('PS4'),
	('XBOX one'),
	('PS3'),
	('XBOX 360');

-- INSERT INTO `developers` (`developer_name`)
-- 	VALUES
-- 	('CD Projekt Red Studio'),
-- 	('Ubisoft');

-- INSERT INTO `publishers`(`publisher_name`)
-- 	VALUES
-- 	('Bandai Namco Games'),
-- 	('Warner Bros. Interactive Entertainment'),
-- 	('CD Projekt');

-- INSERT INTO `games` (`game_name`, `release_date`, `rating`, `description`)
-- 	SELECT 'The Witcher 3'
-- 	,'2015-05-19'
-- 	,'10'
-- 	,'12/10 best'
-- 	FROM `developers`
-- 	WHERE developer_name = 'CD Projekt Red Studio';
	

-- INSERT INTO `game_publisher`(`game_id`, `publisher_id`)
-- 	SELECT `game_id`, `publisher_id`
-- 	FROM `games`, `publishers`
-- 	WHERE `game_name` = 'The Witcher 3'
-- 	AND `publisher_name` = 'CD Projekt'; 

select games.*, publishers.publisher_name from games join game_publisher using(game_id) inner join publishers using(publisher_id);
select genre_name from genres join game_genre using(genre_id) join games using(game_id) where game_name = 'Nier: Automata'

--select genres.genre_name, publishers.publisher_name, developers.developer_name from games join game_genre using(game_id) inn
--er join genres using(genre_id) join game_publisher using(game_id) inner join publishers using(publisher_id) join game_developer using(game_id
--) inner join developers using (developer_id);

select DISTINCT game_name, release_date, rating
from games
join game_genre using(game_id) join genres using(genre_id)
join game_platform using(game_id) join platforms using(platform_id)
join game_publisher using(game_id) join publishers using(publisher_id)
join game_developer using(game_id) join developers using(developer_id);