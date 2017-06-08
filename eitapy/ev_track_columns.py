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
    
    def add_PARSEC_info(self, PARSEC_col_name, PARSEC_col_id, 
                              PARSEC_col_note = ""):
        
        """
        Includes information about the column in the PARSEC tracks
        """
        
        self.PARSEC_col_name = PARSEC_col_name
        self.PARSEC_col_id   = PARSEC_col_id
        self.PARSEC_col_note = PARSEC_col_note


################################################################################
# Defining main columns                                                        #
################################################################################

# Should be imported and used as et_col.age
age = Ev_track_column(name        = "stellar_age",
                      description = "age of the star",
                      unit        = "years",
                      log         = False)

age.add_PARSEC_info(PARSEC_col_name = "AGE",
                    PARSEC_col_id   = 2)

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

log_L = Ev_track_column(name        = "log_L",
                        description = "Log bolometric luminosity",
                        unit        = "L_sun",
                        log         = True)

log_L_div_Leed = Ev_track_column(name        = "log_L_div_Leed",
                                 description = ("Log ratio of bolometric "
                                                "luminosity and Eddington "
                                                "luminosity"), #View MIST readme
                                 unit        = "",
                                 log         = True)

log_LH = Ev_track_column(name        = "log_LH",
                         description = "Log hydrogen-burning luminosity",
                         unit        = "L_sun",
                         log         = True)

log_LHe = Ev_track_column(name        = "log_LHe",
                          description = "Log helium-burning luminosity",
                          unit        = "L_sun",
                          log         = True)

log_LZ = Ev_track_column(name        = "log_LZ",
                         description = ("Log total-burning luminosity "
                                        "excluding H-burn, He-burn and "
                                        "photodisintegrations"),
                         unit        = "L_sun",
                         log         = True)

log_Lgrav = Ev_track_column(name        = "log_Lgrav",
                            description = ("Log gravitational potential "
                                           "luminosity"),
                            unit        = "L_sun",
                            log         = True)

log_Teff = Ev_track_column(name        = "log_Teff",
                           description = "Log effective temperature",
                           unit        = "K",
                           log         = True)

log_R = Ev_track_column(name        = "log_R",
                        description = "Log radius",
                        unit        = "R_sun",
                        log         = True)

log_g = Ev_track_column(name        = "log_g",
                        description = "Log surface gravity",
                        unit        = "cm s-2",
                        log         = True)

log_surf_Z = Ev_track_column(name        = "log_surf_Z",
                             description = ("Log surface mass fraction in "
                                            "metals"),
                             unit        = "",
                             log         = True)

surf_avg_omega = Ev_track_column(name        = "surf_avg_omega",
                                 description = "surface angular rotation speed",
                                 unit        = "", # ?
                                 log         = False)

surf_avg_v_rot = Ev_track_column(name        = "surf_avg_v_rot",
                                 description = "surface rotation speed",
                                 unit        = "", # ?
                                 log         = False)

c12_div_o16 = Ev_track_column(name        = "surf_num_c12_div_num_o16",
                              description = ("ratio of surface number densities"
                                             " of 12C and 16O"),
                              unit        = "",
                              log         = False)

v_wind = Ev_track_column(name             = "v_wind",
                              description = "wind speed",
                              unit        = "km s-1",
                              log         = False)
# \WARNING different track sets may use different phases definition.
# Use for the columns PARSEC_phase, MIST_phase, etc.
