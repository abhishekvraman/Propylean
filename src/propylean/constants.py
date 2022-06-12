class Constants(object):
    g = 9.8 # m/s^2
    R = 8.3144 # J/K/mol
    ROUGHNESS = (4.57e-5, 4.5e-5, 0.000259, 1.5e-5, 1.5e-6) #in m
    Le_BY_D = {"plastic": [17, 13, 72, 46, 3.3, 9, 400, 120, 530, 700],
               "steel": [13, 10, 57, 37, 2.6, 7.5, 320, 95, 420, 560]}
    REDUCER_Le_BY_D_PLASTIC = {9: 10, 8: 30, 7: 75, 6: 175, 5: 420, 4: 1150}
    REDUCER_Le_BY_D_STEEL = {9: 3, 8: 8, 7: 18, 6: 38, 5: 85, 4: 220}
    HEAD_TYPES = ["hemispherical", "elliptical", "torispherical", "flat"]