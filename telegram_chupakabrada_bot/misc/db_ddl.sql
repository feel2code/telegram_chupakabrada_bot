-- public.about definition

-- Drop table

-- DROP TABLE public.about;

CREATE TABLE public.about (
	about_id int8 NOT NULL,
	about_text text NOT NULL
);

-- Permissions

ALTER TABLE public.about OWNER TO postgres;
GRANT ALL ON TABLE public.about TO postgres;


-- public.answers definition

-- Drop table

-- DROP TABLE public.answers;

CREATE TABLE public.answers (
	ans_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	answer text NOT NULL,
	CONSTRAINT answers_pkey PRIMARY KEY (ans_id)
);

-- Permissions

ALTER TABLE public.answers OWNER TO postgres;
GRANT ALL ON TABLE public.answers TO postgres;


-- public.asking definition

-- Drop table

-- DROP TABLE public.asking;

CREATE TABLE public.asking (
	ask_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	ask_answer text NULL,
	CONSTRAINT asking_pkey PRIMARY KEY (ask_id)
);

-- Permissions

ALTER TABLE public.asking OWNER TO postgres;
GRANT ALL ON TABLE public.asking TO postgres;


-- public.cities definition

-- Drop table

-- DROP TABLE public.cities;

CREATE TABLE public.cities (
	cities_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	chat_id text NULL,
	city_name text NULL,
	"temp" int8 NULL,
	expected_day_temp int4 NULL,
	"condition" text NULL,
	CONSTRAINT cities_pkey PRIMARY KEY (cities_id)
);

-- Permissions

ALTER TABLE public.cities OWNER TO postgres;
GRANT ALL ON TABLE public.cities TO postgres;


-- public.course definition

-- Drop table

-- DROP TABLE public.course;

CREATE TABLE public.course (
	course_name text NULL,
	course_value int8 NULL
);

-- Permissions

ALTER TABLE public.course OWNER TO postgres;
GRANT ALL ON TABLE public.course TO postgres;


-- public.dog_stickers definition

-- Drop table

-- DROP TABLE public.dog_stickers;

CREATE TABLE public.dog_stickers (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	sticker_id text NULL
);

-- Permissions

ALTER TABLE public.dog_stickers OWNER TO postgres;
GRANT ALL ON TABLE public.dog_stickers TO postgres;


-- public.films definition

-- Drop table

-- DROP TABLE public.films;

CREATE TABLE public.films (
	id int8 NULL,
	film_name text NULL,
	link text NULL,
	"year" text NULL
);

-- Permissions

ALTER TABLE public.films OWNER TO postgres;
GRANT ALL ON TABLE public.films TO postgres;


-- public.holidays_iso definition

-- Drop table

-- DROP TABLE public.holidays_iso;

CREATE TABLE public.holidays_iso (
	id serial4 NOT NULL,
	dt date NULL,
	holiday_name varchar(250) NULL,
	CONSTRAINT holidays_iso_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.holidays_iso OWNER TO postgres;
GRANT ALL ON TABLE public.holidays_iso TO postgres;


-- public.holidays_ru definition

-- Drop table

-- DROP TABLE public.holidays_ru;

CREATE TABLE public.holidays_ru (
	id serial4 NOT NULL,
	dt date NULL,
	holiday_name varchar(250) NULL,
	CONSTRAINT holidays_ru_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.holidays_ru OWNER TO postgres;
GRANT ALL ON TABLE public.holidays_ru TO postgres;


-- public.holidays_ru_relative definition

-- Drop table

-- DROP TABLE public.holidays_ru_relative;

CREATE TABLE public.holidays_ru_relative (
	id int4 NOT NULL DEFAULT nextval('holiday_ru_relative_id_seq'::regclass),
	rel_name varchar(200) NULL,
	dt date NULL,
	holiday_name varchar(250) NULL,
	week_num int4 NULL,
	day_num int4 NULL,
	CONSTRAINT holiday_ru_relative_pkey PRIMARY KEY (id)
);

-- Permissions

ALTER TABLE public.holidays_ru_relative OWNER TO postgres;
GRANT ALL ON TABLE public.holidays_ru_relative TO postgres;


-- public.markov definition

-- Drop table

-- DROP TABLE public.markov;

CREATE TABLE public.markov (
	chat_id int8 NULL,
	hardness int8 NULL
);

-- Permissions

ALTER TABLE public.markov OWNER TO postgres;
GRANT ALL ON TABLE public.markov TO postgres;


-- public.messages definition

-- Drop table

-- DROP TABLE public.messages;

CREATE TABLE public.messages (
	msg_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	msg_txt text NOT NULL,
	ans_id int8 NOT NULL,
	CONSTRAINT messages_pkey PRIMARY KEY (msg_id)
);

-- Permissions

ALTER TABLE public.messages OWNER TO postgres;
GRANT ALL ON TABLE public.messages TO postgres;


-- public.months definition

-- Drop table

-- DROP TABLE public.months;

CREATE TABLE public.months (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	month_name text NULL
);

-- Permissions

ALTER TABLE public.months OWNER TO postgres;
GRANT ALL ON TABLE public.months TO postgres;


-- public.pig_stickers definition

-- Drop table

-- DROP TABLE public.pig_stickers;

CREATE TABLE public.pig_stickers (
	id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	sticker_id text NULL
);

-- Permissions

ALTER TABLE public.pig_stickers OWNER TO postgres;
GRANT ALL ON TABLE public.pig_stickers TO postgres;


-- public.questions definition

-- Drop table

-- DROP TABLE public.questions;

CREATE TABLE public.questions (
	que_id int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	ans_id int4 NOT NULL,
	question text NOT NULL,
	CONSTRAINT questions_pkey PRIMARY KEY (que_id)
);

-- Permissions

ALTER TABLE public.questions OWNER TO postgres;
GRANT ALL ON TABLE public.questions TO postgres;


-- public.quotes definition

-- Drop table

-- DROP TABLE public.quotes;

CREATE TABLE public.quotes (
	quote_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	"quote" text NOT NULL,
	CONSTRAINT quotes_pkey PRIMARY KEY (quote_id)
);

-- Permissions

ALTER TABLE public.quotes OWNER TO postgres;
GRANT ALL ON TABLE public.quotes TO postgres;


-- public.rolls definition

-- Drop table

-- DROP TABLE public.rolls;

CREATE TABLE public.rolls (
	nick text NULL,
	chat_id int8 NULL,
	"date" date NULL
);

-- Permissions

ALTER TABLE public.rolls OWNER TO postgres;
GRANT ALL ON TABLE public.rolls TO postgres;


-- public.start_q definition

-- Drop table

-- DROP TABLE public.start_q;

CREATE TABLE public.start_q (
	start_id int8 NOT NULL,
	start_text text NOT NULL
);

-- Permissions

ALTER TABLE public.start_q OWNER TO postgres;
GRANT ALL ON TABLE public.start_q TO postgres;


-- public.stats definition

-- Drop table

-- DROP TABLE public.stats;

CREATE TABLE public.stats (
	stat_id int8 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 9223372036854775807 START 1 CACHE 1 NO CYCLE),
	st_chat_id text NULL,
	st_name text NULL,
	st_nick text NULL,
	st_date timestamp NULL,
	CONSTRAINT stats_pkey PRIMARY KEY (stat_id)
);

-- Permissions

ALTER TABLE public.stats OWNER TO postgres;
GRANT ALL ON TABLE public.stats TO postgres;


-- public.stickers definition

-- Drop table

-- DROP TABLE public.stickers;

CREATE TABLE public.stickers (
	sticker_id int4 NOT NULL GENERATED ALWAYS AS IDENTITY( INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE),
	sticker text NOT NULL,
	CONSTRAINT stickers_pkey PRIMARY KEY (sticker)
);

-- Permissions

ALTER TABLE public.stickers OWNER TO postgres;
GRANT ALL ON TABLE public.stickers TO postgres;