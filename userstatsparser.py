#!/usr/bin/python

import csv
from operator import itemgetter
import datetime
import time
import math
import colorsys
from scipy import stats
import numpy as np
import json
from pylab import *
import os
import glob
import fnmatch
import argparse

parser = argparse.ArgumentParser(description='Process userstats.csv into a pretty web display.')
parser.add_argument('infile', help='input file')
parser.add_argument('outpath', help='path for output')
parser.add_argument('region_name', help='the name your region will appear as')
args = parser.parse_args()


fignames=["nwr","ncur","wcur","relcur"]

# for the wedge labels
def val_autopct(pct):
    total=sum(ar)
    val=int(pct*total/100.0)
    return val


# nasty looking!
def parse_csv(c):
    try:
        return int(c)
    except ValueError:
        try:
            return float(c)
        except ValueError:
            try:
                return datetime.datetime(*time.strptime(c, "%m/%d/%Y")[0:5])
            except ValueError:
                return c

def int_wrapper(reader):
    for v in reader:
        yield map(parse_csv,v)
        

with open(args.infile, 'rb') as f:
	reader = csv.reader(f, delimiter = '\t')
	next(reader, None)
	reader = int_wrapper(reader)
	sr = sorted(reader, key=itemgetter(13), reverse=True)
	lastdate = max(map(itemgetter(12),sr))
	firstdate = min(map(itemgetter(11),sr))
	avgdailyeditslist = map(itemgetter(16),sr)
	maxavgdailyedits = max(map(itemgetter(16),sr))
	totaleditslist = map(itemgetter(14),sr)
	currentobjlist = map(itemgetter(15),sr)
	delta = lastdate-firstdate
	totalusers = len(sr)
	snippet = ""
	filteredusers = 0
	lazysonsofbitches = 0
	totalnodes = 0
	totalways = 0
	totalrelations = 0
	first = True
	for row in sr:
		if first:
			pass
			first = False
		nodes = row[2]
		totalnodes += nodes
		ways = row[5]
		totalways += ways
		relations = row[8]
		totalrelations += relations
		currentobjs = row[15]
		if currentobjs < 20:
			filteredusers += 1
		if nodes+ways+relations <= 1 :
			lazysonsofbitches += 1
	
	# replace datetimes with timestamps that JS can read. 
	dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

	usefulstats=[firstdate,lastdate,totalnodes,totalways,totalrelations,totalusers,filteredusers,lazysonsofbitches]
	y=0
	for step in range(delta.days, 0, -365): # not quite a year but close enough
		div = float(step) / float(delta.days)
		stamp = "now" if y == 0 else (str(y) + "y ago") 
		percent = str(100 * float(delta.days - step) / float(delta.days))
		snippet += "<div class=\"dates\" style=\"right:" + percent + "%\">" + stamp + "&nbsp;&nbsp;</div>"
		y += 1
	with open(os.path.join(args.outpath, 'index.html'),'w') as htmlout:
		htmlout.write("<html><head><script language=javascript type=text/javascript src=\'pop.js\'></script><link rel=stylesheet href=\"style.css\" type=\"text/css\" media=screen><title>Brave Mappers of %s</title></head><body>%s<div id=\"title\">The brave mappers of %s<div id=\"sub\">The story of OpenStreetMap in %s in pretty shapes and colors. <a href=\"#\" onClick=\"popinfo('%s')\">more info</a></div></div><div id=logo></div><div id=info></div><div id=maininfo></div><div id=\"wrapper\">\n" % (args.region_name, snippet, args.region_name, args.region_name, json.dumps(usefulstats, default=dthandler).replace("\"","&quot;")))

		# Create the charts for each user, if they don't exist already
		rowcnt = 0
		for row in sr:
			rowcnt += 1
			chartnames=[]
			if not os.path.exists(os.path.join(args.outpath, "charts")):
				os.makedirs(os.path.join(args.outpath, "charts"))
			figcnt = 0
			for fname in fignames:
				figcnt += 1
				name = os.path.join(args.outpath, "charts", fname + str(row[0]) + ".png")
				chartnames.append(name);
				if os.path.exists(name): continue
				print "creating chart user %i/%i, chart %i/%i" % (rowcnt, len(sr), figcnt, len(fignames))
				figure(1, figsize=(6,6))
				ax = axes([0.1, 0.1, 0.8, 0.8])
				if fname == "nwr":
					ar = [row[2], row[5], row[8]]
					labels = ["nodes","ways","relations"]
					charttitle = "All edited nodes, ways, relations"
					colors = [(0.8,0.6,0.6,1),(0.6,0.8,0.6,1),(0.6,0.6,0.8,1)]
				elif fname == "ncur":
					ar = [row[2] - row[4], row[4]]
					labels = ["gone","still here"]
					charttitle = "Nodes still around" 
					colors = [(0.8,0.6,0.6,1),(1.0,0.8,0.8,1)]
				elif fname == "wcur":
					ar = [row[5] - row[7], row[7]]
					labels = ["gone","still here"]
					charttitle = "Ways still around" 
					colors = [(0.6,0.8,0.6,1),(0.8,1.0,0.8,1)]
				elif fname == "relcur":
					ar = [row[8] - row[10], row[10]]
					labels = ["gone","still here"]
					charttitle = "Relations still around" 
					colors = [(0.6,0.6,0.8,1),(0.8,0.8,1,1),(0.1,0.4,0.1,1)]
				pie(ar, explode=None, labels=labels, colors=colors, autopct=val_autopct)
				title(charttitle)
				savefig(name)
				clf()
			nodes = row[2]
			nodes_created = row[3]
			ways = row[5]
			ways_created = row[6]
			relations = row[8]
			relations_created = row[9]
			ufirst = row[11]
			ulast = row[12]
			totaledits = row[14]
			currentobjs = row[15]
			avgdailyedits = row[16]
			persistence = row[17]

			if currentobjs < 20: continue #FILTER OUT REALLY MINOR USERS

			objspercentile = stats.percentileofscore(currentobjlist,currentobjs)

			opacity = persistence
			bold = "bold" if objspercentile > 99.5 else "normal"
			perc_start = ((ufirst - firstdate).total_seconds() / delta.total_seconds()) * 100
			perc_end = 100 - ((ulast - firstdate).total_seconds() / delta.total_seconds()) * 100
			
			height = min(100, max(4,avgdailyedits))
			display = "block" if height > 14 else "none"
			fontsize = min(36,(max(10, avgdailyedits / 10))) 
			perc_nodes_created = 0 if nodes == 0 else float(nodes_created) / float(nodes)
			perc_ways_created = 0 if ways == 0 else float(ways_created) / float(ways)
			perc_relations_created = 0 if relations == 0 else float(relations_created) / float(relations)
			forgotten = 'forgotten ' if (lastdate - ulast).days > 2*365 else 'vaguely remembered ' if (lastdate - ulast).days > 90 else ''
			mayfly = 'mayfly ' if (ulast - ufirst).days < 30 else ''
			power = 'beastly ' if stats.percentileofscore(avgdailyeditslist,avgdailyedits) > 95 and stats.percentileofscore(totaleditslist, totaledits) > 96 else ''

			#distinguish between creators and modifiers
			creator = 'creator' if (perc_nodes_created + perc_ways_created + perc_relations_created) > 1 else 'improver'
			if mayfly == '' and  forgotten == '' and power == '': creator = 'fair ' + creator
			h = 0.3 if creator=='creator' else 0.6
			rgb = colorsys.hsv_to_rgb(h, 1, 1)
			colorstring = "rgb(" + str(int((rgb[0] * 255))) + "," + str(int((rgb[1] * 255))) + "," + str(int((rgb[2] * 255))) + ")"

			#append some generated figures 
			row.append(creator)
			row.append(chartnames)
			row.append(forgotten)
			row.append(power)
			row.append(mayfly)
			
			htmlout.write("<div style=\"\"><div class=\"username\" style=\"display:" + display + ";align:middle;float:left;text-align:right;font-size:" + str(fontsize) + ";opacity:" + str(opacity) + ";font-weight:" + bold + ";width:" + str(perc_start) + "%\" onClick=\"pop('" + json.dumps(row, default=dthandler).replace("\"","&quot;") + "')\">" + str(row[1]) + "&nbsp;&nbsp;</div><div onClick=\"pop('" + json.dumps(row, default=dthandler).replace("\"","&quot;") + "')\" style=\"background-color:" + colorstring + ";px;margin-left:" + str(perc_start) + "%;margin-right:" + str(perc_end) + "%;height:" + str(height) + "px;opacity:" + str(opacity) + "\" class=\"user\" id=\"" + str(row[0]) + "\"></div></div>\n")
		htmlout.write("</div></body></html>")
