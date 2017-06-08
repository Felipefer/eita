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

################################################################################

log_age = Ev_track_column(name        = "log_stellar_age",
                          description = "age of the star",
                          unit        = "years",
                          log         = True)

#\TODO include way to know these quantities are related
################################################################################

initial_mass = Ev_track_column(name        = "initial_mass",
                               description = "initial stellar mass",
                               unit        = "M_sun",
                               log         = False)

################################################################################

mass = Ev_track_column(name        = "mass",
                       description = "current stellar mass",
                       unit        = "M_sun",
                       log         = False)

mass.add_PARSEC_info(PARSEC_col_name = "MASS",
                     PARSEC_col_id   = 1)

################################################################################

log_L = Ev_track_column(name        = "log_L",
                        description = "Log bolometric luminosity",
                        unit        = "L_sun",
                        log         = True)

log_L.add_PARSEC_info(PARSEC_col_name = "LOG_L",
                      PARSEC_col_id   = 3)

################################################################################

log_Teff = Ev_track_column(name        = "log_Teff",
                           description = "Log effective temperature",
                           unit        = "K",
                           log         = True)

log_Teff.add_PARSEC_info(PARSEC_col_name = "LOG_TE",
                         PARSEC_col_id   = 4)

################################################################################

log_R = Ev_track_column(name        = "log_R",
                        description = "Log radius",
                        unit        = "R_sun",
                        log         = True)

log_R.add_PARSEC_info(PARSEC_col_name = "LOG_R",
                      PARSEC_col_id   = 5)

################################################################################

mdot = Ev_track_column(name        = "mdot",
                       description = "mass loss rate",
                       unit        = "M_sun/year",
                       log         = False)

mdot.add_PARSEC_info(PARSEC_col_name = "LOG_RAT",
                     PARSEC_col_id   = 6)

################################################################################

he_core_mass = Ev_track_column(name        = "he_core_mass",
                               description = "mass of helium rich core",
                               unit        = "M_sun",
                               log         = False)

he_core_mass.add_PARSEC_info(PARSEC_col_name = "M_CORE_HE",
                             PARSEC_col_id   = 7)

################################################################################

c_core_mass = Ev_track_column(name        = "c_core_mass",
                              description = "mass of carbon rich core",
                              unit        = "M_sun",
                              log         = False)

c_core_mass.add_PARSEC_info(PARSEC_col_name = "M_CORE_C",
                            PARSEC_col_id   = 8)

################################################################################

center_H = Ev_track_column(name        = "center_H",
                           description = "center mass fraction in Hydrogen",
                           unit        = "",
                           log         = False)

center_H.add_PARSEC_info(PARSEC_col_name = "H_CEN",
                          PARSEC_col_id   = 9)

################################################################################

center_He = Ev_track_column(name        = "center_He",
                            description = "center mass fraction in Helium",
                            unit        = "",
                            log         = False)

center_He.add_PARSEC_info(PARSEC_col_name = "HE_CEN",
                          PARSEC_col_id   = 10)

################################################################################

center_C = Ev_track_column(name        = "center_C",
                           description = "center mass fraction in Carbon",
                           unit        = "",
                           log         = False)

center_C.add_PARSEC_info(PARSEC_col_name = "C_cen",
                         PARSEC_col_id   = 11)

################################################################################

center_O = Ev_track_column(name        = "center_O",
                           description = "center mass fraction in Oxygen",
                           unit        = "",
                           log         = False)

center_O.add_PARSEC_info(PARSEC_col_name = "O_cen",
                         PARSEC_col_id   = 12)

################################################################################

o_core_mass = Ev_track_column(name        = "o_core_mass",
                              description = "mass of oxygen rich core",
                              unit        = "M_sun",
                              log         = False)

################################################################################

log_L_div_Leed = Ev_track_column(name        = "log_L_div_Leed",
                                 description = ("Log ratio of bolometric "
                                                "luminosity and Eddington "
                                                "luminosity"), #View MIST readme
                                 unit        = "",
                                 log         = True)

################################################################################

log_LH = Ev_track_column(name        = "log_LH",
                         description = "Log hydrogen-burning luminosity",
                         unit        = "L_sun",
                         log         = True)

################################################################################

LH_frac = Ev_track_column(name        = "LH_frac",
                         description = "hydrogen-burning luminosity fraction",
                         unit        = "",
                         log         = True)

LH_frac.add_PARSEC_info(PARSEC_col_name = "LX",
                        PARSEC_col_id   = 13)

################################################################################

log_LHe = Ev_track_column(name        = "log_LHe",
                          description = "Log helium-burning luminosity",
                          unit        = "L_sun",
                          log         = True)

################################################################################

LHe_frac = Ev_track_column(name       = "LHe_frac",
                          description = "helium-burning luminosity fraction",
                          unit        = "",
                          log         = True)

LHe_frac.add_PARSEC_info(PARSEC_col_name = "LY",
                         PARSEC_col_id   = 14)

################################################################################

LC_frac = Ev_track_column(name        = "LC_frac",
                          description = "carbon-burning luminosity fraction",
                          unit        = "",
                          log         = True)

LC_frac.add_PARSEC_info(PARSEC_col_name = "LC",
                        PARSEC_col_id   = 15)

################################################################################

LNeutr_frac = Ev_track_column(name        = "LNeutr_frac",
                              description = "neutrino luminosity fraction",
                              unit        = "",
                              log         = True)

LNeutr_frac.add_PARSEC_info(PARSEC_col_name = "LNEUTR",
                            PARSEC_col_id   = 16)

################################################################################

log_LZ = Ev_track_column(name        = "log_LZ",
                         description = ("Log total-burning luminosity "
                                        "excluding H-burn, He-burn and "
                                        "photodisintegrations"),
                         unit        = "L_sun",
                         log         = True)

################################################################################

log_Lgrav = Ev_track_column(name        = "log_Lgrav",
                            description = ("Log gravitational potential "
                                           "luminosity"),
                            unit        = "L_sun",
                            log         = True)

################################################################################

Lgrav_frac = Ev_track_column(name        = "Lgrav_frac",
                             description = "gravity luminosity fraction",
                             unit        = "",
                             log         = True)

Lgrav_frac.add_PARSEC_info(PARSEC_col_name = "L_GRAV",
                           PARSEC_col_id   = 17)

################################################################################

log_g = Ev_track_column(name        = "log_g",
                        description = "Log surface gravity",
                        unit        = "cm s-2",
                        log         = True)

################################################################################

log_surf_Z = Ev_track_column(name        = "log_surf_Z",
                             description = ("Log surface mass fraction in "
                                            "metals"),
                             unit        = "",
                             log         = True)

################################################################################

surf_avg_omega = Ev_track_column(name        = "surf_avg_omega",
                                 description = "surface angular rotation speed",
                                 unit        = "", # ?
                                 log         = False)

################################################################################

surf_avg_v_rot = Ev_track_column(name        = "surf_avg_v_rot",
                                 description = "surface rotation speed",
                                 unit        = "", # ?
                                 log         = False)

################################################################################

c12_div_o16 = Ev_track_column(name        = "surf_num_c12_div_num_o16",
                              description = ("ratio of surface number densities"
                                             " of 12C and 16O"),
                              unit        = "",
                              log         = False)

################################################################################

v_wind = Ev_track_column(name        = "v_wind",
                         description = "wind speed",
                         unit        = "km s-1",
                         log         = False)

################################################################################

surf_H = Ev_track_column(name        = "surf_H",
                         description = "surface mass fraction in Hydrogen",
                         unit        = "",
                         log         = False)

surf_H.add_PARSEC_info(PARSEC_col_name = "H_SUP",
                       PARSEC_col_id   = 18)

################################################################################

surf_He = Ev_track_column(name        = "surf_He",
                          description = "surface mass fraction in Helium",
                          unit        = "",
                          log         = False)

surf_He.add_PARSEC_info(PARSEC_col_name = "HE_SUP",
                        PARSEC_col_id   = 19)

################################################################################

surf_C = Ev_track_column(name        = "surf_C",
                         description = "surface mass fraction in Carbon",
                         unit        = "",
                         log         = False)

surf_C.add_PARSEC_info(PARSEC_col_name = "C_SUP",
                       PARSEC_col_id   = 20)

################################################################################

surf_N = Ev_track_column(name        = "surf_N",
                         description = "surface mass fraction in Nitrogen",
                         unit        = "",
                         log         = False)

surf_N.add_PARSEC_info(PARSEC_col_name = "N_SUP",
                       PARSEC_col_id   = 21)

################################################################################

surf_O = Ev_track_column(name        = "surf_O",
                         description = "surface mass fraction in Oxygen",
                         unit        = "",
                         log         = False)

surf_O.add_PARSEC_info(PARSEC_col_name = "O_SUP",
                       PARSEC_col_id   = 22)

# \WARNING different track sets may use different phases definition.
# Use for the columns PARSEC_phase, MIST_phase, etc.

################################################################################

phase = Ev_track_column(name        = "phase",
                        description = "attributed evolutionary phase",
                        unit        = "",
                        log         = False)

phase.add_PARSEC_info(PARSEC_col_name = "PHASE",
                      PARSEC_col_id   = 23)
