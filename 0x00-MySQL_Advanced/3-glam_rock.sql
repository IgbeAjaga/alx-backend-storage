-- Lists all bands with Glam rock as their main style, ranked by their longevity.
SELECT band_name, (IFNULL(split, 2022) - formed) AS lifespan
FROM metal_bands
WHERE style LIKE '%Glam rock%' OR style = 'Glam rock'  -- Check if 'Glam rock' exists in the 'style' column
ORDER BY lifespan DESC;

