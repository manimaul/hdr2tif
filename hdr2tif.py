#!/usr/bin/python

'''
Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>
Published under the terms of "Simplified BSD License".
License text available at http://opensource.org/licenses/bsd-license.php
'''

import getopt, sys
from os.path import join, getsize, exists, expanduser
from os import walk, getcwd, system, mkdir, listdir, remove
from magic import open as magicopen, MAGIC_NONE
from string import ascii_uppercase

class hdr:
	def __init__(self, indir=getcwd(), outdir=getcwd()+'/TIFS'):
		self.rscan(indir) #finds dirs containin files ending with .A01 that are PCX type

		print '\nTiff files will be created in:'
		print outdir
		
		if not exists(outdir):
			mkdir(outdir)
		self.outdir = outdir

		print '\nFound ' + str(self.folderPaths.__len__()) + ' folders in:'
		print indir

		print 'containing HDR/PCX files.'
		for folder in self.folderPaths:
			self.convert(folder)

	def convert(self, folder):
		fname = folder[folder.rfind('/')+1:folder.__len__()]
		print 'operating on: ' + fname
		outdir = self.outdir+'/'+fname
		try:
			mkdir(outdir)
		except:
			pass
		self.removePCX(outdir)
		for letter in self.letterlist(folder, fname):
			print 'Joining row ' + letter
			cmd = 'convert %s/%s.%s* -append %s/%s/%s.pcx' %(folder, fname, letter, self.outdir, fname, letter)
			system(cmd)
		print 'compiling pcx'
		cmd = 'convert %s/*.pcx +append %s/%s.pcx' %(outdir, outdir, fname)
		system(cmd)
		print 'converting gif'
		cmd = 'convert %s/%s.pcx -font courier -fill red -gravity SouthEast -pointsize 30 -annotate +3+18 \'Manimaul\' %s/%s.gif' %(outdir, fname, outdir, fname)
		system(cmd)
		print 'converting tif'
		cmd = 'convert %s/%s.gif -colors 127 %s/%s.tif' %(outdir, fname, outdir, fname)
		system(cmd)
		print 'converting png'
		cmd = 'convert %s/%s.gif -colors 127 %s/%s.png' %(outdir, fname, outdir, fname)
		system(cmd)
		print 'cleaning up'
		self.removePCX(outdir)
		print 'Your files were created here: ' + outdir

	def removePCX(self, folder):
		for f in listdir(folder):
			if f.endswith('.pcx'):
				remove(folder+'/'+f)
		
	def rscan(self, indir):
		self.folderPaths = []
		#get all folders(recursive) that contain HDR/PCX files
		for root, dirs, files in walk(indir):
			for file in files:
				if file.endswith('.A01') and self.isPCX(root+'/'+file):
					self.folderPaths.append(root)

	def letterlist(self, folder, fname):
		lst = []
		f = folder+'/'+fname
		for letter in ascii_uppercase:
			x = f+'.'+letter+'01'
			if exists(x):
				lst.append(letter)
		return lst


	def isPCX(self, filename):
		ms = magicopen(MAGIC_NONE)
		ms.load()
		ftype =  ms.file(filename)
		ms.close()
		if ftype is not None:
			if ftype[0:3] == 'PCX':
				return True
			else:
				return False

def opt():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
	global outd
	global ind
    outd = outd=expanduser('~/HDR2TIF')
    ind = ''
    for o, a in opts:
        if o == "-i":
            ind = a
        elif o == "-o":
            outd = a
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        else:
			assert False, "unhandled option"

def usage():
	print 'usage: hdr2tif -i [path containing HDR charts] -o [path to output TIFS and PNGS]'
	print '       if -o is not specified path to output defaults to ' + outd

if __name__ == '__main__':
    opt()
    if exists(ind):
        if not ind.endswith('/'):
            ind += '/'
        print ind
        if not outd.endswith('/'):
            outd += '/'
        print outd
        hdr(ind, outd)
    else:
        print 'Please specify a valid input directory.\nExemple: hdr2tif.py -i ' + expanduser('~') + '/some/path/to/hdr/charts'
	

