CREATE TABLE IF NOT EXISTS `users` (
        `id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        `login` VARCHAR(20) NOT NULL UNIQUE,
        `group` ENUM('admin', 'editor', 'user') NOT NULL,
        `created_at` DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS `games` (
	`game_id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	`publisher_id` INT NOT NULL,
	`developer_id` INT NOT NULL,
	`release_date` DATE,
	`rating` FLOAT NOT NULL,
	`description` TEXT
);

CREATE TABLE IF NOT EXISTS `genres` (
	`genre_id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	`genre_name` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `developers` (
	`developer_id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	`developer_name` VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `publishers` (
	`publisher_id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	`publisher_name` VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS `platforms` (
	`platform_id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	`platform_name` VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS `rewiews` (
	`user_id` INT NOT NULL,
	`game_id` INT NOT NULL,
	`user_rating` FLOAT NOT NULL,
	`text` VARCHAR(2000) NOT NULL
);

CREATE TABLE IF NOT EXISTS `game_platform` (
	`game_id` INT,
	`platform_id` INT
);

CREATE TABLE IF NOT EXISTS `game_genre` (
	`game_id` INT NOT NULL,
	`genre_id` INT
);

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
	('XBOX one');

INSERT INTO `developers` (`developer_name`)
	VALUES
	('CD Projekt Red'),
	('Ubisoft');