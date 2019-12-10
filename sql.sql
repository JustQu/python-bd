SET time_zone ='+03:00';

CREATE TABLE IF NOT EXISTS `users` (
        `id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
        `login` VARCHAR(20) NOT NULL UNIQUE,
        `group` ENUM('admin', 'editor', 'user') NOT NULL,
        `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `games` (
	`game_id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	`game_name` VARCHAR(255) NOT NULL,
	`developer_id` INT NOT NULL,
	`release_date` DATE,
	`rating` FLOAT NOT NULL,
	`description` TEXT
);

CREATE TABLE IF NOT EXISTS `genres` (
	`genre_id` INT NOT NULL UNIQUE PRIMARY KEY AUTO_INCREMENT,
	`genre_name` VARCHAR(255) UNIQUE
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
	`game_id` INT NOT NULL,
	`platform_id` INT
);

CREATE TABLE IF NOT EXISTS `game_genre` (
	`game_id` INT NOT NULL,
	`genre_id` INT
);

CREATE TABLE IF NOT EXISTS `game_publisher` (
	`game_id` INT NOT NULL,
	`publisher_id` INT
);

ALTER TABLE `rewiews` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `rewiews` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`);

ALTER TABLE `game_platform` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`);

ALTER TABLE `game_platform` ADD FOREIGN KEY (`platform_id`) REFERENCES `platforms` (`platform_id`);

ALTER TABLE `game_publisher` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`);

ALTER TABLE `game_publisher` ADD FOREIGN KEY (`publisher_id`) REFERENCES `publishers` (`publisher_id`);

ALTER TABLE `games` ADD FOREIGN KEY (`developer_id`) REFERENCES `developers` (`developer_id`);

ALTER TABLE `game_genre` ADD FOREIGN KEY (`game_id`) REFERENCES `games` (`game_id`);

ALTER TABLE `game_genre` ADD FOREIGN KEY (`genre_id`) REFERENCES `genres` (`genre_id`);

INSERT INTO `users` (`login`, `group`)
	VALUES
	('dmelessa', 'admin'),
	('xxx_xxx', 'user');

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
	('CD Projekt Red Studio'),
	('Ubisoft');

INSERT INTO `games` (`game_name`
					,`developer_id`
					,`release_date`
					,`rating`
					,`description`)
	SELECT 'The Witcher 3'
			,developer_id
			,'2015-05-19'
			,'10'
			,'12/10 best'
	FROM `developers`
	WHERE developer_name = 'CD Projekt Red Studio';
	
		