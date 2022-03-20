from typing import OrderedDict
import pytest
import unittest

from thermo import Mixture
from propylean.streams import MaterialStream
import propylean.properties as prop
import pandas as pd

class test_MaterialStream(unittest.TestCase):
    def test_MaterialStream_instantiation_tag_only(self):
        m1 = MaterialStream(tag="m1")
        self.assertEqual(m1.tag, "m1")
        self.assertEqual(m1.pressure, prop.Pressure())
        self.assertEqual(m1.temperature, prop.Temperature())
        self.assertEqual(m1.mass_flowrate, prop.MassFlowRate())
        self.assertIsNone(m1._from_equipment_tag)
        self.assertIsNone(m1._to_equipment_tag)
    
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

    def test_MaterialStream_components_flow_property_density(self):
        m4 = MaterialStream(tag="m4", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        m4.components = OrderedDict([('methane', 0.96522),
                                     ('nitrogen', 0.00259),
                                     ('carbon dioxide', 0.00596),
                                     ('ethane', 0.01819),
                                     ('propane', 0.0046),
                                     ('isobutane', 0.00098),
                                     ('butane', 0.00101),
                                     ('2-methylbutane', 0.00047),
                                     ('pentane', 0.00032),
                                     ('hexane', 0.00066)])
        mx = Mixture(zs=m4.components)
        m4.density.unit = "kg/m3"
        m4.density_l.unit = "kg/m3"
        m4.density_g = "kg/m3"
        self.assertEqual(m4.density.value, mx.rho())
        self.assertEqual(m4.density_l.value, mx.rhol())
        self.assertEqual(m4.density_g.value, mx.rhog())

    def test_MaterialStream_components_flow_property_viscosity(self):
        m4 = MaterialStream(tag="m5", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        m4.components = OrderedDict([('methane', 0.96522),
                                     ('nitrogen', 0.00259),
                                     ('carbon dioxide', 0.00596),
                                     ('ethane', 0.01819),
                                     ('propane', 0.0046),
                                     ('isobutane', 0.00098),
                                     ('butane', 0.00101),
                                     ('2-methylbutane', 0.00047),
                                     ('pentane', 0.00032),
                                     ('hexane', 0.00066)])
        mx = Mixture(zs=m4.components)
        m4.viscosity.unit = "Pa-s"
        m4.viscosity_l.unit = "Pa-s"
        m4.viscosity_g.unit = "Pa-s"
        self.assertEqual(m4.viscosity, mx.mu())
        self.assertEqual(m4.viscosity_l, mx.mul())
        self.assertEqual(m4.viscosity_g, mx.mug())

    def test_MaterialStream_components_flow_property_volumetric_flowrate(self):
        m4 = MaterialStream(tag="m6", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        m4.components = OrderedDict([('methane', 0.96522),
                                     ('nitrogen', 0.00259),
                                     ('carbon dioxide', 0.00596),
                                     ('ethane', 0.01819),
                                     ('propane', 0.0046),
                                     ('isobutane', 0.00098),
                                     ('butane', 0.00101),
                                     ('2-methylbutane', 0.00047),
                                     ('pentane', 0.00032),
                                     ('hexane', 0.00066)])
        mx = Mixture(zs=m4.components)
        m4.vol_flowrate.unit = "m3/h"
        expected_volumetric_flowrate = 1000/mx.rho()
        self.assertEqual(m4.vol_flowrate.value, expected_volumetric_flowrate)
    
    def test_MaterialStream_components_flow_property_molar_flowrate(self):
        m4 = MaterialStream(tag="m7", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        m4.components = OrderedDict([('methane', 0.96522),
                                     ('nitrogen', 0.00259),
                                     ('carbon dioxide', 0.00596),
                                     ('ethane', 0.01819),
                                     ('propane', 0.0046),
                                     ('isobutane', 0.00098),
                                     ('butane', 0.00101),
                                     ('2-methylbutane', 0.00047),
                                     ('pentane', 0.00032),
                                     ('hexane', 0.00066)])
        mx = Mixture(zs=m4.components)
        m4.mol_flowrate.unit = "mol/h"
        expected_molar_flowrate = 1000000/mx.MW()
        self.assertEqual(m4.mol_flowrate.value, expected_molar_flowrate)
    
    def test_MaterialStream_components_thermodynamic_property_MW(self):
        m4 = MaterialStream(tag="m8", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        m4.components = OrderedDict([('methane', 0.96522),
                                     ('nitrogen', 0.00259),
                                     ('carbon dioxide', 0.00596),
                                     ('ethane', 0.01819),
                                     ('propane', 0.0046),
                                     ('isobutane', 0.00098),
                                     ('butane', 0.00101),
                                     ('2-methylbutane', 0.00047),
                                     ('pentane', 0.00032),
                                     ('hexane', 0.00066)])
        mx = Mixture(zs=m4.components)
        m4.MW.unit = "g/mol"
        expected_MW= mx.MW()
        self.assertEqual(m4.MW.value, expected_MW)
    
    def test_MaterialStream_components_thermodynamic_property_compressibity_factor(self):
        m4 = MaterialStream(tag="m9", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        m4.components = OrderedDict([('methane', 0.96522),
                                     ('nitrogen', 0.00259),
                                     ('carbon dioxide', 0.00596),
                                     ('ethane', 0.01819),
                                     ('propane', 0.0046),
                                     ('isobutane', 0.00098),
                                     ('butane', 0.00101),
                                     ('2-methylbutane', 0.00047),
                                     ('pentane', 0.00032),
                                     ('hexane', 0.00066)])
        mx = Mixture(zs=m4.components)
        self.assertEqual(m4.Z, mx.Z())
        self.assertEqual(m4.Z_l, mx.Zl())
        self.assertEqual(m4.Z_g, mx.Zg())
    
    def test_MaterialStream_components_thermodynamic_property_isentropic_exponent(self):
        m4 = MaterialStream(tag="m10", 
                            pressure=(10, 'bar'),
                            temperature=300,
                            mass_flowrate=prop.MassFlowRate(1000, "kg/h"))
        m4.components = OrderedDict([('methane', 0.96522),
                                     ('nitrogen', 0.00259),
                                     ('carbon dioxide', 0.00596),
                                     ('ethane', 0.01819),
                                     ('propane', 0.0046),
                                     ('isobutane', 0.00098),
                                     ('butane', 0.00101),
                                     ('2-methylbutane', 0.00047),
                                     ('pentane', 0.00032),
                                     ('hexane', 0.00066)])
        mx = Mixture(zs=m4.components)
        self.assertEqual(m4.isentropic_exponent, mx.isentropic_exponent)
