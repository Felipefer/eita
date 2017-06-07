"""
Defines the evolutionary track's possible columns and the relations between them
"""

class Ev_track_column(object):
    """
    Contains information about each evolutionary track possible column
    """
    
    def __init__(self, name, description, unit, log):
        """
        param        name: column name
        param description: small text description
        param        unit: column unit
        param         log: bolean telling if it takes the log of the quantity
        """
        
        self.name = name
        self.description = description
        self.unit = unit
        self.log = log


################################################################################
# Defining main columns                                                        #
################################################################################

# Should be imported and used as et_col.age
age = Ev_track_column(name        = "stellar_age",
                      description = "age of the star",
                      unit        = "years",
                      log         = False)

log_age = Ev_track_column(name        = "log_stellar_age",
                          description = "age of the star",
                          unit        = "years",
                          log         = True)

#\TODO include way to know these quantities are related

initial_mass = Ev_track_column(name        = "initial_mass",
                               description = "initial stellar mass",
                               unit        = "M_sun",
                               log         = False)

mass = Ev_track_column(name        = "mass",
                       description = "current stellar mass",
                       unit        = "M_sun",
                       log         = False)

mdot = Ev_track_column(name        = "mdot",
                       description = "mass loss rate",
                       unit        = "M_sun/year",
                       log         = False)

he_core_mass = Ev_track_column(name        = "he_core_mass",
                               description = "mass of helium rich core",
                               unit        = "M_sun",
                               log         = False)

c_core_mass = Ev_track_column(name        = "c_core_mass",
                              description = "mass of carbon rich core",
                              unit        = "M_sun",
                              log         = False)

o_core_mass = Ev_track_column(name        = "o_core_mass",
                              description = "mass of oxygen rich core",
                              unit        = "M_sun",
                              log         = False)

# \WARNING different track sets may use different phases definition.
# Use for the columns PARSEC_phase, MIST_phase, etc.
