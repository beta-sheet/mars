# python interface to bash scripts for pdf operations

import os
import subprocess
import shutil


# lars evince (no tmp file produced, hence no tagging)
def lars_evince (codes, srcpath):

   script = srcpath + "/lars_evince.sh"

   for c in codes:
      subprocess.check_call(['bash', script, c])


# copy pdfs to working dir
def lars_extract (codes, srcpath, tag):

   script = srcpath + "/lars_extract.sh"

   for c in codes:
      subprocess.check_call(['bash', script, c])

   if tag:
      
      script = srcpath + "/lars_tag.sh"

      for c in codes:
         filename = c + ".pdf"
         subprocess.check_call(['bash', script, filename,c])


# make pdf-first-pages summary
def lars_sum (codes, path, tag, outfile):

   # get WD
   cwd = os.getcwd()

   srcpath = path + "/src"
   tmppath = path + "/tmp"

   # first, we extract the pdfs to a dir in tmp
   os.chdir(tmppath)

   tmpdir = tmppath + "/sum_" + str(os.getpid())
   os.mkdir(tmpdir)
   os.chdir(tmpdir)

   lars_extract(codes, srcpath, tag)

  # call sum script to extract 1st pages
   os.chdir(cwd)

   script = srcpath + "/lars_sum.sh"
   subprocess.check_call(['bash', script, tmpdir, outfile])

   # clean up
   shutil.rmtree(tmpdir)
