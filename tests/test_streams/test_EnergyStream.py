import pytest
import unittest

from thermo import Mixture
from propylean.streams import EnergyStream
import propylean.properties as prop
import pandas as pd

class test_EnergyStream(unittest.TestCase):
    @pytest.mark.positive
    def test_EnergyStream_instantiation_tag_only(self):
        e1 = EnergyStream(tag="e1")
        self.assertEqual(e1.tag, "e1")
        self.assertEqual(e1.amount, prop.Power(0, 'W'))
    
    @pytest.mark.positive
    def test_EnergyStream_instantiation_all_base_properties(self):
        e2 = EnergyStream(tag="e2", amount=(10, 'kW'))
        self.assertEqual(e2.amount, prop.Power(10, 'kW'))
    
    @pytest.mark.positive
    def test_EnergyStream_instantiation_no_base_properties(self):
        e3 = EnergyStream()
        self.assertIn("EnergyStream_", e3.tag)
    
    @pytest.mark.positive
    def test_EnergyStream_object_representation(self):
        e4 = EnergyStream(tag="Pump_Inlet_Energy_1")
        self.assertEqual("Energy Stream Tag: Pump_Inlet_Energy_1",str(e4))

    @pytest.mark.negative
    def test_EnergyStream_incorrect_assignment(self):
        with pytest.raises(Exception) as exp:
            e5 = EnergyStream("gggg", [])
        self.assertIn("Incorrect type 'list' provided to 'amount'. Can be any one from '('Power', 'int', 'float', 'tuple', 'Series')'",
                      str(exp)) 

        with pytest.raises(Exception) as exp:
            e5 = EnergyStream()
            e5.amount = []
        self.assertIn("Incorrect type 'list' provided to 'amount'. Can be any one from '('Power', 'int', 'float', 'tuple', 'Series')'",
                      str(exp))     

    @pytest.mark.delete 
    def test_EnergyStream_stream_equipment_delete_without_connection(self):
        e4 = EnergyStream()   
        repr(e4)
        e4.delete()
        with pytest.raises(Exception) as exp:
            repr(e4)     
        self.assertIn("Stream does not exist!",
                      str(exp))         
    
    @pytest.mark.delete
    def test_EnergyStream_stream_equipment_delete_with_connection(self):
        from propylean.equipments.abstract_equipment_classes import _energy_stream_equipment_map as ese_map
        from propylean import Bullet
        pump = Bullet()
        
        inlet_stream = EnergyStream()
        outlet_stream = EnergyStream()

        pump.connect_stream(inlet_stream, direction="in")
        pump.connect_stream(outlet_stream, direction="out")

        self.assertEqual(ese_map[inlet_stream.index][2], pump.index)
        self.assertEqual(ese_map[inlet_stream.index][3], pump.__class__)
        self.assertEqual(ese_map[outlet_stream.index][0], pump.index)
        self.assertEqual(ese_map[outlet_stream.index][1], pump.__class__) 


        repr(inlet_stream)
        repr(outlet_stream)
        outlet_stream.delete()
        inlet_stream.delete()
        with pytest.raises(Exception) as exp:
            repr(inlet_stream)               
        self.assertIn("Stream does not exist!",
                      str(exp))
        
        with pytest.raises(Exception) as exp:
            repr(outlet_stream)               
        self.assertIn("Stream does not exist!",
                      str(exp))
        
        self.assertNotIn(inlet_stream.index, ese_map.keys())
        self.assertNotIn(outlet_stream.index, ese_map.keys())