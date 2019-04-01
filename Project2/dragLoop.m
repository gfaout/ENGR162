clc
clear

maxTime = input('Maximum time to reach destination seconds: ');
dT = input('Time step: ');
currentTime = 0;
airDensity = 1.225;
waterDensity = 1025;
%vAir = importdata('windData.csv');
%vWater = importdata('currentData.csv');
%vIceberg = importdata('iceData.csv')
iceWaterCd = 0.03;
iceAirCd = 0.03 * 10^-3;
formCd = 0.82;

while (currentTime < maxTime)
    %function that takes in time and outputs the dimensions of the iceberg
    width = 0;
    length = 0;
    draft = 2.91 * length^(0.71);
    
    underFricDrag = dragForce(waterDensity, width * length, iceWaterCd,vWater(currentTime), vIceberg(currentTime)); %change parameters based on data
    aboveFricDrag = dragForce(airDensity, width * length, iceAirCd,vAir(currentTime), vIceberg(currentTime));
    underFormDrag = dragForce(waterDensity, draft * length, formCd,vWater(currentTime), vIceberg(currentTime));
    aboveFormDrag = dragForce(airDensity, draft * length, formCd,vAir(currentTime), vIceberg(currentTime));
    currentTime = currentTime + dT;
end