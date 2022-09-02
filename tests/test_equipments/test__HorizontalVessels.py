from cmath import exp
import pytest
import unittest
from propylean.equipments.generic_equipment_classes import _HorizontalVessels
from propylean.streams import MaterialStream, EnergyStream
import propylean.properties as prop
from propylean.constants import Constants

class test__HorizontalVessels(unittest.TestCase):
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__HorizontalVessels_instantiation_only_tag(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_1")
        self.assertEqual(horizontal_vessel.tag, "horizontal_vessel_1")
        self.assertEqual(horizontal_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(horizontal_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__HorizontalVessels_instantiation_tag_and_pressure_drop(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_2")
        horizontal_vessel.operating_pressure = (10, "bar")
        self.assertEqual(horizontal_vessel.tag, "horizontal_vessel_2")
        self.assertEqual(horizontal_vessel.operating_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(horizontal_vessel.inlet_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(horizontal_vessel.outlet_pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(horizontal_vessel.pressure_drop, prop.Pressure(0, 'bar'))
    
    @pytest.mark.positive
    @pytest.mark.instantiation
    def test__HorizontalVessels_instantiation_no_arguments(self):
        horizontal_vessel = _HorizontalVessels()
        self.assertIsNotNone(horizontal_vessel.tag)
        self.assertEqual(horizontal_vessel.pressure_drop, prop.Pressure(0))
        self.assertEqual(horizontal_vessel.pressure_drop, prop.Pressure(0))
    
    @pytest.mark.positive
    @pytest.mark.length_setting
    def test__HorizontalVessels_instantiation_vessel_dimensions_arguments(self):
        horizontal_vessel = _HorizontalVessels(ID = (4, "m"),
                                               OD = 6,
                                               length=prop.Length(10))

        self.assertEqual(horizontal_vessel.ID, prop.Length(4, "m"))
        self.assertEqual(horizontal_vessel.OD, prop.Length(6, "m"))
        self.assertEqual(horizontal_vessel.thickness, prop.Length(2, "m"))
        self.assertEqual(horizontal_vessel.length, prop.Length(10, "m"))

        horizontal_vessel = _HorizontalVessels(thickness = (2, "m"),
                                               OD = 6,
                                               length=prop.Length(10))
        self.assertEqual(horizontal_vessel.ID, prop.Length(4, "m"))
        self.assertEqual(horizontal_vessel.OD, prop.Length(6, "m"))
        self.assertEqual(horizontal_vessel.thickness, prop.Length(2, "m"))
        self.assertEqual(horizontal_vessel.length, prop.Length(10, "m"))

    
    @pytest.mark.positive
    @pytest.mark.length_setting
    def test__HorizontalVessels_instantiation_level_settings_arguments(self):
        Horizontal_vessel = _HorizontalVessels(LLLL=(10, "inch"),
                                             LLL=(20, "inch"),
                                             NLL=prop.Length(30, "inch"),
                                             HLL=prop.Length(40, "inch"),
                                             HHLL=(50, "inch"))

        self.assertEqual(Horizontal_vessel.LLLL, prop.Length(10, "inch"))
        self.assertEqual(Horizontal_vessel.LLL, prop.Length(20, "inch"))
        self.assertEqual(Horizontal_vessel.NLL, prop.Length(30, "inch"))
        self.assertEqual(Horizontal_vessel.HLL, prop.Length(40, "inch"))
        self.assertEqual(Horizontal_vessel.HHLL, prop.Length(50, "inch"))
    
    @pytest.mark.positive
    @pytest.mark.head_type
    def test__HorizontalVessels_instantiation_head_type_argument(self):
        for head_type in Constants.HEAD_TYPES:
            horizontal_vessel = _HorizontalVessels(ID = (4, "m"),
                                                OD = 6,
                                                length=prop.Length(10),
                                                head_type=head_type)
            self.assertEqual(horizontal_vessel.head_type, head_type)
    
    @pytest.mark.positive
    @pytest.mark.main_fluid
    def test__HorizontalVessels_instantiation_main_fluid_argument(self):
        for main_fluid in ["liquid", "gas"]:
            horizontal_vessel = _HorizontalVessels(ID = (4, "m"),
                                                OD = 6,
                                                length=prop.Length(10),
                                                main_fluid=main_fluid)
            self.assertEqual(horizontal_vessel.main_fluid, main_fluid)
    
    @pytest.mark.positive
    def test__HorizontalVessels_setting_inlet_pressure(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_6",
                          pressure_drop=(0.1, 'bar'))
        horizontal_vessel.inlet_pressure = (30, 'bar')
        self.assertEqual(horizontal_vessel.inlet_pressure, prop.Pressure(30, 'bar'))
        self.assertEqual(horizontal_vessel.operating_pressure, prop.Pressure(30, 'bar'))
    
    @pytest.mark.positive
    def test__HorizontalVessels_setting_outlet_pressure(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_7",
                          pressure_drop=(0.1, 'bar'))
        horizontal_vessel.outlet_pressure = (20, 'bar')
        self.assertEqual(horizontal_vessel.inlet_pressure, prop.Pressure(20.1, 'bar'))
        self.assertEqual(horizontal_vessel.operating_pressure, prop.Pressure(20.1, 'bar'))
    
    @pytest.mark.positive
    def test__HorizontalVessels_setting_inlet_temperature(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_8",
                          pressure_drop=(0.1, 'bar'))
        horizontal_vessel.inlet_temperature = (50, 'C')
        self.assertEqual(horizontal_vessel.inlet_temperature, prop.Temperature(50, 'C'))
        self.assertEqual(horizontal_vessel.operating_temperature, prop.Temperature(50, 'C'))
    
    @pytest.mark.positive
    def test__HorizontalVessels_setting_outlet_temperature(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_9",
                          pressure_drop=(0.1, 'bar'))
        horizontal_vessel.outlet_temperature = (130, 'F')
        self.assertLess(abs(horizontal_vessel.inlet_temperature.value-130), 0.0001)
        self.assertEqual(horizontal_vessel.inlet_temperature.unit, 'F')
        self.assertLess(abs(horizontal_vessel.operating_temperature.value-130), 0.0001)
        self.assertEqual(horizontal_vessel.operating_temperature.unit, 'F')
    
    @pytest.mark.positive
    def test__HorizontalVessels_setting_inlet_mass_flowrate(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_10",
                          pressure_drop=(0.1, 'bar'))
        horizontal_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(horizontal_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__HorizontalVessels_setting_outlet_mass_flowrate(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_11",
                          pressure_drop=(0.10, 'bar'))
        horizontal_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
        self.assertEqual(horizontal_vessel.outlet_mass_flowrate, prop.MassFlowRate(1000, 'kg/h'))
    
    @pytest.mark.positive
    def test__HorizontalVessels_connection_with_material_stream_inlet_stream_governed(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_12",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_vessel_12",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(horizontal_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        # Test inlet properties of horizontal_vessel are equal to inlet stream's.
        self.assertEqual(horizontal_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertAlmostEqual(horizontal_vessel.inlet_temperature.value, inlet_stream.temperature.value, 3)
        self.assertEqual(horizontal_vessel.inlet_temperature.unit, inlet_stream.temperature.unit)
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(horizontal_vessel.outlet_pressure, horizontal_vessel.inlet_pressure - horizontal_vessel.pressure_drop)
        self.assertLess(abs(horizontal_vessel.inlet_temperature.value - horizontal_vessel.outlet_temperature.value), 0.001)
        self.assertEqual(horizontal_vessel.inlet_temperature.unit, horizontal_vessel.outlet_temperature.unit)
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, horizontal_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__HorizontalVessels_connection_with_material_stream_outlet_stream_governed(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_13",
                          pressure_drop=(0.1, 'bar'))
        outlet_stream = MaterialStream(tag="Outlet_horizontal_vessel_13",
                                      mass_flowrate=(1000, 'kg/h'),
                                      pressure=(30, 'bar'),
                                      temperature=(130, 'F'))
        # Test connection is made.
        self.assertTrue(horizontal_vessel.connect_stream(outlet_stream, 'out', stream_governed=True))
        # Test outlet properties of horizontal_vessel are equal to outlet stream's.
        self.assertEqual(horizontal_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertAlmostEqual(horizontal_vessel.outlet_temperature.value, outlet_stream.temperature.value, 3)
        self.assertEqual(horizontal_vessel.outlet_temperature.unit, outlet_stream.temperature.unit)
        self.assertEqual(horizontal_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(horizontal_vessel.inlet_pressure, horizontal_vessel.outlet_pressure + horizontal_vessel.pressure_drop)
        self.assertLess(abs(horizontal_vessel.inlet_temperature.value-horizontal_vessel.outlet_temperature.value),0.0001)
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, horizontal_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__HorizontalVessels_connection_with_material_stream_inlet_equipment_governed(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_14",
                          pressure_drop=(0.1, 'bar'))

        horizontal_vessel.inlet_pressure = (30, 'bar')
        horizontal_vessel.inlet_mass_flowrate = (1000, 'kg/h')
        horizontal_vessel.inlet_temperature = (320, 'K')
        inlet_stream = MaterialStream(tag="Inlet_horizontal_vessel_14")
        # Test connection is made.
        self.assertTrue(horizontal_vessel.connect_stream(inlet_stream, 'in', stream_governed=False))
        # Test inlet properties of horizontal_vessel are equal to inlet stream's.
        self.assertEqual(horizontal_vessel.inlet_pressure, inlet_stream.pressure)
        self.assertEqual(horizontal_vessel.inlet_temperature, inlet_stream.temperature)
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, inlet_stream.mass_flowrate)
        # Test outlet properties are calculated accordingly.
        self.assertEqual(horizontal_vessel.outlet_pressure, horizontal_vessel.inlet_pressure - horizontal_vessel.pressure_drop)
        self.assertEqual(horizontal_vessel.inlet_temperature, horizontal_vessel.outlet_temperature)
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, horizontal_vessel.outlet_mass_flowrate)

    @pytest.mark.positive
    def test__HorizontalVessels_connection_with_material_stream_outlet_equipment_governed(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_15",
                          pressure_drop=(0.1, 'bar'))
        horizontal_vessel.outlet_pressure = (130, 'bar')
        horizontal_vessel.outlet_mass_flowrate = (1000, 'kg/h')
        horizontal_vessel.outlet_temperature = (30, 'C')
        outlet_stream = MaterialStream(tag="Outlet_horizontal_vessel_15")
        # Test connection is made.
        self.assertTrue(horizontal_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test outlet properties of horizontal_vessel are equal to outlet stream's.
        self.assertEqual(horizontal_vessel.outlet_pressure, outlet_stream.pressure)
        self.assertEqual(horizontal_vessel.outlet_temperature, outlet_stream.temperature)
        self.assertEqual(horizontal_vessel.outlet_mass_flowrate, outlet_stream.mass_flowrate)
        # Test intlet properties are calculated accordingly.
        self.assertEqual(horizontal_vessel.inlet_pressure, horizontal_vessel.outlet_pressure + horizontal_vessel.pressure_drop)
        self.assertEqual(horizontal_vessel.inlet_temperature, horizontal_vessel.outlet_temperature)
        self.assertEqual(horizontal_vessel.inlet_mass_flowrate, horizontal_vessel.outlet_mass_flowrate)

    # pytest.mark.positive
    # def test__HorizontalVessels_connection_with_energy_stream_inlet_equipment_governed(self):
    #     horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_17",
    #                       pressure_drop=(0.1, 'bar'))
    #     horizontal_vessel_energy_expelled = EnergyStream(tag="Power_horizontal_vessel_17", amount=(10,"MW"))
    #     horizontal_vessel_inlet = MaterialStream(mass_flowrate=(1000, 'kg/h'),
    #                                 pressure=(30, 'bar'),
    #                                 temperature=(25, 'C'))
    #     horizontal_vessel_inlet.components = prop.Components({"water": 1})
    #     # Test connection is made.
    #     self.assertTrue(horizontal_vessel.connect_stream(horizontal_vessel_inlet, "in", stream_governed=True))
    #     # Test inlet properties of horizontal_vessel are equal to outlet stream's.
    #     self.assertAlmostEqual(horizontal_vessel.energy_out.value, horizontal_vessel_energy_expelled.amount.value)
    #     self.assertEqual(horizontal_vessel.energy_out.unit, horizontal_vessel_energy_expelled.amount.unit)
    
    @pytest.mark.positive
    def test__HorizontalVessels_stream_disconnection_by_stream_object(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_18",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_vessel_18", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_horizontal_vessel_18")
        # Test connection is made.
        self.assertTrue(horizontal_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(horizontal_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        # Test disconnection
        self.assertTrue(horizontal_vessel.disconnect_stream(inlet_stream))
        self.assertTrue(horizontal_vessel.disconnect_stream(outlet_stream))
        self.assertIsNone(horizontal_vessel._inlet_material_stream_tag)
        self.assertIsNone(horizontal_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.temp
    def test__HorizontalVessels_stream_disconnection_by_stream_tag(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_19",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_vessel_19")
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_horizontal_vessel_19", pressure=(20, 'bar'))
        # Test connection is made.
        self.assertTrue(horizontal_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(horizontal_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        self.assertEqual(inlet_stream.components, outlet_stream.components)
        # Test disconnection
        self.assertTrue(horizontal_vessel.disconnect_stream(stream_tag="Inlet_horizontal_vessel_19"))
        self.assertTrue(horizontal_vessel.disconnect_stream(stream_tag="Outlet_horizontal_vessel_19"))
        self.assertIsNone(horizontal_vessel._inlet_material_stream_tag)
        self.assertIsNone(horizontal_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    def test__HorizontalVessels_stream_disconnection_by_direction_stream_type(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_20",
                          pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(tag="Inlet_horizontal_vessel_20", pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream(tag="Outlet_horizontal_vessel_20")
        horizontal_vessel_energy_expelled = EnergyStream(tag="Power_horizontal_vessel_20")
        # Test connection is made.
        self.assertTrue(horizontal_vessel.connect_stream(inlet_stream, 'in', stream_governed=True))
        self.assertTrue(horizontal_vessel.connect_stream(outlet_stream, 'out', stream_governed=False))
        
        # Test disconnection
        self.assertTrue(horizontal_vessel.disconnect_stream(direction="in", stream_type="Material"))
        self.assertTrue(horizontal_vessel.disconnect_stream(direction="ouTlet", stream_type="materiaL"))
        self.assertIsNone(horizontal_vessel._inlet_material_stream_tag)
        self.assertIsNone(horizontal_vessel._outlet_material_stream_tag)
        self.assertIsNone(inlet_stream._to_equipment_tag)
        self.assertIsNone(outlet_stream._from_equipment_tag)
    
    @pytest.mark.positive
    @pytest.mark.liquid_level
    def test__HorizontalVessels_liquid_level(self):
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_21",
                                               NLL=(20, "m"))
        self.assertEqual(horizontal_vessel.NLL, horizontal_vessel.liquid_level)
    
    @pytest.mark.positive
    @pytest.mark.vessel_volume
    def test__HorizontalVessels_volume_calculations_elliptical(self):
        """ Filled Volume	m3	61.97
            Total Volume	m3	142.4
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            Inside Dish Depth, a 1000 mm
            Level, H 1800 mm
        """
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_22",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="elliptical")
        horizontal_vessel.liquid_level = prop.Length(1.8, "m")
        horizontal_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(142.4, "m^3")
        expected_liquid_volume = prop.Volume(61.97)
        self.assertAlmostEqual(horizontal_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(horizontal_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = horizontal_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit)       
    
    @pytest.mark.positive
    @pytest.mark.vessel_volume
    def test__HorizontalVessels_volume_calculations_torispherical(self):
        """ Filled Volume	m3	59.23
            Total Volume	m3	136.0
            Inside Dish Depth (a)	mm	677.4
            Dish Radius (fD)	mm	4000
            Knuckle Radius (kD)	mm	240.0
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            f, Dish Radius parameter
            1.0
            k, Knuckle Radius parameter
            0.06
            Level, H 1800 mm
            ASME F&D/ Torispherical	f = 1	k = 0.06
            Standard F&D	f = 1	k = 0.75" to 2"
            80:10 F&D	f = 0.8	k = 0.1

        """
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_23",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="torispherical")
        horizontal_vessel.liquid_level = prop.Length(1.8, "m")
        horizontal_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(158.93, "m^3")
        expected_liquid_volume = prop.Volume(57.95)
        self.assertAlmostEqual(horizontal_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(horizontal_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = horizontal_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 1)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit)       

    @pytest.mark.positive
    @pytest.mark.vessel_volume
    def test__HorizontalVessels_volume_calculations_hemispherical(self):
        """ Filled Volume	m3	69.10
            Total Volume	m3	159.2
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            Inside Dish Depth, a 1000 mm
            Level, H 1800 mm
        """
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_24",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="hemispherical")
        horizontal_vessel.liquid_level = prop.Length(1.8, "m")
        horizontal_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(159.2, "m^3")
        expected_liquid_volume = prop.Volume(69.10)
        self.assertAlmostEqual(horizontal_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(horizontal_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = horizontal_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit) 

    @pytest.mark.vessel_volume
    def test__HorizontalVessels_volume_calculations_flat(self):
        """ Filled Volume	m3	54.85
            Total Volume	m3	125.7
            Diameter, D 4000 mm
            Straight Length, L 10000 mm
            Inside Dish Depth, a 1000 mm
            Level, H 1800 mm
        """
        horizontal_vessel = _HorizontalVessels(tag="horizontal_vessel_25",
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flat")
        horizontal_vessel.liquid_level = prop.Length(1.8, "m")
        horizontal_vessel.main_fluid = "liquid"

        expected_vessel_volume = prop.Volume(125.7, "m^3")
        expected_liquid_volume = prop.Volume(54.85)
        self.assertAlmostEqual(horizontal_vessel.vessel_volume.value,
                               expected_vessel_volume.value, 1)
        self.assertEqual(horizontal_vessel.vessel_volume.unit,
                               expected_vessel_volume.unit)

        calculated_liq_volume = horizontal_vessel.get_inventory()
        self.assertAlmostEqual(calculated_liq_volume.value,
                               expected_liquid_volume.value, 2)
        self.assertEqual(calculated_liq_volume.unit,
                               expected_liquid_volume.unit) 

    @pytest.mark.negative
    def test__HorizontalVessels_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test__HorizontalVessels_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test__HorizontalVessels_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test__HorizontalVessels_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test__HorizontalVessels_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test__HorizontalVessels_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test__HorizontalVessels_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test__HorizontalVessels_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test__HorizontalVessels_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test__HorizontalVessels_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test__HorizontalVessels_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test__HorizontalVessels_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test__HorizontalVessels_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                

    @pytest.mark.negative
    def test__HorizontalVessels_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = _HorizontalVessels(
                                               ID=[4, "m"], length=(10, "m"),
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.ID = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test__HorizontalVessels_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = _HorizontalVessels(
                                               ID=(4, "m"), length=[10, "m"],
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.length = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                  

    @pytest.mark.negative
    def test__HorizontalVessels_heayd_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = _HorizontalVessels(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type=["flat"])
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.head_type = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))
    @pytest.mark.negative
    def test__HorizontalVessels_heayd_type_incorrect_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = _HorizontalVessels(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flatop")
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.head_type = "flatop"
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))                  

    @pytest.mark.negative
    def test__HorizontalVessels_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.LLLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                    

    @pytest.mark.negative
    def test__HorizontalVessels_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.LLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test__HorizontalVessels_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.NLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'NLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test__HorizontalVessels_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.HLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test__HorizontalVessels_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.HHLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HHLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))   

    @pytest.mark.negative
    def test__HorizontalVessels_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.operating_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))  

    @pytest.mark.negative
    def test__HorizontalVessels_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = _HorizontalVessels()
            m4.operating_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                    