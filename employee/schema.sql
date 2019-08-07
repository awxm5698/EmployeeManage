drop table if exists user;
create table user(
  id integer primary key autoincrement,
  login_name char(20) UNIQUE not null,
  password char(50) not null,
  really_name char(20),
  phone char(11) default null,
  email char(50) default null,
  job_id integer default -1,
  company_id integer default -1,
  status integer default -1,
  is_deleted integer check(is_deleted in(0,1)) default 0,
  initiation_time TIMESTAMP,
  departure_time TIMESTAMP,
  create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

insert into user(login_name,password,really_name,job_id)
values('admin','pbkdf2:sha256:150000$Zzo3GwXQ$ff03f92556feceecd5059f293f1048b57d995c2bc2d83d340577eb61c3a915b1','Administrator',0);
insert into user(login_name,password,really_name,job_id)
values('master','pbkdf2:sha256:150000$Zzo3GwXQ$ff03f92556feceecd5059f293f1048b57d995c2bc2d83d340577eb61c3a915b1','Test Master',1);
insert into user(login_name,password,really_name,job_id)
values('tester','pbkdf2:sha256:150000$Zzo3GwXQ$ff03f92556feceecd5059f293f1048b57d995c2bc2d83d340577eb61c3a915b1','tester',2);


drop table if exists job;
create table job(
	id integer primary key autoincrement,
	job_name char(10) not null,
	superior_id integer default null,
	job_desc char(200)
);

insert into job (id,job_name,superior_id) values(-1,'Unknown',-1);
insert into job (id,job_name,superior_id) values(0,'Administrator',0);
insert into job (job_name,superior_id) values('Master',0);
insert into job (job_name,superior_id) values('Tests Master',1);
insert into job (job_name,superior_id) values('Tester',2);

drop table if exists user_status;
create table user_status(
	id integer primary key autoincrement,
	status_name char(10) not null,
	status_desc char(200)
);

insert into user_status (id,status_name) values(-1,'Unknown');
insert into user_status (status_name) values('On');
insert into user_status (status_name) values('Quit');

drop table if exists company;
create table company(
	id integer primary key autoincrement,
	company_name char(10) not null,
	company_desc char(200)
);
insert into company (id,company_name) values(-1,'Unknown');
insert into company (company_name) values('company_01');

DROP TABLE IF EXISTS post;

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);


drop table if exists attendance_application;
CREATE TABLE attendance_application(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    application_nbr char(16) not null,
    type integer default 1,
    applicant_id integer not null,
    begin_date TIMESTAMP not null,
    end_date TIMESTAMP not null,
    duration_time integer not null,
    application_reason char(50) not null,
    auditor_status integer default 1,
    auditor_id integer not null,
    create_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    auditor_reason char(50) default null,
    auditor_time TIMESTAMP
);

drop table if exists auditor_status;
CREATE TABLE auditor_status(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status integer not null,
    status_desc char(50) default null
);
insert into auditor_status (status,status_desc) values (1,'Wait');
insert into auditor_status (status,status_desc) values (2,'Pass');
insert into auditor_status (status,status_desc) values (3,'Reject');
insert into auditor_status (status,status_desc) values (4,'Recall');

drop table if exists application_type;
CREATE TABLE application_type(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type_id integer not null,
    type_desc char(50) default null
);
insert into application_type (type_id,type_desc) values (1,'Leave');
insert into application_type (type_id,type_desc) values (2,'Overtime');