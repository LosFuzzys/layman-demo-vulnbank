# "Why IT Security" Demo for the Layman

The idea is to show a very simple demo, of why simple bugs or careless
programming can lead to security vulnerabilities. Hopefully this example is
something everybody can grasp.

## The App, The Bug, The Vuln

This simple flask web app mimics a banking web interface, where you can
transfer money to other users.

Unfortunately the programmer forgot to check whether the amount the user tries
to transfer is negative. So by sending negative amounts of money, the evil
person can enrich himself.

## Running

It's written in python using flask so I suggest you install everything in a
virtualenv:

    pip install flask flas-bootstrap
    python bank.py

There are a couple of users, such as `jdoe` and `mmustermann`, which you can
use. The login doesn't check the passwords, so it doesn't matter what you put
there.

## Creating the Database's Tables

`users` table:
```
CREATE TABLE users (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
  user VARCHAR(50) NOT NULL, 
  pwd VARCHAR(100) NOT NULL, 
  balance INT NOT NULL
);
```

`sessions` table:
```
CREATE TABLE sessions (
  user_id INT NOT NULL, 
  token VARCHAR(100) NOT NULL,
  CONSTRAINT `fk_user_id` 
    FOREIGN KEY (user_id) REFERENCES users (id) 
    ON DELETE CASCADE 
    ON UPDATE RESTRICT
);
```

After creation of the tables, dump them into a .sql file:
`mysqldump -h <db_host> -P <db_port> -u <db_user> -p<db_password> iron_bank > iron_bank.sql`

When loading the init file, the database (`iron_bank`) must already exist
and has to be selected; which is done for instance automatically by
docker-compose when setting the field `MYSQL_DATABASE`.
 
