-- Create a script to list Glam rock bands ranked by longevity
SELECT 
    band_name, 
    IF(split IS NULL OR formed IS NULL, 0, 2022 - split) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
