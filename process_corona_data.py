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
#import random
import csv
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import colorama

if __name__ == "__main__":
    I_AM_SCRIPT = True
    _me = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    _my_path = os.path.dirname(sys.argv[0])
else:
    I_AM_SCRIPT = False
    _my_path = os.path.dirname(__file__)
_my_path = os.path.realpath(_my_path)

log = None

FORMAT_CSV = "csv"
FORMAT_PLOT = "plot"
FORMAT_XLSX = "xlsx"
_known_formats = (FORMAT_CSV,
                  FORMAT_PLOT,
                  FORMAT_XLSX)

TIMELINE_ORIGINAL = "original"
TIMELINE_FIRST_100_CASES = "first_100_cases"
TIMELINE_FIRST_CASE_PER_1M = "first_case_per_1m"
TIMELINE_FIRST_CASE_PER_10K = "first_case_per_10k"
TIMELINE_FIRST_CASE_PER_10M = "first_case_per_10m"
_known_timelines = (TIMELINE_ORIGINAL,
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

_float_timelines = (TIMELINE_FIRST_100_CASES,
                      TIMELINE_FIRST_CASE_PER_10K,
                      TIMELINE_FIRST_CASE_PER_10M,
                      TIMELINE_FIRST_CASE_PER_1M)

 
DATA_TOTAL_CASES_PER_1M = "total_cases_per_1m"
DATA_TOTAL_CASES_PER_10K = "total_cases_per_10k"
DATA_TOTAL_CASES_PER_10M = "total_cases_per_10m"
DATA_TOTAL_CASES = "total_cases"
DATA_NEW_CASES = "new_cases"
DATA_NEW_CASES_PER_1M = "new_cases_per_1m"
DATA_TOTAL_DEATHS_PER_1M = "total_deaths_per_1m"
DATA_TOTAL_DEATHS = "total_deaths"
DATA_NEW_DEATHS_PER_1M = "new_deaths_per_1m"
DATA_NEW_DEATHS = "new_deaths"
_known_data = (DATA_TOTAL_CASES,
               DATA_TOTAL_CASES_PER_10K,
               DATA_TOTAL_CASES_PER_10M,
               DATA_TOTAL_CASES_PER_1M,
               DATA_NEW_CASES,
               DATA_NEW_CASES_PER_1M,   
               DATA_TOTAL_DEATHS,
               DATA_TOTAL_DEATHS_PER_1M,
               DATA_NEW_DEATHS,
               DATA_NEW_DEATHS_PER_1M,            
               )
_data_type_needs_population = (DATA_TOTAL_CASES_PER_1M, 
                               DATA_TOTAL_CASES_PER_10K, 
                               DATA_TOTAL_CASES_PER_10M,
                               DATA_NEW_CASES_PER_1M,
                               DATA_TOTAL_DEATHS_PER_1M,
                               DATA_NEW_DEATHS_PER_1M,
                               )

FILTER_NONE = "none"
FILTER_TOP_MAX = "top_max"
FILTER_TOP_MAX_MX = "top_max_mx"
FILTER_COUNTRY_LIST = "country_list"
_known_filters = (FILTER_NONE,
                  FILTER_TOP_MAX,
                  FILTER_TOP_MAX_MX,
                  FILTER_COUNTRY_LIST)
_filters_with_int_arg = (FILTER_TOP_MAX,
                         FILTER_TOP_MAX_MX)
_filters_with_string_list = (FILTER_COUNTRY_LIST,
                             )

PLOT_AXIS_FONT_SIZE = 8

PLOT_STYLE_LINE = "line"
PLOT_STYLE_MARKERS = "markers"
_known_plot_styles = (PLOT_STYLE_LINE,
                      PLOT_STYLE_MARKERS,
                      )

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

DATA_SOURCE_TXT = {DATA_SOURCE_CSSEGISSANDATA : "https://github.com/CSSEGISandData/COVID-19",
                   DATA_SOURCE_OURWORLDINDATA : "https://ourworldindata.org/coronavirus-source-data"}

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
CSD_CoronaDayEntry = collections.namedtuple("OWID_CoronaDayEntry", ("total_deaths", "total_cases", "new_deaths", "new_cases", "total_recovered", "new_recovered"))

CSD_CORONA_CSV_DIRECTORY = os.path.join(_my_path, "..", "COVID-19", "csse_covid_19_data", "csse_covid_19_time_series")
CSD_CORONA_CSV_FILENAME_CONFIRMED = "time_series_covid19_confirmed_global.csv"
CSD_CORONA_CSV_FILENAME_DEATHS = "time_series_covid19_deaths_global.csv"
CSD_CORONA_CSV_FILENAME_RECOVERED = "time_series_covid19_recovered_global.csv"
CSD_CORONA_CSV_HDR_STATE = "Province/State"
CSD_CORONA_CSV_HDR_COUNTRY = "Country/Region"
CSD_CORONA_CSV_HDR_DATE_REGEX = re.compile("^[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}$")

    
PLOT_DATA_MARGIN = 0.04
PLOT_EXTERNAL_FONT_COLOR = "#FFFFFF"
PLOT_EXTERNAL_BG_COLOR = "#384048"
PLOT_GRID_COLOR = "#E0F0FF"
    
_plot_line_styles = ((2, 2, 10, 2),  # 2pt line, 2pt break, 10pt line, 2pt break
                     (1, 1,  5, 1),
                     (2, 2,  4, 2),
                     (1, 1,  2, 1),
                     (1, 1,  1, 1),
                     (2, 2,  2, 2),
                     (4, 4,  4, 4),
                     (8, 4,  8, 4),
                     )
_plot_line_markers = (".",
                      "^",
                      "v",
                      "1",
                      "3",
                      "P",
                      "*",
                      "+",
                      "x",
                      "d",
                      )
                          
def init_logger():
    global log
    
    log = logging.getLogger(_me)
    log.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    filename = _me + ".log"
    with open(filename, "w") as fh:
        fh.write("Starting on %s running from %s"%(time.ctime(), repr(sys.argv)))
    fh = logging.FileHandler(filename = filename)
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

class Report:
    
    def __init__(self, cfg_reader, section):
        self._read(cfg_reader, section)
    
    def _read(self,
              config_reader,
              section):
        self.ID = section[7:]
        
        self.data_type = config_reader.get(section, "data_type").strip()
        assert self.data_type in _known_data, "Unsupported data type: %s"%(self.data_type)

        self.timeline = config_reader.get(section, "timeline").strip()
        assert self.timeline in _known_timelines, "Unsupported timeline: %s"%(self.timeline)

        self.formats = [s.strip() for s in config_reader.get(section, "formats").split(",")]
        for format in self.formats:
            assert format in _known_formats, "Unsupported format: %s"%(format)
        
        self.filename = config_reader.get(section, "filename").strip()
        
        self.sort_columns = config_reader.get(section, "sort_columns").strip()
        assert self.sort_columns in _known_sorts, "Unsupported sort_columns: %s"%(self.sort_columns)
        
        self.filter = config_reader.get(section, "filter").strip()
        assert self.filter in _known_filters, "Unsupported filter type: %s"%(self.filter)
        
        self.filter_value = None
        if self.filter in _filters_with_int_arg or self.filter in _filters_with_string_list:
            arg = config_reader.get(section, "filter_value").strip()
            if self.filter in _filters_with_int_arg:
                arg = int(arg)
            elif self.filter in _filters_with_string_list:
                arg = [s.strip() for s in arg.split(",")]
            self.filter_value = arg
        
        if config_reader.has_option(section, "plot_x_range"):
            rng = [s.strip() for s in config_reader.get(section, "plot_x_range").strip().split(",")]
            assert len(rng) == 2, "plot_x_range must contain 2 items, not %i"%(len(rng))
            if self.timeline in _date_timelines:
                self.plot_x_range = [(time.mktime(time.strptime(d, "%y/%m/%d")) if d != "" else None) for d in rng]
            elif self.timeline in _float_timelines:
                self.plot_x_range = [(float(i) if i != "" else None) for i in rng]
            else:
                raise Exception("Don't know what type of range will be used on timeline of type %s"%(self.timeline))
        else:
            self.plot_x_range = None
            
        if config_reader.has_option(section, "plot_y_range"):
            rng = [s.strip() for s in config_reader.get(section, "plot_y_range").strip().split(",")]
            self.plot_y_range = [(float(i) if i != "" else None) for i in rng]
        else:
            self.plot_y_range = None
        
        self.plot_title = None if not config_reader.has_option(section, "plot_title") else config_reader.get(section, "plot_title")
        self.plot_subtitle = None if not config_reader.has_option(section, "plot_subtitle") else config_reader.get(section, "plot_subtitle").replace("\\n","\n")
        
        if config_reader.has_option(section, "exclude_countries"):
            exclude_countries = config_reader.get(section, "exclude_countries")
            exclude_countries = [s.strip() for s in exclude_countries.split(',')]
            self.exclude_countries = exclude_countries
        else:
            self.exclude_countries = None
            

        self.plot_style = PLOT_STYLE_LINE
        if config_reader.has_option(section, "plot_style"):
            self.plot_style = config_reader.get(section, "plot_style")
        assert self.plot_style in _known_plot_styles, "Invalid parameter plot_style: %s"%(self.plot_style, )
                
        self.plot_y_scale = PLOT_SCALE_LINEAR
        if config_reader.has_option(section, "plot_y_scale"):
            self.plot_y_scale = config_reader.get(section, "plot_y_scale")
        assert self.plot_y_scale in _known_plot_scales, "Invalid parameter plot_y_scale: %s"%(self.plot_y_scale, )
        
        
        # AXIS 2
        self.axis2_data_type = None
        if config_reader.has_option(section, "axis2_data_type"):
            self.axis2_data_type = config_reader.get(section, "axis2_data_type").strip()
            assert self.axis2_data_type in _known_data, "Unsupported axis2 data type: %s"%(self.axis2_data_type)

        if config_reader.has_option(section, "axis2_plot_y_range"):
            rng = [s.strip() for s in config_reader.get(section, "axis2_plot_y_range").strip().split(",")]
            self.axis2_plot_y_range = [(float(i) if i != "" else None) for i in rng]
        else:
            self.axis2_plot_y_range = None
        
        self.axis2_plot_style = PLOT_STYLE_LINE
        if config_reader.has_option(section, "axis2_plot_style"):
            self.axis2_plot_style = config_reader.get(section, "axis2_plot_style")
        assert self.axis2_plot_style in _known_plot_styles, "Invalid parameter axis2_plot_style: %s"%(self.axis2_plot_style, )
                
        self.axis2_plot_y_scale = PLOT_SCALE_LINEAR
        if config_reader.has_option(section, "axis2_plot_y_scale"):
            self.axis2_plot_y_scale = config_reader.get(section, "axis2_plot_y_scale")
        assert self.axis2_plot_y_scale in _known_plot_scales, "Invalid parameter plot_y_scale: %s"%(self.axis2_plot_y_scale, )
        

class Parameters:
    def __init__(self, filename):
        assert os.path.isfile(filename)
        self._filename = os.path.realpath(filename)
        self._cfg_path = os.path.dirname(self._filename)
        self._read()
    
    def _read(self):
        #parser = configparser.RawConfigParser()
        parser = configparser.ConfigParser()
        log.debug("Reading parameters from %s"%(self._filename,))
        
        #parser.read(self._filename)
        with codecs.open(self._filename, "r", "utf8") as fh:
            parser.read_file(fh)
        
        self.reports = []
        for section in parser.sections():
            log.debug("Reading section %s"%(section, ))
            if section.startswith("report_"):
                self.reports.append(Report(parser, section))
            elif section == "general":
                self.report_dir = parser.get("general", 'report_dir').strip()
            elif section == "population_name_translation":
                self._read_pop_name_xlation(parser, section)
            elif section == "csd_country_translations":
                self._read_csd_country_xlation(parser, section)
            else:
                raise Exception("Don't know how to read section %s"%(repr(section),))
        
    def _read_pop_name_xlation(self, parser, section):
        self.population_name_xlation = {}
        v = parser.get(section, "names")
        v = [s.strip() for s in v.split("\n")]
        for line in v:
            k, v = [s.strip() for s in line.split(":")]
            self.population_name_xlation[k] = v

    def _read_csd_country_xlation(self, parser, section):
        self.csd_country_xlation = {}
        self.csd_state_xlation = {}
        v = parser.get(section, "country_translations")
        v = [s.strip() for s in v.split("\n")]
        for line in v:
            k, v = [s.strip() for s in line.split(":")]
            self.csd_country_xlation[k] = v
        v = parser.get(section, "state_translations")
        v = [s.strip() for s in v.split("\n")]
        for line in v:
            k, v = [s.strip() for s in line.split(":")]
            self.csd_state_xlation[k] = v
        #print(repr(self.population_name_xlation))
        #miau
            
def strToBool(txt):
    txtl = txt.lower()
    if txtl in _true_values: return True
    if txtl in _false_values: return False
    raise Exception("Cannot convert %s to bool. Accepted values: (For True) %s, (For False) %s"
                    ""%(repr(txt), ",".join(_true_values), ",".join(_false_values),))
                   
def read_population_data(filename = None,
                         country_col = None,
                         population_col = None, 
                         population_name_xlation = None):
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
    
    return data
    
class CoronaBaseData:
    def __init__(self, config_file, csv_filename = None, data_source = DATA_SOURCE_OURWORLDINDATA):
        self.csv_filename = csv_filename
        self.data_source = data_source
        self.config_file = config_file
        
        self.population = None
        if self.data_source == DATA_SOURCE_OURWORLDINDATA:
            self._read_owid()
        elif self.data_source == DATA_SOURCE_CSSEGISSANDATA:
            self._read_csd()
        else:
            raise Exception("Uknown source: %s"%(self.data_source))
    
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
                
                prev_confirmed = confirmed
                prev_recovered = recovered
                prev_deaths = deaths
        
        log.info("Read %i entries from %s to %s"%(len(self.dates), 
                                          time.strftime("%Y/%m/%d", time.localtime(min(self.dates)))  ,
                                          time.strftime("%Y/%m/%d", time.localtime(max(self.dates)))  ))
        
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
                    
                    for index, date in date_indexes.items():
                        try:
                            num = int(row[index])
                        except ValueError as ex:
                            log.debug("Invalid value for date %s (col %i) at %s/%s (row %i): %s (%s)"
                                        ""%(time.strftime("%Y/%m/%d", time.localtime(date)),
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
                    
                except Exception as ex:
                    raise Exception("Failed to process data at row %i: %s"%(rnum, ex))
            
            dates = list(date_indexes.values())
            dates.sort()
            
            log.info("Read %i contries/states from %s to %s"%(rnum - 1, 
                                                              time.strftime("%Y/%m/%d", time.localtime(min(dates)))  ,
                                                              time.strftime("%Y/%m/%d", time.localtime(max(dates)))  ))
            
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
            
            log.info("Read %i entries from %s to %s"%(rnum - 1, 
                                                      time.strftime("%Y/%m/%d", time.localtime(min(self.dates)))  ,
                                                      time.strftime("%Y/%m/%d", time.localtime(max(self.dates)))  ))
            
    def set_country_population(self, pop_data):
        self.population = {}
        for country in self.data.keys():
            if country not in pop_data:
                log.warning("No population data available for %s"%(country))
            else:
                self.population[country] = pop_data[country]
    
    def export(self,
               report):
        log.info("-"*100)
        log.info("Runnning report %s"%(report.ID, ))
        log.debug("    Report file: %s"%(report.filename, ))
        log.debug("   Save formats: %s"%(repr(report.formats), ))
        log.debug("       Timeline: %s"%(report.timeline, ))
        log.debug("      Data type: %s"%(report.data_type, ))
        log.debug("         Filter: %s"%(report.filter, ))
        log.debug("           Sort: %s"%(report.sort_columns, ))
        log.debug("   Filter value: %s"%(repr(report.filter_value), ))
        try:
            # if country population is required, then limit the countries to export
            if report.data_type in _data_type_needs_population or \
                report.filter in _timeline_needs_population:
                countries = self._get_countries_with_population_data()
            else:
                countries = list(self.data.keys())
            
            if report.exclude_countries != None:
                new_countries = []
                for country in countries:
                    if country not in report.exclude_countries:
                        new_countries.append(country)
                    else:
                        log.warning("Skipping country %s"%(country, ))
                countries = new_countries
            
            date_domain, country_timelines = self._get_country_timelines(report.timeline, countries)
            
            report_data = []
            report_data_axis2 = None
            axis2_enabled = False
            if report.axis2_data_type != None:
                report_data_axis2 = []
                axis2_enabled = True
                
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
                                if dt == DATA_TOTAL_CASES:
                                    data = self.data[country][actual_date].total_cases
                                elif dt == DATA_TOTAL_DEATHS:
                                    data = self.data[country][actual_date].total_deaths
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
                                else:
                                    raise Exception("Unsupported data type: %s"%(dt))
                        row[country] = data
                        #data_max = data_max if data == None else (data if data_max == None else max(data, data_max))
                        #data_min = data_min if data == None else (data if data_min == None else min(data, data_min))
                    rd.append(row)
            
            # Apply filters
            # Filters are applied only for the first axis. The second one will follow
            selected_countries = self._filter_report_data(report_data, 
                                                          report.filter, 
                                                          report.filter_value,
                                                          countries)
        
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
                    y_range = self._set_range_margin(nyr, adjust_min, adjust_max)
                
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
                        axis2_y_range = self._set_range_margin(nyr, adjust_min, adjust_max)
                
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
                    x_range = self._set_range_margin(nxr, adjust_min, adjust_max)
                
                self.write_plot(report, date_domain, report_data, selected_countries, x_range, y_range, axis2_y_range = axis2_y_range, axis2_report_data = report_data_axis2)
            
        except Exception as ex:
            log.error("Failed to export data to report %s: %s"%(report.filename, ex))
            log.debug(traceback.format_exc())
    
    def _set_range_margin(self, rng, adjust_min, adjust_max):
        log.debug("Pre-scale:  %s"%(repr(rng)))
        delta = (rng[1] - rng[0]) * PLOT_DATA_MARGIN
        result = ((rng[0] - delta) if adjust_min else rng[0],
                  (rng[1] + delta) if adjust_max else rng[1])
        log.debug("Post-scale: %s"%(repr(result)))
        return result
        
    def write_plot(self, report, date_domain, report_data, selected_countries, x_range = None, y_range = None, axis2_y_range = None, axis2_report_data = None):
        filename = report.filename
        timeline = report.timeline
        data_type = report.data_type
        title = report.plot_title
        
        log.info("Creating plot %s" % (filename, ))
        fig, ax1 = plt.subplots()
        
        if axis2_report_data != None:
            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
        
        for index, country in enumerate(selected_countries):
            x = []
            y = []
            for date_index, adj_date in enumerate(date_domain):
                data = report_data[date_index][country]
                if data == None or \
                    (data == 0): continue
                
                if timeline in _date_timelines:
                    #x.append(datetime.datetime.strptime(adj_date,"%m/%d/%Y").date())
                    x.append(datetime.datetime.fromtimestamp(adj_date))
                else:
                    x.append(adj_date)
                y.append(data)
            
            if axis2_report_data != None:
                x2 = []
                y2 = []
                for date_index, adj_date in enumerate(date_domain):
                    data = axis2_report_data[date_index][country]
                    if data == None or \
                        (data == 0): continue
                    
                    if timeline in _date_timelines:
                        #x.append(datetime.datetime.strptime(adj_date,"%m/%d/%Y").date())
                        x2.append(datetime.datetime.fromtimestamp(adj_date))
                    else:
                        x2.append(adj_date)
                    y2.append(data)
                
            line, = ax1.plot(x, y, label=country, linewidth = 0.75 if country != "Mexico" else 1)
            if report.plot_style == PLOT_STYLE_LINE:
                line.set_dashes(_plot_line_styles[index % len(_plot_line_styles)])
            elif report.plot_style == PLOT_STYLE_MARKERS:
                line.set_dashes((0, 1))
                line.set_marker(_plot_line_markers[index % len(_plot_line_markers)])
                line.set_markersize(3 if country != "Mexico" else 4.5)
            else:
                raise Exception("Unsupported plot style: %s"%(report.plot_style, )) 
            
            if axis2_report_data != None:
                line2, = ax2.plot(x2, y2, label=country, linewidth = 0.75 if country != "Mexico" else 1)
                if report.axis2_plot_style == PLOT_STYLE_LINE:
                    line2.set_dashes(_plot_line_styles[index % len(_plot_line_styles)])
                elif report.axis2_plot_style == PLOT_STYLE_MARKERS:
                    line2.set_dashes((0, 1))
                    line2.set_marker(_plot_line_markers[index % len(_plot_line_markers)])
                    line2.set_markersize(3 if country != "Mexico" else 4.5)
                else:
                    raise Exception("Unsupported plot style for axis2: %s"%(report.axis2_plot_style, ))
                
        #plt.show()
        ax1.set_yscale(report.plot_y_scale)
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
        
        if timeline == TIMELINE_ORIGINAL:
            ax1.set_xlabel("Date", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
        elif timeline == TIMELINE_FIRST_100_CASES:
            ax1.set_xlabel("Days (0 -> First 100 total cases)", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
        elif timeline == TIMELINE_FIRST_CASE_PER_10K:
            ax1.set_xlabel("Days (0 -> First case per 10K habs)", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
        elif timeline == TIMELINE_FIRST_CASE_PER_10M:
            ax1.set_xlabel("Days (0 -> First case per 10M habs)", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
        elif timeline == TIMELINE_FIRST_CASE_PER_1M:
            ax1.set_xlabel("Days (0 -> First case per 1M habs)", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
        else:
            log.warning("No label defined for timeline type %s"%(timeline, ))

        for i in range(0, 2):
            if i == 0:
                dt = report.data_type
                ax = ax1
            else:
                if axis2_report_data == None: continue
                dt = report.axis2_data_type
                ax = ax2
            if dt == DATA_TOTAL_CASES:
                ax.set_ylabel("Total cases", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_TOTAL_CASES_PER_10K:
                ax.set_ylabel("Total cases / 10K Habs", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_TOTAL_CASES_PER_1M:
                ax.set_ylabel("Total cases / 1M Habs", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_TOTAL_CASES_PER_10M:
                ax.set_ylabel("Total cases / 10M Habs", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_NEW_CASES:
                ax.set_ylabel("New cases per day", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_NEW_CASES_PER_1M:
                ax.set_ylabel("New cases per day / 1M Habs", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_TOTAL_DEATHS:
                ax.set_ylabel("Total deaths", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_TOTAL_DEATHS_PER_1M:
                ax.set_ylabel("Total deaths / 1M Habs", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_NEW_DEATHS:
                ax.set_ylabel("New deaths per day", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            elif dt == DATA_NEW_DEATHS_PER_1M:
                ax.set_ylabel("New deaths per day / 1M Habs", fontsize=PLOT_AXIS_FONT_SIZE, color=PLOT_EXTERNAL_FONT_COLOR)
            else:
                log.warning("No label defined for data type %s"%(dt, ))
    
        if x_range != None:
            if timeline in _date_timelines:
                ax1.set_xlim([datetime.datetime.fromtimestamp(d) for d in x_range])
            else:
                plt.xlim(x_range)
        else:
            log.debug("Setting X axis multiplier")
            ax1.set_xmargin(PLOT_DATA_MARGIN)
        if y_range != None:
            ax1.set_ylim(y_range)
        else:
            ax1.set_ymargin(PLOT_DATA_MARGIN)
            log.debug("Setting Y axis multiplier")
        if axis2_report_data != None:
            if axis2_y_range != None:
                ax2.set_ylim(axis2_y_range)
            else:
                ax2.set_ymargin(PLOT_DATA_MARGIN)
                log.debug("Setting Y2 axis multiplier")
        
        if timeline in _date_timelines:
            #ax1.format_xdata = mdates.DateFormatter('%Y-%m-%d')
            formatter = mdates.DateFormatter("%y/%m/%d")
            ax1.xaxis.set_major_formatter(formatter)
        
        ax1.grid(True, color=PLOT_GRID_COLOR)
        fig.set_facecolor(PLOT_EXTERNAL_BG_COLOR)
        #plt.tight_layout()
        
        ax1.legend(fontsize=PLOT_AXIS_FONT_SIZE)
        
        if True or report.plot_y_scale == PLOT_SCALE_LOG:
            ax1.yaxis.set_major_formatter(ticker.FuncFormatter(self.format_log_scale))
        
        plt.gcf().text(0.01, 0.01, "Data Source: %s"%(DATA_SOURCE_TXT.get(self.data_source, "UNK_%s"%(self.data_source))), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        plt.gcf().text(0.01, 0.98, "github.com/tonioluna/corona_graphs", fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        plt.gcf().text(0.8, 0.01, time.strftime("Generated on %Y/%m/%d %H:%M"), fontsize=5, color=PLOT_EXTERNAL_FONT_COLOR)
        
        log.info("Writting plot to file")
        plt.savefig(fname = filename + ".png", dpi=600, facecolor=fig.get_facecolor(), edgecolor='none')
        
    def format_log_scale(self, x, pos=None):
        def round_to_int(n):
            if n%1 == 0:
                return int(n)
            return n
        
        if x >= 1000000: 
            r = "%sM"%(round_to_int(x/1000000))
        elif x >= 1000: 
            r = "%sK"%(round_to_int(x/1000))
        elif x >= 1: 
            r = "%s"%(round_to_int(x))
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
        elif filter in (FILTER_TOP_MAX, FILTER_TOP_MAX_MX):
            assert type(filter_value) == int, "Filter value must be an integer"
            max_country_values = {}
            # get the maximum value per country across all dates
            for country in report_countries:
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
            if len(tmp_country_list) > filter_value:
                tmp_country_list = tmp_country_list[:filter_value]
            if filter == FILTER_TOP_MAX_MX and "Mexico" in report_countries:
                tmp_country_list.append("Mexico")
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
            return time.strftime("%Y/%m/%d", time.localtime(date))
        if timeline in (TIMELINE_FIRST_100_CASES, TIMELINE_FIRST_CASE_PER_1M, TIMELINE_FIRST_CASE_PER_10K, TIMELINE_FIRST_CASE_PER_10M):
            return "%i Days"%(date, )
    
        raise Exception("Unsupported timeline: %s"%(timeline,))
        
    def _get_country_timelines(self, 
                               timeline,
                               selected_countries):
        country_timelines = {}
        
        if timeline == TIMELINE_ORIGINAL:
            base_timeline = {}
            for date in self.dates:
                # The key on the dictionary represents the adjusted date
                base_timeline[date] = date
            for country in selected_countries:
                country_timelines[country] = base_timeline
        elif timeline == TIMELINE_FIRST_100_CASES:
            # Lookup on each country when these got 100 cases or more
            for country in selected_countries:
                log.debug("Country timeline for first 100 cases: %s"%(country, ))
                _100_cases_index = None
                for index, date in enumerate(self.dates):
                    if date in self.data[country] and self.data[country][date].total_cases >= 100:
                        _100_cases_index = index
                        break
                if _100_cases_index == None:
                    continue
                timeline = {}
                for index, date in enumerate(self.dates):
                    days = index - _100_cases_index
                    log.debug("%s, %i days"%(time.strftime("%Y/%m/%d", time.localtime(date)), days))
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
                for index, date in enumerate(self.dates):
                    if date in self.data[country] and \
                        (self.data[country][date].total_cases / (self.population[country] / pop_div)) >= 1:
                        _100_cases_index = index
                        break
                if _100_cases_index == None:
                    continue
                timeline = {}
                for index, date in enumerate(self.dates):
                    days = index - _100_cases_index
                    log.debug("%s, %i days"%(time.strftime("%Y/%m/%d", time.localtime(date)), days))
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
             
def main():
    init_logger()
    
    try:
        config_file = os.path.abspath(CONFIG_FILE)
        config = Parameters(filename = config_file)
        
        population_data = read_population_data(population_name_xlation = config.population_name_xlation)
        
        data_source = DATA_SOURCE_CSSEGISSANDATA
        #data_source = DATA_SOURCE_OURWORLDINDATA
        
        corona_data = CoronaBaseData(data_source = data_source, config_file = config)
        corona_data.set_country_population(population_data)
        
        if config.report_dir == "@AUTO":
            dir = report = time.strftime("report_%y%m%d_%H%M%S")
        elif config.report_dir == "@CWD":
            dir = None
        else:
            dir = config.report_dir
        if dir != None:
            dir = os.path.abspath(dir)
            assert not os.path.exists(dir), "Report directory already exists: %s"%(dir)
            os.mkdir(dir)
            # Wait for f-ing windows to create the directory
            x = 10
            while x > 0:
                if os.path.exists(dir):
                    break
                time.sleep(0.05)
            assert os.path.exists(dir), "Windows at it again, directory was not created: %s"%(dir)
                
            os.chdir(dir)
        
        shutil.copy(config_file, os.path.join(dir, os.path.basename(config_file)))
        
        for report in config.reports:
            corona_data.export(report)
        
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
