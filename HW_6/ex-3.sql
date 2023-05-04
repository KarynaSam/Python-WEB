SELECT 
	gr.name AS [group], 
	d.name AS discipline, 
	ROUND(AVG(g.grade), 2) AS average_rating
FROM grades g 
LEFT JOIN students s ON s.id = g.students_id
LEFT JOIN disciplines d ON d.id = g.disciplines_id 
LEFT JOIN groups gr ON gr.id = s.group_id 
WHERE d.id = 2
GROUP by gr.name, d.name
ORDER by ROUND(AVG(g.grade), 2) ASC; 