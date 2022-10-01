from propylean.equipments.generic_equipment_classes import _EquipmentOneInletOutlet
from propylean.settings import Settings
from propylean.constants import Constants
from propylean import properties as prop
from math import pi
import pandas as pd
from propylean.validators import _Validators

class PipeSegment(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        """ 
        DESCRIPTION:
            Final class for creating objects to represent a Pipe Segmenet.
        
        PARAMETERS:
            Read _EquipmentOneInletOutlet class for more arguments for this class
            ID:
                Required: Yes, if OD and thickness not provided
                Type: int or float or property.Lenght(recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Internal Diameter of the pipe segment.

            OD:
                Required: Yes, if ID not provided
                Type: int or float or property.Lenght(recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Outer Diameter of the pipe segment.
            
            thickness:
                Required: Yes, if ID not provided
                Type: int or float or property.Lenght(recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: Wall thickness of the pipe segment.
            
            length:
                Required: Yes, for straight tube
                Type: int or float or property.Lenght(recommended)
                Acceptable values: Non-negative values
                Default value: None
                Description: length of the pipe segment.
            
            elevation:
                Required: No
                Type: int or float or property.Lenght(recommended)
                Acceptable values: All values
                Default value: 0 m
                Description: elevation of the pipe segment.

            segment_type:
                Required: No
                Type: int
                Acceptable values: 1 to 13.
                Default value: 1
                Description: Segment type/fitting type of the pipe segment.
            
            material:
                Required: No
                Type: int
                Acceptable values: 1 to 5.
                Default value: 1
                Description: Material type of the pipe segment.
            
            shape:
                Required: Yes, only if segment_type is 12 or 13
                Type: tuple
                Description: Only in segment type is reducer or expander 
            
            segment_frame:
                Required: No
                Type: Pandas DataFrame
                Description: List of PipeSegment objects in with columns as above arguments.
                             >>> import pandas as pd
                             For below list of segements, DataFrame to be created is as follows:
                                +-----------------------------------------------------------------------------+
                                | Segment Type   |  ID    |  length   |  material     | elevation  | Shape    |
                                | Straight Tube  | 20 cm  |  10 m     | Carbon Steel  | 2 m down   |          |
                                | Elbow          | 20 cm  |  NA       | Carbon Steel  | NA         |          |
                                | Ball Valve     | 20 cm  |  NA       | Carbon Steel  | NA         |          |
                                | Reducer        |        |  NA       | Carbon Steel  | NA         | (20, 18) |
                                +-----------------------------------------------------------------------------+
                                Note: OD and tickness can also be sepcified instead of ID. If all are provided,
                                      ID will be considered
                             >>> segment_frame = pd.DataFrame({'segment_type': [1, 2, 6, 12],
                                                               'ID': [(20, 'cm'), (20, 'cm'), (20, 'cm'), (18, 'cm')],
                                                               'length': [(10, 'm'), None, None, None],
                                                               'material': [2, 2, 2, 2],
                                                               'elevation': [(-2, 'm'), None, None, None],
                                                               'shape': [None, None, None, (20, 18)]})
        
        RETURN VALUE:
            Type: PipeSegment
            Description: Returns an object of type PipeSegment with all properties of
                         a pipe segments and fittings used in process industry piping.
        
        ERROR RAISED:
            Type:
            Description:
        
        SAMPLE USE CASES:
            >>> PS_1 = PipeSegment(ID=(20, "cm"), 
                                   OD=prop.Length(2200, "mm"),
                                   length=10)
            >>> print(PS_1)
            Pipe Segment with tag: P1
        """
        super().__init__( **inputs)
        self._pressure_drop = prop.Pressure(0)
        self._ID = prop.Length()
        self._OD = prop.Length()
        self._length = prop.Length(0)
        self._elevation = prop.Length(0)
        self._segment_type = 1
        self._material = 1
        from pandas import DataFrame
        self._segment_frame = DataFrame()
        self._segment_obj_list = None
        
        if 'segment_frame' not in inputs:
            del self.segment_frame
            self.segment_type = 1 if 'segment_type' not in inputs else inputs['segment_type']
            if self.segment_type == 1:
                if 'length' in inputs:
                    self.length = inputs['length']               
                else:
                    raise Exception('Straight Tube segment requires "length" value.')
                if 'elevation' in inputs:
                    self.elevation = inputs['elevation']
            elif self.segment_type in range(12, 14):
                self._shape = inputs['shape']
            
            if 'material' in inputs:
                self.material = inputs['material']
            
            if ('ID' in inputs and inputs['ID'] is not None):
                self.ID = inputs['ID']
                if 'OD' in inputs and inputs['OD'] is not None:
                    self.OD = inputs['OD']
                elif 'thickness' in inputs and inputs['thickness'] is not None:
                    self.thickness = inputs['thickness']
            elif ('OD' in inputs and 'thickness' in inputs):
                self.OD = inputs['OD']
                self.ID = inputs['thickness']
                self.ID = self.OD - self.ID
            else:
                raise Exception('Define atleast ID or OD with thickness to define a pipe segment object') 
            
        else:
            self.segment_frame = inputs['segment_frame']   
            self._segment_obj_list = []                                     
            del self.ID
            del self.OD
            del self.material
            del self.segment_type
        self._index = len(PipeSegment.items)
        PipeSegment.items.append(self)
    
    def __repr__(self):
        self = self._get_equipment_object(self)
        return "Pipe Segment with tag: " + self.tag   #ADD SEGMENT TYPE!!
    def __hash__(self):
        return hash(self.__repr__())
    
    @property
    def segment_frame(self):
        self = self._get_equipment_object(self)
        return self._segment_frame
    @segment_frame.setter
    def segment_frame(self, value):
        _Validators.validate_arg_prop_value_type("segment_frame", value, pd.DataFrame)
        self = self._get_equipment_object(self)
        self._segment_frame = value
        self._update_equipment_object(self)
    @segment_frame.deleter
    def segment_frame(self):
        self = self._get_equipment_object(self)
        del self._segment_frame
        self._update_equipment_object(self)

    @property
    def length(self):
        self = self._get_equipment_object(self)
        return self._length
    @length.setter
    def length(self, value):
        _Validators.validate_arg_prop_value_type("length", value, (prop.Length, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._length.unit
        self._length = prop.Length(value, unit)
        self._update_equipment_object(self)
    @property
    def equivalent_length(self):
        self = self._get_equipment_object(self)
        ID = self.ID
        ID.unit = 'm'
        if self.material==5:
            Le_by_D = Constants.Le_BY_D["plastic"]
            if self.segment_type in range(13, 15):
                Le_by_D = Constants.REDUCER_Le_BY_D_PLASTIC
            else:
                Le_by_D = Constants.REDUCER_Le_BY_D_STEEL
        else:
            Le_by_D = Constants.Le_BY_D["steel"]
        if self.segment_type == 1:
            equivalent_length = self.length
        elif self.segment_type in range(2, 12):
            equivalent_length = Le_by_D[self.segment_type-2] * ID.value
            equivalent_length = prop.Length(equivalent_length)
        elif self.segment_type in range(12, 14):
            ratio = int(10*self._shape[1]/self._shape[0])
            if ratio > 9:
                ratio = 9
            elif ratio < 4:
                ratio = 4
            equivalent_length = Le_by_D[ratio] * self._shape[0]
            equivalent_length = prop.Length(equivalent_length)
        return equivalent_length
    @property
    def elevation(self):
        self = self._get_equipment_object(self)
        return self._elevation
    @elevation.setter
    def elevation(self, value):
        _Validators.validate_arg_prop_value_type("elevation", value, (prop.Length, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._elevation.unit
        self._elevation = prop.Length(value, unit)
        self._update_equipment_object(self)

    @property
    def ID(self):
        self = self._get_equipment_object(self)
        return self._ID
    @ID.setter
    def ID(self, value):
        _Validators.validate_arg_prop_value_type("ID", value, (prop.Length, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._ID.unit
        self._ID = prop.Length(value, unit)
        self._update_equipment_object(self)
    @ID.deleter
    def ID(self):
        self = self._get_equipment_object(self)
        del self._ID
        self._update_equipment_object(self)
    
    @property
    def OD(self):
        self = self._get_equipment_object(self)
        return self._OD
    @OD.setter
    def OD(self, value):
        _Validators.validate_arg_prop_value_type("OD", value, (prop.Length, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self._OD.unit
        self._OD =prop.Length(value, unit)
        self._update_equipment_object(self)
    @OD.deleter
    def OD(self):
        self = self._get_equipment_object(self)
        del self._OD
        self._update_equipment_object(self)
    
    @property
    def thickness(self):
        self = self._get_equipment_object(self)
        # if self._OD - self._ID <= prop.Length(0):
        #     raise Exception("ID is not less than OD! Change ID or OD or thickness.")
        return self._OD - self._ID
    @thickness.setter
    def thickness(self, value):
        _Validators.validate_arg_prop_value_type("thickness", value, (prop.Length, int, float, tuple))
        self = self._get_equipment_object(self)
        value, unit = self._tuple_property_value_unit_returner(value, prop.Length)
        if unit is None:
            unit = self.thickness
        self._OD = self._ID + prop.Length(value, unit)
        self._update_equipment_object(self)

    @property
    def segment_type(self):
        self = self._get_equipment_object(self)
        return self._segment_type
    @segment_type.setter
    def segment_type(self, value):
        _Validators.validate_arg_prop_value_type("segment_type", value, int)
        _Validators.validate_arg_prop_value_range("segment_type", value, [1, 13])
        self = self._get_equipment_object(self)
        segments = '''\nSegments can be of following types and in range of numbers below:
                    1. Straight Tube
                    2. Elbow
                    3. Tee (straight through)
                    4. Tee (through branch)
                    5. Butterfly valve 
                    6. Ball valve (full bore)
                    7. Gate valve(full open)
                    8. Globe valve (full open)
                    9. Swing check valve
                    10. Wafer disk check valve
                    11. Lift check valve
                    12. Reducer
                    13. Expander'''
        if value not in range(1,14):
            raise Exception(segments)
        self._segment_type = value
        self._update_equipment_object(self)
    @segment_type.deleter
    def segment_type(self):
        self = self._get_equipment_object(self)
        del self._segment_type
        self._update_equipment_object(self)
    
    @property
    def material(self):
        self = self._get_equipment_object(self)
        return self._material
    @material.setter
    def material(self, value):
        _Validators.validate_arg_prop_value_type("material", value, int)
        _Validators.validate_arg_prop_value_range("material", value, [1, 5])
        self = self._get_equipment_object(self)
        materials = '''\nSegment material can be of following types and in range of numbers below:
                    1. Raw Steel
                    2. Carbon Steel
                    3. Cast Iron
                    4. Stainless Steel
                    5. PVC''' 
        if value not in range(1, 6):
            raise Exception(materials)
        self._material = value
        self._update_equipment_object(self)
    @material.deleter
    def material(self):
        self = self._get_equipment_object(self)
        del self._material
        self._update_equipment_object(self)

    @property
    def pressure_drop(self):
        self = self._get_equipment_object(self)
        pressure_drop = prop.Pressure(0, self.inlet_pressure.unit)
        if self.inlet_mass_flowrate.value == 0:
            return prop.Pressure(0, self._inlet_pressure.unit)
        if (self._outlet_material_stream_tag is None and
            self._inlet_material_stream_tag is None):
            raise Exception("PipeSegment should be connected with MaterialStream either at inlet or outlet")
       
        is_inlet = False if self._inlet_material_stream_index is None else True
        density = self._connected_stream_property_getter(is_inlet, "material", "density")
        viscosity = self._connected_stream_property_getter(is_inlet, "material", "d_viscosity")
        vol_flowrate = self._connected_stream_property_getter(is_inlet, "material", "vol_flowrate")
        density.unit = "kg/m^3"
        viscosity.unit = "Pa-s"
        vol_flowrate.unit = "m^3/s"
        if self._segment_obj_list is None:
            ID = self.ID
            ID.unit = 'm'
            length = self.equivalent_length
            length.unit = 'm'
            drop_friction = self.dp_friction(vol_flowrate, ID, length, density, viscosity)
            drop_hydrostatic = self.dp_hydrostatic(density)
            pressure_drop = drop_friction + drop_hydrostatic
        else:
            for column in ['segment_type', 'ID', 'OD', 'thickness', 'length', 'material', 'elevation', 'shape']:
                if column not in list(self.segment_frame.columns):
                    self.segment_frame[column] = None
            rows = zip(self.segment_frame['segment_type'],
                        self.segment_frame['ID'],
                        self.segment_frame['OD'],
                        self.segment_frame['thickness'],
                        self.segment_frame['length'],
                        self.segment_frame['material'],
                        self.segment_frame['elevation'],
                        self.segment_frame['shape'])
            for row in rows:
                ps = PipeSegment(segment_type=row[0],
                                 ID=row[1],
                                 OD=row[2],
                                 thickness=row[3],
                                 length=row[4],
                                 material=row[5],
                                 elevation=row[6],
                                 shape=row[7])
                ID = ps.ID
                ID.unit = 'm'
                length = ps.equivalent_length
                length.unit = 'm'
                drop_friction = ps.dp_friction(vol_flowrate, ID, length, density, viscosity)
                drop_hydrostatic = ps.dp_hydrostatic(density)
                pressure_drop += drop_friction + drop_hydrostatic
        return pressure_drop
        
    @pressure_drop.setter
    def pressure_drop(self, value):
        raise Exception('''Cannot manually set pressure drop for PipeSegment!\n
                         Pressure drop depends on physical properties of the PipeSegment and MaterialStream connected.''')
    
    def dp_hydrostatic(self, density):
        self = self._get_equipment_object(self)
        elevation_old_unit = self.elevation.unit
        self.elevation.unit = "m"
        hydro_drop = prop.Pressure(self.elevation.value * density.value * 9.8)
        hydro_drop.unit = self.inlet_pressure.unit
        self.elevation.unit = elevation_old_unit
        return hydro_drop

    def dp_friction(self, vol_flowrate, ID, length, density, viscosity,
                    method=Settings.pipe_dp_method, Darcy=Settings.Darcy):
        self = self._get_equipment_object(self)
        from fluids.friction import friction_factor
        from fluids.core import Reynolds, K_from_f, dP_from_K
        from propylean.constants import Constants

        V=(vol_flowrate.value)/(pi* ID.value**2)/4
        Re = Reynolds(V=V,
                    D=ID.value, 
                    rho=density.value, 
                    mu=viscosity.value)
        fd = friction_factor(Re=Re, 
                            eD=Constants.ROUGHNESS[self.material-1]/ID.value,
                            Method=method,
                            Darcy=Darcy)
        K = K_from_f(fd=fd, L=length.value, D=ID.value)        
        drop = round(dP_from_K(K, rho=1000, V=V),3)
        drop = prop.Pressure(drop, 'Pa')
        drop.unit = self._inlet_pressure.unit
        return drop
            
    @classmethod
    def list_objects(cls):
        return cls.items

class Strainers(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self._index = len(Strainers.items)
        Strainers.items.append(self)
        
class Filters(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        super().__init__(**inputs)
        self._index = len(Filters.items)
        Filters.items.append(self)