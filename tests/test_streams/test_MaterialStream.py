from typing import OrderedDict
import pytest
import unittest

from thermo import Mixture
from propylean.streams import MaterialStream
import propylean.properties as prop
import pandas as pd

class test_MaterialStream(unittest.TestCase):
    @pytest.mark.positive
    def test_MaterialStream_instantiation_tag_only(self):
        m1 = MaterialStream(tag="m1")
        self.assertEqual(m1.tag, "m1")
        self.assertEqual(m1.pressure, prop.Pressure())
        self.assertEqual(m1.temperature, prop.Temperature())
        self.assertEqual(m1.mass_flowrate, prop.MassFlowRate())
        self.assertIsNone(m1._from_equipment_tag)
        self.assertIsNone(m1._to_equipment_tag)
    
    @pytest.mark.positive
    def test_MaterialStream_instantiation_all_base_properties(self):
        m2 = MaterialStream(tag="m2", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        self.assertEqual(m2.pressure, prop.Pressure(10, 'bar'))
        self.assertEqual(m2.temperature, prop.Temperature(300, 'K'))
        self.assertEqual(m2.mass_flowrate, prop.MassFlowRate(1, 'ton/h'))

    def test_MaterialStream_instantiation_no_base_properties(self):
        m3 = MaterialStream()
        self.assertIn("MaterialStream_", m3.tag)
        self.assertEqual(m3.pressure, prop.Pressure())
        self.assertEqual(m3.temperature, prop.Temperature())
        self.assertEqual(m3.mass_flowrate, prop.MassFlowRate())

    @pytest.mark.density
    @pytest.mark.positive
    def test_MaterialStream_components_flow_property_density(self):
        m4 = MaterialStream(tag="m4", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        m4.density.unit = "kg/m^3"
        m4.density_l.unit = "kg/m^3"
        m4.density_g.unit = "kg/m^3"
        self.assertAlmostEqual(m4.density.value, mx.rho)
        self.assertEqual(m4.density_l.value, mx.rhol)
        self.assertEqual(m4.density_g.value, mx.rhog)

    @pytest.mark.viscosity
    @pytest.mark.positive
    def test_MaterialStream_components_flow_property_viscosity(self):
        m4 = MaterialStream(tag="m5", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        m4.d_viscosity.unit = "Pa-s"
        m4.d_viscosity_l.unit = "Pa-s"
        m4.d_viscosity_g.unit = "Pa-s"
        self.assertEqual(m4.d_viscosity.value, mx.mu)
        self.assertEqual(m4.d_viscosity_l.value, mx.mul)
        self.assertEqual(m4.d_viscosity_g.value, mx.mug)

    @pytest.mark.positive
    @pytest.mark.vol_flowrate
    def test_MaterialStream_components_flow_property_volumetric_flowrate(self):
        m4 = MaterialStream(tag="m6", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        m4.vol_flowrate.unit = "m^3/h"
        expected_volumetric_flowrate = 1000/mx.rho
        self.assertAlmostEqual(m4.vol_flowrate.value, expected_volumetric_flowrate)
    
    @pytest.mark.positive
    def test_MaterialStream_components_flow_property_mol_flowrate(self):
        m4 = MaterialStream(tag="m7", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        m4.mol_flowrate.unit = "mol/h"
        expected_mol_flowrate = 1000000/mx.MW
        self.assertAlmostEqual(m4.mol_flowrate.value, expected_mol_flowrate)
    
    @pytest.mark.positive
    def test_MaterialStream_components_thermodynamic_property_molecular_weight(self):
        m4 = MaterialStream(tag="m8", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        m4.molecular_weight.unit = "g/mol"
        expected_MW= mx.MW
        self.assertEqual(m4.molecular_weight.value, expected_MW)
    
    @pytest.mark.positive
    def test_MaterialStream_components_thermodynamic_property_compressibility_factor(self):
        m4 = MaterialStream(tag="m9", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        self.assertEqual(m4.Z.value, mx.Z)
        self.assertEqual(m4.Z_l.value, mx.Zl)
        self.assertEqual(m4.Z_g.value, mx.Zg)
    
    @pytest.mark.positive
    def test_MaterialStream_components_thermodynamic_property_isentropic_exponent(self):
        m4 = MaterialStream(tag="m10", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        self.assertEqual(m4.isentropic_exponent.value, mx.isentropic_exponent)
    
    @pytest.mark.positive
    def test_MaterialStream_components_thermodynamic_property_phase(self):
        m4 = MaterialStream(tag="m11", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction, 'mol')
        p = prop.Pressure(10, 'bar')
        p.unit = 'Pa'
        mx = Mixture(zs=mol_fraction, T=300, P=p.value)
        self.assertEqual(m4.phase, mx.phase)

    @pytest.mark.positive
    @pytest.mark.unit_change
    def test_MaterialStream_property_unit_change(self):
        m4 = MaterialStream(tag="m12", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        mol_fraction = OrderedDict([('benzene', 0.96522),('toluene', 0.00259)])
        m4.components = prop.Components(mol_fraction,'mol')
        self.assertEqual(m4.density.unit, "kg/m^3")
        m4.density.unit = "lbm/ft^3"
        self.assertEqual(m4.density.unit, "lbm/ft^3")
        m4.density.unit = "g/cm^3"
        self.assertEqual(m4.density.unit, "g/cm^3")
        m4.vol_flowrate.unit = "m^3/h"
        self.assertEqual(m4.vol_flowrate.unit, "m^3/h")
    
    @pytest.mark.negative
    def test_MaterialStream_pressure_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream(pressure=[10],
                                temperature=300,
                                mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        self.assertIn("Incorrect type 'list' provided to 'pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.pressure = []
        self.assertIn("Incorrect type 'list' provided to 'pressure'. Can be any one from '('Pressure', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_temperature_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream(pressure=10,
                                temperature=[300],
                                mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        self.assertIn("Incorrect type 'list' provided to 'temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.temperature = []
        self.assertIn("Incorrect type 'list' provided to 'temperature'. Can be any one from '('Temperature', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_mass_flowrate_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream(pressure=10,
                                temperature=300,
                                mass_flowrate=[])
        self.assertIn("Incorrect type 'list' provided to 'mass_flowrate'. Can be any one from '('MassFlowRate', 'int', 'float', 'tuple')'",
                      str(exp))
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.mass_flowrate = []
        self.assertIn("Incorrect type 'list' provided to 'mass_flowrate'. Can be any one from '('MassFlowRate', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_molecular_weigth_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.molecular_weight = []
        self.assertIn("Incorrect type 'list' provided to 'molecular_weight'. Can be any one from '('MolecularWeigth', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_components_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.components = []
        self.assertIn("Incorrect type 'list' provided to 'components'. Should be 'Components'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_desnity_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.density = []
        self.assertIn("Incorrect type 'list' provided to 'density'. Can be any one from '('Density', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_desnity_l_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.density_l = []
        self.assertIn("Incorrect type 'list' provided to 'density_l'. Can be any one from '('Density', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_desnity_g_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.density_g = []
        self.assertIn("Incorrect type 'list' provided to 'density_g'. Can be any one from '('Density', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_desnity_s_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.density_s = []
        self.assertIn("Incorrect type 'list' provided to 'density_s'. Can be any one from '('Density', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_d_viscosity_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.d_viscosity = []
        self.assertIn("Incorrect type 'list' provided to 'd_viscosity'. Can be any one from '('DViscosity', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_d_viscosity_l_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.d_viscosity_l = []
        self.assertIn("Incorrect type 'list' provided to 'd_viscosity_l'. Can be any one from '('DViscosity', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_d_viscosity_g_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.d_viscosity_g = []
        self.assertIn("Incorrect type 'list' provided to 'd_viscosity_g'. Can be any one from '('DViscosity', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_isentropic_exponent_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.isentropic_exponent = []
        self.assertIn("Incorrect type 'list' provided to 'isentropic_exponent'. Can be any one from '('Dimensionless', 'int', 'float')'", str(exp))
    
    @pytest.mark.negative
    def test_MaterialStream_phase_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.phase = []
        self.assertIn("Incorrect type 'list' provided to 'phase'. Should be \'str\'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_Z_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.Z = []
        self.assertIn("Incorrect type 'list' provided to 'Z'. Can be any one from '('Dimensionless', 'int', 'float')'", str(exp))
    
    @pytest.mark.negative
    def test_MaterialStream_Z_g_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.Z_g = []
        self.assertIn("Incorrect type 'list' provided to 'Z_g'. Can be any one from '('Dimensionless', 'int', 'float')'", str(exp))
    
    @pytest.mark.negative
    def test_MaterialStream_Z_l_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.Z_l = []
        self.assertIn("Incorrect type 'list' provided to 'Z_l'. Can be any one from '('Dimensionless', 'int', 'float')'", str(exp))
    
    @pytest.mark.negative
    def test_MaterialStream_Pc_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.Pc = []
        self.assertIn("Incorrect type 'list' provided to 'Pc'. Can be any one from '('Pressure', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.negative
    def test_MaterialStream_Psat_incorrect_type_to_value(self):
        with pytest.raises(Exception) as exp:
            m4 = MaterialStream()
            m4.Psat = []
        self.assertIn("Incorrect type 'list' provided to 'Psat'. Can be any one from '('Pressure', 'int', 'float', 'tuple')'", str(exp))

    @pytest.mark.delete 
    def test_MaterialStream_stream_equipment_delete_without_connection(self):
        e4 = MaterialStream()   
        repr(e4)
        e4.delete()
        with pytest.raises(Exception) as exp:
            repr(e4)     
        self.assertIn("Stream does not exist!",
                      str(exp))  

    @pytest.mark.delete
    def test_MaterialStream_stream_equipment_delete_with_connection(self):
        from propylean.equipments.abstract_equipment_classes import _material_stream_equipment_map as mse_map
        from propylean import CentrifugalPump
        pump = CentrifugalPump()
        inlet_stream = MaterialStream(pressure=(20, 'bar'))
        inlet_stream.components = prop.Components({"water": 1})
        outlet_stream = MaterialStream()

        pump.connect_stream(inlet_stream, direction="in")
        pump.connect_stream(outlet_stream, direction="out")

        self.assertEqual(mse_map[inlet_stream.index][2], pump.index)
        self.assertEqual(mse_map[inlet_stream.index][3], pump.__class__)
        self.assertEqual(mse_map[outlet_stream.index][0], pump.index)
        self.assertEqual(mse_map[outlet_stream.index][1], pump.__class__) 


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
        
        self.assertNotIn(inlet_stream.index, mse_map.keys())
        self.assertNotIn(outlet_stream.index, mse_map.keys())
