SELECT 
	s.fullname AS student, 
	d.name AS discipline
FROM grades g
LEFT JOIN students s ON s.id = g.students_id 
LEFT JOIN disciplines d ON d.id = g.disciplines_id
GROUP BY s.fullname, d.name
ORDER BY s.fullname ASC, d.name ASC;