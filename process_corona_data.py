
import os
import datetime
import time
import sys
import logging
import traceback
#import argparse
import configparser
import re
import codecs
import shutil
#import math
import random
import csv
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import colorama
from scipy.ndimage.filters import gaussian_filter1d
import zipfile
import tempfile
        

if __name__ == "__main__":
    I_AM_SCRIPT = True
    _me = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    _my_path = os.path.dirname(sys.argv[0])
else:
    I_AM_SCRIPT = False
    _my_path = os.path.dirname(__file__)
_my_path = os.path.realpath(_my_path)

log = None

_true_values = ("true", "yes", "1", "sure", "why_not")
_false_values = ("false", "no", "0", "nope", "no_way")

FORMAT_CSV = "csv"
FORMAT_PLOT = "plot"
FORMAT_XLSX = "xlsx"
_known_formats = (FORMAT_CSV,
                  FORMAT_PLOT,
                  FORMAT_XLSX)

TIMELINE_ORIGINAL = "original"
TIMELINE_TOTAL_CONFIRMED_CASES = "total_confirmed_cases"
TIMELINE_TOTAL_CONFIRMED_CASES_PER_1M = "total_confirmed_cases_per_1m"
TIMELINE_ACTIVE_CASES = "active_cases"
TIMELINE_FIRST_100_CASES = "first_100_cases"
TIMELINE_FIRST_CASE_PER_1M = "first_case_per_1m"
TIMELINE_FIRST_CASE_PER_10K = "first_case_per_10k"
TIMELINE_FIRST_CASE_PER_10M = "first_case_per_10m"
_known_timelines = (TIMELINE_ORIGINAL,
                    TIMELINE_TOTAL_CONFIRMED_CASES,
                    TIMELINE_TOTAL_CONFIRMED_CASES_PER_1M,
                    TIMELINE_ACTIVE_CASES,
                    TIMELINE_FIRST_100_CASES,
                    TIMELINE_FIRST_CASE_PER_10K,
                    TIMELINE_FIRST_CASE_PER_10M,
                    TIMELINE_FIRST_CASE_PER_1M)
_date_timelines = (TIMELINE_ORIGINAL,
                   )
_timeline_needs_population = (TIMELINE_FIRST_100_CASES,
                              TIMELINE_FIRST_CASE_PER_10K,
                              TIMELINE_FIRST_CASE_PER_10M,
                              TIMELINE_FIRST_CASE_PER_1M,
                              )

_float_timelines = (TIMELINE_TOTAL_CONFIRMED_CASES,
                    TIMELINE_TOTAL_CONFIRMED_CASES_PER_1M,
                    TIMELINE_ACTIVE_CASES,
                    TIMELINE_FIRST_100_CASES,
                    TIMELINE_FIRST_CASE_PER_10K,
                    TIMELINE_FIRST_CASE_PER_10M,
                    TIMELINE_FIRST_CASE_PER_1M)

LEGEND_LOCATION_BEST = "best"
_known_legend_locations = ("best","upper right","upper left","lower left","lower right","right","center left","center right","lower center","upper center","center")
 
DATA_TOTAL_CASES_PER_1M = "total_cases_per_1m"
DATA_TOTAL_CASES_PER_10K = "total_cases_per_10k"
DATA_TOTAL_CASES_PER_10M = "total_cases_per_10m"
DATA_TOTAL_CASES = "total_cases"
DATA_NEW_CASES = "new_cases"
DATA_NEW_CASES_PER_1M = "new_cases_per_1m"
DATA_TOTAL_DEATHS_PER_1M = "total_deaths_per_1m"
DATA_TOTAL_DEATHS = "total_deaths"
DATA_TOTAL_DEATHS_PER_1K_TOTAL_CASES = "total_deaths_per_1k_total_cases"
DATA_NEW_DEATHS_PER_1M = "new_deaths_per_1m"
DATA_NEW_DEATHS_PER_1K = "new_deaths_per_1k"
DATA_NEW_DEATHS = "new_deaths"
DATA_ACTIVE_CASES = "active_cases"
DATA_ACTIVE_CASES_PER_1M = "active_cases_per_1m"
DATA_ACTIVE_CASES_PER_1M_FROM_100_ACTIVE_CASES = "active_cases_per_1m_from_100_active_cases"
DATA_NEW_DEATHS_PER_ACTIVE_CASES = "new_deaths_per_active_cases"
DATA_NEW_DEATHS_PER_ACTIVE_CASES_FROM_1K_ACTIVE_CASES = "new_deaths_per_active_cases_from_1k_active_cases"
DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES = "new_deaths_per_1k_active_cases"
DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES_FROM_1K_ACTIVE_CASES = "new_deaths_per_1k_active_cases_from_1k_active_cases"
DATA_TOTAL_RECOVERED_PER_1M = "total_recovered_per_1m"
DATA_TOTAL_RECOVERED = "total_recovered"
DATA_PENDING_CASES = "pending_cases"
_known_data = (DATA_TOTAL_CASES,
               DATA_TOTAL_CASES_PER_10K,
               DATA_TOTAL_CASES_PER_10M,
               DATA_TOTAL_CASES_PER_1M,
               DATA_NEW_CASES,
               DATA_NEW_CASES_PER_1M,   
               DATA_TOTAL_DEATHS,
               DATA_TOTAL_DEATHS_PER_1K_TOTAL_CASES,
               DATA_TOTAL_DEATHS_PER_1M,
               DATA_NEW_DEATHS,
               DATA_NEW_DEATHS_PER_1M,
               DATA_NEW_DEATHS_PER_1K,
               DATA_ACTIVE_CASES,
               DATA_ACTIVE_CASES_PER_1M,
               DATA_ACTIVE_CASES_PER_1M_FROM_100_ACTIVE_CASES,
               DATA_NEW_DEATHS_PER_ACTIVE_CASES,
               DATA_NEW_DEATHS_PER_ACTIVE_CASES_FROM_1K_ACTIVE_CASES,
               DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES_FROM_1K_ACTIVE_CASES,
               DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES,
               DATA_TOTAL_RECOVERED_PER_1M,
               DATA_TOTAL_RECOVERED,
               DATA_PENDING_CASES,
               )
_data_requires_csd_source = (DATA_ACTIVE_CASES,
                             DATA_TOTAL_RECOVERED_PER_1M,
                             DATA_TOTAL_RECOVERED,
                             DATA_NEW_DEATHS_PER_ACTIVE_CASES,
                             DATA_NEW_DEATHS_PER_ACTIVE_CASES_FROM_1K_ACTIVE_CASES,
                             DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES_FROM_1K_ACTIVE_CASES,
                             DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES,
                             DATA_ACTIVE_CASES_PER_1M,
                             DATA_ACTIVE_CASES_PER_1M_FROM_100_ACTIVE_CASES,
                            )
_data_type_needs_population = (DATA_TOTAL_CASES_PER_1M, 
                               DATA_TOTAL_CASES_PER_10K, 
                               DATA_TOTAL_CASES_PER_10M,
                               DATA_NEW_CASES_PER_1M,
                               DATA_TOTAL_DEATHS_PER_1M,
                               DATA_NEW_DEATHS_PER_1M,
                               DATA_NEW_DEATHS_PER_1K,
                               DATA_ACTIVE_CASES_PER_1M,
                               DATA_ACTIVE_CASES_PER_1M_FROM_100_ACTIVE_CASES,
                               DATA_TOTAL_RECOVERED_PER_1M,
                               )

_data_source_en = "Data Source"
_data_source_sp = "Datos"
_generated_on_en = "Generated on"
_generated_on_sp = "Generado el"
_supressed_data_from_last_n_days_fmtr_en = "Supressed data from last %i days"
_supressed_data_from_last_n_days_fmtr_sp = "Datos de los últimos %i días suprimidos"
_active_cases_fmtr_sp = "Casos activos: Aquellos casos positivos que comenzaron a mostrar síntomas en los últimos %i días"
_active_cases_fmtr_en = "Active case: Those positive cases which started showing symptoms during the last %i days"
_github_url = "github.com/tonioluna/corona_graphs"

LANGUAGE_SP = "sp"
LANGUAGE_EN = "en"
_known_languages = (LANGUAGE_EN,
                    LANGUAGE_SP)

_timeline_display_names_sp = {TIMELINE_ORIGINAL:"Fecha",
                             TIMELINE_TOTAL_CONFIRMED_CASES:"Total de casos confirmados",
                             TIMELINE_TOTAL_CONFIRMED_CASES_PER_1M:"Total de casos confirmados / 1M Habs",
                             TIMELINE_ACTIVE_CASES:"Casos activos", 
                             TIMELINE_FIRST_100_CASES:"Dias (0 -> First 100 total cases)",
                             TIMELINE_FIRST_CASE_PER_10K:"Dias (0 -> Primer caso por 10K habs)",
                             TIMELINE_FIRST_CASE_PER_10M:"Dias (0 -> Primer caso por 10M habs)",
                             TIMELINE_FIRST_CASE_PER_1M:"Dias (0 -> Primer caso por 1M habs)",
                             }

_data_display_names_en = {DATA_TOTAL_CASES:"Total cases",
                          DATA_TOTAL_CASES_PER_10K:"Total cases / 10K Habs", 
                          DATA_TOTAL_CASES_PER_1M:"Total cases / 1M Habs",
                          DATA_TOTAL_CASES_PER_10M:"Total cases / 10M Habs",
                          DATA_NEW_CASES:"New cases per day",
                          DATA_NEW_CASES_PER_1M:"New cases per day / 1M Habs",
                          DATA_TOTAL_DEATHS:"Total deaths",
                          DATA_TOTAL_DEATHS_PER_1K_TOTAL_CASES:"Total deaths / 1K total cases",
                          DATA_TOTAL_DEATHS_PER_1M:"Total deaths / 1M Habs",
                          DATA_NEW_DEATHS:"New deaths per day",
                          DATA_NEW_DEATHS_PER_1M:"New deaths per day / 1M Habs",
                          DATA_NEW_DEATHS_PER_1K:"New deaths per day / 1K Habs",
                          DATA_NEW_DEATHS_PER_ACTIVE_CASES:"New deaths per day / Active Cases",
                          DATA_NEW_DEATHS_PER_ACTIVE_CASES_FROM_1K_ACTIVE_CASES:"New deaths per day / Active Cases\n(With 1K active cases or more)",
                          DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES_FROM_1K_ACTIVE_CASES:"New deaths per day / 1K Active Cases\n(With 1K active cases or more)",
                          DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES:"New deaths per day / 1K Active Cases",
                          DATA_ACTIVE_CASES:"Active Cases",
                          DATA_ACTIVE_CASES_PER_1M:"Active Cases / 1M Habs",
                          DATA_ACTIVE_CASES_PER_1M_FROM_100_ACTIVE_CASES:"Active Cases / 1M Habs\n(With 100 active cases or more)",
                          DATA_TOTAL_RECOVERED_PER_1M:"Recovered Cases / 1M Habs",
                          DATA_TOTAL_RECOVERED:"Recovered Cases",
                          DATA_PENDING_CASES:"Pending Result Cases"
                         }

_data_display_names_sp = {DATA_TOTAL_CASES:"Casos totales",
                          DATA_TOTAL_CASES_PER_10K:"Casos totales / 10K Habs", 
                          DATA_TOTAL_CASES_PER_1M:"Casos totales / 1M Habs",
                          DATA_TOTAL_CASES_PER_10M:"Casos totales / 10M Habs",
                          DATA_NEW_CASES:"Casos nuevos por día",
                          DATA_NEW_CASES_PER_1M:"Casos nuevos por día / 1M Habs",
                          DATA_TOTAL_DEATHS:"Muertes totales",
                          DATA_TOTAL_DEATHS_PER_1K_TOTAL_CASES:"Muertes totales / 1K total cases",
                          DATA_TOTAL_DEATHS_PER_1M:"Muertes totales / 1M Habs",
                          DATA_NEW_DEATHS:"Muertes nuevas por día",
                          DATA_NEW_DEATHS_PER_1M:"Muertes nuevas por día / 1M Habs",
                          DATA_NEW_DEATHS_PER_1K:"Muertes nuevas por día / 1K Habs",
                          DATA_NEW_DEATHS_PER_ACTIVE_CASES:"Muertes nuevas por día / Casos activos",
                          DATA_NEW_DEATHS_PER_ACTIVE_CASES_FROM_1K_ACTIVE_CASES:"Muertes nuevas por día / Casos activos\n(Con 1K casos de activos o más)",
                          DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES_FROM_1K_ACTIVE_CASES:"Muertes nuevas por día / 1K Casos activos\n(Con 1K de casos activos o más)",
                          DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES:"Muertes nuevas por día / 1K Casos activos",
                          DATA_ACTIVE_CASES:"Casos activos",
                          DATA_ACTIVE_CASES_PER_1M:"Casos activos / 1M Habs",
                          DATA_ACTIVE_CASES_PER_1M_FROM_100_ACTIVE_CASES:"Casos activos/ 1M Habs\n(Con 100 casos activos o más)",
                          DATA_TOTAL_RECOVERED_PER_1M:"Casos recuperados / 1M Habs",
                          DATA_TOTAL_RECOVERED:"Casos recuperados",
                          DATA_PENDING_CASES:"Casos con resultado pendiente"
                         }



FILTER_NONE = "none"
FILTER_TOP_MAX = "top_max"
FILTER_TOP_MIN = "top_min"
FILTER_TOP_MAX_MX = "top_max_mx"
FILTER_COUNTRY_LIST = "country_list"
FILTER_TOP_MAX_REGEX_MATCH = "top_max_regex_match"
FILTER_TOP_MAX_REBOUND_MATCH = "top_max_rebound_regex_match"
_known_filters = (FILTER_NONE,
                  FILTER_TOP_MAX,
                  FILTER_TOP_MIN,
                  FILTER_TOP_MAX_MX,
                  FILTER_COUNTRY_LIST,
                  FILTER_TOP_MAX_REGEX_MATCH,
                  FILTER_TOP_MAX_REBOUND_MATCH)
_filters_with_int_arg = (FILTER_TOP_MAX,
                         FILTER_TOP_MIN,
                         FILTER_TOP_MAX_MX)
_filters_with_string_list = (FILTER_COUNTRY_LIST,                       
                       )
_filters_with_regex_and_int = (FILTER_TOP_MAX_REBOUND_MATCH,
                               FILTER_TOP_MAX_REGEX_MATCH
                               )

COUNTRY_MX_X8 = "Mexico x8"
COUNTRY_MX = "Mexico"
_vip_countries = (COUNTRY_MX, COUNTRY_MX_X8)

PLOT_AXIS_FONT_SIZE = 8

PLOT_BAR_TICK_CLEANUP_SPLIT = "split"

PLOT_STYLE_LINE = "line"
PLOT_STYLE_MARKERS = "markers"
PLOT_STYLE_LAST_ENTRY_BARS = "last_entry_bars"
PLOT_STYLE_LAST_ENTRY_HBARS = "last_entry_hbars"
_known_plot_styles = (PLOT_STYLE_LINE,
                      PLOT_STYLE_MARKERS,
                      PLOT_STYLE_LAST_ENTRY_BARS,
                      PLOT_STYLE_LAST_ENTRY_HBARS,
                      )
_plot_styles_full_data_series = (PLOT_STYLE_LINE,
                                 PLOT_STYLE_MARKERS,
                                )
_plot_styles_last_entry_data = (PLOT_STYLE_LAST_ENTRY_BARS,
                                PLOT_STYLE_LAST_ENTRY_HBARS
                               )

PLOT_LINE_MARKERS_NONE = "none" 
PLOT_LINE_MARKERS_LAST_ONE = "last_one" 
PLOT_LINE_MARKERS_ALL = "all" 
_known_plot_line_markers = (PLOT_LINE_MARKERS_ALL,
                            PLOT_LINE_MARKERS_LAST_ONE,
                            PLOT_LINE_MARKERS_NONE)

PLOT_LINE_LEGEND_STYLE_STANDARD = "standard"
PLOT_LINE_LEGEND_STYLE_EOL_MARKER = "end_of_line_marker"
_known_plot_line_legend_styles = (PLOT_LINE_LEGEND_STYLE_EOL_MARKER,
                                  PLOT_LINE_LEGEND_STYLE_STANDARD)

PLOT_SCALE_LOG = "log"
PLOT_SCALE_LINEAR = "linear"
_known_plot_scales = (PLOT_SCALE_LINEAR,
                      PLOT_SCALE_LOG)

SORT_NONE = "none"
_known_sorts = (SORT_NONE,
                )

CONFIG_FILE = "reports.ini"

DATA_SOURCE_OURWORLDINDATA = "ourworldindata."
DATA_SOURCE_CSSEGISSANDATA = "CSSEGISandData"
DATA_SOURCE_COVID19MX = "covid19mx"

REPORT_TYPE_COUNTRIES = "countries"
REPORT_TYPE_MEXICO = "mexico"
REPORT_TYPE_MEXICO_MPIOS = "mexico_municipios"

_known_report_types = (REPORT_TYPE_COUNTRIES,
                       REPORT_TYPE_MEXICO,
                       REPORT_TYPE_MEXICO_MPIOS)

_known_data_sources = {REPORT_TYPE_COUNTRIES   :(DATA_SOURCE_OURWORLDINDATA,
                                                 DATA_SOURCE_CSSEGISSANDATA),
                       REPORT_TYPE_MEXICO      :(DATA_SOURCE_COVID19MX,),         
                       REPORT_TYPE_MEXICO_MPIOS:(DATA_SOURCE_COVID19MX,),               
                      }

DATA_SOURCE_TXT = {DATA_SOURCE_CSSEGISSANDATA : "John Hopkins University - https://github.com/CSSEGISandData/COVID-19",
                   DATA_SOURCE_OURWORLDINDATA : "Our World in Data - https://ourworldindata.org/coronavirus-source-data",
                   DATA_SOURCE_COVID19MX      : "https://www.covid19in.mx/ - https://github.com/mayrop/covid19mx"}

POPULATION_CSV_FILENAME = "population.csv"
POPULATION_CSV_HDR_COUNTRY = "Country"
POPULATION_CSV_HDR_POPULATION = "Population"

OWID_CORONA_CSV_FILENAME = "full_data.csv"
OWID_CORONA_CSV_HDR_DATE = "date"
OWID_CORONA_CSV_HDR_COUNTRY = "location"
OWID_CORONA_CSV_HDR_NEW_CASES = "new_cases"
OWID_CORONA_CSV_HDR_NEW_DEATHS = "new_deaths"
OWID_CORONA_CSV_HDR_TOTAL_CASES = "total_cases"
OWID_CORONA_CSV_HDR_TOTAL_DEATHS = "total_deaths"
_owid_corona_csv_required_cols = (OWID_CORONA_CSV_HDR_COUNTRY,
                             OWID_CORONA_CSV_HDR_DATE,
                             OWID_CORONA_CSV_HDR_NEW_CASES,
                             OWID_CORONA_CSV_HDR_NEW_DEATHS,
                             OWID_CORONA_CSV_HDR_TOTAL_CASES,
                             OWID_CORONA_CSV_HDR_TOTAL_DEATHS)

OWID_CoronaDayEntry = collections.namedtuple("OWID_CoronaDayEntry", ("total_deaths", "total_cases", "new_deaths", "new_cases"))
CSD_CoronaDayEntry = collections.namedtuple("CSD_CoronaDayEntry", ("total_deaths", "total_cases", "new_deaths", "new_cases", "total_recovered", "new_recovered"))

CSD_CORONA_CSV_DIRECTORY = os.path.join(_my_path, "..", "COVID-19", "csse_covid_19_data", "csse_covid_19_time_series")
CSD_CORONA_CSV_FILENAME_CONFIRMED = "time_series_covid19_confirmed_global.csv"
CSD_CORONA_CSV_FILENAME_DEATHS = "time_series_covid19_deaths_global.csv"
CSD_CORONA_CSV_FILENAME_RECOVERED = "time_series_covid19_recovered_global.csv"
CSD_CORONA_CSV_HDR_STATE = "Province/State"
CSD_CORONA_CSV_HDR_COUNTRY = "Country/Region"
CSD_CORONA_CSV_HDR_DATE_REGEX = re.compile("^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}$")


COVID19MX_DATA_TYPE_BY_STATES        = REPORT_TYPE_MEXICO
COVID19MX_DATA_TYPE_BY_MUNICIPES     = REPORT_TYPE_MEXICO_MPIOS

_known_covid19mx_data_type = (COVID19MX_DATA_TYPE_BY_STATES,
                              COVID19MX_DATA_TYPE_BY_MUNICIPES)     

COVID19MX_ACTIVE_CASE_DURATION_DAYS_DEFAULT = 14

COVID19MX_CATALOG_TYPE_SIMPLE = "simple"
COVID19MX_CATALOG_TYPE_MUNICIPIOS = "municipios"
COVID19MX_CATALOG_TYPE_ENTIDADES = "entidades"
# First column is the key column
COVID19MX_CATALOG_TYPE_HDR_COLS = { COVID19MX_CATALOG_TYPE_SIMPLE     : ("CLAVE","DESCRIPCION"),
                                    COVID19MX_CATALOG_TYPE_MUNICIPIOS : ("CLAVE_MUNICIPIO","MUNICIPIO","CLAVE_ENTIDAD"),
                                    COVID19MX_CATALOG_TYPE_ENTIDADES  : ("CLAVE_ENTIDAD","ENTIDAD_FEDERATIVA","ABREVIATURA")}

COVID19MX_CoronaDayEntry = collections.namedtuple("COVID19MX_CoronaDayEntry", ("total_deaths", "total_cases", "new_deaths", "new_cases", "active_cases", "pending_cases"))
COVID19MX_DIR_CATALOGS    = os.path.join(_my_path, "..", "covid19mx", "www", "abiertos", "catalogos")
COVID19MX_CATALOG_ENTIDADES     = "catalog_entidades"
COVID19MX_CATALOG_MUNICIPIOS    = "catalog_municipios"
COVID19MX_CATALOG_NACIONALIDAD  = "catalog_nacionalidad"
COVID19MX_CATALOG_ORIGEN        = "catalog_origen"
COVID19MX_CATALOG_RESULTADO     = "catalog_resultado"
COVID19MX_CATALOG_SECTOR        = "catalog_sector"
COVID19MX_CATALOG_SEXO          = "catalog_sexo"
COVID19MX_CATALOG_SI_NO         = "catalog_si_no" 
COVID19MX_CATALOG_TIPO_PACIENTE = "catalog_tipo_paciente"
COVID19MX_COL_DATE              = "col_date"
COVID19MX_COL_STATE             = "col_state"
COVID19MX_COL_MPIO_RES          = "col_mpio"
COVID19MX_COL_MPIO_RES_STATE_COL = "ENTIDAD_RES"
COVID19MX_CATALOG_FILENAMES = ((COVID19MX_CATALOG_ENTIDADES    , "entidades.csv",    COVID19MX_CATALOG_TYPE_ENTIDADES), 
                               (COVID19MX_CATALOG_MUNICIPIOS   , "municipios.csv",   COVID19MX_CATALOG_TYPE_MUNICIPIOS),
                               (COVID19MX_CATALOG_NACIONALIDAD , "nacionalidad.csv", COVID19MX_CATALOG_TYPE_SIMPLE),
                               (COVID19MX_CATALOG_ORIGEN       , "origen.csv",       COVID19MX_CATALOG_TYPE_SIMPLE),
                               (COVID19MX_CATALOG_RESULTADO    , "resultado.csv",    COVID19MX_CATALOG_TYPE_SIMPLE),
                               (COVID19MX_CATALOG_SECTOR       , "sector.csv",       COVID19MX_CATALOG_TYPE_SIMPLE),
                               (COVID19MX_CATALOG_SEXO         , "sexo.csv",         COVID19MX_CATALOG_TYPE_SIMPLE),
                               (COVID19MX_CATALOG_SI_NO        , "si_no.csv",        COVID19MX_CATALOG_TYPE_SIMPLE),
                               (COVID19MX_CATALOG_TIPO_PACIENTE, "tipo_paciente.csv",COVID19MX_CATALOG_TYPE_SIMPLE),)

COVID19MX_MUNICIPES_DATA_CSV  = os.path.join(_my_path, "..", "covid19mx", "www", "otros", "municipios.csv")
COVID19MX_MUNICIPES_DATA_COL_STATE_CODE     = "Clave_Entidad"
COVID19MX_MUNICIPES_DATA_COL_MUNICIPES_CODE = "Clave_Municipio"
COVID19MX_MUNICIPES_DATA_COL_NAME           = "Nombre"
COVID19MX_MUNICIPES_DATA_COL_FULL_NAME      = "Compossed_full_name"
COVID19MX_MUNICIPES_DATA_COL_POPULATION     = "Poblacion_2019"
COVID19MX_MUNICIPES_DATA_CSV_HDR_COLS = (COVID19MX_MUNICIPES_DATA_COL_STATE_CODE      ,
                                         COVID19MX_MUNICIPES_DATA_COL_MUNICIPES_CODE      ,
                                         COVID19MX_MUNICIPES_DATA_COL_NAME ,
                                         COVID19MX_MUNICIPES_DATA_COL_POPULATION    ,
                                        )
COVID19MX_MUNICIPES_DATA_CSV_HDR_COLS_INT = (COVID19MX_MUNICIPES_DATA_COL_STATE_CODE      ,
                                             COVID19MX_MUNICIPES_DATA_COL_MUNICIPES_CODE  ,
                                             COVID19MX_MUNICIPES_DATA_COL_POPULATION,
                                            )

COVID19MX_STATE_DATA_CSV  = os.path.join(_my_path, "..", "covid19mx", "www", "otros", "estados.csv")
COVID19MX_STATE_DATA_COL_CODE       = "Clave"
COVID19MX_STATE_DATA_COL_NAME       = "Nombre"
COVID19MX_STATE_DATA_COL_FULL_NAME  = "Nombre_Completo"
COVID19MX_STATE_DATA_COL_ABBREV     = "Abreviatura"
COVID19MX_STATE_DATA_COL_POPULATION = "Poblacion_2019"
COVID19MX_STATE_DATA_CSV_HDR_COLS = (COVID19MX_STATE_DATA_COL_CODE      ,
                                     COVID19MX_STATE_DATA_COL_NAME      ,
                                     COVID19MX_STATE_DATA_COL_FULL_NAME ,
                                     COVID19MX_STATE_DATA_COL_ABBREV    ,
                                     COVID19MX_STATE_DATA_COL_POPULATION,
                                    )
COVID19MX_STATE_DATA_CSV_HDR_COLS_INT = (COVID19MX_STATE_DATA_COL_CODE      ,
                                         COVID19MX_STATE_DATA_COL_POPULATION,
                                         )


COVID19MX_ALL_COUNTRY_TAG = "Pais Completo"

# Will duplicate ID and col_header, just in case one of those changes at some point
COVID19MX_COL_ENTRY = collections.namedtuple("Covid19MX_Column_Entry", ("ID", "col_header", "entry_type"))
COVID19MX_REGEX_MAIN_REPORT_MONTH_DIR = re.compile("^(?P<year>\d{4})(?P<month>\d{2})$")
COVID19MX_REGEX_MAIN_REPORT_DAY_FILE  = re.compile("^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})\.zip$")
COVID19MX_REGEX_MAIN_REPORT_DAY_FILE_CSV  = re.compile("^(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})\.csv$")
COVID19MX_DIR_MAIN_REPORT_DIR    = os.path.join(_my_path, "..", "covid19mx", "www", "abiertos", "todos")
COVID19MX_MAIN_REPORT_DATE_REGEX = re.compile("^(?P<year>\d{4})\-(?P<month>\d{2})\-(?P<day>\d{2})$")                    
COVID19MX_DIR_MAIN_REPORT_RESULTADO_POSITIVO = "Positivo SARS-CoV-2"
COVID19MX_DIR_MAIN_REPORT_RESULTADO_NEGATIVO = "No positivo SARS-CoV-2"
COVID19MX_DIR_MAIN_REPORT_RESULTADO_PENDIENTE = "Resultado pendiente"

# Won't use the state catalog to decode states, instead the data from the states sheet which is better
COVID19MX_DIR_MAIN_REPORT_COLS = (COVID19MX_COL_ENTRY("FECHA_ACTUALIZACION",     "FECHA_ACTUALIZACION",   COVID19MX_COL_DATE),
                                  COVID19MX_COL_ENTRY("ID_REGISTRO",             "ID_REGISTRO",           None),
                                  COVID19MX_COL_ENTRY("ORIGEN",                  "ORIGEN",                COVID19MX_CATALOG_ORIGEN),
                                  COVID19MX_COL_ENTRY("SECTOR",                  "SECTOR",                COVID19MX_CATALOG_SECTOR),
                                  COVID19MX_COL_ENTRY("ENTIDAD_UM",              "ENTIDAD_UM",            COVID19MX_COL_STATE),
                                  COVID19MX_COL_ENTRY("SEXO",                    "SEXO",                  COVID19MX_CATALOG_SEXO),
                                  COVID19MX_COL_ENTRY("ENTIDAD_NAC",             "ENTIDAD_NAC",           COVID19MX_COL_STATE),
                                  COVID19MX_COL_ENTRY("ENTIDAD_RES",             COVID19MX_COL_MPIO_RES_STATE_COL,  COVID19MX_COL_STATE),
                                  COVID19MX_COL_ENTRY("MUNICIPIO_RES",           "MUNICIPIO_RES",         COVID19MX_COL_MPIO_RES),
                                  COVID19MX_COL_ENTRY("TIPO_PACIENTE",           "TIPO_PACIENTE",         COVID19MX_CATALOG_TIPO_PACIENTE),
                                  COVID19MX_COL_ENTRY("FECHA_INGRESO",           "FECHA_INGRESO",         COVID19MX_COL_DATE),
                                  COVID19MX_COL_ENTRY("FECHA_SINTOMAS",          "FECHA_SINTOMAS",        COVID19MX_COL_DATE),
                                  COVID19MX_COL_ENTRY("FECHA_DEF",               "FECHA_DEF",             COVID19MX_COL_DATE),
                                  COVID19MX_COL_ENTRY("INTUBADO",                "INTUBADO",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("NEUMONIA",                "NEUMONIA",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("EDAD",                    "EDAD",                  None),
                                  COVID19MX_COL_ENTRY("NACIONALIDAD",            "NACIONALIDAD",          COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("EMBARAZO",                "EMBARAZO",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("HABLA_LENGUA_INDIG",      "HABLA_LENGUA_INDIG",    COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("DIABETES",                "DIABETES",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("EPOC",                    "EPOC",                  COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("ASMA",                    "ASMA",                  COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("INMUSUPR",                "INMUSUPR",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("HIPERTENSION",            "HIPERTENSION",          COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("OTRA_COM",                "OTRA_COM",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("CARDIOVASCULAR",          "CARDIOVASCULAR",        COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("OBESIDAD",                "OBESIDAD",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("RENAL_CRONICA",           "RENAL_CRONICA",         COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("TABAQUISMO",              "TABAQUISMO",            COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("OTRO_CASO",               "OTRO_CASO",             COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("RESULTADO",               "RESULTADO",             COVID19MX_CATALOG_RESULTADO),
                                  COVID19MX_COL_ENTRY("MIGRANTE",                "MIGRANTE",              COVID19MX_CATALOG_SI_NO),
                                  COVID19MX_COL_ENTRY("PAIS_NACIONALIDAD",       "PAIS_NACIONALIDAD",     None),
                                  COVID19MX_COL_ENTRY("PAIS_ORIGEN",             "PAIS_ORIGEN",           None),
                                  COVID19MX_COL_ENTRY("UCI",                     "UCI",                   COVID19MX_CATALOG_SI_NO),
                                 )
# Create the collection for each row entry
COVID19MX_MAIN_REPORT_ENTRY = collections.namedtuple("COVID19MX_MAIN_REPORT_ENTRY", [e.ID for e in COVID19MX_DIR_MAIN_REPORT_COLS])
COVID19MX_MAIN_REPORT_MAX_TOLERATED_ROW_ERRORS = 10

REPLACEMENTS_REGEX = re.compile("\@[a-zA-Z0-9_]+\@")

    
PLOT_DATA_MARGIN_LINEAR = 0.04
PLOT_DATA_MARGIN_LOG = 0.4
PLOT_EXTERNAL_FONT_COLOR = "#FFFFFF"
PLOT_EXTERNAL_FONT_COLOR_WARNING = "#FFC040"
PLOT_EXTERNAL_BG_COLOR = "#384048"
PLOT_GRID_COLOR = "#E0F0FF"
    
SEQUENCE_DATE_INCREMENTAL = "date_incremental"
SEQUENCE_COVID19MX_REPORT_ITERATION = "covid19mx_report_iteration"
_known_sequence_types = (SEQUENCE_DATE_INCREMENTAL,
                         SEQUENCE_COVID19MX_REPORT_ITERATION)
    
#_plot_line_styles = ((2, 2, 10, 2),  # 2pt line, 2pt break, 10pt line, 2pt break
#                     (1, 1,  5, 1),
#                     (2, 2,  4, 2),
#                     (1, 1,  2, 1),
#                     (1, 1,  1, 1),
#                     (2, 2,  2, 2),
#                     (4, 4,  4, 4),
#                     (8, 4,  8, 4),
#                     )
_plot_line_styles = ((1, 2, 6, 2),  # 2pt line, 2pt break, 10pt line, 2pt break
                     (3, 2, 6, 2),
                     (1, 2, 1, 2),
                     (3, 3, 3, 3),
                     #(8, 4, 8, 4),
                     )
_plot_line_markers = (".",
                      "^",
                      "v",
                      "1",
                      #"3",
                      "P",
                      "*",
                      "+",
                      "x",
                      "d",
                      )

SPECIAL_FLAG_ADD_MX_X8 = "ADD_MX_X8"

class SortedDate:
    def __init__(self, tag, year, month, day = None):
        self.tag = tag
        self.year = int(year)
        self.month = int(month)
        self.day = None if day == None else int(day)
        self.date = None 
        if self.day != None:
            self.date = time.mktime(time.strptime("%s/%s/%s"%(self.month, self.day, self.year), "%m/%d/%Y"))
        
    def __lt__(self, other):
        return self._cmp(other) < 0
    def __gt__(self, other):
        return self._cmp(other) > 0
    def __eq__(self, other):
        return self._cmp(other) == 0
    def __le__(self, other):
        return self._cmp(other) <= 0
    def __ge__(self, other):
        return self._cmp(other) >= 0
    def __ne__(self, other):
        return self._cmp(other) != 0
    def _cmp(self, other):
        assert (self.day != None and other.day != None) or (self.day == None and other.day == None), "Can't compare different types of dates"
        if self.year != other.year:
            return self.year - other.year
        if self.month != other.month:
            return self.month - other.month
        if self.day != other.day:
            return self.day - other.day
        return 0
            
def init_logger():
    global log
    
    log = logging.getLogger(_me)
    log.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    filename = _me + ".log"
    with open(filename, "w") as fh:
        fh.write("Starting on %s running from %s"%(time.ctime(), repr(sys.argv)))
    fh = logging.FileHandler(filename = filename,  encoding = "UTF-8")
    fh.setLevel(logging.DEBUG)
    
    
    # create formatter
    formatter = logging.Formatter('%(levelname)s - %(message)s')
    
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    
    log.addHandler(ch)
    log.addHandler(fh)
    
    colorama.init()

    log = LoggerWrapper(log)
    
    log.info("Started on %s at %s running under %s"%(time.ctime(), 
                                                     os.environ.get("COMPUTERNAME", "UNKNOWN_COMPUTER"),
                                                     os.environ.get("USERNAME", "UNKNOWN_USER"),))

class LoggerWrapper:
    
    def __init__(self, parent_logger):
        self._parent_logger = parent_logger

    def __getattr__(self, key):
        if key == "info":
            sys.stdout.write(colorama.Fore.RESET)
        elif key == "debug":
            sys.stdout.write(colorama.Fore.MAGENTA)
        elif key == "warning":
            sys.stdout.write(colorama.Fore.YELLOW)
        elif key == "error":
            sys.stdout.write(colorama.Fore.RED)
        return getattr(self._parent_logger, key)

class SpecialFlags:
    def __init__(self, str_val):
        self.add_mx_x8 = False

        if str_val == None:
            return
        
        for f in [s.strip().upper() for s in str_val.split(",")]:
            if f == SPECIAL_FLAG_ADD_MX_X8:
                self.add_mx_x8 = True
            else:
                raise Exception("Uknown special flag: %s"%(f,))
        
class Report:
    
    def __init__(self, params, section):
        self._read(params, section)
    
    def _read(self,
              params,
              section):
        self.ID = section[7:]
        
        self.filename_postfix = None
        
        #self.special_flags = SpecialFlags( params._get_option(section, "special_flags").strip() if params._has_option(section, "special_flags") else None
        
        if params._has_option(section, "template"):
            template = params._get_option(section, "template").strip()
            params._register_template_section(section, template)
        
        self.data_type = params._get_option(section, "data_type").strip()
        assert self.data_type in _known_data, "Unsupported data type: %s"%(self.data_type)

        self.timeline = params._get_option(section, "timeline").strip()
        assert self.timeline in _known_timelines, "Unsupported timeline: %s"%(self.timeline)

        self.formats = [s.strip() for s in params._get_option(section, "formats").split(",")]
        for format in self.formats:
            assert format in _known_formats, "Unsupported format: %s"%(format)
        
        self.filename = params._get_option(section, "filename").strip() if params._has_option(section, "filename") else "@AUTO"
        if self.filename == "@AUTO":
            self.filename = self.ID
        
        self.filter_sigma = float(params._get_option(section, "filter_sigma")) if params._has_option(section, "filter_sigma") else None
        self.axis2_filter_sigma = float(params._get_option(section, "axis2_filter_sigma")) if params._has_option(section, "axis2_filter_sigma") else None
        
        self.sort_columns = params._get_option(section, "sort_columns").strip()
        assert self.sort_columns in _known_sorts, "Unsupported sort_columns: %s"%(self.sort_columns)
        
        self.filter = params._get_option(section, "filter").strip()
        assert self.filter in _known_filters, "Unsupported filter type: %s"%(self.filter)
        
        self.filter_value = None
        if self.filter in _filters_with_int_arg or \
            self.filter in _filters_with_string_list or \
            self.filter in _filters_with_regex_and_int:
            
            arg = params._get_option(section, "filter_value").strip()
            if self.filter in _filters_with_int_arg:
                arg = int(arg)
            elif self.filter in _filters_with_string_list:
                arg = arg.replace("\\,", "__ESCAPED_COMMA__")
                arg = [s.strip().replace("__ESCAPED_COMMA__", ",") for s in arg.split(",")]
            elif self.filter in _filters_with_regex_and_int:
                s = [s.strip() for s in arg.split(" ")]
                regex = " ".join(s[:-1]).strip()
                val = int(s[-1].strip())
                regex = re.compile(regex) 
                arg = regex, val
            self.filter_value = arg
        
        if params._has_option(section, "plot_x_range"):
            rng = [s.strip() for s in params._get_option(section, "plot_x_range").strip().split(",")]
            assert len(rng) == 2, "plot_x_range must contain 2 items, not %i"%(len(rng))
            if self.timeline in _date_timelines:
                self.plot_x_range = [(time.mktime(time.strptime(d, "%y/%m/%d")) if d != "" else None) for d in rng]
            elif self.timeline in _float_timelines:
                self.plot_x_range = [(float(i) if i != "" else None) for i in rng]
            else:
                log.error("Don't know what type of range will be used on timeline of type %s"%(self.timeline))
        else:
            self.plot_x_range = None
            
        if params._has_option(section, "plot_y_range"):
            rng = [s.strip() for s in params._get_option(section, "plot_y_range").strip().split(",")]
            self.plot_y_range = [(float(i) if i != "" else None) for i in rng]
        else:
            self.plot_y_range = None
        
        self.data_plot_zeros = False if not params._has_option(section, "data_plot_zeros") else strToBool(params._get_option(section, "data_plot_zeros").strip())
        
        self.plot_title = None if not params._has_option(section, "plot_title") else params._get_option(section, "plot_title")
        self.plot_subtitle = None if not params._has_option(section, "plot_subtitle") else params._get_option(section, "plot_subtitle").replace("\\n","\n")
        
        if params._has_option(section, "exclude_countries"):
            exclude_countries = params._get_option(section, "exclude_countries")
            exclude_countries = [s.strip() for s in exclude_countries.split(',')]
            self.exclude_countries = exclude_countries
        else:
            self.exclude_countries = None
            
        self.legend_location = LEGEND_LOCATION_BEST if not params._has_option(section, "legend_location") else params._get_option(section, "legend_location").strip() 
        assert self.legend_location in _known_legend_locations, "Invalid value for legend_location: %s"%(self.legend_location)
        
        self.plot_bar_tick_cleanup = None
        if params._has_option(section, "plot_bar_tick_cleanup"):
            self.plot_bar_tick_cleanup = [i.strip() for i in params._get_option(section, "plot_bar_tick_cleanup").split(",")]
            if self.plot_bar_tick_cleanup[0] == PLOT_BAR_TICK_CLEANUP_SPLIT:
                assert len(self.plot_bar_tick_cleanup) == 2, "plot_bar_tick_cleanup = %s must be len 2"%PLOT_BAR_TICK_CLEANUP_SPLIT
                self.plot_bar_tick_cleanup[1] = int(self.plot_bar_tick_cleanup[1])
            else:
                raise Exception("Invalid plot_bar_tick_cleanup: %s"%(self.plot_bar_tick_cleanup[0], ))
        
        self.plot_style = PLOT_STYLE_LINE
        if params._has_option(section, "plot_style"):
            self.plot_style = params._get_option(section, "plot_style")
        assert self.plot_style in _known_plot_styles, "Invalid parameter plot_style: %s"%(self.plot_style, )

        self.plot_line_width = 0.75 if not params._has_option(section, "plot_line_width") else float(params._get_option(section, "plot_line_width"))
        self.axis2_plot_line_width = 0.75 if not params._has_option(section, "axis2_plot_line_width") else float(params._get_option(section, "axis2_plot_line_width"))
        self.plot_line_legend_style = PLOT_LINE_LEGEND_STYLE_STANDARD if not params._has_option(section, "plot_line_legend_style") else params._get_option(section, "plot_line_legend_style")
        assert self.plot_line_legend_style in _known_plot_line_legend_styles, "Invalid style for plot_line_legend_style: %s"%(self.plot_line_legend_style)
        self.plot_line_markers = PLOT_LINE_MARKERS_NONE if not params._has_option(section, "plot_line_markers") else params._get_option(section, "plot_line_markers")
        assert self.plot_line_markers in _known_plot_line_markers, "Invalid style for plot_line_markers: %s"%(self.plot_line_markers)
        self.legend_line_length = None if not params._has_option(section, "legend_line_length") else int(params._get_option(section, "legend_line_length"))
                
                
        self.plot_y_scale = PLOT_SCALE_LINEAR
        if params._has_option(section, "plot_y_scale"):
            self.plot_y_scale = params._get_option(section, "plot_y_scale")
        assert self.plot_y_scale in _known_plot_scales, "Invalid parameter plot_y_scale: %s"%(self.plot_y_scale, )
        
        self.plot_x_scale = PLOT_SCALE_LINEAR
        if params._has_option(section, "plot_x_scale"):
            self.plot_x_scale = params._get_option(section, "plot_y_scale")
        assert self.plot_x_scale in _known_plot_scales, "Invalid parameter plot_x_scale: %s"%(self.plot_x_scale, )
        
        
        # AXIS 2
        self.axis2_data_type = None
        if params._has_option(section, "axis2_data_type"):
            self.axis2_data_type = params._get_option(section, "axis2_data_type").strip()
            assert self.axis2_data_type in _known_data, "Unsupported axis2 data type: %s"%(self.axis2_data_type)

        if params._has_option(section, "axis2_plot_y_range"):
            rng = [s.strip() for s in params._get_option(section, "axis2_plot_y_range").strip().split(",")]
            self.axis2_plot_y_range = [(float(i) if i != "" else None) for i in rng]
        else:
            self.axis2_plot_y_range = None
        
        self.axis2_plot_style = PLOT_STYLE_LINE
        if params._has_option(section, "axis2_plot_style"):
            self.axis2_plot_style = params._get_option(section, "axis2_plot_style")
        assert self.axis2_plot_style in _known_plot_styles, "Invalid parameter axis2_plot_style: %s"%(self.axis2_plot_style, )
                
        self.axis2_plot_y_scale = PLOT_SCALE_LINEAR
        if params._has_option(section, "axis2_plot_y_scale"):
            self.axis2_plot_y_scale = params._get_option(section, "axis2_plot_y_scale")
        assert self.axis2_plot_y_scale in _known_plot_scales, "Invalid parameter plot_y_scale: %s"%(self.axis2_plot_y_scale, )
        
        self.sync_both_y_axis = False if not params._has_option(section, "sync_both_y_axis") else strToBool(params._get_option(section, "sync_both_y_axis"))
        
        self.sequence_do_export = False if not params._has_option(section, "sequence_do_export") else strToBool(params._get_option(section, "sequence_do_export"))
        if self.sequence_do_export:
            self.sequence_type = params._get_option(section, "sequence_type").strip()
            assert self.sequence_type in _known_sequence_types, "Unsupported sequence_type: %s"%(self.sequence_type)
            
            self.sequence_range = params._get_option(section, "sequence_range").strip()
            if self.sequence_type == SEQUENCE_DATE_INCREMENTAL:
                self.sequence_range = [RelativeDate(s.strip()) for s in self.sequence_range.split(",")]
                assert len(self.sequence_range) == 2, "sequence_range must be len 2, not %i"%(len(self.sequence_range))
            
            self.sequence_clone_last_frame = None if not params._has_option(section, "sequence_clone_last_frame") else int(params._get_option(section, "sequence_clone_last_frame"))
            
            self.sequence_do_postprocess = False if not params._has_option(section, "sequence_do_postprocess") else strToBool(params._get_option(section, "sequence_do_postprocess"))
            if self.sequence_do_postprocess:
                self.sequence_postprocess_command = params._get_option(section, "sequence_postprocess_command").strip()
        
class RelativeDate:
    def __init__(self, v):
        self._rel_date = None
        self._real_date = None
        if re.match("^\-{0,1}\d+$", v):
            self._rel_date = int(v)
        else:
            self._real_date = miau
        
class Parameters:
    def __init__(self, filenames):
        self._filenames = [os.path.realpath(file) for file in filenames]
        for file in self._filenames:
         assert os.path.isfile(file)   
        self.reports = []
        index = 0
        self._parsers = []
        self._replacements = {}
        self._templates = {}
        self._mapped_templates = {}
        self.population_name_xlation = None
        self.csd_country_xlation = None
        self.csd_state_xlation = None
        self.supress_last_n_days = None
        self.language = None
        self.covid19mx_active_case_duration_days = COVID19MX_ACTIVE_CASE_DURATION_DAYS_DEFAULT
        
        while True:
            if index >= len(self._filenames): 
                break
            self._read_file(self._filenames[index])
            index += 1
    
        assert self.report_type in _known_report_types, "Invalid report type: %s"%(self.report_type,)
        assert self.data_source in _known_data_sources[self.report_type], "Invalid data source %s for report type %s"%(self.data_source, repr(self.report_type))
        
    def _read_general_options(self, dir):
        if self._has_option("general", "report_type"):
            self.report_type = self._get_option("general", "report_type").strip()
            
        if self._has_option("general", "language"):
            self.language = self._get_option("general", "language").strip()
            assert self.language in _known_languages
            
        if self._has_option("general", "data_source"):
            self.data_source = self._get_option("general", "data_source").strip()
        
        if self._has_option("general", "supress_last_n_days"):
            self.supress_last_n_days = int(self._get_option("general", "supress_last_n_days").strip())
        
        if self._has_option("general", "covid19mx_active_case_duration_days"):
            self.covid19mx_active_case_duration_days = int(self._get_option("general", "covid19mx_active_case_duration_days").strip())
        
        # First read the general section so the includes are processed first
        if self._has_option("general", "report_dir"):
            self.report_dir = self._get_option("general", 'report_dir').strip()
        if self._has_option("general", "include_files"):
            files = [s.strip() for s in self._get_option("general", "include_files").split(",")]
            #print(repr(files))
            for file in files:
                if not os.path.isabs(file):
                    file = os.path.join(dir, file)
                file = os.path.relpath(file)
                if file not in self._filenames:
                    log.info("Including config file %s"%(file,))
                    #self._filenames.append(file)
                    self._read_file(file)
                else:
                    log.warning("Skipping already-included config file: %s"%(file, ))
    
    def _read_replacements(self):
        if not self._curr_parser().has_section("replacements"):
            return
        
        for option in self._curr_parser().options("replacements"):
            self._replacements[option] = self._curr_parser().get("replacements", option).strip()
        
    def _curr_parser(self):
        return self._parsers[-1]
        
    def _has_option(self, section, option):
        if self._curr_parser().has_option(section, option): return True
        if section in self._mapped_templates:
            return option in self._templates[self._mapped_templates[section]]
        return False
        
    def _get_option(self, section, option):
        p = self._curr_parser()
        if p.has_option(section, option):
            val = p.get(section, option).strip()
        elif section in self._mapped_templates and option in self._templates[self._mapped_templates[section]]:
            val =  self._templates[self._mapped_templates[section]][option].strip()
        else:
            raise Exception("Unable to read option %s:%s"%(section, option))
        log.debug("%s.%s -> %s"%(section, option, val))
        for rep in REPLACEMENTS_REGEX.findall(val):
            rep_name = rep[1:-1]
            if not rep_name in self._replacements:
                raise Exception("Replacement '%s' from %s.%s (at %s) does not exist"%(rep_name, section, option, p._filename))
            new_val = self._replacements[rep_name]
            val = val.replace(rep, new_val)
        log.debug("Final val: %s"%(val,))
        return val
    
    def _register_template_section(self, section, template):
        assert template in self._templates
        self._mapped_templates[section] = template
        
    def _read_templates(self):
        p = self._curr_parser()
        for section in p.sections():
            if section.startswith("template_"):
                template = section[9:]
                self._templates[template] = {}
                for option in p.options(section):
                    self._templates[template][option] = p.get(section, option)
    
    def _read_file(self, filename):
        #parser = configparser.RawConfigParser()
        parser = configparser.ConfigParser()
        log.debug("Reading parameters from %s"%(filename,))
        
        with codecs.open(filename, "r", "utf8") as fh:
            parser.read_file(fh)
            parser._filename = filename
        
        self._parsers.append(parser)
        
        # If available on this file, read replacements
        self._read_replacements()
        self._read_general_options(os.path.dirname(filename))
        self._read_templates()
        
        for section in self._curr_parser().sections():
            log.debug("Reading section %s"%(section, ))
            if section.startswith("report_"):
                self.reports.append(Report(self, section))
            elif section == "general":
                pass
            elif section == "population_name_translation":
                self._read_pop_name_xlation(section)
            elif section == "csd_country_translations":
                self._read_csd_country_xlation(section)
            else:
                log.warning("Don't know how to read section %s"%(repr(section),))
        
        self._parsers.pop()
        
    def _read_pop_name_xlation(self, section):
        self.population_name_xlation = {}
        v = self._get_option(section, "names")
        v = [s.strip() for s in v.split("\n")]
        for line in v:
            k, v = [s.strip() for s in line.split(":")]
            self.population_name_xlation[k] = v

    def _read_csd_country_xlation(self, section):
        self.csd_country_xlation = {}
        self.csd_state_xlation = {}
        v = self._get_option(section, "country_translations")
        v = [s.strip() for s in v.split("\n")]
        for line in v:
            k, v = [s.strip() for s in line.split(":")]
            self.csd_country_xlation[k] = v
        v = self._get_option(section, "state_translations")
        v = [s.strip() for s in v.split("\n")]
        for line in v:
            k, v = [s.strip() for s in line.split(":")]
            self.csd_state_xlation[k] = v
        #print(repr(self.population_name_xlation))
        
            
def strToBool(txt):
    txtl = txt.lower()
    if txtl in _true_values: return True
    if txtl in _false_values: return False
    raise Exception("Cannot convert %s to bool. Accepted values: (For True) %s, (For False) %s"
                    ""%(repr(txt), ",".join(_true_values), ",".join(_false_values),))
                   
class CoronaBaseData:
    def __init__(self, 
                 config_file, 
                 csv_filename = None, 
                 data_source = DATA_SOURCE_OURWORLDINDATA, 
                 report_type = REPORT_TYPE_COUNTRIES,
                 covid19mx_force_report = None):
        self.csv_filename = csv_filename
        self.config_file = config_file
        
        self.date_limit_min = None
        self.date_limit_top = None
        
        self.population = None
        if self.config_file.report_type == REPORT_TYPE_COUNTRIES:
            if self.config_file.data_source == DATA_SOURCE_OURWORLDINDATA:
                self._read_owid()
            elif self.config_file.data_source == DATA_SOURCE_CSSEGISSANDATA:
                self._read_csd()
            else:
                raise Exception("Uknown source: %s"%(self.config_file.data_source))
            population_data = self.read_population_data(population_name_xlation = self.config_file.population_name_xlation)
        elif self.config_file.report_type == REPORT_TYPE_MEXICO:
            population_data = self._read_covid19mx_state_data()
            self._read_covid19mx_municipes_data()
            if self.config_file.data_source == DATA_SOURCE_COVID19MX:
                self._read_covid19mx_data(data_type = COVID19MX_DATA_TYPE_BY_STATES, covid19mx_force_report = covid19mx_force_report)
            else:
                raise Exception("Uknown source: %s"%(self.config_file.data_source))
            
        elif self.config_file.report_type == REPORT_TYPE_MEXICO_MPIOS:
            self._read_covid19mx_state_data()
            population_data = self._read_covid19mx_municipes_data()
            if self.config_file.data_source == DATA_SOURCE_COVID19MX:
                self._read_covid19mx_data(data_type = COVID19MX_DATA_TYPE_BY_MUNICIPES, covid19mx_force_report = covid19mx_force_report)
            else:
                raise Exception("Uknown source: %s"%(self.config_file.data_source))
            
        else:
            raise Exception("Uknown report type: %s"%(self.config_file.report_type))
        
        if population_data != None:
            self.set_country_population(population_data)
        
    def read_population_data(self,
                             filename = None,
                             country_col = None,
                             population_col = None, 
                             population_name_xlation = None, 
                             special_flags = None):
        if filename == None:     filename = POPULATION_CSV_FILENAME
        if country_col == None:  country_col = POPULATION_CSV_HDR_COUNTRY
        if population_col == None:  population_col = POPULATION_CSV_HDR_POPULATION
        
        filename = os.path.abspath(filename)
        
        log.info("Reading contry population from %s"%(filename))
        
        assert os.path.isfile(filename), "Population file does not exist: %s"%(filename)
        
        data = {}
        
        with codecs.open(filename, "r", "utf8") as fh:
            reader = csv.reader(fh)
            # Read header
            hdr_row = next(reader)
            hdr_dict = {}
            for index, cell in enumerate(hdr_row):
                if cell == country_col:
                    hdr_dict[POPULATION_CSV_HDR_COUNTRY] = index
                    continue
                if cell == population_col:
                    hdr_dict[POPULATION_CSV_HDR_POPULATION] = index
                    continue
            assert len(hdr_dict) == 2, "Unable to get all header items %s, %s from %s"%(country_col, population_col, repr(hdr_row),)
            
            conflicted_countries = []
            for row in reader:
                con = row[hdr_dict[POPULATION_CSV_HDR_COUNTRY]]
                if population_name_xlation != None and con in population_name_xlation:
                    con = population_name_xlation[con]
                if con.find(",") != -1:
                    new_con = con.split(",")[0].strip()
                    log.debug("Adjusting country name from %s to %s"%(repr(con), repr(new_con)))
                    con = new_con
                pop_s = row[hdr_dict[POPULATION_CSV_HDR_POPULATION]]
                try:
                    pop = int(pop_s)
                except ValueError as ex:
                    log.warning("Population for %s is invalid: %s. Skipping country."%(con, repr(pop_s)))
                    continue
                if con in data:
                    log.warning("Duplicated country name, removing country from list: %s"%(con, ))
                    conflicted_countries.append(con)
                    data.pop(con)
                if con in conflicted_countries: continue
                data[con] = pop
                #if special_flags != None and special_flags.add_mx_x8 and con = COUNTRY_MX:
                if con == COUNTRY_MX:
                    data[COUNTRY_MX_X8] = pop
        
        return data

    def _read_covid19mx_municipes_data(self):
        # Population data, to return
        data = {}
        self.covid19mx_municipes_data = {}
        
        assert os.path.isfile(COVID19MX_MUNICIPES_DATA_CSV), "Municipe data file is missing: %s"%(COVID19MX_MUNICIPES_DATA_CSV,)
        
        log.info("Reading municipes data from %s"%(COVID19MX_MUNICIPES_DATA_CSV,))
        with codecs.open(COVID19MX_MUNICIPES_DATA_CSV, "r", "utf8") as fh:
            reader = csv.reader(fh)
            # Read header
            hdr_row = next(reader)
            hdr_dict = {}
            req_hdr_cols = COVID19MX_MUNICIPES_DATA_CSV_HDR_COLS
            
            for index, cell in enumerate(hdr_row):
                if cell in req_hdr_cols:
                    hdr_dict[cell] = index
                
            # Verify all items were read
            assert len(hdr_dict) == len(req_hdr_cols), "Unable to get all header items %s. Found: %s."%(repr(req_hdr_cols), repr(hdr_row),)
            
            state_pop = {}
            for k in [d[COVID19MX_STATE_DATA_COL_NAME] for d in self.covid19mx_state_data.values()]:
                state_pop[k] = 0
            
            total_population = 0
            rnum = 1
            for row in reader:
                rnum += 1
                
                d = {}
                for col in req_hdr_cols:
                    v = row[hdr_dict[col]]
                    if col in COVID19MX_MUNICIPES_DATA_CSV_HDR_COLS_INT:
                        try:
                            v = int(v)
                        except:
                            log.warning("Failed to convert to integer the value %s from row %i"%(v, rnum))
                            v = None
                    d[col] = v 
                
                # Need to format the code with a leading zero so it matches the other reports. Should I use integers instead?
                state_code = d[COVID19MX_MUNICIPES_DATA_COL_STATE_CODE]
                mpio_code =  d[COVID19MX_MUNICIPES_DATA_COL_MUNICIPES_CODE]
                
                self.covid19mx_municipes_data["%i_%i"%(mpio_code, state_code)] = d
                
                state_abbrev = self.covid19mx_state_data[state_code][COVID19MX_STATE_DATA_COL_ABBREV]
                state_name = self.covid19mx_state_data[state_code][COVID19MX_STATE_DATA_COL_NAME]
                full_mpio_name = "%s, %s"%(d[COVID19MX_MUNICIPES_DATA_COL_NAME], state_abbrev)
                
                d[COVID19MX_MUNICIPES_DATA_COL_FULL_NAME] = full_mpio_name
                
                pop = d[COVID19MX_MUNICIPES_DATA_COL_POPULATION]
                if pop == None:
                    log.warning("Population for %s is not available: %s"%(full_mpio_name, pop))
                    continue
                
                data[full_mpio_name] = pop
                state_pop[state_name] += pop
                total_population += pop
               
            for state, pop in state_pop.items():
                data[state] = pop    
            data[COVID19MX_ALL_COUNTRY_TAG] = total_population   
                
        log.debug("Municipe data has keys %s"%(repr(data.keys())))
                    
        return data    
    
    def _read_covid19mx_state_data(self):
        # Population data, to return
        data = {}
        self.covid19mx_state_data = {}
        
        assert os.path.isfile(COVID19MX_STATE_DATA_CSV), "State data file is missing: %s"%(COVID19MX_STATE_DATA_CSV,)
        
        log.info("Reading state data from %s"%(COVID19MX_STATE_DATA_CSV,))
        with codecs.open(COVID19MX_STATE_DATA_CSV, "r", "utf8") as fh:
            reader = csv.reader(fh)
            # Read header
            hdr_row = next(reader)
            hdr_dict = {}
            req_hdr_cols = COVID19MX_STATE_DATA_CSV_HDR_COLS
            
            for index, cell in enumerate(hdr_row):
                if cell in req_hdr_cols:
                    hdr_dict[cell] = index
                
            # Verify all items were read
            assert len(hdr_dict) == len(req_hdr_cols), "Unable to get all header items %s. Found: %s."%(repr(req_hdr_cols), repr(hdr_row),)
            
            total_population = 0
            rnum = 1
            for row in reader:
                rnum += 1
                
                d = {}
                for col in req_hdr_cols:
                    v = row[hdr_dict[col]]
                    if col in COVID19MX_STATE_DATA_CSV_HDR_COLS_INT:
                        try:
                            v = int(v)
                        except:
                            log.warning("Failed to convert to integer the value %s from row %i"%(v, rnum))
                            v = None
                    d[col] = v 
                
                # Need to format the code with a leading zero so it matches the other reports. Should I use integers instead?
                code = d[COVID19MX_STATE_DATA_COL_CODE]
                self.covid19mx_state_data[code] = d
                
                pop = int(d[COVID19MX_STATE_DATA_COL_POPULATION])
                data[d[COVID19MX_STATE_DATA_COL_NAME]] = pop
                
                total_population += pop
                   
            data[COVID19MX_ALL_COUNTRY_TAG] = total_population   
                
        log.debug("State data has keys %s"%(repr(data.keys())))
                    
        return data    
    
    def _read_covid19mx_data(self, data_type, covid19mx_force_report = None):
        assert data_type in _known_covid19mx_data_type
        doing_municipes = data_type == COVID19MX_DATA_TYPE_BY_MUNICIPES
        doing_states    = data_type == COVID19MX_DATA_TYPE_BY_STATES
        
        catalogs = self._read_covid19mx_catalogs()
        
        entries = self._read_covid19mx_entries(catalogs, covid19mx_force_report)
        
        # There's five parameters we could measure: Deaths, Positive, recovered, negative, total tested, pending
        # The reference dates for every data type:
        # Deaths: FECHA_DEF
        # Positive: FECHA_SINTOMAS
        # Recovered: Not supported just yet
        # Negative: FECHA_SINTOMAS
        # Tested: FECHA_SINTOMAS
        # Pending: FECHA_SINTOMAS
        
        # {state/country] = {date = count}}
        dicts = []
        deaths = {}
        positive = {}
        #recovered = {}
        negative = {}
        tested = {}
        pending = {}
        active = {}
        
        
        log.debug("Initializing data dictionaries")
        # get all the posible dates
        all_dates = []
        for e in entries:
            if e.FECHA_DEF != None and e.FECHA_DEF not in all_dates:
                all_dates.append(e.FECHA_DEF)
            if e.FECHA_SINTOMAS != None and e.FECHA_SINTOMAS not in all_dates:
                all_dates.append(e.FECHA_SINTOMAS)
        
        # Make sure all dates exist
        # Convert the dates to integer to simplity this
        all_dates = [int(d) for d in all_dates]
        
        min_date = min(all_dates)
        max_date = max(all_dates)
        d = min_date
        while d < max_date:
            if d not in all_dates:
                log.warning("Inserting missing date: %s"%(_format_date(d),))
                all_dates.append(d)
            d = _add_date_full_days(d, 1)
            
        # Back to float
        all_dates = [float(d) for d in all_dates]
        all_dates.sort()
        
        self.dates = []
        if self.config_file.supress_last_n_days != None:
            log.warning("Suppressing data from the last %i days"%(self.config_file.supress_last_n_days,))
            self.dates.extend(all_dates[:-self.config_file.supress_last_n_days])
        else:
            self.dates.extend(all_dates)
        
        log.debug("Dates to process: (%i) %s"%(len(all_dates), repr([_format_date(d) for d in all_dates])))
        
        if doing_municipes:
            #all_countries = [state[0] for state in catalogs[COVID19MX_CATALOG_ENTIDADES].values()]
            all_countries = [d[COVID19MX_MUNICIPES_DATA_COL_FULL_NAME] for d in self.covid19mx_municipes_data.values()]
            all_countries.sort()
            # Insert also all states
            all_states = [d[COVID19MX_STATE_DATA_COL_NAME] for d in self.covid19mx_state_data.values()]
            all_states.sort()
            all_countries.extend(all_states)
            # And the whole country
            all_countries.insert(0, COVID19MX_ALL_COUNTRY_TAG) 
        elif doing_states:
            all_countries = [d[COVID19MX_STATE_DATA_COL_NAME] for d in self.covid19mx_state_data.values()]
            all_countries.sort()
            all_countries.insert(0, COVID19MX_ALL_COUNTRY_TAG) 
        else:
            raise Exception("Internal error")
        
        log.debug("Countries/states/Municipes to process: (%i) %s"%(len(all_countries), repr(all_countries)))
            
        # Initialize all dictionaries
        dicts = [deaths, positive, negative, tested, pending, active]
        for d in dicts:
            #d["Mexico"] = {}
            #for state in catalogs[COVID19MX_CATALOG_ENTIDADES]:
            #    d[state[0]] = {}
            for country in all_countries:
                d[country] = {}
                for date in all_dates:
                    d[country][date] = 0
        
        log.info("Sorting data")
        
        for entry in entries:
            state = entry.ENTIDAD_RES
            municipe = entry.MUNICIPIO_RES
            if doing_municipes:
                if municipe == None: 
                    continue
                mpio_code ="%s_%s"%(municipe, state) 
            # Deaths
            if entry.FECHA_DEF != None:
                deaths[COVID19MX_ALL_COUNTRY_TAG][entry.FECHA_DEF] += 1
                deaths[state][entry.FECHA_DEF] += 1
                if doing_municipes:
                    deaths[municipe][entry.FECHA_DEF] += 1
            # Cases
            if entry.RESULTADO == COVID19MX_DIR_MAIN_REPORT_RESULTADO_POSITIVO:
                positive[COVID19MX_ALL_COUNTRY_TAG][entry.FECHA_SINTOMAS] += 1
                positive[state][entry.FECHA_SINTOMAS] += 1
                if doing_municipes:
                    positive[municipe][entry.FECHA_SINTOMAS] += 1
            # Negative
            if entry.RESULTADO == COVID19MX_DIR_MAIN_REPORT_RESULTADO_NEGATIVO:
                negative[COVID19MX_ALL_COUNTRY_TAG][entry.FECHA_SINTOMAS] += 1
                negative[state][entry.FECHA_SINTOMAS] += 1
                if doing_municipes:
                    negative[municipe][entry.FECHA_SINTOMAS] += 1
            # Pending
            if entry.RESULTADO == COVID19MX_DIR_MAIN_REPORT_RESULTADO_PENDIENTE:
                pending[COVID19MX_ALL_COUNTRY_TAG][entry.FECHA_SINTOMAS] += 1
                pending[state][entry.FECHA_SINTOMAS] += 1
                if doing_municipes:
                    pending[municipe][entry.FECHA_SINTOMAS] += 1
                    #if municipe.find("Zacapu") != -1:
                    #    print("")
                    #    print(entry)
                    #    print("(A) %s, %s"%(_format_date(entry.FECHA_SINTOMAS), pending[municipe][entry.FECHA_SINTOMAS]))

            # Tested
            tested[COVID19MX_ALL_COUNTRY_TAG][entry.FECHA_SINTOMAS] += 1
            tested[state][entry.FECHA_SINTOMAS] += 1
            if doing_municipes:
                tested[municipe][entry.FECHA_SINTOMAS] += 1
            # Active
        
        log.info("Building data statistics")
        
        
        last_total_deaths = {}
        last_total_positive = {}
        last_active_positive = {}
        last_pending = {}
        last_recovered = {}
        
        for d in [last_total_deaths, last_total_positive, last_active_positive, last_recovered, last_pending]:
            for c in all_countries:
                d[c] = 0
        
        self.data = {}
        
        
        update_period = random.randint(40,60)
        
        for cindex, country in enumerate(all_countries):
            if cindex % update_period == 0:
                sys.stdout.write(" " + country + "\r")
                sys.stdout.flush()
            
            self.data[country] = {}
            
            active_expiration_dates = {}
            pending_expiration_dates = {}
            for d in all_dates:
                active_expiration_dates[d] = 0
                pending_expiration_dates[d] = 0
            
            #dbg = False if country not in ("Panindícuaro, Mich.", "Puruándiro, Mich.") else True
            
            #if country.startswith("Jim"):
            #    print("%s, %s"%(country, country == "Jiménez, Mich."))
            
            #if dbg: log.debug("Statistics debug for: %s"%(country, ))
        
            for date in all_dates:
                #if dbg: log.debug("Date: %s"%(_format_date(date), ))
                # Total Deaths
                prev_val = last_total_deaths[country]
                if date in deaths[country]:
                    day_val = deaths[country][date]
                else:
                    day_val = 0
                entry_total_deaths = prev_val + day_val
                entry_new_deaths = day_val
                last_total_deaths[country] = entry_total_deaths
                
                # Positive Cases
                prev_val = last_total_positive[country]
                if date in positive[country]:
                    day_val = positive[country][date]
                else:
                    day_val = 0
                entry_total_cases = prev_val + day_val
                entry_new_cases = day_val
                last_total_positive[country] = entry_total_cases
                #if dbg: 
                #    log.debug("Positive cases")
                #    log.debug("              prev_val: %s"%(repr(prev_val), ))
                #    log.debug("              day_val: %s"%(repr(day_val), ))
                #    log.debug("    entry_total_cases: %s"%(repr(entry_total_cases), ))
                #    log.debug("      entry_new_cases: %s"%(repr(entry_new_cases), ))
                    
                
                # Active cases
                prev_val = last_active_positive[country]
                if date in positive[country]:
                    day_val = positive[country][date]
                    exp_date = _add_date_full_days(date, self.config_file.covid19mx_active_case_duration_days)
                    # if the date falls beyond the dates already-inserted then there's no need to register the expiration as that is after the report ends
                    if exp_date in active_expiration_dates:
                        active_expiration_dates[exp_date] += day_val 
                else:
                    day_val = 0
                entry_active_cases = prev_val + day_val - active_expiration_dates[date]
                entry_new_active = day_val
                last_active_positive[country] = entry_active_cases

                # Pending cases
                # Need to do the same as active, make them expire automatically. There's lots of pending cases which never got a result
                prev_val = last_pending[country]
                if date in pending[country]:
                    day_val = pending[country][date]
                    #if country.find("Zacapu") != -1 and day_val != 0:
                    #    print("(B) Day val %s, %i"%(_format_date(date), day_val))
                    
                    exp_date = _add_date_full_days(date, self.config_file.covid19mx_active_case_duration_days)
                    # if the date falls beyond the dates already-inserted then there's no need to register the expiration as that is after the report ends
                    if exp_date in pending_expiration_dates:
                        pending_expiration_dates[exp_date] += day_val 
                else:
                    day_val = 0
                entry_pending_cases = prev_val + day_val - pending_expiration_dates[date]
                entry_new_pending = day_val
                last_pending[country] = entry_pending_cases
                #if country.find("Zacapu") != -1:
                #    print("(C) %s, %i"%(_format_date(d), entry_pending_cases))
                
                # Recovered cases
                #prev_val = last_recovered[country]
                #if date in positive[country]:
                #    day_val = positive[country][date]
                #else:
                #    day_val = 0
                #entry_total_recovered = prev_val + day_val
                #entry_new_recovered = day_val
                #last_recovered[country] = entry_total_cases
                
                
                #CONTINUEHERE, active cases. Need to set an expiration date for active cases, or better said, create a dictionary of negative cases to add 
                # into the mix int he future. Maybe make sure the date range includes all days in order to make stuff easier.
                
                #COVID19MX_CoronaDayEntry = collections.namedtuple("COVID19MX_CoronaDayEntry", ("total_deaths", "total_cases", "new_deaths", "new_cases", "active_cases", "pending_cases"))
        
                e = COVID19MX_CoronaDayEntry(entry_total_deaths, entry_total_cases, entry_new_deaths, entry_new_cases, entry_active_cases, entry_pending_cases)
                #if country.find("Zacapu") != -1:
                #    print("(D) %s"%(e, ))
                self.data[country][date] = e
                
    
        
    def _read_covid19mx_entries(self, catalogs, covid19mx_force_report = None):
        filename = self._get_covid19mx_main_report(covid19mx_force_report)
        
        # Create a dictionary of catalog types
        catalog_types = {}
        for id, file, cat_type in COVID19MX_CATALOG_FILENAMES:
            catalog_types[id] = cat_type
        
        entries = []
        
        i = None
        b, e = os.path.splitext(os.path.basename(filename))
        while True:
            processed_csv = "covid19mx.%s.processed%s%s"%(b, "" if i == None else ".%i"%(i),  e)
            if not os.path.exists(processed_csv):
                break
            if i == None:
                i = 2
            else:
                i += 1
        
        log.info("Writting processed CSV to %s"%(processed_csv,))
        
        with open(processed_csv, "w", newline="") as fho:
            writer = csv.writer(fho)
            hdr = [e.ID for e in COVID19MX_DIR_MAIN_REPORT_COLS]
            writer.writerow(hdr)
        
            log.info("Reading main report file from %s"%(filename,))
            with codecs.open(filename, "r", "utf8", "ignore") as fh:
                reader = csv.reader(fh)
                # Read header
                hdr_row = next(reader)
                hdr_dict = {}
                req_hdr_cols = [e.col_header for e in COVID19MX_DIR_MAIN_REPORT_COLS]
                
                for index, cell in enumerate(hdr_row):
                    if cell in req_hdr_cols:
                        hdr_dict[cell] = index
                    else:
                        log.warning("Uknown hdr entry at col %i under catalog %s: %s"%(index, cat_id, ffilename))
                
                # Verify all items were read
                assert len(hdr_dict) == len(req_hdr_cols), "At catalog %s/%s, unable to get all header items %s from %s"%(cat_id, ffilename, repr(req_hdr_cols), repr(hdr_row),)
                
                date_first = True
                
                row_errors = 0
                rnum = 1
                try:
                    
                    for row in reader:
                        rnum += 1
                        
                        if rnum % 1000 == 0:
                            sys.stdout.write(" At row %iK\r"%(rnum/1000, ))
                            sys.stdout.flush()
                        
                        entry_values = []
                    
                        for known_col in COVID19MX_DIR_MAIN_REPORT_COLS:
                            raw_val = row[hdr_dict[known_col.col_header]]
                            try:
                                if known_col.entry_type == None:
                                    val = raw_val
                                elif known_col.entry_type == COVID19MX_COL_DATE:
                                    m = COVID19MX_MAIN_REPORT_DATE_REGEX.match(raw_val)
                                    if m == None:
                                        log.warning("Invalid date at row %i, col %s: %s"%(rnum, known_col, raw_val))
                                        val = None
                                    else:
                                        g = m.groupdict()
                                        y = int(g["year"])
                                        m = int(g["month"])
                                        d = int(g["day"])
                                        if y == 9999 and m == 99 and d == 99:
                                            val = None
                                        elif y < 2020:
                                            log.warning("Skipping too-early date: %s"%(raw_val,))
                                            val = None
                                        else:
                                            val = time.mktime(time.strptime(raw_val, "%Y-%m-%d"))
                                elif known_col.entry_type == COVID19MX_COL_STATE:
                                    try:
                                        iraw_val = int(raw_val)
                                    except Exception as ex:
                                        raise Exception("Cannot convert %s to integer as expected for column %s on row %i"%(raw_val, known_col.ID, rnum))
                                    if iraw_val in self.covid19mx_state_data:
                                        val = self.covid19mx_state_data[iraw_val][COVID19MX_STATE_DATA_COL_NAME]
                                    else:
                                        #log.warning("Unknown state %s at row %i from state data sheet, falling back to entities catalog"%(repr(raw_val), rnum))
                                        # Check if the state is on the state catalog
                                        val = catalogs[COVID19MX_CATALOG_ENTIDADES][raw_val][0]
                                        #raise Exception("Not sure how to read data from the municipes catalog. This is only the fallback path so it is probably not rerquired. Faile state key is %s"%(iraw_val,))
                                elif known_col.entry_type == COVID19MX_COL_MPIO_RES:
                                    try:
                                        iraw_val = int(raw_val)
                                    except Exception as ex:
                                        raise Exception("Cannot convert %s to integer as expected for column %s on row %i"%(raw_val, known_col.ID, rnum))
                                    mpio_code = iraw_val
                                    # Get the state code. It should be from the residency state
                                    state_code = row[hdr_dict[COVID19MX_COL_MPIO_RES_STATE_COL]]
                                    try:
                                        state_code = int(state_code)
                                    except Exception as ex:
                                        raise Exception("Cannot convert %s to integer as expected for column %s on row %i"%(state_code, COVID19MX_COL_MPIO_RES_STATE_COL, rnum))
                                    
                                    key = "%i_%i"%(mpio_code, state_code)
                                    
                                    if key in self.covid19mx_municipes_data:
                                        val = self.covid19mx_municipes_data[key][COVID19MX_MUNICIPES_DATA_COL_FULL_NAME]
                                    else:
                                        if mpio_code not in (99, 999):
                                            log.warning("Invalid residency municipe code %s (mpio, state) at row %i."%(key, rnum))
                                        val = None
                                        #log.warning("Unknown state %s at row %i from state data sheet, falling back to entities catalog"%(repr(raw_val), rnum))
                                        # Check if the state is on the state catalog
                                        #val = catalogs[COVID19MX_CATALOG_MUNICIPIOS][entity_code][0]
                                        #raise Exception("Not sure how to read data from the municipes catalog. This is only the fallback path so it is probably not rerquired. Faile mpio key is %s"%(key,))
                                elif known_col.entry_type in catalogs:
                                    catalog_type = catalog_types[known_col.entry_type]
                                    catalog = catalogs[known_col.entry_type]
                                    
                                    decoded_vals = catalog.get(raw_val, None)
                                    if decoded_vals == None:
                                        val = "<%s>"%(raw_val)
                                    else:
                                        if catalog_type == COVID19MX_CATALOG_TYPE_SIMPLE:
                                            val = decoded_vals[0]
                                        # These have been replaced to fetch data from the population sheets. If needed, the code below will need updates
                                        #elif catalog_type == COVID19MX_CATALOG_TYPE_ENTIDADES:
                                        #    val = decoded_vals[0]
                                        #elif catalog_type == COVID19MX_CATALOG_TYPE_MUNICIPIOS:
                                        #    mpio = decoded_vals[0]
                                        #    entity_code = decoded_vals[1]
                                        #    # Index 1 of entitys, is the entity abbreviation
                                        #    #entity_abbrev = catalogs[COVID19MX_CATALOG_ENTIDADES][entity_code][1]
                                        #    entity_abbrev = self.covid19mx_state_data[entity_code][COVID19MX_STATE_DATA_COL_ABBREV] if entity_code in self.covid19mx_state_data else catalogs[COVID19MX_CATALOG_ENTIDADES][entity_code][1]
                                        #    val = "%s, %s"%(mpio, entity_abbrev)
                                        else:
                                            raise Exception("Internal error: Unknown catalog type: %s"%(catalog_type))
                                
                                entry_values.append(val)
                            except Exception as ex:
                                log.error("Failed to read COVID19MX main data sheet %s at row %i, column %s with value %s: %s"
                                          ""%(filename, rnum, known_col.ID, raw_val, ex))
                                log.debug(traceback.format_exc())
                                row_errors += 1
                                if row_errors > COVID19MX_MAIN_REPORT_MAX_TOLERATED_ROW_ERRORS:
                                    raise Exception("Failed to ready COVID19MX main data sheet, exceeded number of errors")
                                
                                entry_values = None
                                break
                        
                        if entry_values != None:
                            e = COVID19MX_MAIN_REPORT_ENTRY(*entry_values) 
                            entries.append(e)
                            
                            orow = []
                            for he, ee in zip(hdr, e):
                                if he.find("FECHA") != -1:
                                    orow.append(_format_date(ee) if ee != None else "")
                                else:
                                    orow.append(ee)       
                            writer.writerow(orow)
                
                except Exception as ex:
                        log.error("Failed to read COVID19MX main data sheet %s at row %i: %s"%(filename, rnum, ex))
                        log.info("Last read entry: %s"%("None" if len(entries) == 0 else repr(entries[-1])))
                        log.debug(traceback.format_exc())
                        raise Exception("Failed to ready COVID19MX main data sheet")
            
        log.info("Read %i MX COVID19 entries"%(len(entries)))
             
        return entries            
        
    def _get_covid19mx_main_report(self, covid19mx_force_report = None):
        latest_day_file = covid19mx_force_report if covid19mx_force_report != None else os.path.realpath(_get_covid19mx_reports()[-1].tag)
        log.info("MX COVID 19 data file: %s"%(latest_day_file, ))

        tmp_dir = tempfile.TemporaryDirectory(prefix = "covid19mx_").name
        
        log.debug("Extracting %s to %s"%(latest_day_file, tmp_dir))
        
        with zipfile.ZipFile(latest_day_file, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)
        
        files = os.listdir(tmp_dir)
        matches = []
        for f in files:
            if COVID19MX_REGEX_MAIN_REPORT_DAY_FILE_CSV.match(f):
                matches.append(f)
        assert len(matches) == 1, "Expected 1 csv matched file out of the zip file, found %i: %s (out of %s)"%(len(matches), repr(matches), repr(files))
        
        return os.path.join(tmp_dir, files[0])
    
    def _read_covid19mx_catalogs(self):
        catalogs = {}
        for cat_id, filename, cat_type  in COVID19MX_CATALOG_FILENAMES:
            ffilename = os.path.realpath(os.path.join(COVID19MX_DIR_CATALOGS, filename))
            assert os.path.isfile(ffilename), "File for catalog %s is missing: %s"%(cat_id, ffilename)
            
            catalog = {}
            catalogs[cat_id] = catalog
            
            log.info("Reading catalog %s"%(ffilename,))
            with codecs.open(ffilename, "r", "utf8") as fh:
                reader = csv.reader(fh)
                # Read header
                hdr_row = next(reader)
                hdr_dict = {}
                req_hdr_cols = COVID19MX_CATALOG_TYPE_HDR_COLS[cat_type]
                
                for index, cell in enumerate(hdr_row):
                    if cell in req_hdr_cols:
                        hdr_dict[cell] = index
                    else:
                        log.warning("Uknown hdr entry at col %i under catalog %s: %s"%(index, cat_id, ffilename))
                
                # Verify all items were read
                assert len(hdr_dict) == len(req_hdr_cols), "At catalog %s/%s, unable to get all header items %s from %s"%(cat_id, ffilename, repr(req_hdr_cols), repr(hdr_row),)
                
                rnum = 1
                for row in reader:
                    rnum += 1
                    #for col, index in hdr_dict.items():
                    #    catalog[col] = row[index]
                    
                    # First col at req_hdr_cols/COVID19MX_CATALOG_TYPE_HDR_COLS is the header 
                    key_col = row[hdr_dict[req_hdr_cols[0]]]
                    vals = []
                    
                    for col in req_hdr_cols[1:]:
                        vals.append(row[hdr_dict[col]])
                    
                    catalog[key_col] = vals
            
            log.debug("Catalog %s has keys %s"%(cat_id, repr(catalog.keys())))
                    
        return catalogs       
                        
            
    
    def _read_csd(self):
        # Worry about how to receive the filename later
        assert self.csv_filename == None
        assert os.path.isdir(CSD_CORONA_CSV_DIRECTORY), "CSD data source directory does not exist at %s. Did you get the repo from https://github.com/CSSEGISandData/COVID-19?"%(CSD_CORONA_CSV_DIRECTORY,)
            
        self.csv_filename_confirmed = os.path.join(CSD_CORONA_CSV_DIRECTORY, CSD_CORONA_CSV_FILENAME_CONFIRMED)
        self.csv_filename_recovered = os.path.join(CSD_CORONA_CSV_DIRECTORY, CSD_CORONA_CSV_FILENAME_RECOVERED)
        self.csv_filename_deaths = os.path.join(CSD_CORONA_CSV_DIRECTORY, CSD_CORONA_CSV_FILENAME_DEATHS)
        
        assert os.path.isfile(self.csv_filename_confirmed), "CSD data source (confirmed) does not exist at %s. Did you get the repo from https://github.com/CSSEGISandData/COVID-19?"%(self.csv_filename_confirmed,)
        assert os.path.isfile(self.csv_filename_recovered), "CSD data source (recovered) does not exist at %s. Did you get the repo from https://github.com/CSSEGISandData/COVID-19?"%(self.csv_filename_recovered,)
        assert os.path.isfile(self.csv_filename_deaths),    "CSD data source (deaths) does not exist at %s. Did you get the repo from https://github.com/CSSEGISandData/COVID-19?"%(self.csv_filename_deaths,)
        
        data_confirmed, dates1 = self._read_csd_csv_file(self.csv_filename_confirmed)
        data_recovered, dates2 = self._read_csd_csv_file(self.csv_filename_recovered)
        data_deaths   , dates3 = self._read_csd_csv_file(self.csv_filename_deaths)
        
        self.dates = []
        for date_list in (dates1, dates2, dates3):
            for d in date_list:
                if d not in self.dates: 
                    self.dates.append(d)
        self.dates.sort()
        if self.config_file.supress_last_n_days != None:
            log.warning("Suppressing data from the last %i days"%(self.config_file.supress_last_n_days,))
            self.dates = self.dates[:-self.config_file.supress_last_n_days]
        
        countries = []
        for data_dict in (data_confirmed, data_recovered, data_deaths):
            for c in data_dict.keys():
                if c not in countries:
                    countries.append(c)
        
        countries.sort()
        self.data = {}
            
            
        for country in countries:
            prev_confirmed = 0
            prev_recovered = 0
            prev_deaths = 0
            
            self.data[country] = {}
            if country == COUNTRY_MX:
                self.data[COUNTRY_MX_X8] = {}

            for date in self.dates:
                confirmed = data_confirmed.get(country, {}).get(date, prev_confirmed)
                recovered = data_recovered.get(country, {}).get(date, prev_recovered)
                deaths = data_deaths.get(country, {}).get(date, prev_deaths)
                                
                total_deaths    = deaths 
                new_deaths      = deaths - prev_deaths
                total_cases     = confirmed
                new_cases       = confirmed - prev_confirmed
                total_recovered = recovered
                new_recovered   = recovered - prev_recovered
                
                e = CSD_CoronaDayEntry(total_deaths, total_cases, new_deaths, new_cases, total_recovered, new_recovered)
                self.data[country][date] = e
                #if country == COUNTRY_MX:
                #    e2 = CSD_CoronaDayEntry(total_deaths*8, total_cases*20, new_deaths*8, new_cases*8, total_recovered*8, new_recovered*8)
                #    self.data[COUNTRY_MX_X8][date] = e2
                
                prev_confirmed = confirmed
                prev_recovered = recovered
                prev_deaths = deaths
        
        log.info("Read %i entries from %s to %s"%(len(self.dates), 
                                          _format_date(min(self.dates))  ,
                                          _format_date(max(self.dates))  ))
        
    def _read_csd_csv_file(self, filename):
    
        log.info("Reading partial CSD corona data from %s"%(filename))
        
        with codecs.open(filename, "r", "utf8") as fh:
            reader = csv.reader(fh)
            # Read header
            hdr_row = next(reader)
            hdr_dict = {}
            
            state_hdr_index = None
            country_hdr_index = None
            date_indexes = {}
            for index, cell in enumerate(hdr_row):
                if cell == CSD_CORONA_CSV_HDR_COUNTRY:
                    country_hdr_index = index
                elif cell == CSD_CORONA_CSV_HDR_STATE:
                    state_hdr_index = index
                elif CSD_CORONA_CSV_HDR_DATE_REGEX.match(cell) != None:
                    date = time.mktime(time.strptime(cell, "%m/%d/%y"))
                    date_indexes[index] = date
                else:
                    log.warning("Unknown header item at col %i: %s"%(index, cell, ))
                
            assert state_hdr_index != None and country_hdr_index != None, "" +\
                "Unable to get all header items"
            
            data = {}
            
            rnum = 1
            for row in reader:
                rnum += 1
                try:
                    country = row[country_hdr_index]
                    state = row[state_hdr_index]
                    
                    # first do xlation on states
                    country_state = "%s.%s"%(country, state)
                    if country_state in self.config_file.csd_state_xlation:
                        country = self.config_file.csd_state_xlation[country_state]
                    # Then do country xlation
                    if country in self.config_file.csd_country_xlation:
                        country = self.config_file.csd_country_xlation[country]
                    
                    if country not in data:
                        data[country] = {}
                        if country == COUNTRY_MX:
                            data[COUNTRY_MX_X8] = {}
                    
                    for index, date in date_indexes.items():
                        try:
                            num = int(row[index])
                        except ValueError as ex:
                            log.debug("Invalid value for date %s (col %i) at %s/%s (row %i): %s (%s)"
                                        ""%(_format_date(date),
                                            index,
                                            state,
                                            country,
                                            rnum,
                                            repr(row[index]),
                                            ex
                                            ))
                            continue
                        # Do this so countries which take multiple rows can be added
                        data[country][date] = num + data[country].get(date, 0)
                        if country == COUNTRY_MX:
                            data[COUNTRY_MX_X8][date] = data[country][date] * 8
                    
                except Exception as ex:
                    raise Exception("Failed to process data at row %i: %s"%(rnum, ex))
            
            dates = list(date_indexes.values())
            dates.sort()
            
            log.info("Read %i contries/states from %s to %s"%(rnum - 1, 
                                                              _format_date(min(dates))  ,
                                                              _format_date(max(dates))  ))
            
            return data, dates
    
    
    def _read_owid(self):
        if self.csv_filename == None:
            self.csv_filename = OWID_CORONA_CSV_FILENAME
        self.csv_filename = os.path.abspath(self.csv_filename)
    
        log.info("Reading corona data from %s"%(self.csv_filename))
        
        with codecs.open(self.csv_filename, "r", "utf8") as fh:
            reader = csv.reader(fh)
            # Read header
            hdr_row = next(reader)
            hdr_dict = {}
            for index, cell in enumerate(hdr_row):
                if cell in _owid_corona_csv_required_cols:
                    assert cell not in hdr_dict, "Duplicated header entry: %s"%(cell,)
                    hdr_dict[cell] = index
            assert len(hdr_dict) == len(_owid_corona_csv_required_cols), "Unable to get all header items %s from %s"%(repr(_owid_corona_csv_required_cols), repr(hdr_row),)
            
            self.data = {}
            self.dates = []
            
            rnum = 1
            for row in reader:
                rnum += 1
                try:
                    country = row[hdr_dict[OWID_CORONA_CSV_HDR_COUNTRY]]
                    if country not in self.data:
                        self.data[country] = {}
                    date_s = row[hdr_dict[OWID_CORONA_CSV_HDR_DATE]]
                    date = time.mktime(time.strptime(date_s, "%Y-%m-%d"))
                    if date not in self.dates:
                        self.dates.append(date)
                    
                    total_deaths = int(row[hdr_dict[OWID_CORONA_CSV_HDR_TOTAL_DEATHS]]) if row[hdr_dict[OWID_CORONA_CSV_HDR_TOTAL_DEATHS]] != "" else 0 
                    total_cases  = int(row[hdr_dict[OWID_CORONA_CSV_HDR_TOTAL_CASES]])  if row[hdr_dict[OWID_CORONA_CSV_HDR_TOTAL_CASES]]  != "" else 0
                    new_deaths   = int(row[hdr_dict[OWID_CORONA_CSV_HDR_NEW_DEATHS]])   if row[hdr_dict[OWID_CORONA_CSV_HDR_NEW_DEATHS]]   != "" else 0
                    new_cases    = int(row[hdr_dict[OWID_CORONA_CSV_HDR_NEW_CASES]])    if row[hdr_dict[OWID_CORONA_CSV_HDR_NEW_CASES]]    != "" else 0
                    
                    e = OWID_CoronaDayEntry(total_deaths, total_cases, new_deaths, new_cases)
                    self.data[country][date] = e
                except Exception as ex:
                    raise Exception("Failed to process data at row %i: %s"%(rnum, ex))
            
            self.dates.sort()
            if self.config_file.supress_last_n_days != None:
                log.warning("Suppressing data from the last %i days"%(self.config_file.supress_last_n_days,))
                self.dates = self.dates[:-self.config_file.supress_last_n_days]
            
            log.info("Read %i entries from %s to %s"%(rnum - 1, 
                                                      _format_date(min(self.dates))  ,
                                                      _format_date(max(self.dates))  ))
            
    def set_country_population(self, pop_data):
        self.population = {}
        for country in self.data.keys():
            if country not in pop_data:
                log.warning("No population data available for %s"%(country))
            else:
                log.debug("Population of %s: %i"%(repr(country), pop_data[country]))
                self.population[country] = pop_data[country]
                
    
    def export(self, report, covid19mx_iter_report_date = None):
        if report.sequence_do_export and report.sequence_type == SEQUENCE_DATE_INCREMENTAL:
            assert covid19mx_iter_report_date == None, "Internal Error"
            filenames = []
            # Calculate the range to go over
            self._country_label_order = []
            first_ok_frame = None
            for index, date in enumerate(self.dates):
                if index == 0: continue
                self.date_limit_min = None
                self.date_limit_top = date
                report.filename_postfix = ".frame_%03i"%(index,)
                #props = dict(boxstyle='round', facecolor='#808080', alpha=0.5)
                #date_legend = dict(x = 0.78, y = 0.17, s = _format_date(date), fontsize=7, color="#000000", bbox=props)
                props = dict(boxstyle='round', facecolor='#8080C0', alpha=0.7)
                date_legend = dict(x = 0.80, y = 0.91, s = _format_date(date), fontsize=7, color="#000000", bbox=props)
                filename = self._export(report, plot_args = dict(extra_labels = [date_legend]))
                if filename != None:
                    filenames.append(filename)
                    if first_ok_frame == None:
                        first_ok_frame = index
                else:
                    first_ok_frame = None
                    
            if report.sequence_clone_last_frame != None:
                log.info("Copying last frame %s %i times"%(filename, report.sequence_clone_last_frame))
                for i in range(0, report.sequence_clone_last_frame):
                    new_file = filename.replace(report.filename_postfix, ".frame_%03i"%(len(self.dates) + i))
                    shutil.copy(src = filename, dst = new_file)

            if report.sequence_do_postprocess:
                cmd = report.sequence_postprocess_command
                cmd = cmd.replace("#FILENAME_WILDCARD#", os.path.basename(filename.replace(report.filename_postfix, ".frame_%03d")))
                cmd = cmd.replace("#REPORT_NAME#", report.ID)
                cmd = cmd.replace("#FIRST_OK_FRAME#", str(first_ok_frame))
                cwd = os.getcwd()
                try:
                    d = os.path.dirname(filename)
                    log.info("Post-processing sequence at %s with command %s"%(d, cmd))
                    os.chdir(d)
                    ec = os.system(cmd)
                    if ec != 0:
                        log.error("Failed to prostprocess, exit code %i"%(ec,))
                    else:
                        log.info("Sequence postprocessing finished ok")
                finally:
                    os.chdir(cwd)
            return filenames
        elif covid19mx_iter_report_date != None:
            props = dict(boxstyle='round', facecolor='#8080C0', alpha=0.7)
            date_legend = dict(x = 0.80, y = 0.91, s = _format_date(covid19mx_iter_report_date), fontsize=7, color="#000000", bbox=props)
            return self._export(report, plot_args = dict(extra_labels = [date_legend]))
        else:
            self._country_label_order = None
            return self._export(report)

                    
    def _export(self,
               report,
               plot_args = {}):
        log.info("-"*100)
        log.info("Running report %s%s"%(report.ID, "" if report.filename_postfix == None else report.filename_postfix))
        log.debug("    Report file: %s"%(report.filename, ))
        log.debug("   Save formats: %s"%(repr(report.formats), ))
        log.debug("       Timeline: %s"%(report.timeline, ))
        log.debug("      Data type: %s"%(report.data_type, ))
        log.debug("         Filter: %s"%(report.filter, ))
        log.debug("           Sort: %s"%(report.sort_columns, ))
        log.debug("   Filter value: %s"%(repr(report.filter_value), ))
        try:
            axis2_enabled = False
            if report.axis2_data_type != None:
                axis2_enabled = True
            
            #if report.data_type in _data_requires_csd_source or (axis2_enabled and report.axis2_data_type in _data_requires_csd_source):
            #    assert self.config_file.data_source == DATA_SOURCE_CSSEGISSANDATA, "This report requires data available only on source %s"%(_get_data_source_name(self.config_file.data_source)) 
            
            # if country population is required, then limit the countries to export
            if report.data_type in _data_type_needs_population or \
                report.filter in _timeline_needs_population:
                countries = self._get_countries_with_population_data()
            else:
                countries = list(self.data.keys())
            
            if report.exclude_countries != None:
                exclude_count = 0
                new_countries = []
                for country in countries:
                    if country not in report.exclude_countries:
                        new_countries.append(country)
                    else:
                        log.debug("Skipping country %s"%(country, ))
                        exclude_count += 1
                countries = new_countries
                if exclude_count != 0:
                    log.warning("%i countries excluded as indicated on report parameters"%(exclude_count))
            
            date_domain, country_timelines = self._get_country_timelines(report.timeline, countries)
            
            report_data = []
            report_data_axis2 = None
            if axis2_enabled:
                report_data_axis2 = []
                
            zeroDivisionErrorCount = 0
            for adj_date in date_domain:
                for axis_index in range(0, 2):
                    if axis_index == 0:
                        rd = report_data
                        dt = report.data_type
                    else:
                        if not axis2_enabled: continue
                        rd = report_data_axis2
                        dt = report.axis2_data_type
                        
                    row = {}
                    for country in countries:
                        data = None
                        if country in country_timelines and adj_date in country_timelines[country]:
                            actual_date = country_timelines[country][adj_date]
                            if actual_date in self.data[country]:
                                try:
                                    if dt == DATA_TOTAL_CASES:
                                        data = self.data[country][actual_date].total_cases
                                    elif dt == DATA_TOTAL_DEATHS:
                                        data = self.data[country][actual_date].total_deaths
                                    elif dt == DATA_TOTAL_DEATHS_PER_1K_TOTAL_CASES:
                                        data = self.data[country][actual_date].total_deaths / (self.data[country][actual_date].total_cases / 1000)
                                    elif dt == DATA_ACTIVE_CASES:
                                        if self.config_file.data_source == DATA_SOURCE_COVID19MX:
                                            data = self.data[country][actual_date].active_cases
                                        else:
                                            data = self.data[country][actual_date].total_cases - self.data[country][actual_date].total_recovered 
                                    elif dt == DATA_ACTIVE_CASES_PER_1M:
                                        if self.config_file.data_source == DATA_SOURCE_COVID19MX:
                                            data = self.data[country][actual_date].active_cases / (self.population[country] / 1000000)
                                        else:
                                            data = (self.data[country][actual_date].total_cases - self.data[country][actual_date].total_recovered) / (self.population[country] / 1000000)
                                    elif dt == DATA_ACTIVE_CASES_PER_1M_FROM_100_ACTIVE_CASES:
                                        if self.config_file.data_source == DATA_SOURCE_COVID19MX:
                                            active_cases = self.data[country][actual_date].active_cases
                                        else:
                                            active_cases = (self.data[country][actual_date].total_cases - self.data[country][actual_date].total_recovered)
                                        if active_cases >= 100:
                                            data = ac / (self.population[country] / 1000000)
                                    elif dt == DATA_TOTAL_RECOVERED:
                                        data = self.data[country][actual_date].total_recovered 
                                    elif dt == DATA_PENDING_CASES:
                                        data = self.data[country][actual_date].pending_cases 
                                        #if country.find("Zacapu") != -1:
                                        #    print("(E) %s, %i"%(_format_date(actual_date), data))
                                    elif dt == DATA_TOTAL_RECOVERED_PER_1M:
                                        data = self.data[country][actual_date].total_recovered / (self.population[country] / 1000000)
                                    elif dt == DATA_NEW_DEATHS_PER_ACTIVE_CASES:
                                        data = self.data[country][actual_date].new_deaths / (self.data[country][actual_date].total_cases - self.data[country][actual_date].total_recovered)
                                    elif dt == DATA_NEW_DEATHS_PER_ACTIVE_CASES_FROM_1K_ACTIVE_CASES:
                                        active_cases = (self.data[country][actual_date].total_cases - self.data[country][actual_date].total_recovered)
                                        if active_cases >= 1000:
                                            data = self.data[country][actual_date].new_deaths / active_cases 
                                    elif dt == DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES_FROM_1K_ACTIVE_CASES:
                                        active_cases = (self.data[country][actual_date].total_cases - self.data[country][actual_date].total_recovered)
                                        if active_cases >= 1000:
                                            data = self.data[country][actual_date].new_deaths / (active_cases / 1000) 
                                    elif dt == DATA_NEW_DEATHS_PER_1K_ACTIVE_CASES:
                                        data = self.data[country][actual_date].new_deaths / ( (self.data[country][actual_date].total_cases - self.data[country][actual_date].total_recovered) / 1000)
                                    elif dt == DATA_NEW_DEATHS:
                                        data = self.data[country][actual_date].new_deaths
                                    elif dt == DATA_TOTAL_CASES_PER_1M:
                                        data = self.data[country][actual_date].total_cases / (self.population[country] / 1000000)
                                    elif dt == DATA_TOTAL_CASES_PER_10M:
                                        data = self.data[country][actual_date].total_cases / (self.population[country] / 10000000)
                                    elif dt == DATA_TOTAL_CASES_PER_10K:
                                        data = self.data[country][actual_date].total_cases / (self.population[country] / 10000)
                                    elif dt == DATA_NEW_CASES:
                                        data = self.data[country][actual_date].new_cases
                                    elif dt == DATA_NEW_CASES_PER_1M:
                                        data = self.data[country][actual_date].new_cases / (self.population[country] / 1000000)
                                    elif dt == DATA_TOTAL_DEATHS_PER_1M:
                                        data = self.data[country][actual_date].total_deaths / (self.population[country] / 1000000)
                                    elif dt == DATA_NEW_DEATHS_PER_1M:
                                        data = self.data[country][actual_date].new_deaths / (self.population[country] / 1000000)
                                    elif dt == DATA_NEW_DEATHS_PER_1K:
                                        data = self.data[country][actual_date].new_deaths / (self.population[country] / 1000)
                                    else:
                                        raise Exception("Unsupported data type: %s"%(dt))
                                except ZeroDivisionError:
                                    log.debug("Zero-division error on data %s on %s at %s, ignoring data point"%(dt, _format_date(actual_date), country))
                                    zeroDivisionErrorCount += 1 
                            
                        row[country] = data
                        #data_max = data_max if data == None else (data if data_max == None else max(data, data_max))
                        #data_min = data_min if data == None else (data if data_min == None else min(data, data_min))
                    rd.append(row)
            
            if zeroDivisionErrorCount > 0:
                log.warning("Detected %i zero-division errorw while running report %s. Those data points were ignored."%(zeroDivisionErrorCount, report.ID))
                                    
            
            # Apply filters
            # Filters are applied only for the first axis. The second one will follow
            selected_countries = self._filter_report_data(report_data, 
                                                          report.filter, 
                                                          report.filter_value,
                                                          countries)
            
            # Smooth data
            if report.filter_sigma != None:
                self.smooth_data(report_data, report.filter_sigma, selected_countries)
            if axis2_enabled and report.axis2_filter_sigma != None:
                self.smooth_data(report_data_axis2, report.axis2_filter_sigma, selected_countries)
        
            # Calculate max and min only after the filter is applied
            data_max = None
            data_min = None
            for row in report_data:
                for country in selected_countries:
                    data_max = data_max if (row[country] == None) else (row[country] if data_max == None else max(row[country], data_max))
                    data_min = data_min if (row[country] == None) else (row[country] if data_min == None else min(row[country], data_min))
            
            if axis2_enabled:
                axis2_data_max = None
                axis2_data_min = None
                for row in report_data_axis2:
                    for country in selected_countries:
                        axis2_data_max = axis2_data_max if (row[country] == None) else (row[country] if axis2_data_max == None else max(row[country], axis2_data_max))
                        axis2_data_min = axis2_data_min if (row[country] == None) else (row[country] if axis2_data_min == None else min(row[country], axis2_data_min))
            
            # Sort data
            #miau
            
            if FORMAT_CSV in report.formats:
                self.write_csv(report.filename, report.timeline, date_domain, report_data, selected_countries)
            if FORMAT_PLOT in report.formats:
                # Adjust ranges, in case a range is open
                y_range = report.plot_y_range
                if y_range != None:
                    nyr = []
                    nyr.extend(y_range)
                    adjust_min = False
                    adjust_max = False
                    if nyr[0] == None: 
                        nyr[0] = data_min
                        adjust_min = True
                    if nyr[1] == None: 
                        nyr[1] = data_max
                        adjust_max = True
                    y_range = self._set_range_margin(nyr, adjust_min, adjust_max, report.plot_y_scale)
                
                axis2_y_range = None
                if axis2_enabled:
                    axis2_y_range = report.axis2_plot_y_range
                    if axis2_y_range != None:
                        nyr = []
                        nyr.extend(axis2_y_range)
                        adjust_min = False
                        adjust_max = False
                        if nyr[0] == None: 
                            nyr[0] = axis2_data_min
                            adjust_min = True
                        if nyr[1] == None: 
                            nyr[1] = axis2_data_max
                            adjust_max = True
                        axis2_y_range = self._set_range_margin(nyr, adjust_min, adjust_max, report.axis2_plot_y_scale)
                
                x_range = report.plot_x_range
                if x_range != None:
                    nxr = []
                    nxr.extend(x_range)
                    adjust_min = False
                    adjust_max = False
                    if nxr[0] == None: 
                        nxr[0] = min(date_domain)
                        adjust_min = True
                    if nxr[1] == None: 
                        nxr[1] = max(date_domain)
                        adjust_max = True
                    x_range = self._set_range_margin(nxr, adjust_min, adjust_max, report.plot_x_scale)
                
                return self.write_plot(report, date_domain, report_data, selected_countries, x_range, y_range, axis2_y_range = axis2_y_range, axis2_report_data = report_data_axis2, **plot_args)
            
        except Exception as ex:
            log.error("Failed to export data to report %s: %s"%(report.filename, ex))
            log.debug(traceback.format_exc())
            return None
    
    def smooth_data(self, data, filter_sigma, selected_countries):
        log.info("Smoothing data...")
        for country in selected_countries:
            # First, extract the data series from the dictionary
            # And save which rows had data
            rows_with_data = []
            array = []
            for index, row in enumerate(data):
                if not country in row or row[country] == None: continue
                rows_with_data.append(index)
                array.append(row[country])
                    
            # Smooth the data
            array = gaussian_filter1d(array, filter_sigma)
            
            # Then, put the data back into the array
            read_index = 0
            for index, row in enumerate(data):
                if index not in rows_with_data: continue
                row[country] = array[read_index]
                read_index += 1
    
    def _set_range_margin(self, rng, adjust_min, adjust_max, axis_scale):
        log.debug("Pre-scale:  %s"%(repr(rng)))
        delta = (rng[1] - rng[0]) * ( PLOT_DATA_MARGIN_LINEAR if axis_scale == PLOT_SCALE_LINEAR else PLOT_DATA_MARGIN_LOG)
        result = ((rng[0] - delta) if adjust_min else rng[0],
                  (rng[1] + delta) if adjust_max else rng[1])
        log.debug("Post-scale: %s"%(repr(result)))
        return result
        
    def write_plot(self, report, date_domain, report_data, selected_countries, x_range = None, y_range = None, axis2_y_range = None, axis2_report_data = None, extra_labels = None):
        if report.plot_style in _plot_styles_last_entry_data:
            return self.write_last_entry_plot(report, date_domain, report_data, selected_countries, x_range = None, y_range = None, axis2_y_range = axis2_y_range, axis2_report_data = axis2_report_data)
        
        if report.filename_postfix == None:
            fname = report.filename + ".png"
        else:
            fname = report.filename + report.filename_postfix + ".png"
        fname = os.path.abspath(fname)
        
        timeline = report.timeline
        data_type = report.data_type
        title = report.plot_title
        
        log.info("Creating plot %s" % (fname, ))
        fig, ax1 = plt.subplots()
        
        if axis2_report_data != None:
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        
        countries = []
        if self._country_label_order == None:
            countries.extend(selected_countries)
        else:
            for c in self._country_label_order:
                if c in selected_countries:
                    countries.append(c)
            for c in selected_countries:
                if c not in countries:
                    countries.append(c)
        
        # non-skipped country index
        nsc_index = -1
        for index, country in enumerate(countries):
            # Prepare X,Y data
            x = []
            y = []
            for date_index, adj_date in enumerate(date_domain):
                data = report_data[date_index][country]
                if data == None or \
                    (data == 0 and not report.data_plot_zeros): continue
                
                if timeline in _date_timelines:
                    #x.append(datetime.datetime.strptime(adj_date,"%m/%d/%Y").date())
                    x.append(datetime.datetime.fromtimestamp(adj_date))
                else:
                    x.append(adj_date)
                y.append(data)
            
            #log.debug("%s, %s:%s"%(country, len(x), len(y)))
            if len(y) == 0: continue
            if self._country_label_order != None and country not in self._country_label_order:
                self._country_label_order.append(country)
            nsc_index += 1
            
            #log.debug("%s X: %s"%(country, repr(x)))
            #log.debug("%s Y: %s"%(country, repr(y)))
            
            if axis2_report_data != None:
                x2 = []
                y2 = []
                for date_index, adj_date in enumerate(date_domain):
                    data = axis2_report_data[date_index][country]
                    if data == None or \
                        (data == 0 and not report.data_plot_zeros): continue
                    
                    if timeline in _date_timelines:
                        #x.append(datetime.datetime.strptime(adj_date,"%m/%d/%Y").date())
                        x2.append(datetime.datetime.fromtimestamp(adj_date))
                    else:
                        x2.append(adj_date)
                    y2.append(data)
            
            if report.plot_style == PLOT_STYLE_LINE:
                args = {}
                if report.plot_line_markers == PLOT_LINE_MARKERS_LAST_ONE:
                    args["markevery"] = [len(x) - 1]
                    args["marker"] = _plot_line_markers[nsc_index % len(_plot_line_markers)]
                    args["markersize"] = (4.5 if (country not in _vip_countries) else 5.5)
                elif report.plot_line_markers == PLOT_LINE_MARKERS_ALL:
                    args["marker"] = _plot_line_markers[nsc_index % len(_plot_line_markers)]
                    args["markersize"] = (3 if (country not in _vip_countries) else 4.2)
                
                line, = ax1.plot(x, 
                                 y, 
                                 label = country if report.plot_line_legend_style == PLOT_LINE_LEGEND_STYLE_STANDARD else None, 
                                 linewidth = report.plot_line_width if (country not in _vip_countries) else report.plot_line_width * 1.5,
                                 **args)
                                 
                if report.plot_line_legend_style == PLOT_LINE_LEGEND_STYLE_EOL_MARKER:
                    ax1.scatter(x[-1], y[-1], marker=_plot_line_markers[nsc_index % len(_plot_line_markers)], color=line.get_color(), zorder=7, s = (20 if (country not in _vip_countries) else 40), label=country)
                line.set_dashes(_plot_line_styles[nsc_index % len(_plot_line_styles)])
            elif report.plot_style == PLOT_STYLE_MARKERS:
                line, = ax1.plot(x, y, label=country, linewidth = 0.75 if (country not in _vip_countries) else 1)
                line.set_dashes((0, 1))
                line.set_marker(_plot_line_markers[nsc_index % len(_plot_line_markers)])
                line.set_markersize(3 if (country not in _vip_countries) else 4.2)
            else:
                raise Exception("Unsupported plot style: %s"%(report.plot_style, )) 
            
            if axis2_report_data != None:
                line2, = ax2.plot(x2, y2, 
                                  linewidth = report.axis2_plot_line_width if (country not in _vip_countries) else report.axis2_plot_line_width * 1.5)
                if report.axis2_plot_style == PLOT_STYLE_LINE:
                    line2.set_dashes(_plot_line_styles[nsc_index % len(_plot_line_styles)])
                elif report.axis2_plot_style == PLOT_STYLE_MARKERS:
                    line2.set_dashes((0, 1))
                    line2.set_marker(_plot_line_markers[nsc_index % len(_plot_line_markers)])
                    line2.set_markersize(3 if (country not in _vip_countries) else 4.2)
                else:
                    raise Exception("Unsupported plot style for axis2: %s"%(report.axis2_plot_style, ))
                
        #plt.show()
        ax1.set_yscale(report.plot_y_scale)
        ax1.set_xscale(report.plot_x_scale)
        if axis2_report_data != None:
            ax2.set_yscale(report.axis2_plot_y_scale)
        
        ax1.tick_params(labelsize=PLOT_AXIS_FONT_SIZE - 2, colors=PLOT_EXTERNAL_FONT_COLOR, which = 'both')
        
        if axis2_report_data != None:
            ax1.legend(fontsize=PLOT_AXIS_FONT_SIZE)
            ax2.tick_params(labelsize=PLOT_AXIS_FONT_SIZE - 2, colors=PLOT_EXTERNAL_FONT_COLOR, which = 'both')
        
        if timeline in _date_timelines:
            ax1.tick_params(labelsize=PLOT_AXIS_FONT_SIZE - 3, axis="x", rotation = 35)
        
        # Title
        if title != None:
            txt = plt.suptitle(title, fontsize = 8, fontweight='bold')
            plt.setp(txt, color=PLOT_EXTERNAL_FONT_COLOR)
        # Sub-title
        if report.plot_subtitle != None:
            txt = plt.title(report.plot_subtitle, fontsize = 7)
            plt.setp(txt, color=PLOT_EXTERNAL_FONT_COLOR)
        
        if timeline in _timeline_display_names:
            ax1.set_xlabel(_timeline_display_names.get(timeline), fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
        else:
            log.warning("No label defined for timeline type %s"%(timeline, ))

        for i in range(0, 2):
            if i == 0:
                dt = report.data_type
                ax = ax1
                filter_sigma = report.filter_sigma
            else:
                if axis2_report_data == None: continue
                dt = report.axis2_data_type
                ax = ax2
                filter_sigma = report.axis2_filter_sigma

            if dt in _data_display_names:
                txt = _data_display_names.get(dt)
                if filter_sigma != None:
                    txt += " (Filter $\sigma$ %.2f)"%(filter_sigma,)
                ax.set_ylabel(txt, fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            else:
                log.warning("No label defined for data type %s"%(dt, ))
    
        if x_range != None:
            if timeline in _date_timelines:
                ax1.set_xlim([datetime.datetime.fromtimestamp(d) for d in x_range])
            else:
                plt.xlim(x_range)
        else:
            log.debug("Setting X axis multiplier")
            ax1.set_xmargin(PLOT_DATA_MARGIN_LINEAR if report.plot_x_scale == PLOT_SCALE_LINEAR else PLOT_DATA_MARGIN_LOG)
        if y_range != None:
            ax1.set_ylim(y_range)
        else:
            ax1.set_ymargin(PLOT_DATA_MARGIN_LINEAR if report.plot_y_scale == PLOT_SCALE_LINEAR else PLOT_DATA_MARGIN_LOG)
            log.debug("Setting Y axis multiplier")
        if axis2_report_data != None:
            if axis2_y_range != None:
                ax2.set_ylim(axis2_y_range)
            else:
                ax2.set_ymargin(PLOT_DATA_MARGIN_LINEAR if report.axis2_plot_y_scale == PLOT_SCALE_LINEAR else PLOT_DATA_MARGIN_LOG)
                log.debug("Setting Y2 axis multiplier")
        
        if timeline in _date_timelines:
            #ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            formatter = mdates.DateFormatter("%y/%m/%d")
            ax1.xaxis.set_major_formatter(formatter)
        elif timeline in (TIMELINE_TOTAL_CONFIRMED_CASES, TIMELINE_TOTAL_CONFIRMED_CASES_PER_1M, TIMELINE_ACTIVE_CASES):
            ax1.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_axis_ticks))
            
        ax1.grid(True, color=PLOT_GRID_COLOR)
        fig.set_facecolor(PLOT_EXTERNAL_BG_COLOR)
        #plt.tight_layout()
        
        args = {}
        if report.legend_line_length != None:
            args["handlelength"] = report.legend_line_length
        
        ax1.legend(fontsize=PLOT_AXIS_FONT_SIZE - 2, loc = report.legend_location, **args)
        
        ax1.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_axis_ticks))
        if axis2_report_data != None:
            ax2.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_axis_ticks))
        
        if report.sync_both_y_axis:
            ax2.set_yticks(ax1.get_yticks())
            ax2.set_ylim(ax1.get_ylim())
        
        plt.gcf().text(0.01, 0.01, "%s:\n%s"%(_data_source, _get_data_source_name(self.config_file.data_source)), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        plt.gcf().text(0.01, 0.98, _github_url, fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        if self.config_file.supress_last_n_days != None:
            plt.gcf().text(0.98, 0.12, time.strftime(_supressed_data_from_last_n_days_fmtr%self.config_file.supress_last_n_days), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR_WARNING, rotation = 90)
        if report.data_type in (DATA_ACTIVE_CASES, DATA_ACTIVE_CASES_PER_1M):
            plt.gcf().text(0.965, 0.12, _active_cases_fmtr%self.config_file.covid19mx_active_case_duration_days, fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR_WARNING, rotation = 90)
        plt.gcf().text(0.80, 0.01, time.strftime("%s %%Y/%%m/%%d %%H:%%M"%(_generated_on,)), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        
        if extra_labels != None:
            for label in extra_labels:
                plt.gcf().text(**label)
        
        log.info("Writting plot to file")
        plt.savefig(fname = fname, dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        return fname
        
    def write_last_entry_plot(self, report, date_domain, report_data, selected_countries, x_range = None, y_range = None, axis2_y_range = None, axis2_report_data = None):
        if report.filename_postfix == None:
            fname = report.filename + ".png"
        else:
            fname = report.filename + report.filename_postfix + ".png"
        fname = os.path.abspath(fname)
        
        timeline = report.timeline
        data_type = report.data_type
        title = report.plot_title
        
        log.info("Creating last entry plot %s" % (fname, ))
        fig, ax1 = plt.subplots()
        
        axis2_enabled = axis2_report_data != None
        
        # Prepare X,Y data
        x_indexes = []
        x_ticks = []
        y = []
        y2 = []
        incremental_index = 0
        for index, country in enumerate(selected_countries):
            last_y = None
            last_y2 = None
            for date_index, adj_date in enumerate(date_domain):
                data = report_data[date_index][country]
                if data != None:
                    last_y = data
                
                if axis2_enabled:
                    data2 = axis2_report_data[date_index][country]
                    if data2 != None:
                        last_y2 = data2
                        #if country.find("Zacapu") != -1:
                        #    print("(F), %i"%(last_y2,))
                
            if last_y == None and (not axis2_enabled or last_y2 == None):
                continue
            
            if last_y == None:
                log.warning("No final data for country %s, forcing to 0 since the second series has a value"%(country))
                last_y = 0
            if last_y2 == None:
                log.warning("No final data for country %s, forcing to 0 since the first series has a value"%(country))
                last_y2 = 0
                
            if last_y == 0 and (not axis2_enabled or last_y2 == 0) and not report.data_plot_zeros:
                # Ignore countries which have only zeros
                continue
            
            x_indexes.append(incremental_index)
            x_ticks.append(country)
            y.append(last_y)
            if axis2_enabled:
                y2.append(last_y2)
            incremental_index += 1
            #print(country, last_y)
            
        if report.plot_bar_tick_cleanup != None:
            if report.plot_bar_tick_cleanup[0] == PLOT_BAR_TICK_CLEANUP_SPLIT:
                for i in range(0, len(x_ticks)):
                    x_ticks[i] = "\n".join(_string_line_split(x_ticks[i], report.plot_bar_tick_cleanup[1]))
            else:
                raise Exception("Internal error")
#        print(x_ticks, y, y2)
            
        if report.plot_style == PLOT_STYLE_LAST_ENTRY_BARS:
            plot0 = plt.bar(x_indexes, y, zorder=3)
            if axis2_enabled:
                plot1 = plt.bar(x_indexes, y2, zorder=3, bottom = y)
            plt.xticks(x_indexes, x_ticks)
            ax1.tick_params(labelsize=PLOT_AXIS_FONT_SIZE - 2, colors=PLOT_EXTERNAL_FONT_COLOR, which = 'both')
            ax1.tick_params(labelsize=PLOT_AXIS_FONT_SIZE - 3, axis="x", rotation = 35)
            ax1.grid(True, color=PLOT_GRID_COLOR, axis="y", zorder=-1)
            ax1.set_yscale(report.plot_y_scale)
        elif report.plot_style == PLOT_STYLE_LAST_ENTRY_HBARS:
            plot0 = plt.barh(x_indexes, y, zorder=3, align='center')
            if axis2_enabled:
                plot1 = plt.barh(x_indexes, y2, zorder=3, align='center', left = y)
            ax1.invert_yaxis()  # labels read top-to-bottom
            plt.yticks(x_indexes, x_ticks)
            #ax1.set_yticks(x_indexes)
            #ax1.set_yticklabels(x_ticks)
            ax1.tick_params(labelsize=PLOT_AXIS_FONT_SIZE - 3, colors=PLOT_EXTERNAL_FONT_COLOR, which = 'both')
            ax1.grid(True, color=PLOT_GRID_COLOR, axis="x", zorder=-1)
            ax1.set_xscale(report.plot_y_scale)
        else:
            raise Exception("Unsupported plot style: %s"%(report.plot_style, ))
                
        
        #if axis2_report_data != None:
        #    ax2.set_yscale(report.axis2_plot_y_scale)
        
        # Title
        if title != None:
            txt = plt.suptitle(title, fontsize = 8, fontweight='bold')
            plt.setp(txt, color=PLOT_EXTERNAL_FONT_COLOR)
        # Sub-title
        if report.plot_subtitle != None:
            txt = plt.title(report.plot_subtitle, fontsize = 7)
            plt.setp(txt, color=PLOT_EXTERNAL_FONT_COLOR)
        
        #if timeline in _timeline_display_names:
        #    ax1.set_xlabel(_timeline_display_names.get(timeline), fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
        #else:
        #    log.warning("No label defined for timeline type %s"%(timeline, ))

                
        if report.data_type in _data_display_names:
            if not axis2_enabled:
                if report.plot_style == PLOT_STYLE_LAST_ENTRY_BARS:
                    ax1.set_ylabel(_data_display_names.get(report.data_type), fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
                elif report.plot_style == PLOT_STYLE_LAST_ENTRY_HBARS:
                    ax1.set_xlabel(_data_display_names.get(report.data_type), fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
                else:
                    raise Exception("Unsupported plot style: %s"%(report.plot_style, ))
            else:
                plt.legend((plot0[0], plot1[0]), (_data_display_names.get(report.data_type), _data_display_names.get(report.axis2_data_type)), loc = report.legend_location, fontsize=PLOT_AXIS_FONT_SIZE - 2)

        else:
            log.warning("No label defined for data type %s"%(report.data_type, ))
    
        if y_range != None:
            ax1.set_ylim(y_range)
        else:
            ax1.set_ymargin(PLOT_DATA_MARGIN_LINEAR if report.plot_y_scale == PLOT_SCALE_LINEAR else PLOT_DATA_MARGIN_LOG)
            log.debug("Setting Y axis multiplier")
#        if axis2_report_data != None:
#            if axis2_y_range != None:
#                ax2.set_ylim(axis2_y_range)
#            else:
#                ax2.set_ymargin(PLOT_DATA_MARGIN_LINEAR if report.axis2_plot_y_scale == PLOT_SCALE_LINEAR else PLOT_DATA_MARGIN_LOG)
#                log.debug("Setting Y2 axis multiplier")
        
        
        fig.set_facecolor(PLOT_EXTERNAL_BG_COLOR)
        #plt.tight_layout()
        
        #ax1.legend(fontsize=PLOT_AXIS_FONT_SIZE - 2)
        
        if report.plot_style == PLOT_STYLE_LAST_ENTRY_BARS:
            ax1.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_axis_ticks))
        elif report.plot_style == PLOT_STYLE_LAST_ENTRY_HBARS:
            ax1.xaxis.set_major_formatter(ticker.FuncFormatter(self.format_axis_ticks))
        else:
            raise Exception("Unsupported plot style: %s"%(report.plot_style, ))
#        if axis2_report_data != None:
 #           ax2.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_axis_ticks))
        
#        if report.sync_both_y_axis:
#            ax2.set_yticks(ax1.get_yticks())
#            ax2.set_ylim(ax1.get_ylim())
        
        plt.gcf().text(0.01, 0.01, "%s:\n%s"%(_data_source, _get_data_source_name(self.config_file.data_source)), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        plt.gcf().text(0.01, 0.98, _github_url, fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        if self.config_file.supress_last_n_days != None:
            plt.gcf().text(0.98, 0.12, time.strftime(_supressed_data_from_last_n_days_fmtr%self.config_file.supress_last_n_days), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR_WARNING, rotation = 90)
        if report.data_type in (DATA_ACTIVE_CASES, DATA_ACTIVE_CASES_PER_1M):
            plt.gcf().text(0.965, 0.12, _active_cases_fmtr%self.config_file.covid19mx_active_case_duration_days, fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR_WARNING, rotation = 90)
        plt.gcf().text(0.80, 0.01, time.strftime("%s %%Y/%%m/%%d %%H:%%M"%(_generated_on,)), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        
        log.info("Writting plot to file")
        plt.savefig(fname = fname, dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
        plt.close()
        return fname
        
    def format_axis_ticks(self, x, pos=None):
        def round_to_int(n):
            n2 = n + 0.001
            if n2%1 < 0.002:
                return int(n2)
            return n
        
        if x >= 1000000: 
            r = "%sM"%(round_to_int(x/1000000))
        elif x >= 1000: 
            r = "%sk"%(round_to_int(x/1000))
        elif x >= 1: 
            r = "%s"%(round_to_int(x))
        elif x >= 0.001: 
            r = "%s$m$"%(round_to_int(x*1000))
        elif x >= 0.000001: 
            r = "%s$\mu$"%(round_to_int(x*1000000))
        else:
            r = "%s"%x 
        
        return r
        
    def write_csv(self, filename, timeline, date_domain, report_data, selected_countries):
        log.info("Writting CSV report %s" % (filename, ))
        with open(filename + ".csv", "w", newline="") as fh:
            hdr = ["Adjusted Date"]
            for country in selected_countries:
                hdr.append(country)
            writer = csv.writer(fh)
            writer.writerow(hdr)
            for date_index, adj_date in enumerate(date_domain):
                fmt_date = self.format_adjusted_date(adj_date, timeline)
                row = [fmt_date]
                for country in selected_countries:
                    data = report_data[date_index][country]
                    data_s = "%.3f" % (float(data)) if data != None else ""
                    row.append(data_s)
                
                writer.writerow(row)

        
    def _filter_report_data(self, report_data, filter, filter_value, report_countries):
        log.info("Filtering report data")
        selected_countries = []
        
        if filter == FILTER_NONE:
            selected_countries.extend(report_countries)
        elif filter == FILTER_COUNTRY_LIST:
            assert type(filter_value) in (tuple, list), "Filter value must be a list or tuple"
            for country in filter_value:
                if country in report_countries:
                    selected_countries.append(country)
                else:
                    log.warning("Country not found on report data, cannot add into filter: %s"%(country,))
        elif filter in (FILTER_TOP_MAX, FILTER_TOP_MAX_MX, FILTER_TOP_MIN, FILTER_TOP_MAX_REGEX_MATCH):
            if filter == FILTER_TOP_MAX_REGEX_MATCH:
                regex = filter_value[0]
                filter_int_value = filter_value[1]
                available_countries = []
                for country in report_countries:
                    if regex.match(country) != None:
                        available_countries.append(country)
                filter = FILTER_TOP_MAX
            else:
                available_countries = report_countries
                filter_int_value = filter_value
            
            assert type(filter_int_value) == int, "Filter value must be an integer"
            max_country_values = {}
            # get the maximum value per country across all dates
            for country in available_countries:
                country_max = None
                for row in report_data:
                    val = row[country]
                    if val == None: continue
                    country_max = val if country_max == None else max(country_max, val)
                if country_max == None: continue
                if country_max not in max_country_values:
                    max_country_values[country_max] = []
                log.debug("%s, max=%i"%(country, country_max))
                max_country_values[country_max].append(country)
            # sort the max values
            values = list(max_country_values.keys())
            values.sort(reverse = True)
            tmp_country_list = []
            # and add the countries into a list using the max repetition value fount
            for v in values:
                # Also sort the countries per value in case there's more than one per value
                countries = max_country_values[v]
                countries.sort()
                tmp_country_list.extend(countries)
            # Limit the number of countries as requested
            if filter in (FILTER_TOP_MAX, FILTER_TOP_MAX_MX, FILTER_TOP_MAX_REGEX_MATCH):
                if len(tmp_country_list) > filter_int_value:
                    tmp_country_list = tmp_country_list[:filter_int_value]
            elif filter == FILTER_TOP_MIN:
                if len(tmp_country_list) > filter_int_value:
                    tmp_country_list = tmp_country_list[filter_int_value:]
            else:
                raise Exception("Internal error")
            if filter == FILTER_TOP_MAX_MX and COUNTRY_MX in report_countries:
                tmp_country_list.append(COUNTRY_MX)
            # Now, keep the original order of countries
            for country in report_countries:
                if country in tmp_country_list:
                    selected_countries.append(country)
        elif filter in (FILTER_TOP_MAX_REBOUND_MATCH):
            regex = filter_value[0]
            filter_int_value = filter_value[1]
            available_countries = []
            for country in report_countries:
                if regex.match(country) != None:
                    available_countries.append(country)
            
            assert type(filter_int_value) == int, "Filter value must be an integer"
        
            max_country_valley_score = {}
            # get the maximum valley size per country country across all dates
            for country in available_countries:
                country_max = None
                
                data = [row[country] for row in report_data]
                valleys = get_valleys(data)
                max_valley_score = 0 if len(valleys) == 0 else max([valley.size_score for valley in valleys])
                
                if max_valley_score not in max_country_valley_score:
                    max_country_valley_score[max_valley_score] = []
                log.debug("%s, max_valley_score=%i"%(country, max_valley_score))
                max_country_valley_score[max_valley_score].append(country)
            # sort the max values
            values = list(max_country_valley_score.keys())
            values.sort(reverse = True)
            tmp_country_list = []
            # and add the countries into a list using the max repetition value fount
            for v in values:
                # Also sort the countries per value in case there's more than one per value
                countries = max_country_valley_score[v]
                countries.sort()
                tmp_country_list.extend(countries)
            # Limit the number of countries as requested
            if filter in (FILTER_TOP_MAX_REBOUND_MATCH, ):
                if len(tmp_country_list) > filter_int_value:
                    tmp_country_list = tmp_country_list[:filter_int_value]
            else:
                raise Exception("Internal error")
            # Now, keep the original order of countries
            for country in report_countries:
                if country in tmp_country_list:
                    selected_countries.append(country)
        else:
            raise Exception("unsupporte filter type: %s"%(filter, ))
        
        return selected_countries
                
    def _get_countries_with_population_data(self):
        assert self.population != None, "Population data is needed for this report"
        countries = []
        for country in self.data.keys():
            if country not in self.population: continue
            countries.append(country)
        return countries
        
    def format_adjusted_date(self, date, timeline):
        if timeline == TIMELINE_ORIGINAL:
            return _format_date(date)
        if timeline in (TIMELINE_FIRST_100_CASES, TIMELINE_FIRST_CASE_PER_1M, TIMELINE_FIRST_CASE_PER_10K, TIMELINE_FIRST_CASE_PER_10M):
            return "%i Days"%(date, )
        if timeline == TIMELINE_TOTAL_CONFIRMED_CASES:
            return "%i Confirmed Cases"%(date,)
        if timeline == TIMELINE_TOTAL_CONFIRMED_CASES_PER_1M:
            return "%i Confirmed Cases / 1M Habs"%(date,)
        if timeline == TIMELINE_ACTIVE_CASES:
            return "%i Active Cases"%(date,)
    
        raise Exception("Unsupported timeline: %s"%(timeline,))
        
    def get_limited_dates(self):
        if self.date_limit_min == None and self.date_limit_top == None: 
            return self.dates
        
        dates = []
        s = 0
        for date in self.dates:
            if s == 0:
                if self.date_limit_min == None or date >= self.date_limit_min:
                    s = 1
            
            if s == 1:
                dates.append(date)
            
                if self.date_limit_top != None and date >= self.date_limit_top:
                    break
        
        return dates
        
    def _get_country_timelines(self, 
                               timeline,
                               selected_countries):
        country_timelines = {}
        
        if timeline == TIMELINE_ORIGINAL:
            base_timeline = {}
            for date in self.get_limited_dates():
                # The key on the dictionary represents the adjusted date
                base_timeline[date] = date
            for country in selected_countries:
                country_timelines[country] = base_timeline
        elif timeline == TIMELINE_TOTAL_CONFIRMED_CASES:
            for country in selected_countries:
                timeline = {}
                for index, date in enumerate(self.get_limited_dates()):
                    if date not in self.data[country] or self.data[country][date].total_cases == None: continue
                    timeline[self.data[country][date].total_cases] = date
                country_timelines[country] = timeline
        elif timeline == TIMELINE_TOTAL_CONFIRMED_CASES_PER_1M:
            for country in selected_countries:
                timeline = {}
                for index, date in enumerate(self.get_limited_dates()):
                    if date not in self.data[country] or self.data[country][date].total_cases == None: continue
                    timeline[self.data[country][date].total_cases / (self.population[country] / 1000000)] = date
                country_timelines[country] = timeline
        elif timeline == TIMELINE_ACTIVE_CASES:
            for country in selected_countries:
                timeline = {}
                for index, date in enumerate(self.get_limited_dates()):
                    if date not in self.data[country] or self.data[country][date].total_cases == None or self.data[country][date].total_recovered == None: continue
                    timeline[self.data[country][date].total_cases - self.data[country][date].total_recovered] = date
                country_timelines[country] = timeline
        elif timeline == TIMELINE_FIRST_100_CASES:
            # Lookup on each country when these got 100 cases or more
            for country in selected_countries:
                log.debug("Country timeline for first 100 cases: %s"%(country, ))
                _100_cases_index = None
                for index, date in enumerate(self.get_limited_dates()):
                    if date in self.data[country] and self.data[country][date].total_cases >= 100:
                        _100_cases_index = index
                        break
                if _100_cases_index == None:
                    continue
                timeline = {}
                for index, date in enumerate(self.get_limited_dates()):
                    days = index - _100_cases_index
                    log.debug("%s, %i days"%(_format_date(date), days))
                    timeline[days] = date
                country_timelines[country] = timeline
        elif timeline in (TIMELINE_FIRST_CASE_PER_1M, TIMELINE_FIRST_CASE_PER_10K, TIMELINE_FIRST_CASE_PER_10M):
            if timeline == TIMELINE_FIRST_CASE_PER_1M:
                pop_div = 1000000
            elif timeline == TIMELINE_FIRST_CASE_PER_10K:
                pop_div = 10000
            elif timeline == TIMELINE_FIRST_CASE_PER_10M:
                pop_div = 10000000
            else:
                raise Exception("Unsupported timeline: %s"%(timeline, ))
            # Lookup on each country when these got 1 cases per million
            for country in selected_countries:
                log.debug("Country timeline for first case per %i habitants: %s"%(pop_div, country, ))
                _100_cases_index = None
                for index, date in enumerate(self.get_limited_dates()):
                    if date in self.data[country] and \
                        (self.data[country][date].total_cases / (self.population[country] / pop_div)) >= 1:
                        _100_cases_index = index
                        break
                if _100_cases_index == None:
                    continue
                timeline = {}
                for index, date in enumerate(self.get_limited_dates()):
                    days = index - _100_cases_index
                    log.debug("%s, %i days"%(_format_date(date), days))
                    timeline[days] = date
                country_timelines[country] = timeline
        else:
            raise Exception("Unsupported timeline: %s"%(timeline,))
        
        domain = []
        for country in country_timelines:
            for value in country_timelines[country].keys():
                if value not in domain:
                    domain.append(value)
        
        domain.sort()
        
        return domain, country_timelines
    
def _string_line_split(strn, max_line_width):
    words = strn.split(" ")
    lines = []
    curr_line = ""
    while len(words) > 0:
        # Try the next word
        if len(curr_line) + 1 + len(words[0]) <= max_line_width:
            curr_line += ((" " if len(curr_line) > 0 else "")  + words.pop(0))
        else:
            if len(curr_line) > 0:
                lines.append(curr_line)
                curr_line = ""
            else:
                # need to split the word
                w = words[0]
                lines.append(w[:max_line_width])
                words[0] = w[max_line_width:]
    if curr_line != "":
        lines.append(curr_line)
    return lines    
        
    
def _add_date_full_days(d, days):
    # Add 25 hours for 1 day (to account for daylight time changes)
    d += (24*days + 1)*60*60
    # Then adjust back to the beginning of the day
    d = time.mktime(time.strptime(time.strftime("%Y-%m-%d", time.localtime(d)), "%Y-%m-%d"))
    
    return d

Valley = collections.namedtuple("Valley", ("start_index", "end_index", "height", "width", "size_score"))

def get_valleys(data, is_reversed = False):
    assert len(data) >= 3
    
    base_index = 0
    
    valleys = []
    
    while True:
        # log.debug("Locating beggining of valley from index %i"%(base_index,))
        # Locate the beggining of the next valley
        prev_val = None
        start_of_drop_index = None
        start_of_drop_value = None
        while True:
            v = data[base_index]
            if prev_val != None and prev_val > v:
                start_of_drop_index = base_index - 1
                start_of_drop_value = prev_val
                # log.debug("Located beggining of valley at index %i with value %s"%(start_of_drop_index, start_of_drop_value))
                break
            
            prev_val = v
            base_index += 1
            # No data drop has been found
            if base_index >= len(data):
                break
        
        # Could not find the beginning of the next valley
        if start_of_drop_index == None:
            # log.debug("Out of data, did not find a valley start. Stopping.")
            break
        
        # Scan the valley
        # Need to find the next data point which is equal or higher than the beggining of the valley
        # No need to check for overflow, can't be the last value on the list
        fwd_index = start_of_drop_index + 1
        min_valley_val = start_of_drop_value
        while True:
            v = data[fwd_index]
            if v >= start_of_drop_value:
                # log.debug("End of valley located at index %i"%(fwd_index,))
            
                #Valley = collections.namedtuple("Valley", ("start_index", "end_index", "height", "width", "size_score"))
                start_index = start_of_drop_index
                end_index = fwd_index
                height = start_of_drop_value - min_valley_val
                width = end_index - start_index
                # TODO: Make an area calculation method for this
                size_score = height * width
                
                valley = Valley(start_index, end_index, height, width, size_score)
                valleys.append(valley)
                
                # log.debug("Found valley: %s"%(repr(valley)))
                break
            
            min_valley_val = min(v, min_valley_val)
            
            fwd_index += 1
            # No data drop has been found
            if fwd_index >= len(data):
                # log.debug("Out of data, did not find end of valley")
                break
        
        # Now, continue from the start data point and find the next raise of values
        # log.debug("Locating the next data raise from index %i"%(base_index,))
        # Locate the beggining of the next valley
        prev_val = None
        while True:
            v = data[base_index]
            if prev_val != None and prev_val < v:
                # log.debug("Located data raise at index %i with value %s"%(base_index, v))
                break
            
            prev_val = v
            base_index += 1
            # No data drop has been found
            if base_index >= len(data):
                base_index = None
                break
        
        # Could not find the beginning of the next valley
        if base_index == None:
            # log.debug("Out of data, did not find a data raise. Stopping.")
            break
        
    if not is_reversed:
        rev_data = []
        rev_data.extend(data)
        rev_data.reverse()
        valleys.extend(get_valleys(rev_data, is_reversed = True))
        
        # Remove duplicated valleys
        new_valleys = []
        for v in valleys:
            if v not in new_valleys:
                new_valleys.append(v)
        valleys = new_valleys
        
    else:
        # Reverse the located valleys
        new_valleys = []
        #("start_index", "end_index", "height", "width", "size_score"))
        last_index = len(data) - 1
        for valley in valleys:
            new_valley = Valley(last_index - valley.end_index, last_index - valley.start_index, valley.height, valley.width, valley.size_score)
            new_valleys.append(new_valley)
        valleys = new_valleys
    
    return valleys    
             
def _format_date(d):
    return time.strftime("%Y/%m/%d", time.localtime(d))
             
def _get_data_source_name(data_source):
    return DATA_SOURCE_TXT.get(data_source, "UNK_%s"%(data_source))
        
def get_args():
    config_files = []
    
    for arg in sys.argv[1:]:
        if os.path.splitext(arg)[1].lower() == ".ini":
            config_files.append(arg)
    
    if len(config_files) == 0:
        log.warning("Using default config file: %s"%(CONFIG_FILE, ))
        config_files.append(CONFIG_FILE)
    
    for i in range(0, len(config_files)):
        config_files[i] = os.path.abspath(config_files[i])
    
    return config_files
             

def _iterate_covid19mx_reports(config_file, out_dir, report, cwd, covid19mx_reports):
    filenames = []
    # Calculate the range to go over
    _country_label_order = []
    first_ok_frame = None
    for index, covid19mx_report in enumerate(covid19mx_reports):
        # TODO: store these DBs on on a factory for the cases with multiple reports
        corona_data = CoronaBaseData(config_file=config_file, covid19mx_force_report = covid19mx_report.tag)
        try:
            if out_dir != None:
                os.chdir(out_dir)
            
            report.filename_postfix = ".frame_%03i"%(index,)
            corona_data._country_label_order = _country_label_order
            filename = corona_data.export(report, covid19mx_iter_report_date = covid19mx_report.date)
    
            if filename != None:
                filenames.append(filename)
                if first_ok_frame == None:
                    first_ok_frame = index
            else:
                first_ok_frame = None
             
        finally:
            if cwd != None:
                os.chdir(cwd)
                
    if report.sequence_clone_last_frame != None:
        log.info("Copying last frame %s %i times"%(filename, report.sequence_clone_last_frame))
        for i in range(0, report.sequence_clone_last_frame):
            new_file = filename.replace(report.filename_postfix, ".frame_%03i"%(len(covid19mx_reports) + i))
            shutil.copy(src = filename, dst = new_file)

    if report.sequence_do_postprocess:
        cmd = report.sequence_postprocess_command
        cmd = cmd.replace("#FILENAME_WILDCARD#", os.path.basename(filename.replace(report.filename_postfix, ".frame_%03d")))
        cmd = cmd.replace("#REPORT_NAME#", report.ID)
        cmd = cmd.replace("#FIRST_OK_FRAME#", str(first_ok_frame))
        local_cwd = os.getcwd()
        try:
            d = os.path.dirname(filename)
            log.info("Post-processing sequence at %s with command %s"%(d, cmd))
            os.chdir(d)
            ec = os.system(cmd)
            if ec != 0:
                log.error("Failed to prostprocess, exit code %i"%(ec,))
            else:
                log.info("Sequence postprocessing finished ok")
        finally:
            os.chdir(local_cwd)

    
    return filenames

def _get_covid19mx_reports():
    log.debug("Looking for the latest MX covid data file under %s"%(COVID19MX_DIR_MAIN_REPORT_DIR, ))
    
    reports = []
    
    months_items = os.listdir(COVID19MX_DIR_MAIN_REPORT_DIR)
    months_items.sort()
    for month_dir in months_items:
        m = COVID19MX_REGEX_MAIN_REPORT_MONTH_DIR.match(month_dir)
        if m == None: continue
        fmonth_dir = os.path.join(COVID19MX_DIR_MAIN_REPORT_DIR, month_dir)
    
        day_items = os.listdir(fmonth_dir)
        day_items.sort()
        for day_file in day_items:
            m = COVID19MX_REGEX_MAIN_REPORT_DAY_FILE.match(day_file)
            if m == None: continue
            reports.append(SortedDate(tag = os.path.join(fmonth_dir, day_file), 
                                     year = m.groupdict()["year"], 
                                     month = m.groupdict()["month"], 
                                     day = m.groupdict()["day"]))
    reports.sort()
    return reports
    
def set_language(lang):
    global _timeline_display_names
    global _data_display_names
    global _data_source
    global _generated_on
    global _supressed_data_from_last_n_days_fmtr
    global _active_cases_fmtr
    
    assert lang in _known_languages, "Invalid language: %s. Known languages: %s"%(repr(lang), repr(_known_languages))

    log.info("Setting language to %s"%(lang))

    if lang == LANGUAGE_SP:
        _timeline_display_names = _timeline_display_names_sp
        _data_display_names = _data_display_names_sp
        _data_source = _data_source_sp
        _generated_on = _generated_on_sp
        _supressed_data_from_last_n_days_fmtr = _supressed_data_from_last_n_days_fmtr_sp
        _active_cases_fmtr = _active_cases_fmtr_sp
    elif lang == LANGUAGE_EN:
        _timeline_display_names = _timeline_display_names_en
        _data_display_names = _data_display_names_en
        _data_source = _data_source_en
        _generated_on = _generated_on_en
        _supressed_data_from_last_n_days_fmtr = _supressed_data_from_last_n_days_fmtr_en
        _active_cases_fmtr = _active_cases_fmtr_en 
    else:
        raise Exception("Internal error")

def main():
    init_logger()
    
    try:
        config_files = get_args()
        config = Parameters(filenames = config_files)
        
        set_language(config.language)
                
        if config.report_dir == "@AUTO":
            out_dir = report = time.strftime("report_%y%m%d_%H%M%S")
        elif config.report_dir == "@CWD":
            out_dir = None
        else:
            out_dir = config.report_dir
        if out_dir != None:
            out_dir = os.path.abspath(out_dir)
            assert not os.path.exists(out_dir), "Report directory already exists: %s"%(out_dir)
            os.mkdir(out_dir)
            # Wait for f-ing windows to create the directory
            x = 10
            while x > 0:
                if os.path.exists(out_dir):
                    break
                time.sleep(0.05)
            assert os.path.exists(out_dir), "Windows at it again, directory was not created: %s"%(out_dir)
                
            for config_file in config_files:
                shutil.copy(config_file, os.path.join(out_dir, os.path.basename(config_file)))
        
        cwd = None
        if out_dir != None:
            cwd = os.getcwd()
        
        default_corona_data = None
        first = False
        covid19mx_reports = None
        
        for report in config.reports:
            if report.sequence_do_export and report.sequence_type == SEQUENCE_COVID19MX_REPORT_ITERATION:
                if covid19mx_reports == None:
                    covid19mx_reports = _get_covid19mx_reports()
                
                _iterate_covid19mx_reports(config_file = config, out_dir = out_dir, report = report, cwd = cwd, covid19mx_reports = covid19mx_reports)
                
            else:
                if default_corona_data == None:
                    default_corona_data = CoronaBaseData(config_file = config)
                
                try:
                    if out_dir != None: os.chdir(out_dir)
                    default_corona_data.export(report)
                finally:
                    if cwd != None: os.chdir(cwd)
                
        
    except Exception as ex:
        log.error("Caught high-level exception: %s"%(ex,))
        log.debug(traceback.format_exc())
        return 1
    return 0
    
if I_AM_SCRIPT:
    rc = main()
    if type(rc) is not int:
        rc = -1
    exit(rc)
