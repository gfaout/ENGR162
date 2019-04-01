clc
clear

maxTime = input('Maximum time to reach destination seconds: ');
dT = input('Time step: ');
currentTime = 0;
airDensity = 1.225;
waterDensity = 1025;
%vAir = importdata('windData.csv');
%vWater = importdata('currentData.csv');
%vIceberg = importdata('iceData.csv');
%temp = importdata('temp.csv');
iceWaterCd = 0.03;
iceAirCd = 0.03 * 10^-3;
formCd = 0.82;

width = 804.672; % Initial width
length = 804.672; % Initial length
height = 228.6 ; % Initial height

while (currentTime < maxTime)
    [height, length, width, volume_loss, mass_loss] = Iceberg_melt(vIceberg.data(currentTime), temp.data(currentTime), length, width, height, vAir.data(currentTime), vWater.data(currentTime), currentTime);

    draft = 2.91 * length^(0.71);
    
    if (draft > height) % Don't think this is necessary but just for precautions
        draft = height;
    end
    
    underFricDrag = dragForce(waterDensity, width * length, iceWaterCd,vWater.data(currentTime), vIceberg.data(currentTime)); %change parameters based on data
    aboveFricDrag = dragForce(airDensity, width * length, iceAirCd,vAir.data(currentTime), vIceberg.data(currentTime));
    underFormDrag = dragForce(waterDensity, draft * length, formCd,vWater.data(currentTime), vIceberg.data(currentTime));
    aboveFormDrag = dragForce(airDensity, draft * length, formCd,vAir.data(currentTime), vIceberg.data(currentTime));
    currentTime = currentTime + dT;
end
