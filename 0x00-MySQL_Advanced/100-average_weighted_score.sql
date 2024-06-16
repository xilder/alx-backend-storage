-- computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
DECLARE weighted_total INT;
DECLARE averager INT;
SELECT SUM(projects.weight * corrections.score)
    INTO weighted_total
    FROM corrections
    INNER JOIN projects
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

SELECT SUM(projects.weight)
    INTO averager
    FROM corrections
    INNER JOIN projects
    ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

IF averager = 0 THEN
    UPDATE users
    SET average_score = 0
    WHERE users.id = user_id;
ELSE
    UPDATE users
        SET average_score = weighted_total / averager
        WHERE users.id = user_id;
END IF;
END $$
DELIMITER ;
