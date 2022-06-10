from propylean.equipments.generic_equipment_classes import _EquipmentOneInletOutlet


class FlowMeter(_EquipmentOneInletOutlet):
    items = []
    def __init__(self, **inputs) -> None:
        self._index = len(FlowMeter.items)
        super().__init__( **inputs)
        del self.energy_out
        del self.energy_in
        FlowMeter.items.append(self)

    def __repr__(self):
        return "Flow Meter with tag: " + self.tag   
    def __hash__(self):
        return hash(self.__repr__())

    @classmethod
    def list_objects(cls):
        return cls.items
# End of final classes of Piping and instruments