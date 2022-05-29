from propylean.generic_equipment_classes import _EquipmentOneInletOutlet

class PressureSafetyValve(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:  
        self._index = len(PressureSafetyValve.items)     
        super().__init__( **inputs)
        PressureSafetyValve.items.append(self)
    
    def __repr__(self):
        return "Pressure Safety Valve with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items
