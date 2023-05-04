SELECT 
	s.fullname AS student, 
	t.fullname AS teacher, 
	d.name AS discipline
FROM grades g  
LEFT JOIN disciplines d ON g.disciplines_id = d.id 
LEFT JOIN teachers t ON t.id = d.teacher_id 
LEFT JOIN students s ON s.id = g.students_id 
WHERE t.id = 2 AND s.id = 3
GROUP BY s.fullname, t.fullname, d.name;