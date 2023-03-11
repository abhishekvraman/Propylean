import pytest
import unittest
from propylean.equipments.generic_equipment_classes import _SphericalVessels
from propylean.streams import MaterialStream, EnergyStream
from propylean.constants import Constants
import propylean.properties as prop

class test__SphericalVessels(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__SphericalVessels_instantiation_only_tag(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_1")
        self.assertEqual(Spherical_vessel.tag, "Spherical_vessel_1")
        self.assertEqual(Spherical_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(Spherical_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__SphericalVessels_instantiation_tag_and_pressure_drop(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_2")
        Spherical_vessel.operating_pressure = prop.Pressure(10, "bar")
        self.assertEqual(Spherical_vessel.tag, "Spherical_vessel_2")
        self.assertEqual(Spherical_vessel.operating_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(Spherical_vessel.outlet_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(Spherical_vessel.inlet_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(Spherical_vessel.pressure_drop, prop.Pressure(0, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__SphericalVessels_instantiation_no_arguments(self):
        Spherical_vessel = _SphericalVessels()
        self.assertIsNotNone(Spherical_vessel.tag)
        self.assertEqual(Spherical_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(Spherical_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.length_setting
    def test__SphericalVessels_instantiation_vessel_dimensions_arguments(self):
        Spherical_vessel = _SphericalVessels(ID = (4, "m"),
                                               OD = 6)

        self.assertEqual(Spherical_vessel.ID, prop.Length(4, "m"))
        self.assertEqual(Spherical_vessel.OD, prop.Length(6, "m"))
        self.assertEqual(Spherical_vessel.thickness, prop.Length(2, "m"))

        Spherical_vessel = _SphericalVessels(thickness = (2, "m"),
                                               OD = 6,
                                               length=prop.Length(10))
        self.assertEqual(Spherical_vessel.ID, prop.Length(4, "m"))
        self.assertEqual(Spherical_vessel.OD, prop.Length(6, "m"))
        self.assertEqual(Spherical_vessel.thickness, prop.Length(2, "m"))

    @pytest.mark.positive
    @pytest.mark.length_setting
    def test__SphericalVessels_instantiation_level_settings_arguments(self):
        Spherical_vessel = _SphericalVessels(LLLL=(10, "inch"),
                                             LLL=(20, "inch"),
                                             NLL=prop.Length(30, "inch"),
                                             HLL=prop.Length(40, "inch"),
                                             HHLL=(50, "inch"))

        self.assertEqual(Spherical_vessel.LLLL, prop.Length(10, "inch"))
        self.assertEqual(Spherical_vessel.LLL, prop.Length(20, "inch"))
        self.assertEqual(Spherical_vessel.NLL, prop.Length(30, "inch"))
        self.assertEqual(Spherical_vessel.HLL, prop.Length(40, "inch"))
        self.assertEqual(Spherical_vessel.HHLL, prop.Length(50, "inch"))
    
    @pytest.mark.positive
    @pytest.mark.main_fluid
    def test__SphericalVessels_instantiation_main_fluid_argument(self):
        for main_fluid in ["liquid", "gas"]:
            Spherical_vessel = _SphericalVessels(ID = (4, "m"),
                                                OD = 6,
                                                length=prop.Length(10),
                                                main_fluid=main_fluid)
            self.assertEqual(Spherical_vessel.main_fluid, main_fluid)
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_inlet_pressure(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_6",
                          pressure_drop=(0.1, 'bar'))
        Spherical_vessel.inlet_pressure = (30, 'bar')
        self.assertEqual(Spherical_vessel.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(Spherical_vessel.outlet_pressure, prop.Pressure(29.9, 'bar'))
        self.assertEqual(Spherical_vessel.operating_pressure, prop.Pressure(30, 'bar'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_outlet_pressure(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_7",
                          pressure_drop=(0.1, 'bar'))
        Spherical_vessel.outlet_pressure = (20, 'bar')
        self.assertEqual(Spherical_vessel.inlet_pressure, prop.Pressure(20.1, 'bar'))
        self.assertEqual(Spherical_vessel.operating_pressure, prop.Pressure(20.1, 'bar'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_inlet_temperature(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_8",
                          pressure_drop=(0.1, 'bar'))
        Spherical_vessel.inlet_temperature = (50, 'C')
        self.assertEqual(Spherical_vessel.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(Spherical_vessel.operating_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_outlet_temperature(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_9",
                          pressure_drop=(0.1, 'bar'))
        Spherical_vessel.outlet_temperature = (130, 'F')
        self.assertLess(abs(Spherical_vessel.inlet_temperature.value-130), 0.0001)
        self.assertEqual(Spherical_vessel.inlet_temperature.unit, 'F')
        self.assertLess(abs(Spherical_vessel.operating_temperature.value-130), 0.0001)
        self.assertEqual(Spherical_vessel.operating_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_inlet_mass_flowrate(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_10",
                          pressure_drop=(0.1, 'bar'))
        Spherical_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(Spherical_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_outlet_mass_flowrate(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_11",
                          pressure_drop=(0.10, 'bar'))
        Spherical_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(Spherical_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_inlet_stream_governed(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Spherical_vessel_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(Spherical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of Spherical_vessel are equal to inlet stream's.
        self.assertEqual(Spherical_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(Spherical_vessel.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(Spherical_vessel.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(Spherical_vessel.outlet_pressure, Spherical_vessel.inlet_pressure - Spherical_vessel.pressure_drop)
        self.assertLess(abs(Spherical_vessel.inlet_temperature.value - Spherical_vessel.outlet_temperature.value), 0.001)
        self.assertEqual(Spherical_vessel.inlet_temperature.unit, Spherical_vessel.outlet_temperature.unit)
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, Spherical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_outlet_stream_governed(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_Spherical_vessel_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(Spherical_vessel.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of Spherical_vessel are equal to outlet stream's.
        self.assertEqual(Spherical_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(Spherical_vessel.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(Spherical_vessel.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(Spherical_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(Spherical_vessel.inlet_pressure, Spherical_vessel.outlet_pressure + Spherical_vessel.pressure_drop)
        self.assertLess(abs(Spherical_vessel.inlet_temperature.value-Spherical_vessel.outlet_temperature.value),0.0001)
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, Spherical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_inlet_equipment_governed(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_14",
                          pressure_drop=(0.1, 'bar'))

        Spherical_vessel.inlet_pressure = (30, 'bar')
        Spherical_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        Spherical_vessel.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_Spherical_vessel_14")
        # Test connection is made.
        self.assertTrue(Spherical_vessel.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of Spherical_vessel are equal to inlet stream's.
        self.assertEqual(Spherical_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(Spherical_vessel.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(Spherical_vessel.outlet_pressure, Spherical_vessel.inlet_pressure - Spherical_vessel.pressure_drop)
        self.assertEqual(Spherical_vessel.inlet_temperature, Spherical_vessel.outlet_temperature)
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, Spherical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_outlet_equipment_governed(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_15",
                          pressure_drop=(0.1, 'bar'))
        Spherical_vessel.outlet_pressure = (130, 'bar')
        Spherical_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        Spherical_vessel.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_Spherical_vessel_15")
        # Test connection is made.
        self.assertTrue(Spherical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of Spherical_vessel are equal to outlet stream's.
        self.assertEqual(Spherical_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(Spherical_vessel.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(Spherical_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(Spherical_vessel.inlet_pressure, Spherical_vessel.outlet_pressure + Spherical_vessel.pressure_drop)
        self.assertEqual(Spherical_vessel.inlet_temperature, Spherical_vessel.outlet_temperature)
        self.assertEqual(Spherical_vessel.inlet_mass_flowrate, Spherical_vessel.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test__SphericalVessels_connection_with_energy_stream_inlet_equipment_governed(self):
    #     Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     Spherical_vessel_energy_expelled = EnergyStream(tag="Power_Spherical_vessel_17", amount=(10,"MW"))
    #     Spherical_vessel_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     Spherical_vessel_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(Spherical_vessel.connect_stream(Spherical_vessel_inlet, "in", stream_governed=True))
    #     # Test inlet properties of Spherical_vessel are equal to outlet stream's.
    #     self.assertAlmostEqual(Spherical_vessel.energy_out.value, Spherical_vessel_energy_expelled.amount.value)
    #     self.assertEqual(Spherical_vessel.energy_out.unit, Spherical_vessel_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test__SphericalVessels_stream_disconnection_by_stream_object(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Spherical_vessel_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_Spherical_vessel_18")
        # Test connection is made.
        self.assertTrue(Spherical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(Spherical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(Spherical_vessel.disconnect_stream(inlet_stream))
        self.assertTrue(Spherical_vessel.disconnect_stream(outlet_stream))
        self.assertIsNone(Spherical_vessel._inlet_material_stream_tag)
        self.assertIsNone(Spherical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test__SphericalVessels_stream_disconnection_by_stream_tag(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Spherical_vessel_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_Spherical_vessel_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(Spherical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(Spherical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(Spherical_vessel.disconnect_stream(stream_tag="Inlet_Spherical_vessel_19"))
        self.assertTrue(Spherical_vessel.disconnect_stream(stream_tag="Outlet_Spherical_vessel_19"))
        self.assertIsNone(Spherical_vessel._inlet_material_stream_tag)
        self.assertIsNone(Spherical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test__SphericalVessels_stream_disconnection_by_direction_stream_type(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_Spherical_vessel_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_Spherical_vessel_20")
        Spherical_vessel_energy_expelled = EnergyStream(tag="Power_Spherical_vessel_20")
        # Test connection is made.
        self.assertTrue(Spherical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(Spherical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(Spherical_vessel.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(Spherical_vessel.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(Spherical_vessel._inlet_material_stream_tag)
        self.assertIsNone(Spherical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.liquid_level
    def test__SphericalVessels_liquid_level(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_21",
                                               NLL=(20, "m"))
        self.assertEqual(Spherical_vessel.NLL, Spherical_vessel.liquid_level)
    
    @pytest.mark.positive
    @pytest.mark.vessel_volume
    def test__SphericalVessels_volume_calculations(self):
        Spherical_vessel = _SphericalVessels(tag="Spherical_vessel_22",
                                               ID=(4, "m"))
        Spherical_vessel.liquid_level = prop.Length(1.8, "m")
        Spherical_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(33.51, "m^3")
        expected_liquid_volume = prop.Volume(14.25)
        self.assertAlmostEqual(Spherical_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(Spherical_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = Spherical_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit)       

    @pytest.mark.negative
    def test__SphericalVessels_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__SphericalVessels_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__SphericalVessels_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.pressure_drop = []
        self.assertIn("Incorrect type 'list' provided to 'pressure_drop'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))                                    

    @pytest.mark.negative
    def test__SphericalVessels_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.design_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'design_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__SphericalVessels_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__SphericalVessels_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__SphericalVessels_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_decrease'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__SphericalVessels_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.temperature_increase = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_increase'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test__SphericalVessels_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.design_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'design_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__SphericalVessels_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__SphericalVessels_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__SphericalVessels_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.energy_in = []
        self.assertIn("Incorrect type 'list' provided to 'energy_in'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))      

    @pytest.mark.negative
    def test__SphericalVessels_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.energy_out = []
        self.assertIn("Incorrect type 'list' provided to 'energy_out'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__SphericalVessels_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            Spherical_vessel = _SphericalVessels(
                                               ID=[4, "m"], length=(10, "m"),
                                               head_type="flat")
        self.assertIn("Incorrect type 'list' provided to 'ID'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.ID = []
        self.assertIn("Incorrect type 'list' provided to 'ID'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__SphericalVessels_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            Spherical_vessel = _SphericalVessels(
                                               ID=(4, "m"), length=[10, "m"],
                                               head_type="flat")
        self.assertIn("Incorrect type 'list' provided to 'length'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.length = []
        self.assertIn("Incorrect type 'list' provided to 'length'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                  

    @pytest.mark.negative
    def test__SphericalVessels_heayd_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            Spherical_vessel = _SphericalVessels(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type=["flat"])
        self.assertIn("Incorrect type 'list' provided to 'head_type'. Should be 'str'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.head_type = []
        self.assertIn("Incorrect type 'list' provided to 'head_type'. Should be 'str'",
                      str(exp))

    @pytest.mark.negative
    def test__SphericalVessels_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.LLLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                    

    @pytest.mark.negative
    def test__SphericalVessels_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.LLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__SphericalVessels_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.NLL = []
        self.assertIn("Incorrect type 'list' provided to 'NLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__SphericalVessels_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.HLL = []
        self.assertIn("Incorrect type 'list' provided to 'HLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__SphericalVessels_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.HHLL = []
        self.assertIn("Incorrect type 'list' provided to 'HHLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))   

    @pytest.mark.negative
    def test__SphericalVessels_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.operating_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'operating_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))  

    @pytest.mark.negative
    def test__SphericalVessels_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.operating_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'operating_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))   

    @pytest.mark.negative
    def test__SphericalVessels_heayd_type_incorrect_value(self):
        with pytest.raises(Exception) as exp:
            Spherical_vessel = _SphericalVessels(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flatop")
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.head_type = "flatop"
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'",
                      str(exp))                               

    @pytest.mark.negative
    def test__SphericalVessels_stream_connecion_disconnection_incorrect_type(self):
        cv = _SphericalVessels()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
            
        with pytest.raises(Exception) as exp:
            cv.connect_stream([inlet_stream], 'in', stream_governed=True)
        self.assertIn("Incorrect type \'list\' provided to \'stream_object\'. Should be \'('MaterialStream', 'EnergyStream')\'",
                      str(exp)) 
        
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, ['in'], stream_governed=True)
        self.assertIn("Incorrect type \'list\' provided to \'direction\'. Should be \'str\'",
                      str(exp)) 
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, 'in', stream_governed=[True])
        self.assertIn("Incorrect type \'list\' provided to \'stream_governed\'. Should be \'bool\'",
                      str(exp)) 

        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        with pytest.raises(Exception) as exp:
            cv.disconnect_stream(stream_tag=["Inlet_cv_19"])
        self.assertIn("Incorrect type \'list\' provided to \'stream_tag\'. Should be \'str\'",
                      str(exp))    

    @pytest.mark.negative
    def test__SphericalVessels_stream_disconnection_before_connecion(self):  
        cv = _SphericalVessels()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        import warnings
        with warnings.catch_warnings(record=True) as exp:
            cv.disconnect_stream(inlet_stream)
         
        self.assertIn("Already there is no connection.",
                      str(exp[-1].message))   

    @pytest.mark.negative
    @pytest.mark.get_inventory
    def test__SphericalVessels_get_inventory_incorrect_type_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.get_inventory([])
        self.assertIn("Incorrect type 'list' provided to 'type'. Should be 'str",
                      str(exp))   
    @pytest.mark.negative
    @pytest.mark.get_inventory
    def test__SphericalVessels_get_inventory_incorrect_value_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = _SphericalVessels()
            m4.get_inventory('list')
        self.assertIn("Incorrect value \'list\' provided to \'type\'. Should be among \'[\'volume\', \'mass\']\'.",
                      str(exp))                                                                       