import pytest
import unittest
from propylean.instruments.measurement import FlowMeter
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop

class test_FlowMeter(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_FlowMeter_instantiation_only_tag(self):
        flow_meter = FlowMeter(tag="flow_meter_1")
        self.assertEqual(flow_meter.tag, "flow_meter_1")
        self.assertEqual(flow_meter.pressure_drop, prop.Pressure(0))
        self.assertEqual(flow_meter.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_FlowMeter_instantiation_tag_and_pressure_drop(self):
        flow_meter = FlowMeter(tag="flow_meter_2",
                          pressure_drop=prop.Pressure(100, 'bar'))
        self.assertEqual(flow_meter.tag, "flow_meter_2")
        self.assertEqual(flow_meter.pressure_drop, prop.Pressure(100, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test_FlowMeter_instantiation_no_arguments(self):
        flow_meter = FlowMeter()
        self.assertIsNotNone(flow_meter.tag)
        self.assertEqual(flow_meter.pressure_drop, prop.Pressure(0))
        self.assertEqual(flow_meter.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    def test_FlowMeter_representation(self):
        flow_meter = FlowMeter(tag="flow_meter_5")
        self.assertIn("Flow Meter with tag: flow_meter_5", str(flow_meter))
    
    @pytest.mark.positive
    def test_FlowMeter_setting_inlet_pressure(self):
        flow_meter = FlowMeter(tag="flow_meter_6",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.inlet_pressure = (30, 'bar')
        self.assertEqual(flow_meter.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(flow_meter.outlet_pressure, prop.Pressure(29.9, 'bar'))
    
    @pytest.mark.positive
    def test_FlowMeter_setting_outlet_pressure(self):
        flow_meter = FlowMeter(tag="flow_meter_7",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.outlet_pressure = (20, 'bar')
        self.assertEqual(flow_meter.inlet_pressure, prop.Pressure(20.1, 'bar'))
        self.assertEqual(flow_meter.outlet_pressure, prop.Pressure(20, 'bar'))
    
    @pytest.mark.positive
    def test_FlowMeter_setting_inlet_temperature(self):
        flow_meter = FlowMeter(tag="flow_meter_8",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.inlet_temperature = (50, 'C')
        self.assertEqual(flow_meter.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(flow_meter.outlet_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test_FlowMeter_setting_outlet_temperature(self):
        flow_meter = FlowMeter(tag="flow_meter_9",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.outlet_temperature = (130, 'F')
        self.assertLess(abs(flow_meter.inlet_temperature.value-130), 0.0001)
        self.assertEqual(flow_meter.inlet_temperature.unit, 'F')
        self.assertLess(abs(flow_meter.outlet_temperature.value-130), 0.0001)
        self.assertEqual(flow_meter.outlet_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test_FlowMeter_setting_inlet_mass_flowrate(self):
        flow_meter = FlowMeter(tag="flow_meter_10",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(flow_meter.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(flow_meter.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_FlowMeter_setting_outlet_mass_flowrate(self):
        flow_meter = FlowMeter(tag="flow_meter_11",
                          pressure_drop=(0.10, 'bar'))
        flow_meter.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(flow_meter.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(flow_meter.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test_FlowMeter_connection_with_material_stream_inlet_stream_governed(self):
        flow_meter = FlowMeter(tag="flow_meter_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of flow_meter are equal to inlet stream's.
        self.assertEqual(flow_meter.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(flow_meter.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(flow_meter.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(flow_meter.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(flow_meter.outlet_pressure, flow_meter.inlet_pressure - flow_meter.pressure_drop)
        self.assertLess(abs(flow_meter.inlet_temperature.value - flow_meter.outlet_temperature.value), 0.001)
        self.assertEqual(flow_meter.inlet_temperature.unit, flow_meter.outlet_temperature.unit)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_FlowMeter_connection_with_material_stream_outlet_stream_governed(self):
        flow_meter = FlowMeter(tag="flow_meter_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of flow_meter are equal to outlet stream's.
        self.assertEqual(flow_meter.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(flow_meter.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(flow_meter.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(flow_meter.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(flow_meter.inlet_pressure, flow_meter.outlet_pressure + flow_meter.pressure_drop)
        self.assertLess(abs(flow_meter.inlet_temperature.value-flow_meter.outlet_temperature.value),0.0001)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_FlowMeter_connection_with_material_stream_inlet_equipment_governed(self):
        flow_meter = FlowMeter(tag="flow_meter_14",
                          pressure_drop=(0.1, 'bar'))

        flow_meter.inlet_pressure = (30, 'bar')
        flow_meter.inlet_mass_flowrate = (1000, 'kg/h')
        flow_meter.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_14")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of flow_meter are equal to inlet stream's.
        self.assertEqual(flow_meter.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(flow_meter.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(flow_meter.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(flow_meter.outlet_pressure, flow_meter.inlet_pressure - flow_meter.pressure_drop)
        self.assertEqual(flow_meter.inlet_temperature, flow_meter.outlet_temperature)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    @pytest.mark.positive
    def test_FlowMeter_connection_with_material_stream_outlet_equipment_governed(self):
        flow_meter = FlowMeter(tag="flow_meter_15",
                          pressure_drop=(0.1, 'bar'))
        flow_meter.outlet_pressure = (130, 'bar')
        flow_meter.outlet_mass_flowrate = (1000, 'kg/h')
        flow_meter.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_15")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of flow_meter are equal to outlet stream's.
        self.assertEqual(flow_meter.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(flow_meter.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(flow_meter.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(flow_meter.inlet_pressure, flow_meter.outlet_pressure + flow_meter.pressure_drop)
        self.assertEqual(flow_meter.inlet_temperature, flow_meter.outlet_temperature)
        self.assertEqual(flow_meter.inlet_mass_flowrate, flow_meter.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test_FlowMeter_connection_with_energy_stream_inlet_equipment_governed(self):
    #     flow_meter = FlowMeter(tag="flow_meter_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     flow_meter_energy_expelled = EnergyStream(tag="Power_flow_meter_17", amount=(10,"MW"))
    #     flow_meter_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     flow_meter_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(flow_meter.connect_stream(flow_meter_inlet, "in", stream_governed=True))
    #     # Test inlet properties of flow_meter are equal to outlet stream's.
    #     self.assertAlmostEqual(flow_meter.energy_out.value, flow_meter_energy_expelled.amount.value)
    #     self.assertEqual(flow_meter.energy_out.unit, flow_meter_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test_FlowMeter_stream_disconnection_by_stream_object(self):
        flow_meter = FlowMeter(tag="flow_meter_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_18")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(flow_meter.disconnect_stream(inlet_stream))
        self.assertTrue(flow_meter.disconnect_stream(outlet_stream))
        self.assertIsNone(flow_meter._inlet_material_stream_tag)
        self.assertIsNone(flow_meter._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test_FlowMeter_stream_disconnection_by_stream_tag(self):
        flow_meter = FlowMeter(tag="flow_meter_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(flow_meter.disconnect_stream(stream_tag="Inlet_flow_meter_19"))
        self.assertTrue(flow_meter.disconnect_stream(stream_tag="Outlet_flow_meter_19"))
        self.assertIsNone(flow_meter._inlet_material_stream_tag)
        self.assertIsNone(flow_meter._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test_FlowMeter_stream_disconnection_by_direction_stream_type(self):
        flow_meter = FlowMeter(tag="flow_meter_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_flow_meter_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_flow_meter_20")
        flow_meter_energy_expelled = EnergyStream(tag="Power_flow_meter_20")
        # Test connection is made.
        self.assertTrue(flow_meter.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(flow_meter.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(flow_meter.disconnect_stream(direction="In", stream_type="Material"))
        self.assertTrue(flow_meter.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(flow_meter._inlet_material_stream_tag)
        self.assertIsNone(flow_meter._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)