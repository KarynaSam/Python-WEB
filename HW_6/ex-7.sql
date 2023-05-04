SELECT 
	s.fullname AS student, 
	g.name AS [group], 
	d.name AS discipline, 
	gr.grade, 
	gr.date_of
FROM grades gr 
LEFT JOIN disciplines d ON d.id = gr.disciplines_id
LEFT JOIN students s ON s.id = gr.students_id 
LEFT JOIN groups g ON s.group_id = g.id 
WHERE d.id = 1 AND g.id = 1
ORDER BY s.fullname ASC, gr.date_of ASC;