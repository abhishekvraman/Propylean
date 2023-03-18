import pytest
import unittest
from propylean.equipments.generic_equipment_classes import _VerticalVessels
from propylean.streams import MaterialStream, EnergyStream
from propylean.constants import Constants
import propylean.properties as prop

class test__VerticalVessels(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__VerticalVessels_instantiation_only_tag(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_1")
        self.assertEqual(vertical_vessel.tag, "vertical_vessel_1")
        self.assertEqual(vertical_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(vertical_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__VerticalVessels_instantiation_tag_and_pressure_drop(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_2")
        vertical_vessel.operating_pressure = prop.Pressure(10, "bar")
        self.assertEqual(vertical_vessel.tag, "vertical_vessel_2")
        self.assertEqual(vertical_vessel.operating_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(vertical_vessel.outlet_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(vertical_vessel.inlet_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(vertical_vessel.pressure_drop, prop.Pressure(0, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__VerticalVessels_instantiation_no_arguments(self):
        vertical_vessel = _VerticalVessels()
        self.assertIsNotNone(vertical_vessel.tag)
        self.assertEqual(vertical_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(vertical_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.length_setting
    def test__VerticalVessels_instantiation_vessel_dimensions_arguments(self):
        vertical_vessel = _VerticalVessels(ID = (4, "m"),
                                               OD = 6,
                                               length=prop.Length(10))

        self.assertEqual(vertical_vessel.ID, prop.Length(4, "m"))
        self.assertEqual(vertical_vessel.OD, prop.Length(6, "m"))
        self.assertEqual(vertical_vessel.thickness, prop.Length(2, "m"))
        self.assertEqual(vertical_vessel.length, prop.Length(10, "m"))

        Vertical_vessel = _VerticalVessels(thickness = (2, "m"),
                                               OD = 6,
                                               length=prop.Length(10))
        self.assertEqual(Vertical_vessel.ID, prop.Length(4, "m"))
        self.assertEqual(Vertical_vessel.OD, prop.Length(6, "m"))
        self.assertEqual(Vertical_vessel.thickness, prop.Length(2, "m"))
        self.assertEqual(Vertical_vessel.length, prop.Length(10, "m"))

    @pytest.mark.positive
    @pytest.mark.length_setting
    def test__VerticalVessels_instantiation_level_settings_arguments(self):
        vertical_vessel = _VerticalVessels(LLLL=(10, "inch"),
                                             LLL=(20, "inch"),
                                             NLL=prop.Length(30, "inch"),
                                             HLL=prop.Length(40, "inch"),
                                             HHLL=(50, "inch"))

        self.assertEqual(vertical_vessel.LLLL, prop.Length(10, "inch"))
        self.assertEqual(vertical_vessel.LLL, prop.Length(20, "inch"))
        self.assertEqual(vertical_vessel.NLL, prop.Length(30, "inch"))
        self.assertEqual(vertical_vessel.HLL, prop.Length(40, "inch"))
        self.assertEqual(vertical_vessel.HHLL, prop.Length(50, "inch"))
    
    @pytest.mark.positive
    @pytest.mark.head_type
    def test__VerticalVessels_instantiation_head_type_argument(self):
        for head_type in Constants.HEAD_TYPES:
            Vertical_vessel = _VerticalVessels(ID = (4, "m"),
                                                OD = 6,
                                                length=prop.Length(10),
                                                head_type=head_type)
            self.assertEqual(Vertical_vessel.head_type, head_type)
    
    @pytest.mark.positive
    @pytest.mark.main_fluid
    def test__VerticalVessels_instantiation_main_fluid_argument(self):
        for main_fluid in ["liquid", "gas"]:
            Vertical_vessel = _VerticalVessels(ID = (4, "m"),
                                                OD = 6,
                                                length=prop.Length(10),
                                                main_fluid=main_fluid)
            self.assertEqual(Vertical_vessel.main_fluid, main_fluid)
    
    @pytest.mark.positive
    def test__VerticalVessels_setting_inlet_pressure(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_6",
                          pressure_drop=(0.1, 'bar'))
        vertical_vessel.inlet_pressure = (30, 'bar')
        self.assertEqual(vertical_vessel.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(vertical_vessel.outlet_pressure, prop.Pressure(29.9, 'bar'))
        self.assertEqual(vertical_vessel.operating_pressure, prop.Pressure(30, 'bar'))
    
    @pytest.mark.positive
    def test__VerticalVessels_setting_outlet_pressure(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_7",
                          pressure_drop=(0.1, 'bar'))
        vertical_vessel.outlet_pressure = (20, 'bar')
        self.assertEqual(vertical_vessel.inlet_pressure, prop.Pressure(20.1, 'bar'))
        self.assertEqual(vertical_vessel.operating_pressure, prop.Pressure(20.1, 'bar'))
    
    @pytest.mark.positive
    def test__VerticalVessels_setting_inlet_temperature(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_8",
                          pressure_drop=(0.1, 'bar'))
        vertical_vessel.inlet_temperature = (50, 'C')
        self.assertEqual(vertical_vessel.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(vertical_vessel.operating_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test__VerticalVessels_setting_outlet_temperature(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_9",
                          pressure_drop=(0.1, 'bar'))
        vertical_vessel.outlet_temperature = (130, 'F')
        self.assertLess(abs(vertical_vessel.inlet_temperature.value-130), 0.0001)
        self.assertEqual(vertical_vessel.inlet_temperature.unit, 'F')
        self.assertLess(abs(vertical_vessel.operating_temperature.value-130), 0.0001)
        self.assertEqual(vertical_vessel.operating_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test__VerticalVessels_setting_inlet_mass_flowrate(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_10",
                          pressure_drop=(0.1, 'bar'))
        vertical_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(vertical_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__VerticalVessels_setting_outlet_mass_flowrate(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_11",
                          pressure_drop=(0.10, 'bar'))
        vertical_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(vertical_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__VerticalVessels_connection_with_material_stream_inlet_stream_governed(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_vessel_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(vertical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of vertical_vessel are equal to inlet stream's.
        self.assertEqual(vertical_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(vertical_vessel.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(vertical_vessel.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(vertical_vessel.outlet_pressure, vertical_vessel.inlet_pressure - vertical_vessel.pressure_drop)
        self.assertLess(abs(vertical_vessel.inlet_temperature.value - vertical_vessel.outlet_temperature.value), 0.001)
        self.assertEqual(vertical_vessel.inlet_temperature.unit, vertical_vessel.outlet_temperature.unit)
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, vertical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__VerticalVessels_connection_with_material_stream_outlet_stream_governed(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_vertical_vessel_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(vertical_vessel.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of vertical_vessel are equal to outlet stream's.
        self.assertEqual(vertical_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(vertical_vessel.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(vertical_vessel.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(vertical_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(vertical_vessel.inlet_pressure, vertical_vessel.outlet_pressure + vertical_vessel.pressure_drop)
        self.assertLess(abs(vertical_vessel.inlet_temperature.value-vertical_vessel.outlet_temperature.value),0.0001)
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, vertical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__VerticalVessels_connection_with_material_stream_inlet_equipment_governed(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_14",
                          pressure_drop=(0.1, 'bar'))

        vertical_vessel.inlet_pressure = (30, 'bar')
        vertical_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        vertical_vessel.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_vertical_vessel_14")
        # Test connection is made.
        self.assertTrue(vertical_vessel.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of vertical_vessel are equal to inlet stream's.
        self.assertEqual(vertical_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(vertical_vessel.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(vertical_vessel.outlet_pressure, vertical_vessel.inlet_pressure - vertical_vessel.pressure_drop)
        self.assertEqual(vertical_vessel.inlet_temperature, vertical_vessel.outlet_temperature)
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, vertical_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__VerticalVessels_connection_with_material_stream_outlet_equipment_governed(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_15",
                          pressure_drop=(0.1, 'bar'))
        vertical_vessel.outlet_pressure = (130, 'bar')
        vertical_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        vertical_vessel.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_vertical_vessel_15")
        # Test connection is made.
        self.assertTrue(vertical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of vertical_vessel are equal to outlet stream's.
        self.assertEqual(vertical_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(vertical_vessel.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(vertical_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(vertical_vessel.inlet_pressure, vertical_vessel.outlet_pressure + vertical_vessel.pressure_drop)
        self.assertEqual(vertical_vessel.inlet_temperature, vertical_vessel.outlet_temperature)
        self.assertEqual(vertical_vessel.inlet_mass_flowrate, vertical_vessel.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test__VerticalVessels_connection_with_energy_stream_inlet_equipment_governed(self):
    #     vertical_vessel = _VerticalVessels(tag="vertical_vessel_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     vertical_vessel_energy_expelled = EnergyStream(tag="Power_vertical_vessel_17", amount=(10,"MW"))
    #     vertical_vessel_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     vertical_vessel_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(vertical_vessel.connect_stream(vertical_vessel_inlet, "in", stream_governed=True))
    #     # Test inlet properties of vertical_vessel are equal to outlet stream's.
    #     self.assertAlmostEqual(vertical_vessel.energy_out.value, vertical_vessel_energy_expelled.amount.value)
    #     self.assertEqual(vertical_vessel.energy_out.unit, vertical_vessel_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test__VerticalVessels_stream_disconnection_by_stream_object(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_vessel_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_vertical_vessel_18")
        # Test connection is made.
        self.assertTrue(vertical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(vertical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(vertical_vessel.disconnect_stream(inlet_stream))
        self.assertTrue(vertical_vessel.disconnect_stream(outlet_stream))
        self.assertIsNone(vertical_vessel._inlet_material_stream_tag)
        self.assertIsNone(vertical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test__VerticalVessels_stream_disconnection_by_stream_tag(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_vessel_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_vertical_vessel_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(vertical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(vertical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(vertical_vessel.disconnect_stream(stream_tag="Inlet_vertical_vessel_19"))
        self.assertTrue(vertical_vessel.disconnect_stream(stream_tag="Outlet_vertical_vessel_19"))
        self.assertIsNone(vertical_vessel._inlet_material_stream_tag)
        self.assertIsNone(vertical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test__VerticalVessels_stream_disconnection_by_direction_stream_type(self):
        vertical_vessel = _VerticalVessels(tag="vertical_vessel_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_vertical_vessel_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_vertical_vessel_20")
        vertical_vessel_energy_expelled = EnergyStream(tag="Power_vertical_vessel_20")
        # Test connection is made.
        self.assertTrue(vertical_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(vertical_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(vertical_vessel.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(vertical_vessel.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(vertical_vessel._inlet_material_stream_tag)
        self.assertIsNone(vertical_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.liquid_level
    def test__VerticalVessels_liquid_level(self):
        Vertical_vessel = _VerticalVessels(tag="Vertical_vessel_21",
                                               NLL=(20, "m"))
        self.assertEqual(Vertical_vessel.NLL, Vertical_vessel.liquid_level)
    
    @pytest.mark.positive
    @pytest.mark.vessel_volume
    def test__VerticalVessels_volume_calculations_elliptical(self):
        """ Filled Volume	m3		46.08
            Total Volume	m3	142.4
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            Inside Dish Depth, a 1000 mm
            Level, H 3000 mm
        """
        Vertical_vessel = _VerticalVessels(tag="Vertical_vessel_22",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="elliptical")
        Vertical_vessel.liquid_level = prop.Length(3.0, "m")
        Vertical_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(142.4, "m^3")
        expected_liquid_volume = prop.Volume(46.08)
        self.assertAlmostEqual(Vertical_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(Vertical_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = Vertical_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit)      

    @pytest.mark.positive
    @pytest.mark.vessel_volume
    def test__VerticalVessels_volume_calculations_torispherical(self):
        """ ASME F&D/ Torispherical	f = 1	k = 0.06
            Standard F&D	f = 1	k = 0.75" to 2"
            80:10 F&D	f = 0.8	k = 0.1
            Filled Volume	m3	19.29
            Total Volume	m3	136.0
            Inside Dish Depth (a)	mm	677.4
            Dish Radius (fD)	mm	4000
            Knuckle Radius (kD)	mm	300.0
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            Level, H 1800 mm
            f, Dish Radius parameter
            1.0
            k, Knuckle Radius parameter
            0.06
        """
        Vertical_vessel = _VerticalVessels(tag="Vertical_vessel_23",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="torispherical")
        Vertical_vessel.liquid_level = prop.Length(3, "m")
        Vertical_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(158.93, "m^3")
        expected_liquid_volume = prop.Volume(70.97)
        self.assertAlmostEqual(Vertical_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(Vertical_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = Vertical_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit)        

    @pytest.mark.positive
    @pytest.mark.vessel_volume
    def test__VerticalVessels_volume_calculations_hemispherical(self):
        """ Filled Volume	m3	54.45
            Total Volume	m3	159.2
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            Inside Dish Depth, a 1000 mm
            Level, H 3000 mm
        """
        Vertical_vessel = _VerticalVessels(tag="Vertical_vessel_24",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="hemispherical")
        Vertical_vessel.liquid_level = prop.Length(3.0, "m")
        Vertical_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(159.2, "m^3")
        expected_liquid_volume = prop.Volume(54.45)
        self.assertAlmostEqual(Vertical_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(Vertical_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = Vertical_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit)  

    @pytest.mark.vessel_volume
    def test__VerticalVessels_volume_calculations_flat(self):
        """ Filled Volume	m3	22.62
            Total Volume	m3	125.7
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            Inside Dish Depth, a 1000 mm
            Level, H 1800 mm
        """
        Vertical_vessel = _VerticalVessels(tag="Vertical_vessel_25",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flat")
        Vertical_vessel.liquid_level = prop.Length(1.8, "m")
        Vertical_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(125.7, "m^3")
        expected_liquid_volume = prop.Volume(22.62)
        self.assertAlmostEqual(Vertical_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(Vertical_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = Vertical_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit)        

    @pytest.mark.negative
    def test__VerticalVessels_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__VerticalVessels_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__VerticalVessels_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.pressure_drop = []
        self.assertIn("Incorrect type 'list' provided to 'pressure_drop'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))                                    

    @pytest.mark.negative
    def test__VerticalVessels_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.design_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'design_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__VerticalVessels_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__VerticalVessels_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__VerticalVessels_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_decrease'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__VerticalVessels_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.temperature_increase = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_increase'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test__VerticalVessels_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.design_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'design_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test__VerticalVessels_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__VerticalVessels_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__VerticalVessels_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.energy_in = []
        self.assertIn("Incorrect type 'list' provided to 'energy_in'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))      

    @pytest.mark.negative
    def test__VerticalVessels_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.energy_out = []
        self.assertIn("Incorrect type 'list' provided to 'energy_out'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))                               

    @pytest.mark.negative
    def test__VerticalVessels_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            Veritcal_vessel = _VerticalVessels(
                                               ID=[4, "m"], length=(10, "m"),
                                               head_type="flat")
        self.assertIn("Incorrect type 'list' provided to 'ID'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.ID = []
        self.assertIn("Incorrect type 'list' provided to 'ID'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test__VerticalVessels_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            Veritcal_vessel = _VerticalVessels(
                                               ID=(4, "m"), length=[10, "m"],
                                               head_type="flat")
        self.assertIn("Incorrect type 'list' provided to 'length'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.length = []
        self.assertIn("Incorrect type 'list' provided to 'length'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                  

    @pytest.mark.negative
    def test__VerticalVessels_heayd_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            Veritcal_vessel = _VerticalVessels(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type=["flat"])
        self.assertIn("Incorrect type 'list' provided to 'head_type'. Should be 'str'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.head_type = []
        self.assertIn("Incorrect type 'list' provided to 'head_type'. Should be 'str'",
                      str(exp))

    @pytest.mark.negative
    def test__VerticalVessels_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.LLLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                    

    @pytest.mark.negative
    def test__VerticalVessels_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.LLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__VerticalVessels_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.NLL = []
        self.assertIn("Incorrect type 'list' provided to 'NLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__VerticalVessels_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.HLL = []
        self.assertIn("Incorrect type 'list' provided to 'HLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test__VerticalVessels_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.HHLL = []
        self.assertIn("Incorrect type 'list' provided to 'HHLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))   

    @pytest.mark.negative
    def test__VerticalVessels_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.operating_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'operating_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))  

    @pytest.mark.negative
    def test__VerticalVessels_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.operating_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'operating_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))      

    @pytest.mark.negative
    def test__VerticalVessels_heayd_type_incorrect_value(self):
        with pytest.raises(Exception) as exp:
            Vertical_vessel = _VerticalVessels(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flatop")
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.head_type = "flatop"
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'",
                      str(exp))     

    @pytest.mark.negative
    def test__VerticalVessels_stream_connecion_disconnection_incorrect_type(self):
        cv = _VerticalVessels()
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
    def test__VerticalVessels_stream_disconnection_before_connecion(self):  
        cv = _VerticalVessels()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        import warnings
        with warnings.catch_warnings(record=True) as exp:
            cv.disconnect_stream(inlet_stream)
         
        self.assertIn("Already there is no connection.",
                      str(exp[-1].message))                                                                                                   

    @pytest.mark.negative
    @pytest.mark.get_inventory
    def test__VerticalVessels_get_inventory_incorrect_type_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.get_inventory([])
        self.assertIn("Incorrect type 'list' provided to 'type'. Should be 'str",
                      str(exp))   
    @pytest.mark.negative
    @pytest.mark.get_inventory
    def test__VerticalVessels_get_inventory_incorrect_value_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = _VerticalVessels()
            m4.get_inventory('list')
        self.assertIn("Incorrect value \'list\' provided to \'type\'. Should be among \'[\'volume\', \'mass\']\'.",
                      str(exp))