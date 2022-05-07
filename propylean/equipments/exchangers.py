from propylean.generic_equipment_classes import _Exchangers

# Start of final classes of heat exchangers
class ShellnTubeExchanger(_Exchangers):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(ShellnTubeExchanger.items)
        super().__init__( **inputs)
        ShellnTubeExchanger.items.append(self)
    
    def __repr__(self):
        return "Shell & Tube Exchanger with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items

class AirCooler(_Exchangers):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(AirCooler.items)
        super().__init__( **inputs)
        AirCooler.items.append(self)
    
    def __repr__(self):
        return "Air Cooler with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())
    
    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of heat exchangers      