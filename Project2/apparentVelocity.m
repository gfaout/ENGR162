function[apparentVelocity] = apparentVelocity(fluid, iceberg)
%each input is a two dimensional with x and y 
apparentVelocity(1) = fluid(1) - iceberg(1);
apparentVelocity(2) = fluid(2) - iceberg(2);