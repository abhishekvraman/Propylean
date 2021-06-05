import pytest

from productionplant.equipments import centrifugal_pump
from productionplant.equipments import pipe

cp = centrifugal_pump(inlet_pressure=50, design_pressure = 50, pressure_drop=-60)
assert cp.suction_pressure == 50
assert cp.outlet_pressure == 110
assert cp.discharge_pressure == 110
cp.outlet_pressure = 90
assert cp.pressure_drop == -40
assert cp.differential_pressure == 40


