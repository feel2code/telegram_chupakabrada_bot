CREATE TABLE about (
	about_id int8 NOT NULL,
	about_text text NOT NULL
);

CREATE TABLE answers (
	ans_id int4 AUTO_INCREMENT,
	answer text NOT NULL,
	CONSTRAINT answers_pkey PRIMARY KEY (ans_id)
);


CREATE TABLE asking (
	ask_id int8 AUTO_INCREMENT,
	ask_answer text NULL,
	CONSTRAINT asking_pkey PRIMARY KEY (ask_id)
);

CREATE TABLE cities (
	cities_id int8 AUTO_INCREMENT,
	chat_id text NULL,
	city_name text NULL,
	temp int8 NULL,
	expected_day_temp int4 NULL,
	conditions text NULL,
	CONSTRAINT cities_pkey PRIMARY KEY (cities_id)
);

CREATE TABLE course (
	course_name text NULL,
	course_value int8 NULL
);


CREATE TABLE dog_stickers (
	id int8 AUTO_INCREMENT PRIMARY KEY,
	sticker_id text NULL
);


CREATE TABLE films (
	id int8 NULL,
	film_name text NULL,
	link text NULL,
	film_year text NULL
);


CREATE TABLE holidays_iso (
	id int4 AUTO_INCREMENT NOT NULL,
	dt date NULL,
	holiday_name varchar(250) NULL,
	CONSTRAINT holidays_iso_pkey PRIMARY KEY (id)
);

CREATE TABLE holidays_ru (
	id int4 AUTO_INCREMENT NOT NULL,
	dt date NULL,
	holiday_name varchar(250) NULL,
	CONSTRAINT holidays_ru_pkey PRIMARY KEY (id)
);


CREATE TABLE holidays_ru_relative (
	id int4 AUTO_INCREMENT NOT NULL,
	rel_name varchar(200) NULL,
	dt date NULL,
	holiday_name varchar(250) NULL,
	week_num int4 NULL,
	day_num int4 NULL,
	CONSTRAINT holiday_ru_relative_pkey PRIMARY KEY (id)
);


CREATE TABLE markov (
	chat_id int8 NULL,
	hardness int8 NULL
);


CREATE TABLE messages (
	msg_id int8 AUTO_INCREMENT,
	msg_txt text NOT NULL,
	ans_id int8 NOT NULL,
	CONSTRAINT messages_pkey PRIMARY KEY (msg_id)
);


CREATE TABLE months (
	id int8 AUTO_INCREMENT PRIMARY KEY,
	month_name text NULL
);


CREATE TABLE pig_stickers (
	id int8 AUTO_INCREMENT PRIMARY KEY,
	sticker_id text NULL
);


CREATE TABLE questions (
	que_id int4 AUTO_INCREMENT,
	ans_id int4 NOT NULL,
	question text NOT NULL,
	CONSTRAINT questions_pkey PRIMARY KEY (que_id)
);


CREATE TABLE quotes (
	quote_id int4 AUTO_INCREMENT,
	quote_value text NOT NULL,
	CONSTRAINT quotes_pkey PRIMARY KEY (quote_id)
);


CREATE TABLE rolls (
	nick text NULL,
	chat_id int8 NULL,
	cur_date date NULL
);


CREATE TABLE start_q (
	start_id int8 NOT NULL,
	start_text text NOT NULL
);


CREATE TABLE stats (
	stat_id int8 AUTO_INCREMENT,
	st_chat_id text NULL,
	st_name text NULL,
	st_nick text NULL,
	st_date timestamp NULL,
	CONSTRAINT stats_pkey PRIMARY KEY (stat_id)
);


CREATE TABLE stickers (
	sticker_id int4 AUTO_INCREMENT,
	sticker text NOT NULL,
	CONSTRAINT stickers_pkey PRIMARY KEY (sticker_id)
);

alter table holidays_ru_relative add column is_last int4;
update holidays_ru_relative set is_last=1 where rel_name like '%Последн%';
