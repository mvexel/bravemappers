#!/usr/bin/python

import os, subprocess, fnmatch
from Queue import Queue
from threading import Thread

INPATH = '/osm/planet/us/140331-historical/us'
OUTBASEPATH = '/osm/out/userstats/'
OSMJSCRIPT = '/osm/software/OSMQualityMetrics/UserStats.js'
OSMJSEXEC = '/osm/software/osmium/osmjs/osmjs'
USERSTATS_OUTPATH = '/osm/tmp/userstats.csv'
WORKER_THREADS = 16

def worker():
    while True:
        item = q.get()
        process(item)
        q.task_done()

def process(infile):
	statename = infile.split('/')[-1].split('.')[0]
	print 'doing ' + statename
	outdir = os.path.join(OUTBASEPATH, statename)
	if not os.path.exists(outdir):
		print 'creating %s' % outdir
		os.makedirs(outdir)
	elif os.path.exists(os.path.join(outdir, 'userstats.csv')):
		print '%s done, moving along..' % statename
		return
	print 'processing %s...' % statename
	subprocess.call((OSMJSEXEC, '-j', OSMJSCRIPT, infile))
	os.rename(USERSTATS_OUTPATH, os.path.join(outdir, 'userstats.csv'))

if not os.path.exists(OUTBASEPATH):
    os.makedirs(OUTBASEPATH)
	
q = Queue()

for i in range(WORKER_THREADS):
     t = Thread(target=worker)
     t.daemon = True
     t.start()

files = []
for root, dirnames, filenames in os.walk(INPATH):
	for filename in fnmatch.filter(filenames, '*.osm.pbf'):
		files.append(os.path.join(root, filename))

for item in files:
    q.put(item)

q.join()