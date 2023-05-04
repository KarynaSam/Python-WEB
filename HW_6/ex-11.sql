SELECT 
	t.fullname AS teacher, 
	s.fullname AS student, 
	ROUND(AVG(g.grade), 2) AS average_rating
FROM grades g 
LEFT JOIN disciplines d ON g.disciplines_id = d.id 
LEFT JOIN teachers t ON t.id = d.teacher_id 
LEFT JOIN students s ON s.id = g.students_id 
WHERE t.id = 2 AND s.id = 1;