-- computes and store the average score for a student. Note: An average score can be a decimal

DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id VARCHAR(255))
BEGIN
    DECLARE score_total INT DEFAULT 0;
    DECLARE subjects_total INT DEFAULT 0;

    SELECT SUM(score)
        INTO score_total
        FROM corrections
        WHERE `corrections`.`user_id` = user_id
        LIMIT 1;

    SELECT COUNT(*)
        INTO subjects_total
        FROM corrections
        WHERE `corrections`.`user_id` = user_id;

    UPDATE users
        SET average_score = (score_total / subjects_total)
        WHERE id = user_id;

END $$
DELIMITER ;