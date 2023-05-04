SELECT 
	t.fullname AS teacher, 
	d.name AS discipline
FROM disciplines d 
LEFT JOIN teachers t ON t.id = d.teacher_id
WHERE t.id = 2
;