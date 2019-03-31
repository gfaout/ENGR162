function [new_height_iceberg, new_length_iceberg, new_width_iceberg, volume_loss, mass_loss] = Iceberg_melt(vi, Tw, length_iceberg, width_iceberg,height_iceberg, va, vw, t)
%Ti = -10;
height_loss = 0.58 * ((sqrt((vw(1) - vi(1))^2 + (vw(2) - vi(2))^2))^0.8) * (Tw - (-10)) / (length_iceberg ^ 0.2);
side_loss = 0.75 * (sqrt((va(1) - vw(1))^2 + (va(2) - vw(2))^2))^0.5 + 0.05 * sqrt((va(1)-vw(1))^2 + (va(2) - vw(2))^2) + 0.0076 * Tw + 0.0013 * (Tw)^2;

volume_iceberg = height_iceberg * length_iceberg * width_iceberg;

new_height_iceberg = height_iceberg - t * height_loss;
new_length_iceberg = length_iceberg - t * side_loss;
new_width_iceberg = width_iceberg - t * side_loss;

new_volume_iceberg = new_height_iceberg * new_length_iceberg * new_width_iceberg;

volume_loss = volume_iceberg - new_volume_iceberg;

mass_loss = volume_loss * 920;

end