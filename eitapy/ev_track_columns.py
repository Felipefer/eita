__version__ = "0.0.1"
__author__  = "Felipe de Almeida Fernandes"
__email__   = "felipefer42@gmail.com"

"""
Defines the evolutionary track's possible columns and the relations between them
"""

class Ev_track_column(object):
    """
    Contains information about each evolutionary track possible column
    """
    
    def __init__(self, name, description, unit, log, fmt = None):
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

        if fmt is not None:
            self.fmt = fmt

        self.model = {}

    def add_model_info(self, model_name, **kargs):
        """
        Includes information about the column in a given model, named
        model_name. Information is stored as a dictionary inside the, also
        dictionary self.model[model_name].

        Information must include the index (id) of the column in the model
        files. and can also include name, fmt, etc.

        :param model_name: string
        :param **kargs   : dictionary with the informations to include and add
                           to self.model[model_name]
        """

        self.model[model_name] = {}
        keys = kargs.keys()

        for key in keys:
            self.model[model_name][key] = kargs[key]

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

# This dictionary is used to provide a way to access the Ev_Track_column object
# given that the column name is known
columns = {}

# Should be imported and used as et_col.Z
Z = Ev_track_column(name        = "Z",
                    description = "metallicity of the star",
                    unit        = "",
                    log         = False,
                    fmt         = "%8.6f")

Z.add_model_info("PARSEC_ISOC_1_2",
                 name = "Z",
                 id = 0,
                 fmt = "%8.6f")

columns[Z.name] = Z

################################################################################

age = Ev_track_column(name        = "age",
                      description = "age of the star",
                      unit        = "years",
                      log         = False,
                      fmt         = "%16.10E")

age.add_PARSEC_info(PARSEC_col_name = "AGE",
                    PARSEC_col_id   = 2)

age.add_model_info("PARSEC", name = "AGE", id = 2, fmt = "%16.10E")

columns[age.name] = age

################################################################################

log_age = Ev_track_column(name        = "log_age",
                          description = "age of the star",
                          unit        = "years",
                          log         = True)

log_age.add_model_info("PARSEC_ISOC_1_2",
                       name = "log(age/yr)",
                       id = 1,
                       fmt = "%7.4f")

columns[log_age.name] = log_age

#\TODO include way to know these quantities are related
################################################################################

initial_mass = Ev_track_column(name        = "initial_mass",
                               description = "initial stellar mass",
                               unit        = "M_sun",
                               log         = False,
                               fmt="%7.3f")

initial_mass.add_model_info("PARSEC_ISOC_1_2",
                            name = "M_ini",
                            id = 2,
                            fmt = "%10.8f")

columns[initial_mass.name] = initial_mass

################################################################################

mass = Ev_track_column(name        = "mass",
                       description = "current stellar mass",
                       unit        = "M_sun",
                       log         = False,
                       fmt="%9.5f")

mass.add_PARSEC_info(PARSEC_col_name = "MASS",
                     PARSEC_col_id   = 1)

mass.add_model_info("PARSEC", name = "MASS", id = 1)
mass.add_model_info("PARSEC_ISOC_1_2",
                    name = "M_act",
                    id = 3,
                    fmt = "%6.4f")

columns[mass.name] = mass

################################################################################

log_L = Ev_track_column(name        = "log_L",
                        description = "Log bolometric luminosity",
                        unit        = "L_sun",
                        log         = True,
                        fmt="% 10.5f")

log_L.add_PARSEC_info(PARSEC_col_name = "LOG_L",
                      PARSEC_col_id   = 3)

log_L.add_model_info("PARSEC", name = "LOG_L", id = 3)
log_L.add_model_info("PARSEC_ISOC_1_2",
                     name = "logL/Lo",
                     id = 4,
                     fmt = "%6.4f")

columns[log_L.name] = log_L

################################################################################

log_Teff = Ev_track_column(name        = "log_Teff",
                           description = "Log effective temperature",
                           unit        = "K",
                           log         = True,
                           fmt         = "%8.5f")

log_Teff.add_PARSEC_info(PARSEC_col_name = "LOG_TE",
                         PARSEC_col_id   = 4)

log_Teff.add_model_info("PARSEC", name = "LOG_Teff", id = 4)
log_Teff.add_model_info("PARSEC_ISOC_1_2",
                        name = "logTe",
                        id = 5,
                        fmt = "%6.4f")

columns[log_Teff.name] = log_Teff

################################################################################

mag_bol = Ev_track_column(name        = "mag_abs",
                          description = "Bolometric absolute magnitude",
                          unit        = "",
                          log         = False,
                          fmt         = "%8.5f")

mag_bol.add_model_info("PARSEC_ISOC_1_2",
                       name = "mbol",
                       id = 7,
                       fmt = "%6.3f")

columns[mag_bol.name] = mag_bol

################################################################################

log_R = Ev_track_column(name        = "log_R",
                        description = "Log radius",
                        unit        = "R_sun",
                        log         = True,
                        fmt         = "%9.5f")

log_R.add_PARSEC_info(PARSEC_col_name = "LOG_R",
                      PARSEC_col_id   = 5)

log_R.add_model_info("PARSEC", name = "LOG_R", id = 5)

columns[log_R.name] = log_R

################################################################################

mdot = Ev_track_column(name        = "mdot",
                       description = "mass loss rate",
                       unit        = "M_sun/year",
                       log         = False)

mdot.add_PARSEC_info(PARSEC_col_name = "LOG_RAT",
                     PARSEC_col_id   = 6)

mdot.add_model_info("PARSEC", name = "LOG_RAT", id = 6)

columns[mdot.name] = mdot

################################################################################

he_core_mass = Ev_track_column(name        = "he_core_mass",
                               description = "mass of helium rich core",
                               unit        = "M_sun",
                               log         = False)

he_core_mass.add_PARSEC_info(PARSEC_col_name = "M_CORE_HE",
                             PARSEC_col_id   = 7)

he_core_mass.add_model_info("PARSEC", name = "M_CORE_HE", id = 7)

columns[he_core_mass.name] = he_core_mass

################################################################################

c_core_mass = Ev_track_column(name        = "c_core_mass",
                              description = "mass of carbon rich core",
                              unit        = "M_sun",
                              log         = False)

c_core_mass.add_PARSEC_info(PARSEC_col_name = "M_CORE_C",
                            PARSEC_col_id   = 8)

c_core_mass.add_model_info("PARSEC", name = "M_CORE_C", id = 8)

columns[c_core_mass.name] = c_core_mass

################################################################################

center_H = Ev_track_column(name        = "center_H",
                           description = "center mass fraction in Hydrogen",
                           unit        = "",
                           log         = False)

center_H.add_PARSEC_info(PARSEC_col_name = "H_CEN",
                          PARSEC_col_id   = 9)

center_H.add_model_info("PARSEC", name = "H_CEN", id = 9)

columns[center_H.name] = center_H

################################################################################

center_He = Ev_track_column(name        = "center_He",
                            description = "center mass fraction in Helium",
                            unit        = "",
                            log         = False)

center_He.add_PARSEC_info(PARSEC_col_name = "HE_CEN",
                          PARSEC_col_id   = 10)

center_He.add_model_info("PARSEC", name = "HE_CEN", id = 10)

columns[center_He.name] = center_He

################################################################################

center_C = Ev_track_column(name        = "center_C",
                           description = "center mass fraction in Carbon",
                           unit        = "",
                           log         = False)

center_C.add_PARSEC_info(PARSEC_col_name = "C_cen",
                         PARSEC_col_id   = 11)

center_C.add_model_info("PARSEC", name = "C_Cen", id = 11)

columns[center_C.name] = center_C

################################################################################

center_O = Ev_track_column(name        = "center_O",
                           description = "center mass fraction in Oxygen",
                           unit        = "",
                           log         = False)

center_O.add_PARSEC_info(PARSEC_col_name = "O_cen",
                         PARSEC_col_id   = 12)

center_O.add_model_info("PARSEC", name = "O_cen", id = 12)

columns[center_O.name] = center_O

################################################################################

o_core_mass = Ev_track_column(name        = "o_core_mass",
                              description = "mass of oxygen rich core",
                              unit        = "M_sun",
                              log         = False)

columns[o_core_mass.name] = o_core_mass

################################################################################

log_L_div_Leed = Ev_track_column(name        = "log_L_div_Leed",
                                 description = ("Log ratio of bolometric "
                                                "luminosity and Eddington "
                                                "luminosity"), #View MIST readme
                                 unit        = "",
                                 log         = True)

columns[log_L_div_Leed.name] = log_L_div_Leed

################################################################################

log_LH = Ev_track_column(name        = "log_LH",
                         description = "Log hydrogen-burning luminosity",
                         unit        = "L_sun",
                         log         = True)

columns[log_LH.name] = log_LH

################################################################################

LH_frac = Ev_track_column(name        = "LH_frac",
                         description = "hydrogen-burning luminosity fraction",
                         unit        = "",
                         log         = True)

LH_frac.add_PARSEC_info(PARSEC_col_name = "LX",
                        PARSEC_col_id   = 13)

LH_frac.add_model_info("PARSEC", name = "LX", id = 13)

columns[LH_frac.name] = LH_frac

################################################################################

log_LHe = Ev_track_column(name        = "log_LHe",
                          description = "Log helium-burning luminosity",
                          unit        = "L_sun",
                          log         = True)

columns[log_LHe.name] = log_LHe

################################################################################

LHe_frac = Ev_track_column(name       = "LHe_frac",
                          description = "helium-burning luminosity fraction",
                          unit        = "",
                          log         = True)

LHe_frac.add_PARSEC_info(PARSEC_col_name = "LY",
                         PARSEC_col_id   = 14)

LHe_frac.add_model_info("PARSEC", name = "LY", id = 14)

columns[LHe_frac.name] = LHe_frac

################################################################################

LC_frac = Ev_track_column(name        = "LC_frac",
                          description = "carbon-burning luminosity fraction",
                          unit        = "",
                          log         = True)

LC_frac.add_PARSEC_info(PARSEC_col_name = "LC",
                        PARSEC_col_id   = 15)

LC_frac.add_model_info("PARSEC", name = "LC", id = 15)

columns[LC_frac.name] = LC_frac

################################################################################

LNeutr_frac = Ev_track_column(name        = "LNeutr_frac",
                              description = "neutrino luminosity fraction",
                              unit        = "",
                              log         = True)

LNeutr_frac.add_PARSEC_info(PARSEC_col_name = "LNEUTR",
                            PARSEC_col_id   = 16)

LNeutr_frac.add_model_info("PARSEC", name = "LNEUTR", id = 16)

columns[LNeutr_frac.name] = LNeutr_frac

################################################################################

log_LZ = Ev_track_column(name        = "log_LZ",
                         description = ("Log total-burning luminosity "
                                        "excluding H-burn, He-burn and "
                                        "photodisintegrations"),
                         unit        = "L_sun",
                         log         = True)

columns[log_LZ.name] = log_LZ

################################################################################

log_Lgrav = Ev_track_column(name        = "log_Lgrav",
                            description = ("Log gravitational potential "
                                           "luminosity"),
                            unit        = "L_sun",
                            log         = True)

columns[log_Lgrav.name] = log_Lgrav

################################################################################

Lgrav_frac = Ev_track_column(name        = "Lgrav_frac",
                             description = "gravity luminosity fraction",
                             unit        = "",
                             log         = True)

Lgrav_frac.add_PARSEC_info(PARSEC_col_name = "L_GRAV",
                           PARSEC_col_id   = 17)

Lgrav_frac.add_model_info("PARSEC", name = "L_GRAV", id = 17)

columns[Lgrav_frac.name] = Lgrav_frac
################################################################################

log_g = Ev_track_column(name        = "log_g",
                        description = "Log surface gravity",
                        unit        = "cm s-2",
                        log         = True)

log_g.add_model_info("PARSEC_ISOC_1_2",
                     name = "logG",
                     id = 6,
                     fmt = "%6.4f")

columns[log_g.name] = log_g

################################################################################

log_surf_Z = Ev_track_column(name        = "log_surf_Z",
                             description = ("Log surface mass fraction in "
                                            "metals"),
                             unit        = "",
                             log         = True)

columns[log_surf_Z.name] = log_surf_Z

################################################################################

surf_avg_omega = Ev_track_column(name        = "surf_avg_omega",
                                 description = "surface angular rotation speed",
                                 unit        = "", # ?
                                 log         = False)

columns[surf_avg_omega.name] = surf_avg_omega

################################################################################

surf_avg_v_rot = Ev_track_column(name        = "surf_avg_v_rot",
                                 description = "surface rotation speed",
                                 unit        = "", # ?
                                 log         = False)

columns[surf_avg_v_rot.name] = surf_avg_v_rot

################################################################################

c12_div_o16 = Ev_track_column(name        = "surf_num_c12_div_num_o16",
                              description = ("ratio of surface number densities"
                                             " of 12C and 16O"),
                              unit        = "",
                              log         = False)

columns[c12_div_o16.name] = c12_div_o16

################################################################################

v_wind = Ev_track_column(name        = "v_wind",
                         description = "wind speed",
                         unit        = "km s-1",
                         log         = False)

columns[v_wind.name] = v_wind

################################################################################

surf_H = Ev_track_column(name        = "surf_H",
                         description = "surface mass fraction in Hydrogen",
                         unit        = "",
                         log         = False)

surf_H.add_PARSEC_info(PARSEC_col_name = "H_SUP",
                       PARSEC_col_id   = 18)

surf_H.add_model_info("PARSEC", name = "H_SUP", id = 18)

columns[surf_H.name] = surf_H

################################################################################

surf_He = Ev_track_column(name        = "surf_He",
                          description = "surface mass fraction in Helium",
                          unit        = "",
                          log         = False)

surf_He.add_PARSEC_info(PARSEC_col_name = "HE_SUP",
                        PARSEC_col_id   = 19)

surf_He.add_model_info("PARSEC", name = "HE_SUP", id = 19)

columns[surf_He.name] = surf_He

################################################################################

surf_C = Ev_track_column(name        = "surf_C",
                         description = "surface mass fraction in Carbon",
                         unit        = "",
                         log         = False)

surf_C.add_PARSEC_info(PARSEC_col_name = "C_SUP",
                       PARSEC_col_id   = 20)

surf_C.add_model_info("PARSEC", name = "C_SUP", id = 20)

columns[surf_C.name] = surf_C

################################################################################

surf_N = Ev_track_column(name        = "surf_N",
                         description = "surface mass fraction in Nitrogen",
                         unit        = "",
                         log         = False)

surf_N.add_PARSEC_info(PARSEC_col_name = "N_SUP",
                       PARSEC_col_id   = 21)

surf_N.add_model_info("PARSEC", name = "N_SUP", id = 21)

columns[surf_N.name] = surf_N

################################################################################

surf_O = Ev_track_column(name        = "surf_O",
                         description = "surface mass fraction in Oxygen",
                         unit        = "",
                         log         = False)

surf_O.add_PARSEC_info(PARSEC_col_name = "O_SUP",
                       PARSEC_col_id   = 22)

surf_O.add_model_info("PARSEC", name = "O_SUP", id = 22)

columns[surf_O.name] = surf_O

################################################################################

magU = Ev_track_column(name        = "magU",
                       description = "Absolute magnitude in the U band",
                       unit        = "",
                       log         = False)

magU.add_model_info("PARSEC_ISOC_1_2",
                     name = "U",
                     id = 8,
                     fmt = "%6.3f")

columns[magU.name] = magU

################################################################################

magB = Ev_track_column(name        = "magB",
                       description = "Absolute magnitude in the B band",
                       unit        = "",
                       log         = False)

magB.add_model_info("PARSEC_ISOC_1_2",
                     name = "B",
                     id = 9,
                     fmt = "%6.3f")

columns[magB.name] = magB

################################################################################

magV = Ev_track_column(name        = "magV",
                       description = "Absolute magnitude in the V band",
                       unit        = "",
                       log         = False)

magV.add_model_info("PARSEC_ISOC_1_2",
                     name = "V",
                     id = 10,
                     fmt = "%6.3f")

columns[magV.name] = magV

################################################################################

magR = Ev_track_column(name        = "magR",
                       description = "Absolute magnitude in the R band",
                       unit        = "",
                       log         = False)

magR.add_model_info("PARSEC_ISOC_1_2",
                     name = "R",
                     id = 11,
                     fmt = "%6.3f")

columns[magR.name] = magR

################################################################################

magI = Ev_track_column(name        = "magI",
                       description = "Absolute magnitude in the I band",
                       unit        = "",
                       log         = False)

magI.add_model_info("PARSEC_ISOC_1_2",
                     name = "I",
                     id = 12,
                     fmt = "%6.3f")

columns[magI.name] = magI

################################################################################

magJ = Ev_track_column(name        = "magJ",
                       description = "Absolute magnitude in the J band",
                       unit        = "",
                       log         = False)

magJ.add_model_info("PARSEC_ISOC_1_2",
                     name = "J",
                     id = 13,
                     fmt = "%6.3f")

columns[magJ.name] = magJ

################################################################################

magH = Ev_track_column(name        = "magH",
                       description = "Absolute magnitude in the H band",
                       unit        = "",
                       log         = False)

magH.add_model_info("PARSEC_ISOC_1_2",
                     name = "H",
                     id = 14,
                     fmt = "%6.3f")

columns[magH.name] = magH

################################################################################

magK = Ev_track_column(name        = "magK",
                       description = "Absolute magnitude in the U band",
                       unit        = "",
                       log         = False)

magK.add_model_info("PARSEC_ISOC_1_2",
                     name = "K",
                     id = 15,
                     fmt = "%6.3f")

columns[magK.name] = magK

################################################################################

int_IMF = Ev_track_column(name        = "int_IMF",
                          description = "",
                          unit        = "",
                          log         = False)

int_IMF.add_model_info("PARSEC_ISOC_1_2",
                       name = "int_IMF",
                       id = 16,
                       fmt = "%10.8f")

columns[int_IMF.name] = int_IMF

################################################################################

# \WARNING different track sets may use different phases definition.
# Use for the columns PARSEC_phase, MIST_phase, etc.

phase = Ev_track_column(name        = "phase",
                        description = "attributed evolutionary phase",
                        unit        = "",
                        log         = False)

phase.add_PARSEC_info(PARSEC_col_name = "PHASE",
                      PARSEC_col_id   = 23)

phase.add_model_info("PARSEC", name = "PHASE", id = 23)
phase.add_model_info("PARSEC_ISOC_1_2", name = "stage", id = -1)

columns[phase.name] = phase