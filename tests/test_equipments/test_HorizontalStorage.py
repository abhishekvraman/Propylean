import pytest
import unittest
from propylean.equipments.static import HorizontalStorage
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop

class test_HorizontalStorage(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_HorizontalStorage_instantiation_only_tag(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_1")
        self.assertEqual(horizontal_storage.tag, "horizontal_storage_1")
        self.assertEqual(horizontal_storage.pressure_drop, prop.Pressure(0))
        self.assertEqual(horizontal_storage.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_HorizontalStorage_instantiation_tag_and_pressure_drop(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_2",
                          pressure_drop=prop.Pressure(100, 'bar'))
        self.assertEqual(horizontal_storage.tag, "horizontal_storage_2")
        self.assertEqual(horizontal_storage.pressure_drop, prop.Pressure(100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_HorizontalStorage_instantiation_no_arguments(self):
        horizontal_storage = HorizontalStorage()
        self.assertIsNotNone(horizontal_storage.tag)
        self.assertEqual(horizontal_storage.pressure_drop, prop.Pressure(0))
        self.assertEqual(horizontal_storage.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    def test_HorizontalStorage_representation(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_5")
        self.assertIn("Horizontal Storage with tag: horizontal_storage_5", str(horizontal_storage))
    
    @pytest.mark.positive
    def test_HorizontalStorage_setting_inlet_pressure(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_6",
                          pressure_drop=(0.1, 'bar'))
        horizontal_storage.inlet_pressure = (30, 'bar')
        self.assertEqual(horizontal_storage.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(horizontal_storage.outlet_pressure, prop.Pressure(29.9, 'bar'))
    
    @pytest.mark.positive
    def test_HorizontalStorage_setting_outlet_pressure(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_7",
                          pressure_drop=(0.1, 'bar'))
        horizontal_storage.outlet_pressure = (20, 'bar')
        self.assertEqual(horizontal_storage.inlet_pressure, prop.Pressure(20.1, 'bar'))
        self.assertEqual(horizontal_storage.outlet_pressure, prop.Pressure(20, 'bar'))
    
    @pytest.mark.positive
    def test_HorizontalStorage_setting_inlet_temperature(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_8",
                          pressure_drop=(0.1, 'bar'))
        horizontal_storage.inlet_temperature = (50, 'C')
        self.assertEqual(horizontal_storage.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(horizontal_storage.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_HorizontalStorage_setting_outlet_temperature(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_9",
                          pressure_drop=(0.1, 'bar'))
        horizontal_storage.outlet_temperature = (130, 'F')
        self.assertLess(abs(horizontal_storage.inlet_temperature.value-130), 0.0001)
        self.assertEqual(horizontal_storage.inlet_temperature.unit, 'F')
        self.assertLess(abs(horizontal_storage.outlet_temperature.value-130), 0.0001)
        self.assertEqual(horizontal_storage.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_HorizontalStorage_setting_inlet_mass_flowrate(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_10",
                          pressure_drop=(0.1, 'bar'))
        horizontal_storage.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(horizontal_storage.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_HorizontalStorage_setting_outlet_mass_flowrate(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_11",
                          pressure_drop=(0.10, 'bar'))
        horizontal_storage.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(horizontal_storage.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_HorizontalStorage_connection_with_material_stream_inlet_stream_governed(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_storage_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(horizontal_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of horizontal_storage are equal to inlet stream's.
        self.assertEqual(horizontal_storage.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(horizontal_storage.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(horizontal_storage.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(horizontal_storage.outlet_pressure, horizontal_storage.inlet_pressure - horizontal_storage.pressure_drop)
        self.assertLess(abs(horizontal_storage.inlet_temperature.value - horizontal_storage.outlet_temperature.value), 0.001)
        self.assertEqual(horizontal_storage.inlet_temperature.unit, horizontal_storage.outlet_temperature.unit)
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, horizontal_storage.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_HorizontalStorage_connection_with_material_stream_outlet_stream_governed(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_horizontal_storage_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(horizontal_storage.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of horizontal_storage are equal to outlet stream's.
        self.assertEqual(horizontal_storage.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(horizontal_storage.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(horizontal_storage.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(horizontal_storage.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(horizontal_storage.inlet_pressure, horizontal_storage.outlet_pressure + horizontal_storage.pressure_drop)
        self.assertLess(abs(horizontal_storage.inlet_temperature.value-horizontal_storage.outlet_temperature.value),0.0001)
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, horizontal_storage.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_HorizontalStorage_connection_with_material_stream_inlet_equipment_governed(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_14",
                          pressure_drop=(0.1, 'bar'))

        horizontal_storage.inlet_pressure = (30, 'bar')
        horizontal_storage.inlet_mass_flowrate = (1000, 'kg/h')
        horizontal_storage.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_horizontal_storage_14")
        # Test connection is made.
        self.assertTrue(horizontal_storage.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of horizontal_storage are equal to inlet stream's.
        self.assertEqual(horizontal_storage.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(horizontal_storage.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(horizontal_storage.outlet_pressure, horizontal_storage.inlet_pressure - horizontal_storage.pressure_drop)
        self.assertEqual(horizontal_storage.inlet_temperature, horizontal_storage.outlet_temperature)
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, horizontal_storage.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_HorizontalStorage_connection_with_material_stream_outlet_equipment_governed(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_15",
                          pressure_drop=(0.1, 'bar'))
        horizontal_storage.outlet_pressure = (130, 'bar')
        horizontal_storage.outlet_mass_flowrate = (1000, 'kg/h')
        horizontal_storage.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_horizontal_storage_15")
        # Test connection is made.
        self.assertTrue(horizontal_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of horizontal_storage are equal to outlet stream's.
        self.assertEqual(horizontal_storage.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(horizontal_storage.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(horizontal_storage.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(horizontal_storage.inlet_pressure, horizontal_storage.outlet_pressure + horizontal_storage.pressure_drop)
        self.assertEqual(horizontal_storage.inlet_temperature, horizontal_storage.outlet_temperature)
        self.assertEqual(horizontal_storage.inlet_mass_flowrate, horizontal_storage.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test_HorizontalStorage_connection_with_energy_stream_inlet_equipment_governed(self):
    #     horizontal_storage = HorizontalStorage(tag="horizontal_storage_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     horizontal_storage_energy_expelled = EnergyStream(tag="Power_horizontal_storage_17", amount=(10,"MW"))
    #     horizontal_storage_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     horizontal_storage_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(horizontal_storage.connect_stream(horizontal_storage_inlet, "in", stream_governed=True))
    #     # Test inlet properties of horizontal_storage are equal to outlet stream's.
    #     self.assertAlmostEqual(horizontal_storage.energy_out.value, horizontal_storage_energy_expelled.amount.value)
    #     self.assertEqual(horizontal_storage.energy_out.unit, horizontal_storage_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test_HorizontalStorage_stream_disconnection_by_stream_object(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_storage_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_horizontal_storage_18")
        # Test connection is made.
        self.assertTrue(horizontal_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(horizontal_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(horizontal_storage.disconnect_stream(inlet_stream))
        self.assertTrue(horizontal_storage.disconnect_stream(outlet_stream))
        self.assertIsNone(horizontal_storage._inlet_material_stream_tag)
        self.assertIsNone(horizontal_storage._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_HorizontalStorage_stream_disconnection_by_stream_tag(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_storage_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_horizontal_storage_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(horizontal_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(horizontal_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(horizontal_storage.disconnect_stream(stream_tag="Inlet_horizontal_storage_19"))
        self.assertTrue(horizontal_storage.disconnect_stream(stream_tag="Outlet_horizontal_storage_19"))
        self.assertIsNone(horizontal_storage._inlet_material_stream_tag)
        self.assertIsNone(horizontal_storage._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_HorizontalStorage_stream_disconnection_by_direction_stream_type(self):
        horizontal_storage = HorizontalStorage(tag="horizontal_storage_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_storage_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_horizontal_storage_20")
        horizontal_storage_energy_expelled = EnergyStream(tag="Power_horizontal_storage_20")
        # Test connection is made.
        self.assertTrue(horizontal_storage.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(horizontal_storage.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(horizontal_storage.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(horizontal_storage.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(horizontal_storage._inlet_material_stream_tag)
        self.assertIsNone(horizontal_storage._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)