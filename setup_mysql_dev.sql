-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Create the user if it doesn't exist and set the password
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant all privileges on the database to the user
GRANT ALL ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Grant select privileges on performance_schema to the user
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';
