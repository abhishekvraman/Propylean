import pytest
import unittest
from propylean.equipments.storages import Bullet
from propylean import properties as prop
from propylean import MaterialStream, EnergyStream

class test_Bullet(unittest.TestCase):
    def test_Bullet_representation(self):
        vessel = Bullet(tag="Propane_1")
        self.assertIn("Bullet with tag: Propane_1", str(vessel))
    
    def test_Bullet_blanketing(self):
        v_1 = Bullet(is_blanketed=True, tag="Propylene Storage")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Propylene Storage_blanketing",
                      str(v_1.blanketing))

    @pytest.mark.negative
    def test_Bullet_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Bullet_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Bullet_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.pressure_drop = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'pressure_drop'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_Bullet_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.design_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Bullet_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Bullet_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Bullet_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_decrease'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Bullet_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.temperature_increase = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'temperature_increase'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_Bullet_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.design_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'design_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Bullet_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'inlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Bullet_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'outlet_mass_flowrate'. Should be '(<class 'propylean.properties.MassFlowRate'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Bullet_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.energy_in = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_in'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))      

    @pytest.mark.negative
    def test_Bullet_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.energy_out = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'energy_out'. Should be '(<class 'propylean.properties.Power'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))  

    @pytest.mark.negative
    def test_Bullet_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            bullet = Bullet(
                                               ID=[4, "m"], length=(10, "m"),
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.ID = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'ID'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))

    @pytest.mark.negative
    def test_Bullet_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            bullet = Bullet(
                                               ID=(4, "m"), length=[10, "m"],
                                               head_type="flat")
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.length = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'length'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                  

    @pytest.mark.negative
    def test_Bullet_heayd_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            bullet = Bullet(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type=["flat"])
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.head_type = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'head_type'. Should be '<class 'str'>'",
                      str(exp))

    @pytest.mark.negative
    def test_Bullet_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.LLLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                    

    @pytest.mark.negative
    def test_Bullet_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.LLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'LLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Bullet_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.NLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'NLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Bullet_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.HLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Bullet_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.HHLL = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'HHLL'. Should be '(<class 'propylean.properties.Length'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))   

    @pytest.mark.negative
    def test_Bullet_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.operating_temperature = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_temperature'. Should be '(<class 'propylean.properties.Temperature'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))  

    @pytest.mark.negative
    def test_Bullet_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.operating_pressure = []
        self.assertIn("Incorrect type '<class 'list'>' provided to 'operating_pressure'. Should be '(<class 'propylean.properties.Pressure'>, <class 'int'>, <class 'float'>, <class 'tuple'>)'",
                      str(exp))          

    @pytest.mark.negative
    def test_Bullet_heayd_type_incorrect_value(self):
        with pytest.raises(Exception) as exp:
            Vertical_vessel = Bullet(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flatop")
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Bullet()
            m4.head_type = "flatop"
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Should be among \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'.\\n            ",
                      str(exp))  

    @pytest.mark.negative
    def test_Bullet_stream_connecion_disconnection_incorrect_type(self):
        cv = Bullet()
        from propylean import MaterialStream
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
            
        with pytest.raises(Exception) as exp:
            cv.connect_stream([inlet_stream], 'in', stream_governed=True)
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_object\'. Should be \'(<class \'propylean.streams.MaterialStream\'>, <class \'propylean.streams.EnergyStream\'>)\'.\\n            ",
                      str(exp)) 
        
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, ['in'], stream_governed=True)
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'direction\'. Should be \'<class \'str\'>\'.\\n            ",
                      str(exp)) 
        with pytest.raises(Exception) as exp:
            cv.connect_stream(inlet_stream, 'in', stream_governed=[True])
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_governed\'. Should be \'<class \'bool\'>\'.\\n            ",
                      str(exp)) 

        cv.connect_stream(inlet_stream, 'in', stream_governed=True)
        with pytest.raises(Exception) as exp:
            cv.disconnect_stream(stream_tag=["Inlet_cv_19"])
        self.assertIn("Incorrect type \'<class \'list\'>\' provided to \'stream_tag\'. Should be \'<class \'str\'>\'.\\n            ",
                      str(exp))    

    @pytest.mark.negative
    def test_Bullet_stream_disconnection_before_connecion(self):  
        cv = Bullet()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        import warnings
        with warnings.catch_warnings(record=True) as exp:
            cv.disconnect_stream(inlet_stream)
         
        self.assertIn("Already there is no connection.",
                      str(exp[-1].message))

    @pytest.mark.mapping
    def test_Bullet_stream_equipment_mapping(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map 
        bullet = Bullet(pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        bullet.connect_stream(inlet_stream, direction="in")
        bullet.connect_stream(outlet_stream, direction="out")
        bullet.connect_stream(energy_in, direction="in")
        bullet.connect_stream(energy_out, direction="out")

        self.assertEqual(mse_map[inlet_stream.index][2], bullet.index)
        self.assertEqual(mse_map[inlet_stream.index][3], bullet.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], bullet.index)
        self.assertEqual(mse_map[outlet_stream.index][1], bullet.__class__) 

        self.assertEqual(ese_map[energy_in.index][2], bullet.index)
        self.assertEqual(ese_map[energy_in.index][3], bullet.__class__)
        self.assertEqual(ese_map[energy_out.index][0], bullet.index)
        self.assertEqual(ese_map[energy_out.index][1], bullet.__class__)    

        bullet.disconnect_stream(inlet_stream)
        bullet.disconnect_stream(outlet_stream)
        bullet.disconnect_stream(energy_in)
        bullet.disconnect_stream(energy_out)  

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 

        self.assertIsNone(ese_map[energy_in.index][2])
        self.assertIsNone(ese_map[energy_in.index][3])
        self.assertIsNone(ese_map[energy_out.index][0])
        self.assertIsNone(ese_map[energy_out.index][1])   

    @pytest.mark.delete 
    def test_Bullet_stream_equipment_delete_without_connection(self):
        bullet = Bullet(pressure_drop=(0.1, 'bar'))   
        repr(bullet)
        bullet.delete()
        with pytest.raises(Exception) as exp:
            repr(bullet)
        self.assertIn("Equipment does not exist!",
                      str(exp))
    
    @pytest.mark.delete 
    def test_Bullet_stream_equipment_delete_with_connection(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map 
        bullet = Bullet(pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        bullet.connect_stream(inlet_stream, direction="in")
        bullet.connect_stream(outlet_stream, direction="out")
        bullet.connect_stream(energy_in, direction="in")
        bullet.connect_stream(energy_out, direction="out")
        
        repr(bullet)
        bullet.delete()
        with pytest.raises(Exception) as exp:
            repr(bullet)
        self.assertIn("Equipment does not exist!",
                      str(exp))
        
        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 

        self.assertIsNone(ese_map[energy_in.index][2])
        self.assertIsNone(ese_map[energy_in.index][3])
        self.assertIsNone(ese_map[energy_out.index][0])
        self.assertIsNone(ese_map[energy_out.index][1]) 