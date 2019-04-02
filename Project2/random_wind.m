function va = random_wind(old_va, t_total)
% outputs wind speed in m/s, dependent on the number of days passed.  
if (mod((t_total * 2),2) == 0)
shape_parameter = 2.1;
scale_parameter = 10;
wind_speed = wblrnd(scale_parameter, shape_parameter);
wind_angle = unifrnd(0, 360);

va = [wind_speed * cosd(wind_angle), wind_speed * sind(wind_angle)];
    
elseif (mod((t_total * 2),2) == 1)
va = old_va;
end
end