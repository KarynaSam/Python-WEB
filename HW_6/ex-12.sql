SELECT 
	sg.name AS group_name, 
	s.fullname AS student, 
	d.name AS discipline, 
	g.grade  AS grade, 
	g.date_of AS date_of
FROM grades g  
JOIN disciplines d ON d.id = g.disciplines_id 
JOIN students s ON s.id = g.students_id
JOIN groups sg ON sg.id = s.group_id
WHERE sg.id = 1 AND d.id = 1 AND g.date_of = 
(
  SELECT MAX(date_of)
  FROM grades g2 
  JOIN students s2 ON s2.id = g2.students_id
  JOIN groups sg2 ON sg2.id = s2.group_id
  WHERE g2.disciplines_id = g.disciplines_id AND sg2.id = sg.id
)
ORDER BY student;