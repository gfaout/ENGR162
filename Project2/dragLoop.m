clc
clear

maxTime = input('Maximum time to reach destination seconds: ');
dT = input('Time step: ');
currentTime = 0;
airDensity = 1.225;
waterDensity = 1025;
%vAir = importdata('windData.csv');
vWater = .11; %.11 m/s to .23 m/s Benguela Current
%vIceberg = importdata('iceData.csv');
%temp = importdata('temp.csv');
iceWaterCd = 0.03;
iceAirCd = 0.03 * 10^-3;
formCd = 0.82;

width = 450; % Initial width
length = 800; % Initial length
height = 225; % Initial height

while (currentTime < maxTime)
    [height, length, width, volume_loss, mass_loss] = Iceberg_melt(vIceberg.data(currentTime), temp.data(currentTime), length, width, height, vAir.data(currentTime), vWater, currentTime);

    draft = height * 5 / 6;
    
    underFricDrag = dragForce(waterDensity, width * length, iceWaterCd,vWater, vIceberg.data(currentTime)); %change parameters based on data
    aboveFricDrag = dragForce(airDensity, width * length, iceAirCd,vAir.data(currentTime), vIceberg.data(currentTime));
    underFormDrag = dragForce(waterDensity, draft * length, formCd,vWater), vIceberg.data(currentTime));
    aboveFormDrag = dragForce(airDensity, (height - draft) * length, formCd,vAir.data(currentTime), vIceberg.data(currentTime));
    currentTime = currentTime + dT;
end
