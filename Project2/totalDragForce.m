%Length: 880 yards or 804.672 m
%Width: 500 yards or 457.2 m
%Depth: 250 yards or 228.6 m


%Frictional Drag Force Under Water
rho = 1025; %density of fluid (kg/m^3)
A = ; %total surface area parallel to fluid flow
Cd = 
vFluid = 
vIceberg = 
underFricDrag = dragForce(rho, A, Cd,vFluid, vIceberg);

%Frictional Drag Force Above Water
rho = 1.225; %density of air (kg/m^3)
A = ; %total surface area parallel to air flow
Cd = ;
vFluid = 
vIceberg = 
aboveFricDrag = dragForce(rho, A, Cd,vFluid, vIceberg);

%Form Drag Force Under Water
rho = 1025; %density of fluid (kg/m^3)
A = ; %surface area perpendicular to fluid flow
Cd = 
vFluid = 
vIceberg = 
underFormDrag = dragForce(rho, A, Cd,vFluid, vIceberg);

%Form Drag Force Above Water
rho = 1.225; %density of air (kg/m^3)
A = ; %surface area perpendicular to air flow
Cd = ;
vFluid = 
vIceberg = 
aboveFormDrag = dragForce(rho, A, Cd,vFluid, vIceberg);
