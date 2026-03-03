USE bvc5vq_db;

SELECT user_posts.user_id,
       user_info.first_name,
       user_posts.post_text

FROM user_posts
JOIN user_info ON user_posts.user_id = user_info.user_id;