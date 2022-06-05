import pytest
import unittest
from propylean.equipments.static import VerticalStorage
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop

class test_VerticalStorage(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_VerticalStorage_instantiation_only_tag(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_1")
        self.assertEqual(vertical_storage.tag, "vertical_storage_1")
        self.assertEqual(vertical_storage.pressure_drop, prop.Pressure(0))
        self.assertEqual(vertical_storage.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_VerticalStorage_instantiation_tag_and_pressure_drop(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_2",
                          pressure_drop=prop.Pressure(100, 'bar'))
        self.assertEqual(vertical_storage.tag, "vertical_storage_2")
        self.assertEqual(vertical_storage.pressure_drop, prop.Pressure(100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_VerticalStorage_instantiation_no_arguments(self):
        vertical_storage = VerticalStorage()
        self.assertIsNotNone(vertical_storage.tag)
        self.assertEqual(vertical_storage.pressure_drop, prop.Pressure(0))
        self.assertEqual(vertical_storage.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    def test_VerticalStorage_representation(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_5")
        self.assertIn("Vertical Storage with tag: vertical_storage_5", str(vertical_storage))
    
    @pytest.mark.positive
    def test_VerticalStorage_setting_inlet_pressure(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_6",
                          pressure_drop=(0.1, 'bar'))
        vertical_storage.inlet_pressure = (30, 'bar')
        self.assertEqual(vertical_storage.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(vertical_storage.outlet_pressure, prop.Pressure(29.9, 'bar'))
    
    @pytest.mark.positive
    def test_VerticalStorage_setting_outlet_pressure(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_7",
                          pressure_drop=(0.1, 'bar'))
        vertical_storage.outlet_pressure = (20, 'bar')
        self.assertEqual(vertical_storage.inlet_pressure, prop.Pressure(20.1, 'bar'))
        self.assertEqual(vertical_storage.outlet_pressure, prop.Pressure(20, 'bar'))
    
    @pytest.mark.positive
    def test_VerticalStorage_setting_inlet_temperature(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_8",
                          pressure_drop=(0.1, 'bar'))
        vertical_storage.inlet_temperature = (50, 'C')
        self.assertEqual(vertical_storage.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(vertical_storage.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_VerticalStorage_setting_outlet_temperature(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_9",
                          pressure_drop=(0.1, 'bar'))
        vertical_storage.outlet_temperature = (130, 'F')
        self.assertLess(abs(vertical_storage.inlet_temperature.value-130), 0.0001)
        self.assertEqual(vertical_storage.inlet_temperature.unit, 'F')
        self.assertLess(abs(vertical_storage.outlet_temperature.value-130), 0.0001)
        self.assertEqual(vertical_storage.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_VerticalStorage_setting_inlet_mass_flowrate(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_10",
                          pressure_drop=(0.1, 'bar'))
        vertical_storage.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(vertical_storage.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(vertical_storage.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_VerticalStorage_setting_outlet_mass_flowrate(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_11",
                          pressure_drop=(0.10, 'bar'))
        vertical_storage.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(vertical_storage.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(vertical_storage.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_VerticalStorage_connection_with_material_stream_inlet_stream_governed(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_storage_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(vertical_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of vertical_storage are equal to inlet stream's.
        self.assertEqual(vertical_storage.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(vertical_storage.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(vertical_storage.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(vertical_storage.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(vertical_storage.outlet_pressure, vertical_storage.inlet_pressure - vertical_storage.pressure_drop)
        self.assertLess(abs(vertical_storage.inlet_temperature.value - vertical_storage.outlet_temperature.value), 0.001)
        self.assertEqual(vertical_storage.inlet_temperature.unit, vertical_storage.outlet_temperature.unit)
        self.assertEqual(vertical_storage.inlet_mass_flowrate, vertical_storage.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_VerticalStorage_connection_with_material_stream_outlet_stream_governed(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_vertical_storage_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(vertical_storage.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of vertical_storage are equal to outlet stream's.
        self.assertEqual(vertical_storage.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(vertical_storage.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(vertical_storage.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(vertical_storage.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(vertical_storage.inlet_pressure, vertical_storage.outlet_pressure + vertical_storage.pressure_drop)
        self.assertLess(abs(vertical_storage.inlet_temperature.value-vertical_storage.outlet_temperature.value),0.0001)
        self.assertEqual(vertical_storage.inlet_mass_flowrate, vertical_storage.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_VerticalStorage_connection_with_material_stream_inlet_equipment_governed(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_14",
                          pressure_drop=(0.1, 'bar'))

        vertical_storage.inlet_pressure = (30, 'bar')
        vertical_storage.inlet_mass_flowrate = (1000, 'kg/h')
        vertical_storage.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_vertical_storage_14")
        # Test connection is made.
        self.assertTrue(vertical_storage.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of vertical_storage are equal to inlet stream's.
        self.assertEqual(vertical_storage.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(vertical_storage.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(vertical_storage.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(vertical_storage.outlet_pressure, vertical_storage.inlet_pressure - vertical_storage.pressure_drop)
        self.assertEqual(vertical_storage.inlet_temperature, vertical_storage.outlet_temperature)
        self.assertEqual(vertical_storage.inlet_mass_flowrate, vertical_storage.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_VerticalStorage_connection_with_material_stream_outlet_equipment_governed(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_15",
                          pressure_drop=(0.1, 'bar'))
        vertical_storage.outlet_pressure = (130, 'bar')
        vertical_storage.outlet_mass_flowrate = (1000, 'kg/h')
        vertical_storage.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_vertical_storage_15")
        # Test connection is made.
        self.assertTrue(vertical_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of vertical_storage are equal to outlet stream's.
        self.assertEqual(vertical_storage.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(vertical_storage.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(vertical_storage.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(vertical_storage.inlet_pressure, vertical_storage.outlet_pressure + vertical_storage.pressure_drop)
        self.assertEqual(vertical_storage.inlet_temperature, vertical_storage.outlet_temperature)
        self.assertEqual(vertical_storage.inlet_mass_flowrate, vertical_storage.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test_VerticalStorage_connection_with_energy_stream_inlet_equipment_governed(self):
    #     vertical_storage = VerticalStorage(tag="vertical_storage_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     vertical_storage_energy_expelled = EnergyStream(tag="Power_vertical_storage_17", amount=(10,"MW"))
    #     vertical_storage_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     vertical_storage_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(vertical_storage.connect_stream(vertical_storage_inlet, "in", stream_governed=True))
    #     # Test inlet properties of vertical_storage are equal to outlet stream's.
    #     self.assertAlmostEqual(vertical_storage.energy_out.value, vertical_storage_energy_expelled.amount.value)
    #     self.assertEqual(vertical_storage.energy_out.unit, vertical_storage_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test_VerticalStorage_stream_disconnection_by_stream_object(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_storage_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_vertical_storage_18")
        # Test connection is made.
        self.assertTrue(vertical_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(vertical_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(vertical_storage.disconnect_stream(inlet_stream))
        self.assertTrue(vertical_storage.disconnect_stream(outlet_stream))
        self.assertIsNone(vertical_storage._inlet_material_stream_tag)
        self.assertIsNone(vertical_storage._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_VerticalStorage_stream_disconnection_by_stream_tag(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_storage_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_vertical_storage_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(vertical_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(vertical_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(vertical_storage.disconnect_stream(stream_tag="Inlet_vertical_storage_19"))
        self.assertTrue(vertical_storage.disconnect_stream(stream_tag="Outlet_vertical_storage_19"))
        self.assertIsNone(vertical_storage._inlet_material_stream_tag)
        self.assertIsNone(vertical_storage._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_VerticalStorage_stream_disconnection_by_direction_stream_type(self):
        vertical_storage = VerticalStorage(tag="vertical_storage_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_storage_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_vertical_storage_20")
        vertical_storage_energy_expelled = EnergyStream(tag="Power_vertical_storage_20")
        # Test connection is made.
        self.assertTrue(vertical_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(vertical_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(vertical_storage.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(vertical_storage.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(vertical_storage._inlet_material_stream_tag)
        self.assertIsNone(vertical_storage._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)