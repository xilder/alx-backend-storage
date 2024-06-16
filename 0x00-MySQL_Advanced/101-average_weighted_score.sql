-- Creates a stored procedure ComputeAverageWeightedScoreForUsers that

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
ALTER TABLE users ADD total_weighted_score INT NOT NULL DEFAULT 0;
ALTER TABLE users ADD total_weight INT NOT NULL DEFAULT 0;

UPDATE users
    SET users.total_weighted_score = (
        SELECT SUM(projects.weight * corrections.score)
        FROM corrections
        INNER JOIN projects
        ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );
UPDATE users
    SET users.total_weight = (
        SELECT SUM(projects.weight)
        FROM corrections
        INNER JOIN projects
        ON corrections.project_id = projects.id
        WHERE corrections.user_id = users.id
    );
UPDATE users
    SET users.average_score = users.total_weighted_score / users.total_weight;

ALTER TABLE users DROP COLUMN total_weighted_score;
ALTER TABLE users DROP total_weight;
END $$
DELIMITER ;
