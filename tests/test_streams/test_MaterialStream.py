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
        self.assertEqual(m3.tag, "MaterialStream_1")
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
        self.assertEqual(m4.vol_flowrate.value, expected_volumetric_flowrate)
    
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
        self.assertEqual(m4.Z, mx.Z)
        self.assertEqual(m4.Z_l, mx.Zl)
        self.assertEqual(m4.Z_g, mx.Zg)
    
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
        self.assertEqual(m4.isentropic_exponent, mx.isentropic_exponent)
    
    @pytest.mark.positive
    @pytest.mark.unit_change
    def test_MaterialStream_property_unit_change(self):
        m4 = MaterialStream(tag="m11", 
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
