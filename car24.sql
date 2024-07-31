#Database import 
use sakila;

#Getting view of data
 Select count(*) from car_data_cleaned;
 select * from  car_data_cleaned;
 
 
 #The least expensive and most expensive cars for each brand along with their specifications.
WITH MinPriceCars AS (
    SELECT Brand, 
           Car_Name, 
           Car_Variant, 
           Car_Model, 
           Car_Transmission, 
           Fuel_Type, 
           Car_Price, 
           KM_Driven, 
           Owner_Type, 
           Location,
           ROW_NUMBER() OVER (PARTITION BY Brand ORDER BY Car_Price ASC) AS rn
    FROM car_data_cleaned
),
MaxPriceCars AS (
    SELECT Brand, 
           Car_Name, 
           Car_Variant, 
           Car_Model, 
           Car_Transmission, 
           Fuel_Type, 
           Car_Price, 
           KM_Driven, 
           Owner_Type, 
           Location,
           ROW_NUMBER() OVER (PARTITION BY Brand ORDER BY Car_Price DESC) AS rn
    FROM car_data_cleaned
)
SELECT Brand, 
       Car_Name, 
       Car_Variant, 
       Car_Model, 
       Car_Transmission, 
       Fuel_Type, 
       Car_Price, 
       KM_Driven, 
       Owner_Type, 
       Location,
       'Least Expensive' AS Price_Type
FROM MinPriceCars
WHERE rn = 1
UNION ALL
SELECT Brand, 
       Car_Name, 
       Car_Variant, 
       Car_Model, 
       Car_Transmission, 
       Fuel_Type, 
       Car_Price, 
       KM_Driven, 
       Owner_Type, 
       Location,
       'Most Expensive' AS Price_Type
FROM MaxPriceCars
WHERE rn = 1;


#Comparison of the average prices of cars from each brand this year to those from last year
WITH CurrentYear AS (
    SELECT Brand, 
           AVG(Car_Price) AS Avg_Price_This_Year
    FROM car_data_cleaned
    where Car_Model = year(current_date())
    GROUP BY Brand
),
LastYear AS (
    SELECT Brand, 
           AVG(Car_Price) AS Avg_Price_Last_Year
    FROM car_data_cleaned
    WHERE Car_Model = year(current_date()) - 1
    GROUP BY Brand
)
SELECT c.Brand, 
       c.Avg_Price_This_Year, 
       l.Avg_Price_Last_Year,
       (c.Avg_Price_This_Year - l.Avg_Price_Last_Year) AS Price_Difference
FROM CurrentYear c
LEFT JOIN LastYear l ON c.Brand = l.Brand;

select distinct(brand) from car_data_cleaned;


