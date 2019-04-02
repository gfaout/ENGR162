function temp_water = Water_Temperature(dist_traveled)
if (dist_traveled < 2500)
temp_water = 15 + (dist_traveled/2604) * 5;
elseif (dist_traveled > 2500 && dist_traveled <= 2604)
temp_water = 20 - (dist_traveled - 2500)/104 * 3;    
end
end



