-- creates a stored procedure AddBonus that adds a new correction for a student.

DROP PROCEDURE IF EXISTS AddBonus;
DELIMITER $$
CREATE PROCEDURE AddBonus(IN user_id INT, IN project_name VARCHAR(255), IN score FLOAT)
BEGIN
    DECLARE project_count INT DEFAULT 0;
    DECLARE project_idd INT DEFAULT 0;

    SELECT COUNT(*)
        INTO project_count
        FROM projects
        WHERE name = project_name;

    IF project_count < 1 THEN
        INSERT INTO projects (name)
            VALUES (project_name);
        SET project_idd = LAST_INSERT_ID();
    ELSE
        SELECT id
            INTO project_idd
            FROM projects
            WHERE name = project_name;
    END IF;

    INSERT INTO corrections (user_id, project_id, score)
        VALUES (user_id, project_idd, score);
END $$
DELIMITER ;