SELECT Users.firstname, Users.telephone_number,
    json_group_array(json_object('name', Children.name, 'age', Children.age)) AS children
FROM Users
JOIN Children ON Users.id = Children.user_id
WHERE Users.id IN (
    SELECT DISTINCT user_id
    FROM Children
    WHERE age = ?
)
AND Users.id != ?
GROUP BY Users.id;
