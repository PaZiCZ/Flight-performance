import pytest
from power import power_available
from constants import rho0

# Dummy aircraft data class
class DummyAdata:
    def __init__(self, engtype):
        self.engtype = engtype
        self.pmax = 200.0      # kW, max. power at sea level
        self.vnom = 200      # km/h,  nominal speed
        self.etaprop = 0.85    # max. propeller efficiency


@pytest.mark.parametrize("engtype", [1, 2])
def test_power_positive_at_sea_level(engtype):
    adata = DummyAdata(engtype)
    rho = rho0
    speed = 50.0  # m/s

    power = power_available(rho, speed, adata)
    assert power > 0, "Power should be positive at sea level"
    assert power < adata.pmax, "Power should not exceed maximum pmax"

def test_reciprocal_vs_turboprop_in_altitude():
    adata1 = DummyAdata(engtype=1)
    adata2 = DummyAdata(engtype=2)
    rho = rho0 * 0.75
    speed = 50.0 # m/s

    p1 = power_available(rho, speed, adata1)
    p2 = power_available(rho, speed, adata2)

    assert p1 != p2, "Different engine types should provide different power at nonzero altitude"

def test_propeller_efficiency_range():
    adata = DummyAdata(engtype=1)
    rho = rho0 * 0.7   # nonzero altitude
    speed = 80.0       # m/s

    # replicate computation of E
    L = speed / adata.vnom * 3.6
    E = 1 - (1 - L) ** 2 * (1 + (0.8722 * L ** 2 - 1.3959 * L))

    assert E > 0, "E (prop efficiency characteristic) should be positive"
    assert E <= 1, "E should not exceed 1"