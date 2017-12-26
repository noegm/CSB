# -*- coding: utf-8 -*-
import configparser
import argparse
import re
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
obs["US"]={"zone":"na-usa-1", "area":"na-usa-1a"}
obs["ES"]={"zone":"eu-spain-1", "area":"eu-spain-1a"}

res_rgxp = re.compile("\${(.*)}")
parser = argparse.ArgumentParser()
parser.add_argument("confFile", help="configuration File: day range, OBs scope, subscriptions")
parser.add_argument("cdrTemplate", help="cdr Template by subscription. It will be replicated for every subscription")

args = parser.parse_args()

config = configparser.ConfigParser()
config.read(args.confFile)

for st in config.sections():
    print (st)
    for pa in config[st]: print (pa, config[st][pa])

ob_source_list = config["OBs"]["OB_source_list"].split(',')
ob_destiny_list = config["OBs"]["OB_destiny_list"].split(',')
xdomain_list = config["Subscriptions"]["subs_list"].split(',')

template_dict = dict()

ini_date = datetime(int(config["Dates"]["date"][0:4]), int(config["Dates"]["date"][4:6]), int(config["Dates"]["date"][6:8]))

template_file = open(args.cdrTemplate, 'r')

count_id = 0  #'{:0>6}'.format(count_id)

file_lines = template_file.readlines()

resIds_dict = dict()
# Resource Id calculation
for fline in file_lines:
    if fline.split(' | ')[10] != '':
        resId_code = res_rgxp.match(fline.split(' | ')[10]).group(1)
        resIds_dict[resId_code] = dict()

        for xd in xdomain_list:

            resIds_dict[resId_code][xd] = uuid.uuid4()



for ob_d in ob_destiny_list:

    template_dict["ob_destiny"] = ob_d.strip()

    for ob_s in ob_source_list:

        template_dict["ob_source_zone"] = obs[ob_s.strip()]["zone"]
        template_dict["ob_source_area"] = obs[ob_s.strip()]["area"]

        for use_date in (ini_date + timedelta(days=x) for x in range(0, config.getint("Dates","number_of_dates"))):

            template_dict["use_date"] = '{:%Y%m%d}'.format(use_date)
            template_dict["report_date"] = '{:%Y%m%d}'.format(use_date + timedelta(days=1))
            template_dict["past_use_date"] = '{:%Y%m%d}'.format(use_date - timedelta(days=1))



            # f_name = HWS_${ob_source}_${ob_destiny}_${report_date}_${count_id}.csv
            csv_filename = Template(config["File"]["f_name"]).substitute(
                                                                ob_source=ob_s.strip(),
                                                                ob_destiny=ob_d.strip(),
                                                                report_date=template_dict["report_date"],
                                                                count_id='{:0>6}'.format(count_id))
            print (csv_filename)

            csv_file = open(csv_filename, 'w')

            count_id += 1

            csv_lines = [Template(config["File"]["f_header"]).substitute(report_date=template_dict["report_date"])]
            csv_file.write(csv_lines[0]+'\n')

            for template_dict["xdomain"] in xdomain_list:

                # project_id hex de 32 dígitos. Lo implemento como 4 bloques de 8 dígitos. 16^8 = 4294967296
                template_dict["project_id"] = '{:0>8x}{:0>8x}{:0>8x}{:0>8x}'.format(random.randrange(4294967296),
                                                                    random.randrange(4294967296),
                                                                    random.randrange(4294967296),
                                                                    random.randrange(4294967296))

                for fline in file_lines:

                    #Only uses with resourceId
                    if fline.split(' | ')[10] != '':
                        resId_code = res_rgxp.match(fline.split(' | ')[10]).group(1)
                        template_dict[resId_code] = resIds_dict[resId_code][template_dict["xdomain"]]

                    csv_line = Template(fline).safe_substitute(template_dict)

                    csv_lines.append(csv_line)
                    csv_file.write(csv_line)
                #Template does not have NewLine character at the end of last record, so ...
                csv_file.write('\n')
            csv_lines.append(Template(config["File"]["f_footer"]).substitute(report_date=template_dict["report_date"], data_lines=str(len(csv_lines)-1)))
            csv_file.write(csv_lines[-1])

            print (csv_lines)

            csv_file.close()

template_file.close()
