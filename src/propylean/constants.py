class Constants(object):
    g = 9.8 # m/s^2
    R = 8.3144 # J/K/mol
    ROUGHNESS = (4.57e-5, 4.5e-5, 0.000259, 1.5e-5, 1.5e-6) #in m
    Le_BY_D = {"plastic": [17, 13, 72, 46, 3.3, 9, 400, 120, 530, 700],
               "steel": [13, 10, 57, 37, 2.6, 7.5, 320, 95, 420, 560]}
    REDUCER_Le_BY_D_PLASTIC = {9: 10, 8: 30, 7: 75, 6: 175, 5: 420, 4: 1150}
    REDUCER_Le_BY_D_STEEL = {9: 3, 8: 8, 7: 18, 6: 38, 5: 85, 4: 220}
    HEAD_TYPES = ["hemispherical", "elliptical", "torispherical", "flat"]

class ConversionFactors(object):
    """
    Class to store all conversion factors for a specific property.
    """
    LENGTH = {
            'foot': 1/3.28083,
            'yard': 1/1.09361,
            'mile': 1/0.000621371,
            'cm': 1/100,
            'inch': 1/39.3701,
            'km':10^3,
            'mm': 1/1000,
            'm': 1
            }
    TIME = {
            'year': (3600*24*30*12),
            'month': (3600*24*30),
            'week': (3600*24*7),
            'day': (3600*24),
            'hour':3600,
            'min': 60,
            'sec': 1
            }
    PRESSURE = {'atm': 101320,
                'bar': 100000,
                'psi': 6893,
                'kPa': 1000,
                'MPa': 1000000,
                'kg/cm^2': 98070,
                'ata': 98070,
                'Torr': 133.3,
                'mm Hg': 133.3,
                'in water':2490,
                'm water': 0.00981,
                'Pa': 1
                }
    MASSFLOWRATE = {'g/s': 1000,
                    'kg/min': 1/(1/60),
                    'kg/d': 1*(24*60*60),
                    'kg/h': 1*(60*60),
                    'lb/s': 2.204,
                    'lb/min': 2.204*60,
                    'lb/h': 2.204*(60*60),
                    'lb/d': 2.204*(60*60*24),
                    'ton/h': 0.001*(60*60),
                    'ton/d': 0.001*(60*60*24),
                    'kg/s': 1
                    }
    MASS = {'g': 1000,
            'lb': 2.204,
            'ton': 0.001,
            'kg': 1
            }
    MOLECULARWEIGTH = {
                        'kg/mol': 0.001,
                        'g/mol': 1
                    }
    MOLARFLOWRATE = {'lbmol/h': 7.93664,
                                'mol/min': 1*60,
                                'mol/d': 1*(24*60*60),
                                'mol/h': 1*(60*60),
                                'lbmol/s': 7.93664*3600,
                                'lbmol/min': 7.93664*60,
                                'lbmol/d': 7.93664*24,
                                'kmol/h': 1/1000*(60*24),
                                'kmol/d': 1000*(60*60*24),
                                'mol/s': 1
                                }
    VOLUMETRICFLOWRATE = {'ft^3/s': 35.3146,
                            'cm^3/s': 1000000,
                            'm^3/min': 60,
                            'm^3/h': 3600,
                            'm^3/d': 3600*24,
                            'ft^3/min': 35.3146*60,
                            'ft^3/h': 35.3146*60*60,
                            'ft^3/d': 35.3146*60*60*24,
                            'gal/s': 264.172,
                            'gal/min': 264.172*60,
                            'gal/h': 264.172*60*60,
                            'gal/d': 264.172*60*60*24,
                            'lit/s': 1000,
                            'lit/min': 60000,
                            'lit/h': 3600000,
                            'lit/d': 3600000*24,
                            'm^3/s': 1
                            }
    VOLUME = {'ft^3': 35.3146,
            'cm^3': 1000000,
            'gal': 264.172,
            'lit': 1000,
            'm^3': 1
            }
    DENSITY = {'g/cm^3': 0.001,
                'lbm/ft^3': 0.062479,
                'kg/m^3': 1
                }
    DVISCOSITY = {'lb/(ft-s)': 1.4881,
                    'cP': 1000,
                    'Pa-s': 1
                    }
    POWER = {'BTU/h': 0.293071070172222,
            'BTU/min': 17.5842642103333,
            'BTU/s': 1055.05585262,
            'cal/h': 0.001163,
            'cal/s': 4.1868,
            'erg/h': 2.777778E-11,
            'erg/min': 1.666667E-9,
            'erg/s': 1E-7,
            'hp': 735.49875,
            'MMBTU/h': 293071.070172222,
            'MMBTU/min': 17584264.2103333,
            'MMBTU/s': 1055055852.62,
            'kW': 1000,
            'MW': 1000000,
            'GW': 1000000000,
            'TW': 1000000000000,
            'kWh/d': 41.667,
            'MWh/d': 41666.67,
            'GWh/d': 41666666.67,
            'TWh/d': 41666666666.67,
            'W': 1
            }
    FREQUENCY = {'/hour': 3600,
                '/min': 60,
                'Hz': 1
                }