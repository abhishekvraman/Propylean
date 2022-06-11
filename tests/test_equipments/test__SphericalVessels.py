import pytest
import unittest
from propylean.equipments.generic_equipment_classes import _SphericalVessels
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop

class test__SphericalVessels(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__SphericalVessels_instantiation_only_tag(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_1")
        self.assertEqual(sperical_vessel.tag, "sperical_vessel_1")
        self.assertEqual(sperical_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(sperical_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__SphericalVessels_instantiation_tag_and_pressure_drop(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_2",
                          pressure_drop=prop.Pressure(100, 'bar'))
        self.assertEqual(sperical_vessel.tag, "sperical_vessel_2")
        self.assertEqual(sperical_vessel.pressure_drop, prop.Pressure(100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__SphericalVessels_instantiation_no_arguments(self):
        sperical_vessel = _SphericalVessels()
        self.assertIsNotNone(sperical_vessel.tag)
        self.assertEqual(sperical_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(sperical_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_inlet_pressure(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_6",
                          pressure_drop=(0.1, 'bar'))
        sperical_vessel.inlet_pressure = (30, 'bar')
        self.assertEqual(sperical_vessel.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(sperical_vessel.outlet_pressure, prop.Pressure(29.9, 'bar'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_outlet_pressure(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_7",
                          pressure_drop=(0.1, 'bar'))
        sperical_vessel.outlet_pressure = (20, 'bar')
        self.assertEqual(sperical_vessel.inlet_pressure, prop.Pressure(20.1, 'bar'))
        self.assertEqual(sperical_vessel.outlet_pressure, prop.Pressure(20, 'bar'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_inlet_temperature(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_8",
                          pressure_drop=(0.1, 'bar'))
        sperical_vessel.inlet_temperature = (50, 'C')
        self.assertEqual(sperical_vessel.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(sperical_vessel.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_outlet_temperature(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_9",
                          pressure_drop=(0.1, 'bar'))
        sperical_vessel.outlet_temperature = (130, 'F')
        self.assertLess(abs(sperical_vessel.inlet_temperature.value-130), 0.0001)
        self.assertEqual(sperical_vessel.inlet_temperature.unit, 'F')
        self.assertLess(abs(sperical_vessel.outlet_temperature.value-130), 0.0001)
        self.assertEqual(sperical_vessel.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_inlet_mass_flowrate(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_10",
                          pressure_drop=(0.1, 'bar'))
        sperical_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(sperical_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__SphericalVessels_setting_outlet_mass_flowrate(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_11",
                          pressure_drop=(0.10, 'bar'))
        sperical_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(sperical_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_inlet_stream_governed(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_sperical_vessel_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(sperical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of sperical_vessel are equal to inlet stream's.
        self.assertEqual(sperical_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(sperical_vessel.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(sperical_vessel.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(sperical_vessel.outlet_pressure, sperical_vessel.inlet_pressure - sperical_vessel.pressure_drop)
        self.assertLess(abs(sperical_vessel.inlet_temperature.value - sperical_vessel.outlet_temperature.value), 0.001)
        self.assertEqual(sperical_vessel.inlet_temperature.unit, sperical_vessel.outlet_temperature.unit)
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, sperical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_outlet_stream_governed(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_sperical_vessel_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(sperical_vessel.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of sperical_vessel are equal to outlet stream's.
        self.assertEqual(sperical_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(sperical_vessel.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(sperical_vessel.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(sperical_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(sperical_vessel.inlet_pressure, sperical_vessel.outlet_pressure + sperical_vessel.pressure_drop)
        self.assertLess(abs(sperical_vessel.inlet_temperature.value-sperical_vessel.outlet_temperature.value),0.0001)
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, sperical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_inlet_equipment_governed(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_14",
                          pressure_drop=(0.1, 'bar'))

        sperical_vessel.inlet_pressure = (30, 'bar')
        sperical_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        sperical_vessel.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_sperical_vessel_14")
        # Test connection is made.
        self.assertTrue(sperical_vessel.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of sperical_vessel are equal to inlet stream's.
        self.assertEqual(sperical_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(sperical_vessel.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(sperical_vessel.outlet_pressure, sperical_vessel.inlet_pressure - sperical_vessel.pressure_drop)
        self.assertEqual(sperical_vessel.inlet_temperature, sperical_vessel.outlet_temperature)
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, sperical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__SphericalVessels_connection_with_material_stream_outlet_equipment_governed(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_15",
                          pressure_drop=(0.1, 'bar'))
        sperical_vessel.outlet_pressure = (130, 'bar')
        sperical_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        sperical_vessel.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_sperical_vessel_15")
        # Test connection is made.
        self.assertTrue(sperical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of sperical_vessel are equal to outlet stream's.
        self.assertEqual(sperical_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(sperical_vessel.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(sperical_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(sperical_vessel.inlet_pressure, sperical_vessel.outlet_pressure + sperical_vessel.pressure_drop)
        self.assertEqual(sperical_vessel.inlet_temperature, sperical_vessel.outlet_temperature)
        self.assertEqual(sperical_vessel.inlet_mass_flowrate, sperical_vessel.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test__SphericalVessels_connection_with_energy_stream_inlet_equipment_governed(self):
    #     sperical_vessel = _SphericalVessels(tag="sperical_vessel_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     sperical_vessel_energy_expelled = EnergyStream(tag="Power_sperical_vessel_17", amount=(10,"MW"))
    #     sperical_vessel_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     sperical_vessel_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(sperical_vessel.connect_stream(sperical_vessel_inlet, "in", stream_governed=True))
    #     # Test inlet properties of sperical_vessel are equal to outlet stream's.
    #     self.assertAlmostEqual(sperical_vessel.energy_out.value, sperical_vessel_energy_expelled.amount.value)
    #     self.assertEqual(sperical_vessel.energy_out.unit, sperical_vessel_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test__SphericalVessels_stream_disconnection_by_stream_object(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_sperical_vessel_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_sperical_vessel_18")
        # Test connection is made.
        self.assertTrue(sperical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(sperical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(sperical_vessel.disconnect_stream(inlet_stream))
        self.assertTrue(sperical_vessel.disconnect_stream(outlet_stream))
        self.assertIsNone(sperical_vessel._inlet_material_stream_tag)
        self.assertIsNone(sperical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test__SphericalVessels_stream_disconnection_by_stream_tag(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_sperical_vessel_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_sperical_vessel_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(sperical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(sperical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(sperical_vessel.disconnect_stream(stream_tag="Inlet_sperical_vessel_19"))
        self.assertTrue(sperical_vessel.disconnect_stream(stream_tag="Outlet_sperical_vessel_19"))
        self.assertIsNone(sperical_vessel._inlet_material_stream_tag)
        self.assertIsNone(sperical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test__SphericalVessels_stream_disconnection_by_direction_stream_type(self):
        sperical_vessel = _SphericalVessels(tag="sperical_vessel_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_sperical_vessel_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_sperical_vessel_20")
        sperical_vessel_energy_expelled = EnergyStream(tag="Power_sperical_vessel_20")
        # Test connection is made.
        self.assertTrue(sperical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(sperical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(sperical_vessel.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(sperical_vessel.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(sperical_vessel._inlet_material_stream_tag)
        self.assertIsNone(sperical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)