-- computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
DECLARE weighted_total INT;
DECLARE result INT;
SELECT SUM(projects.weight)
    INTO weighted_total
    FROM corrections
    INNER JOIN projects
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
SELECT SUM(projects.weight * corrections.score / weighted_total)
    INTO result
    FROM corrections
    INNER JOIN projects
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;
UPDATE users
    SET average_score = result
    WHERE id = user_id;
END $$
DELIMITER ;
