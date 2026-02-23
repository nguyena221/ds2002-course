CREATE TABLE user_info (
	user_id INT AUTO_INCREMENT PRIMARY KEY,
	first_name VARCHAR(50),
	last_name VARCHAR(50),
	email VARCHAR(50)
);

CREATE TABLE user_posts (
    post_id INT AUTO_INCREMENT PRIMARY KEY, 
    user_id INT, 
    post_text TEXT, 
    date_posted DATETIME,
    FOREIGN KEY (user_id) REFERENCES user_info(user_id)
);

USE user_info; 
INSERT INTO users (first_name, last_name, email) VALUES ('Annie', 'Nguyen', 'bvc5vq@virginia.edu');

SELECT * FROM users;