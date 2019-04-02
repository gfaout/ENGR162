height_iceberg = 117;
length_iceberg = 5*height_iceberg;
width_iceberg = 5*height_iceberg;
va = [0,0];
height_loss = [];
all_height = [];
vi = [2,2];
vw = [0.1,0.1];
time = 2640/((86400 / 1000) * (vi(1) * sqrt(2)));
for i = 0:0.5:ceil(time)
    old_va = va;
    va = Random_Wind_Speed(old_va,i);
    dist = 2604*(i/60);
    Tw = Water_Temperature(dist);
    [height_iceberg, length_iceberg, width_iceberg, new_height_loss] = Iceberg_Melt(vi, Tw, length_iceberg, width_iceberg, height_iceberg, va, vw, 0.50);
    height_loss = [height_loss, round(new_height_loss)];
    all_height = [all_height, round(height_iceberg)];
end
for i = 1:size(height_loss)  
fprintf('%d\n',mod(height_loss(i),1))
end