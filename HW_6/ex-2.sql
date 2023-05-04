SELECT 
	d.name AS discipline, 
	s.fullname AS student, 
	ROUND(AVG(r.grade), 2) AS average_rating 
FROM grades r 
LEFT JOIN students s ON s.id = r.students_id
LEFT JOIN disciplines d ON d.id = r.disciplines_id 
WHERE d.id = 1
GROUP by s.fullname 
ORDER by average_rating DESC 
LIMIT 1;