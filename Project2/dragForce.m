function [drag] = dragForce(rho, A, Cd,vFluid, vIceberg)

vApparent = apparentVelocity(vFluid, vIceberg);

drag = 0.5 * rho * A * Cd * abs(vApparent) * vApparent;
