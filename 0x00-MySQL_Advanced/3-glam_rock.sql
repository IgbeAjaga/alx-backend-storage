-- Create a script to list Glam rock bands ranked by longevity
SELECT 
    band_name, 
    IF(formed IS NOT NULL AND split IS NOT NULL, 2022 - LEAST(formed, split), 2022 - GREATEST(formed, split)) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;

