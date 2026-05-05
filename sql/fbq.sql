-- I. View users’s all posts and display the number of likes and number of comments to that post.


SELECT p.post_id, p.post_content,
COUNT(DISTINCT r.reaction_id) AS total_likes,
COUNT(DISTINCT c.comment_id) AS total_comments
FROM posts p
LEFT JOIN reactions r
ON p.post_id = r.post_id
AND r.reaction_type = 'LIKE'
LEFT JOIN comments c
ON p.post_id = c.post_id
WHERE p.user_id = 1
GROUP BY p.post_id, p.post_content;

-- II. Display the comments posted by the user.

SELECT c.comment_id, c.comment_text, p.post_content
FROM comments c
JOIN posts p
ON c.post_id = p.post_id

WHERE c.user_id = 2;


-- ||| Display the online friends of a particular user.

SELECT u.user_id, u.first_name, u.last_name
FROM friends f
JOIN users u
ON f.friend_user_id = u.user_id
WHERE f.user_id = 1
AND u.is_online = TRUE;



-- Display the Group name, number of members of that Group and admin of that Group.


SELECT g.group_name,  u.first_name, u.last_name , 
COUNT(gm.user_id) AS total_members FROM groupss g 
join  users u on g.admin_user_id = u.user_id
left join group_members gm 
on g.group_id = gm.group_id
group by
g.group_id, g.group_name;
    
select 
g.group_name , g.admin_user_id , count(gm.group_member_id) from groupss as g 
join group_members  gm 
on g.group_id = gm.group_id 
group by g.group_name  , g.admin_user_id  ;



-- Display the Members of the particular Group.

SELECT g.group_name, u.first_name , u.last_name FROM group_members gm
JOIN users u
ON gm.user_id = u.user_id
JOIN groupss g
ON gm.group_id = g.group_id
WHERE g.group_id = 1;



 --  Display post which don’t have any like.
 
 
SELECT p.post_id, p.post_content FROM posts p
LEFT JOIN reactions r ON p.post_id = r.post_id
AND r.reaction_type = 'LIKE'
WHERE r.reaction_id IS NULL;



 -- Display post which don’t have any comment.
 
 SELECT p.post_id , p.post_content FROM posts p
LEFT JOIN comments c ON p.post_id = c.post_id
WHERE c.comment_id IS NULL;




 
-- VIII. Display post which are liked by user's friend.

SELECT DISTINCT p.post_id, p.post_content
FROM friends f
JOIN reactions r ON f.friend_user_id = r.user_id
JOIN posts p ON r.post_id = p.post_id
WHERE f.user_id = 1 AND r.reaction_type = 'LIKE';


-- IX. Display Comments of a particular user which are liked by user’s friends.

SELECT DISTINCT c.comment_id, c.comment_text FROM comments c
JOIN reactions r ON c.comment_id = r.comment_id
JOIN friends f ON r.user_id = f.friend_user_id
WHERE c.user_id = 2
AND f.user_id = 5
AND r.reaction_type = 'LIKE';


-- X. Display Posts of a particular user which are liked by user’s friends.

SELECT DISTINCT p.post_id, p.post_content FROM posts p
JOIN reactions r ON r.post_id = r.post_id
JOIN friends f ON r.user_id = f.friend_user_id
WHERE p.user_id = 2
AND f.user_id = 1
AND r.reaction_type = 'LIKE';


-- XI. Display Posts to particular group and also display the user’s name who posted it.

SELECT
    g.group_name,

    CONCAT(u.first_name, ' ', u.last_name)
    AS posted_by,

    p.post_content

FROM posts p

JOIN post_shares ps
ON p.post_id = ps.post_id

JOIN groupss g
ON ps.shared_to_group_id = g.group_id

JOIN users u
ON p.user_id = u.user_id

WHERE g.group_id = 1;

-- XII. Display posts of a group that is not liked by anyone.


SELECT DISTINCT
    p.post_id,
    p.post_content
FROM posts p

JOIN reactions r
ON r.post_id = r.post_id

JOIN friends f
ON r.user_id = f.friend_user_id

WHERE p.user_id = 4
AND f.user_id = 1
AND r.reaction_type = 'LIKE';





 
