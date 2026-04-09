USE bvc5vq_db;

-- Add users
INSERT INTO user_info (first_name, last_name, email)
VALUES
('Amy', 'Nguyen', 'an1234@gmail.com'),
('Andy', 'Newyen', 'anewy345@gmail.com');

-- Add posts
INSERT INTO user_posts (user_id, post_text, date_posted)
VALUES
(1, 'Hello world!', '2026-04-08 10:00:00'),
(2, 'This is my first post', '2026-04-08 10:15:00'),
(1, 'blah blah', '2026-04-08 10:30:00');
