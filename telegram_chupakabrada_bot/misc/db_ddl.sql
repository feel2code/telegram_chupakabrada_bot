drop table if exists about;
drop table if exists answers;
drop table if exists asking;
drop table if exists cities;
drop table if exists dog_stickers;
drop table if exists films;
drop table if exists holidays_iso;
drop table if exists holidays_ru;
drop table if exists holidays_ru_relative;
drop table if exists markov;
drop table if exists messages;
drop table if exists months;
drop table if exists pig_stickers;
drop table if exists questions;
drop table if exists quotes;
drop table if exists rates;
drop table if exists rolls;
drop table if exists start_q;
drop table if exists stats;
drop table if exists stickers;

CREATE TABLE about (
	about_id int8 NOT NULL,
	about_text text NOT NULL
);

CREATE TABLE answers (
	ans_id integer primary key,
	answer text NOT NULL
);


CREATE TABLE asking (
	ask_id integer primary key,
	ask_answer text NULL
);

CREATE TABLE cities (
	cities_id integer primary key,
	chat_id text NULL,
	city_name text NULL,
	temp int8 NULL,
	expected_day_temp int4 NULL,
	conditions text NULL
);

CREATE TABLE course (
	course_name text NULL,
	course_value int8 NULL
);


CREATE TABLE dog_stickers (
	id integer primary key,
	sticker_id text NULL
);


CREATE TABLE films (
	id int8 NULL,
	film_name text NULL,
	link text NULL,
	film_year text NULL
);


CREATE TABLE holidays_iso (
	dt date NULL,
	holiday_name varchar(250) NULL
);

CREATE TABLE holidays_ru (
	dt date NULL,
	holiday_name varchar(250) NULL
);


CREATE TABLE holidays_ru_relative (
	rel_name varchar(200) NULL,
	dt date NULL,
	holiday_name varchar(250) NULL,
	week_num int4 NULL,
	day_num int4 NULL
);


CREATE TABLE markov (
	chat_id int8 NULL,
	hardness int8 NULL
);


CREATE TABLE messages (
	msg_id integer primary key,
	msg_txt text NOT NULL,
	ans_id int8 NOT NULL
);


CREATE TABLE months (
	id integer primary key,
	month_name text NULL
);


CREATE TABLE pig_stickers (
	id integer primary key,
	sticker_id text NULL
);


CREATE TABLE questions (
	que_id integer primary key,
	ans_id int4 NOT NULL,
	question text NOT NULL
);


CREATE TABLE quotes (
	quote_id integer primary key,
	quote_value text NOT NULL
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
	stat_id integer primary key,
	st_chat_id text NULL,
	st_name text NULL,
	st_nick text NULL,
	st_date timestamp NULL
);


CREATE TABLE stickers (
	sticker_id integer primary key,
	sticker text NOT NULL
);

alter table holidays_ru_relative add column is_last integer;
update holidays_ru_relative set is_last=1 where rel_name like '%Последн%';

drop table if exists course;
create table if not exists rates (
  ccy_iso3 varchar(3),
  rate numeric(10, 6),
  prev_rate numeric(10,6)
);

insert into rates values
('USD', 1, 1),
('RUB', 1, 1),
('GEL', 1, 1);

delete from holidays_iso where holiday_name='День матери';
insert into holidays_ru_relative (rel_name, dt, holiday_name, week_num, day_num, is_last) values ('Второе воскресенье', '2000-05-01', 'День матери (международный)', 2, 7, 0);

alter table cities add column updated_at timestamp NULL;
alter table cities add column is_active integer NULL;

CREATE TABLE city_chat_id (
	chat_id int8 NOT NULL,
	city_name text NOT NULL
);

insert into city_chat_id (chat_id, city_name) select cast(chat_id as integer), city_name from cities;

drop table if exists cities;
CREATE TABLE cities (
	city_name text NULL,
	temp int8 NULL,
	expected_day_temp int4 NULL,
	conditions text NULL,
  updated_at timestamp NULL,
  is_active integer NULL
);
