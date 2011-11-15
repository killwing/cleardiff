#!/usr/bin/python
import sys, os, difflib, optparse, shlex, shutil, re
from subprocess import *

class ClearDiff:
    def __init__(self, wrapcol=None):
        self.wrapcol = wrapcol
        self.makeOutdir()

    def makeOutdir(self):
        ctargs = shlex.split('cleartool catcs')
        pipe = Popen(ctargs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (out, err) = pipe.communicate()
        g = re.search(r'-mkbranch ([\w\.\_]+)', out)
        if g == None:
            return

        branch = g.group(1)
        if branch == '':
            return

        self.branch = branch

        srcdir = sys.path[0]
        outdir = os.getcwd()+'/cleardiff_'+branch
        if not os.path.exists(outdir):
            #shutil.rmtree(outdir)
            os.mkdir(outdir)
            shutil.copytree(srcdir+'/ext', outdir+'/ext')

        self.outdir = outdir


    def render(self, title, table):
        head = r'''
<html>
<head>
    <title>%s</title>
    <link type="text/css" href="ext/main.css" rel="stylesheet" />
    <script type="text/javascript" src="ext/jquery-1.7.min.js"></script>
    <script type="text/javascript" src="ext/searchhi_slim.js"></script>
    <script type="text/javascript" src="ext/base.js"></script>
    <script type="text/javascript">
        $(function() {
            $('.diff_next a').text(String.fromCharCode(8681));

            var tableId = 'table.diff';
            $(tableId).dblclick(function() {
                unhighlight($(tableId).get(0));
                localSearchHighlight(getSelectedText().trim());
            });

            //highlightKeywords(tableId, cppkeywords); //'font-weight:bold');
        });
    </script>
</head>

<body>
    <span class="diff_add">&nbsp;Added&nbsp;</span> <span class="diff_chg">&nbsp;Changed&nbsp;</span> <span class="diff_sub">&nbsp;Deleted&nbsp;</span> <span class="title">&nbsp;%s&nbsp;</span>
''' % (os.path.basename(title), title)

        foot = r'''
</body>
</html>
'''

        return head + table + foot


    def diffBranch(self): 
        print 'finding files in branch '+ self.branch + '...'
        ctargs = shlex.split('cleartool find . -branch brtype('+ self.branch +') -print')
        pipe = Popen(ctargs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (out, err) = pipe.communicate()

        files = out.split('\n')
        self.doDiff(files, '0', 'LATEST', False)

    def diffFiles(self, files, from_ver, to_ver):
        ctargs = shlex.split('cleartool ls -short ' + ' '.join(files))
        pipe = Popen(ctargs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        (out, err) = pipe.communicate()

        files = out.split('\n')
        self.doDiff(files, from_ver, to_ver, True)

    def doDiff(self, files, from_ver, to_ver, trimVer):
        print 'start diff...'
        htmlDiff = difflib.HtmlDiff(4, self.wrapcol)
        for file in files:
            file = file.strip()
            if trimVer:
                sp = file.rfind('/')
                if sp != -1:
                    file = file[0:sp]

            sp = file.find('@@')
            if sp == -1:
                #print 'ignore: '+file
                continue

            filename = file[0:sp]
            fileversion = file[sp:]
            if not os.path.exists(filename) or os.path.isdir(filename):
                print 'ignore: '+filename
                continue

            print 'diff file: '+filename
            
            fromfile = file + '/' + from_ver
            if to_ver == '':
                tofile = filename
            else:
                tofile = file + '/' + to_ver
            fromVersion = fileversion + '/' + from_ver
            toVersion = fileversion + '/' + to_ver

            fromlines = open(fromfile, 'U').readlines()
            tolines = open(tofile, 'U').readlines()

            table = htmlDiff.make_table(fromlines, tolines, fromVersion, toVersion, False)

            outfile = self.outdir+'/'+os.path.basename(filename)+'.html'
            difffile = open(outfile, 'w')
            difffile.write(self.render(filename, table))
            difffile.close()

        print 'done! diff result: ' + self.outdir


def main():

    usage = "usage: %prog [options] [files]"
    parser = optparse.OptionParser(usage)
    #parser.add_option('-k', action='store_true', default=False, help='Highlight C++ keywords')
    parser.add_option('-b', action='store_true', default=False, help='diff with branch of current view in current directory (from 0 to LATEST)')
    parser.add_option('-f', '--from', type='string', default='LATEST', help='from version to diff with files (default LATEST)')
    parser.add_option('-t', '--to', type='string', default='', help='to version to diff with files (default CURRENT)')
    parser.add_option('-w', '--wrapcolumn', type='int', default=None, help='column number where lines are broken and wrapped (default None)')
    (options, args) = parser.parse_args()

    if options.b:
        ClearDiff(options.wrapcolumn).diffBranch()
    elif len(args) != 0:
        ClearDiff(options.wrapcolumn).diffFiles(args, vars(options)['from'], options.to)
    else:
        parser.print_help()
        return

if __name__ == '__main__':
    main()

