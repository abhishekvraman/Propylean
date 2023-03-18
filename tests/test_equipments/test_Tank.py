import pytest
import unittest
from propylean.equipments.storages import Tank
from propylean import properties as prop
from propylean import MaterialStream, EnergyStream

class test_Tank(unittest.TestCase):
    def test_Tank_representation(self):
        vessel = Tank(tag="Caustic Storage tank")
        self.assertIn("Tank with tag: Caustic Storage tank", str(vessel))
    
    def test_Tank_blanketing(self):
        v_1 = Tank(is_blanketed=True, tag="Palm Oil Storage")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Palm Oil Storage_blanketing",
                      str(v_1.blanketing))

    @pytest.mark.negative
    def test_Tank_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_Tank_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Tank_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.pressure_drop = []
        self.assertIn("Incorrect type 'list' provided to 'pressure_drop'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_Tank_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.design_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'design_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Tank_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_Tank_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Tank_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_decrease'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Tank_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.temperature_increase = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_increase'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_Tank_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.design_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'design_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_Tank_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Tank_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_mass_flowrate'. Should be '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_Tank_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.energy_in = []
        self.assertIn("Incorrect type 'list' provided to 'energy_in'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))      

    @pytest.mark.negative
    def test_Tank_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.energy_out = []
        self.assertIn("Incorrect type 'list' provided to 'energy_out'. Should be '('Power', 'int', 'float', 'tuple')'",
                      str(exp))                      

    @pytest.mark.negative
    def test_Tank_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = Tank(ID=[4, "m"], length=(10, "m"))
        self.assertIn("Incorrect type 'list' provided to 'ID'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.ID = []
        self.assertIn("Incorrect type 'list' provided to 'ID'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_Tank_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = Tank(ID=(4, "m"), length=[10, "m"])
        self.assertIn("Incorrect type 'list' provided to 'length'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.length = []
        self.assertIn("Incorrect type 'list' provided to 'length'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                  

     

    @pytest.mark.negative
    def test_Tank_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.LLLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                    

    @pytest.mark.negative
    def test_Tank_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.LLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Tank_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.NLL = []
        self.assertIn("Incorrect type 'list' provided to 'NLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Tank_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.HLL = []
        self.assertIn("Incorrect type 'list' provided to 'HLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_Tank_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.HHLL = []
        self.assertIn("Incorrect type 'list' provided to 'HHLL'. Should be '('Length', 'int', 'float', 'tuple')'",
                      str(exp))   

    @pytest.mark.negative
    def test_Tank_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.operating_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'operating_temperature'. Should be '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))  

    @pytest.mark.negative
    def test_Tank_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.operating_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'operating_pressure'. Should be '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))                                                                      

    @pytest.mark.negative
    def test_Tank_stream_connecion_disconnection_incorrect_type(self):
        cv = Tank()
        from propylean import MaterialStream
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
    def test_Tank_stream_disconnection_before_connecion(self):  
        cv = Tank()
        from propylean import MaterialStream
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        import warnings
        with warnings.catch_warnings(record=True) as exp:
            cv.disconnect_stream(inlet_stream)
         
        self.assertIn("Already there is no connection.",
                      str(exp[-1].message))                  

    @pytest.mark.negative
    @pytest.mark.get_inventory
    def test_Tank_get_inventory_incorrect_type_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.get_inventory([])
        self.assertIn("Incorrect type 'list' provided to 'type'. Should be 'str",
                      str(exp))   
    @pytest.mark.negative
    @pytest.mark.get_inventory
    def test_Tank_get_inventory_incorrect_value_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = Tank()
            m4.get_inventory('list')
        self.assertIn("Incorrect value \'list\' provided to \'type\'. Should be among \'[\'volume\', \'mass\']\'.",
                      str(exp))
    
    @pytest.mark.mapping
    def test_Tank_stream_equipment_mapping(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        tank = Tank(pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        tank.connect_stream(inlet_stream, direction="in")
        tank.connect_stream(outlet_stream, direction="out")
        tank.connect_stream(energy_in, direction="in")
        tank.connect_stream(energy_out, direction="out")

        self.assertEqual(mse_map[inlet_stream.index][2], tank.index)
        self.assertEqual(mse_map[inlet_stream.index][3], tank.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], tank.index)
        self.assertEqual(mse_map[outlet_stream.index][1], tank.__class__) 

        self.assertEqual(ese_map[energy_in.index][2], tank.index)
        self.assertEqual(ese_map[energy_in.index][3], tank.__class__)
        self.assertEqual(ese_map[energy_out.index][0], tank.index)
        self.assertEqual(ese_map[energy_out.index][1], tank.__class__)    

        tank.disconnect_stream(inlet_stream)
        tank.disconnect_stream(outlet_stream)
        tank.disconnect_stream(energy_in)
        tank.disconnect_stream(energy_out)  

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 

        self.assertIsNone(ese_map[energy_in.index][2])
        self.assertIsNone(ese_map[energy_in.index][3])
        self.assertIsNone(ese_map[energy_out.index][0])
        self.assertIsNone(ese_map[energy_out.index][1])   

    @pytest.mark.delete 
    def test_Tank_stream_equipment_delete_without_connection(self):
        tank = Tank(pressure_drop=(0.1, 'bar'))   
        repr(tank)
        tank.delete()
        with pytest.raises(Exception) as exp:
            repr(tank)     
        self.assertIn("Equipment does not exist!",
                      str(exp))   
    
    @pytest.mark.delete 
    def test_Tank_stream_equipment_delete_with_connection(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        tank = Tank(pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        tank.connect_stream(inlet_stream, direction="in")
        tank.connect_stream(outlet_stream, direction="out")
        tank.connect_stream(energy_in, direction="in")
        tank.connect_stream(energy_out, direction="out")

        repr(tank)
        tank.delete()
        with pytest.raises(Exception) as exp:
            repr(tank)     
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