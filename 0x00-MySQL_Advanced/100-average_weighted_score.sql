-- Create a stored procedure to compute the average weighted score for a user
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE weighted_avg FLOAT;
    
    SELECT SUM(p.weight * c.score) / SUM(p.weight)
    INTO weighted_avg
    FROM corrections c
    JOIN projects p ON c.project_id = p.id
    WHERE c.user_id = user_id;
    
    UPDATE users
    SET average_score = weighted_avg
    WHERE id = user_id;
END //

DELIMITER ;
