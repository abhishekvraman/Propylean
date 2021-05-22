from equipments import vertical_separator as vs

separator = vs(operating_pressure=10, operating_temperature=50)
print(separator.operating_pressure,separator.design_pressure)
