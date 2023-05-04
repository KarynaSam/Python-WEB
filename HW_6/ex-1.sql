SELECT 
	s.fullname AS student, 
	ROUND(AVG(r.grade), 2) AS average_rating 
FROM grades r 
LEFT JOIN students s ON s.id = r.students_id
GROUP by s.fullname 
ORDER by average_rating DESC 
LIMIT 5;