USE bvc5vq_db; 
DROP TABLE IF EXISTS user_posts;
DROP TABLE IF EXISTS user_info;

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


INSERT INTO user_info (first_name, last_name, email) 
VALUES 
('Annie', 'Nguyen', 'bvc5vq@virginia.edu'), 
('Emma', 'Chung', 'hng0pv@virginia.edu'),
('Andrew', 'Nguyen', 'fru4yr@virginia.edu'),
('Emujin', 'Batzorig', 'yur9pw@virginia.edu'),
('Jia', 'Park', 'uy23mn@virginia.edu'), 
('Aiden', 'Nguyen', 'tyr6up@virginia.edu'),
('Teri', 'Phan', 'bhn9er@virginia.edu'),
('Andrew', 'Nguyen', 'tye0jk@virginia.edu'),
('Stephanie', 'Lim', 'sth4nr@virginia.edu'),
('Thea', 'Budlong', 'uol7qg@virginia.edu');

INSERT INTO user_posts (user_id, post_text, date_posted)
VALUES
(1, 'Excited to join the platform!', '2026-02-23 09:00:00'),
(2, 'Hello everyone!', '2026-02-23 09:15:00'),
(3, 'Working on my SQL lab today.', '2026-02-23 09:30:00'),
(4, 'Just finished my first post.', '2026-02-23 10:00:00'),
(5, 'Learning about foreign keys.', '2026-02-23 10:20:00'),
(6, 'Auto increment makes life easier.', '2026-02-23 10:45:00'),
(7, 'Database relationships are cool.', '2026-02-23 11:00:00'),
(8, 'Practicing SQL joins next.', '2026-02-23 11:30:00'),
(9, 'Almost done with this lab!', '2026-02-23 12:00:00'),
(10, 'Time for lunch after coding.', '2026-02-23 12:30:00');
