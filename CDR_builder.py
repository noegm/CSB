# -*- coding: utf-8 ner-*- 
import configparser
import argparse
from datetime import datetime
from datetime import timedelta
from string import Template
import uuid, random

obs= {}
obs["BR"]={"zone":"sa-brazil-1", "area":"sa-brazil-1a"}
obs["CL"]={"zone":"sa-chile-1", "area":"sa-chile-1a"}
obs["MX"]={"zone":"na-mexico-1", "area":"na-mexico-1a"}
obs["PE"]={"zone":"sa-peru-1", "area":"sa-peru-1a"}
obs["AR"]={"zone":"sa-argentina-1", "area":"sa-argentina-1a"}
obs["US"]={"zone":"na-usa-1", "area":"sa-usa-1a"}
obs["ES"]={"zone":"eu-spain-1", "area":"eu-spain-1a"}

parser = argparse.ArgumentParser()
parser.add_argument("confFile", help="configuration File: day range, OBs scope, subscriptions")
parser.add_argument("cdrTemplate", help="cdr Template by subscription. It will be replicated for every subscription")

args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.confFile)

for st in config.sections():
    for pa in config[st]: print (pa, config[st][pa])

ob_source_list = config["OBs"]["ob_source_list"].split(',')
ob_destiny_list = config["OBs"]["ob_destiny_list"].split(',')
xdomain_list = config["Subscriptions"]["subs_list"].split(',')

ini_date = datetime(int(config["Dates"]["date"][0:4]), int(config["Dates"]["date"][4:6]), int(config["Dates"]["date"][6:8]))

template_file = open(args.cdrTemplate, 'r')

count_id = 0  #'{:0>6}'.format(count_id)
timeTemp = datetime.now()
timeNowToFile = timeTemp.strftime("%H%M%S")

file_lines = template_file.readlines()

for ob_d in ob_destiny_list:

    for ob_s in ob_source_list:

        for use_date in (ini_date + timedelta(days=x) for x in range(0, config.getint("Dates","number_of_dates"))):

            report_date = use_date + timedelta(days=1)

            # f_name = HWS_${ob_source}_${ob_destiny}_${report_date}_${count_id}.csv
            csv_filename = Template(config["File"]["f_name"]).substitute(
                                                                ob_source=ob_s.strip(),
                                                                ob_destiny=ob_d.strip(),
                                                                report_date='{:%Y%m%d}'.format(report_date),
                                                                count_id='{:0>6}'.format(count_id),
		                                                timeNowToFile=timeNowToFile)
            print (csv_filename)

            csv_file = open(csv_filename, 'w')

            count_id += 1

            csv_lines = [Template(config["File"]["f_header"]).substitute(report_date='{:%Y%m%d}'.format(report_date))]
            csv_file.write(csv_lines[0]+'\n')

            for xdomain in xdomain_list:

                # project_id hex de 32 dígitos. Lo implemento como 4 bloques de 8 dígitos. 16^8 = 4294967296
                project_id = '{:0>8x}{:0>8x}{:0>8x}{:0>8x}'.format(random.randrange(4294967296),
                                                                    random.randrange(4294967296),
                                                                    random.randrange(4294967296),
                                                                    random.randrange(4294967296))

                for fline in file_lines:

                    csv_line = Template(fline).safe_substitute(
                                                    report_date='{:%Y%m%d}'.format(report_date),
                                                    project_id=project_id,
                                                    xdomain=xdomain.strip(),
                                                    ob_destiny=ob_d.strip(),
                                                    ob_source_zone=obs[ob_s.strip()]["zone"],
                                                    ob_source_area=obs[ob_s.strip()]["area"],
                                                    use_date='{:%Y%m%d}'.format(use_date))

                    csv_lines.append(csv_line)
                    csv_file.write(csv_line)
                #Template file does not have new line character at the end of the last record, so ....
                csv_file.write('\n') 
            csv_lines.append(Template(config["File"]["f_footer"]).substitute(report_date='{:%Y%m%d}'.format(report_date), data_lines=str(len(csv_lines)-1)))
            csv_file.write(csv_lines[len(csv_lines)-1])

            print (csv_lines)

            csv_file.close()

template_file.close()


