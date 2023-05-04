SELECT 
	t.fullname AS teacher, 
	d.name AS discipline, 
	ROUND(AVG(g.grade), 2) AS average_rating
FROM grades g
LEFT JOIN disciplines d ON d.id = g.disciplines_id 
LEFT JOIN teachers t ON t.id = d.teacher_id 
WHERE t.id = 5
GROUP BY t.fullname, d.name;