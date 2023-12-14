-- Create a stored procedure to compute the average weighted score for all users
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_id_val INT;
    
    -- Loop through all users and compute their average weighted score
    DECLARE done INT DEFAULT FALSE;
    DECLARE cur CURSOR FOR SELECT id FROM users;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;
    
    OPEN cur;
    read_loop: LOOP
        FETCH cur INTO user_id_val;
        IF done THEN
            LEAVE read_loop;
        END IF;
        
        CALL ComputeAverageWeightedScoreForUser(user_id_val);
    END LOOP;
    CLOSE cur;
END //

DELIMITER ;
