-- Create index on the first letter of name and the score in the table names
CREATE INDEX idx_name_first_score ON names(name(1), score);
