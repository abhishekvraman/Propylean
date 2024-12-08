import pytest
import unittest
from propylean.equipments.storages import VerticalStorage
from propylean import properties as prop
from propylean import MaterialStream, EnergyStream

class test_VerticalStorage(unittest.TestCase):
    def test_VerticalStorage_representation(self):
        vessel = VerticalStorage(tag="Silo_1")
        self.assertIn("Vertical Storage with tag: Silo_1", str(vessel))
    
    def test_VerticalStorage_blanketing(self):
        v_1 = VerticalStorage(is_blanketed=True, tag="Ethenol_feed_tank")
        v_1.operating_pressure = prop.Pressure(1.5, "atm")
        self.assertEqual(v_1.blanketing.inlet_pressure, prop.Pressure(1.5, "atm"))
        self.assertEqual(v_1.blanketing.outlet_pressure, prop.Pressure(1.5, "atm"))

        self.assertIn("Blanketing with tag: Ethenol_feed_tank_blanketing",
                      str(v_1.blanketing))

    @pytest.mark.negative
    def test_VerticalStorage_inlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.inlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_outlet_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.outlet_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_pressure_drop_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.pressure_drop = []
        self.assertIn("Incorrect type 'list' provided to 'pressure_drop'. Can be any one from '('Pressure', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))                                    

    @pytest.mark.negative
    def test_VerticalStorage_design_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.design_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'design_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_inlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.inlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_outlet_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.outlet_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_temperature_decrease_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.temperature_decrease = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_decrease'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_temperature_increase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.temperature_increase = []
        self.assertIn("Incorrect type 'list' provided to 'temperature_increase'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))                                                      

    @pytest.mark.negative
    def test_VerticalStorage_design_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.design_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'design_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 

    @pytest.mark.negative
    def test_VerticalStorage_inlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.inlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'inlet_mass_flowrate'. Can be any one from '('MassFlowRate', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_outlet_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.outlet_mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'outlet_mass_flowrate'. Can be any one from '('MassFlowRate', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_energy_in_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.energy_in = []
        self.assertIn("Incorrect type 'list' provided to 'energy_in'. Can be any one from '('Power', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))      

    @pytest.mark.negative
    def test_VerticalStorage_energy_out_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.energy_out = []
        self.assertIn("Incorrect type 'list' provided to 'energy_out'. Can be any one from '('Power', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))   

    @pytest.mark.negative
    def test_VerticalStorage_ID_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = VerticalStorage(
                                               ID=[4, "m"], length=(10, "m"),
                                               head_type="flat")
        self.assertIn("Incorrect type 'list' provided to 'ID'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.ID = []
        self.assertIn("Incorrect type 'list' provided to 'ID'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_length_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = VerticalStorage(
                                               ID=(4, "m"), length=[10, "m"],
                                               head_type="flat")
        self.assertIn("Incorrect type 'list' provided to 'length'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.length = []
        self.assertIn("Incorrect type 'list' provided to 'length'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                  

    @pytest.mark.negative
    def test_VerticalStorage_heayd_type_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            horizontal_vessel = VerticalStorage(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type=["flat"])
        self.assertIn("Incorrect type 'list' provided to 'head_type'. Should be \'str\'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.head_type = []
        self.assertIn("Incorrect type 'list' provided to 'head_type'. Should be \'str\'",
                      str(exp))

    @pytest.mark.negative
    def test_VerticalStorage_LLLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.LLLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLLL'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                    

    @pytest.mark.negative
    def test_VerticalStorage_LLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.LLL = []
        self.assertIn("Incorrect type 'list' provided to 'LLL'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_NLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.NLL = []
        self.assertIn("Incorrect type 'list' provided to 'NLL'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_HLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.HLL = []
        self.assertIn("Incorrect type 'list' provided to 'HLL'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))                   

    @pytest.mark.negative
    def test_VerticalStorage_HHLL_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.HHLL = []
        self.assertIn("Incorrect type 'list' provided to 'HHLL'. Can be any one from '('Length', 'int', 'float', 'tuple')'",
                      str(exp))   

    @pytest.mark.negative
    def test_VerticalStorage_operating_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.operating_temperature = []
        self.assertIn("Incorrect type 'list' provided to 'operating_temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))  

    @pytest.mark.negative
    def test_VerticalStorage_operating_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.operating_pressure = []
        self.assertIn("Incorrect type 'list' provided to 'operating_pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))                                  
                      
    @pytest.mark.negative
    def test_VerticalStorage_heayd_type_incorrect_value(self):
        with pytest.raises(Exception) as exp:
            Vertical_vessel = VerticalStorage(
                                               ID=(4, "m"), length=(10, "m"),
                                               head_type="flatop")
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Can be any one from \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.head_type = "flatop"
        self.assertIn("Incorrect value \'flatop\' provided to \'head_type\'. Can be any one from \'[\'hemispherical\', \'elliptical\', \'torispherical\', \'flat\']\'",
                      str(exp))   

    @pytest.mark.negative
    def test_VerticalStorage_stream_connecion_disconnection_incorrect_type(self):
        cv = VerticalStorage()
        from propylean import MaterialStream
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
            
        with pytest.raises(Exception) as exp:
            cv.connect_stream([inlet_stream], 'in', stream_governed=True)
        self.assertIn("Incorrect type \'list\' provided to \'stream_object\'. Can be any one from \'('MaterialStream', 'EnergyStream')\'",
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
    def test_VerticalStorage_stream_disconnection_before_connecion(self):  
        cv = VerticalStorage()
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
    def test_VerticalStorage_get_inventory_incorrect_type_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.get_inventory([])
        self.assertIn("Incorrect type 'list' provided to 'type'. Should be \'str\'",
                      str(exp))   
    @pytest.mark.negative
    @pytest.mark.get_inventory
    def test_VerticalStorage_get_inventory_incorrect_value_to_type(self):
        with pytest.raises(Exception) as exp:
            m4 = VerticalStorage()
            m4.get_inventory('list')
        self.assertIn("Incorrect value \'list\' provided to \'type\'. Can be any one from \'[\'volume\', \'mass\']\'.",
                      str(exp)) 

    @pytest.mark.mapping
    def test_VerticalStorage_stream_equipment_mapping(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        vs = VerticalStorage(pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        vs.connect_stream(inlet_stream, direction="in")
        vs.connect_stream(outlet_stream, direction="out")
        vs.connect_stream(energy_in, direction="in")
        vs.connect_stream(energy_out, direction="out")

        self.assertEqual(mse_map[inlet_stream.index][2], vs.index)
        self.assertEqual(mse_map[inlet_stream.index][3], vs.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], vs.index)
        self.assertEqual(mse_map[outlet_stream.index][1], vs.__class__) 

        self.assertEqual(ese_map[energy_in.index][2], vs.index)
        self.assertEqual(ese_map[energy_in.index][3], vs.__class__)
        self.assertEqual(ese_map[energy_out.index][0], vs.index)
        self.assertEqual(ese_map[energy_out.index][1], vs.__class__)    

        vs.disconnect_stream(inlet_stream)
        vs.disconnect_stream(outlet_stream)
        vs.disconnect_stream(energy_in)
        vs.disconnect_stream(energy_out)  

        self.assertIsNone(mse_map[inlet_stream.index][2])
        self.assertIsNone(mse_map[inlet_stream.index][3])
        self.assertIsNone(mse_map[outlet_stream.index][0])
        self.assertIsNone(mse_map[outlet_stream.index][1]) 

        self.assertIsNone(ese_map[energy_in.index][2])
        self.assertIsNone(ese_map[energy_in.index][3])
        self.assertIsNone(ese_map[energy_out.index][0])
        self.assertIsNone(ese_map[energy_out.index][1])   

    @pytest.mark.delete 
    def test_VerticalStorage_stream_equipment_delete_without_connection(self):
        vs = VerticalStorage(pressure_drop=(0.1, 'bar'))   
        print(vs)
        vs.delete()
        with pytest.raises(Exception) as exp:
            print(vs)                                          
        self.assertIn("Equipment does not exist!",
                      str(exp))
    
    @pytest.mark.delete 
    def test_VerticalStorage_stream_equipment_delete_with_connection(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        vs = VerticalStorage(pressure_drop=(0.1, 'bar'))
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()
        energy_in = EnergyStream()
        energy_out = EnergyStream()

        vs.connect_stream(inlet_stream, direction="in")
        vs.connect_stream(outlet_stream, direction="out")
        vs.connect_stream(energy_in, direction="in")
        vs.connect_stream(energy_out, direction="out")

        vs.delete()
        with pytest.raises(Exception) as exp:
            print(vs)                                          
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