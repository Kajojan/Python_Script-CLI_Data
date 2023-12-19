SELECT Users.id, Users.firstname, Users.telephone_number, Users.email, Users.role, Users.created_at,
    json_group_array(json_object('name', Children.name, 'age', Children.age)) AS children
FROM Users
LEFT JOIN Children ON Users.id = Children.user_id
WHERE Users.email = ?
GROUP BY Users.id;
