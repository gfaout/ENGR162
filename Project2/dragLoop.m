clc
clear

maxTime = input('Maximum time to reach destination days: '); %2604 max distance
dT = input('Time step: ');
currentTime = 0;
airDensity = 1.225;
waterDensity = 1025;
%vAir = importdata('windData.csv');
vWater = .11; %.11 m/s to .23 m/s Benguela Current
vIceberg = 0.194444 %0.19444 m/s to 1 m/s natural movement
iceWaterCd = 0.03;
iceAirCd = 0.03 * 10^-3;
formCd = 0.82;

width = input('Iceberg inital width: '); % Initial width 450
length = input('Iceberg inital length: '); % Initial length 800
height = input('Iceberg inital height: '); % Initial height 225

while (currentTime < maxTime)
    [height, length, width, volume_loss, mass_loss] = Iceberg_melt(vIceberg.data(currentTime), Water_Temperature(currentTime * vIceberg), length, width, height, vAir.data(currentTime), vWater, currentTime);

    draft = height * 5 / 6;
    
    underFricDrag = dragForce(waterDensity, width * length, iceWaterCd, vWater, vIceberg); %change parameters based on data
    aboveFricDrag = dragForce(airDensity, width * length, iceAirCd, vAir.data(currentTime), vIceberg);
    underFormDrag = dragForce(waterDensity, draft * length, formCd, vWater, vIceberg);
    aboveFormDrag = dragForce(airDensity, (height - draft) * length, formCd,vAir.data(currentTime), vIceberg);
    currentTime = currentTime + dT;
end
