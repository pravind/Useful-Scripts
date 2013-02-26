import re
import sys
import string
from sh import svn
from sh import rm



def error_handler(e):
    print 'In error handler'
    print e

def output(e):
    print 'in out put'
    
def svn_cleanup():
    try:
        svn("cleanup")
    except:
        print "svn cleanup failed" 
    else:
        print "svn cleanup succeeded"

def handle_unversionedFile(error):
    """Get the file name and delete it, along with its associated files"""
    filePath = error[error.find("'") + 1:error.rfind("'")]
    """if filePath.rfind("-expected"):
        files = filePath[:filePath.rfind("-expected")]
    else:
        files = filePath[:filePath.rfind(".")]
    files = files + '*'
    print files
    #might want to put it in a try catch
    #rm(files,"-v")"""
    rm(filePath)

               
def update(version):
    """ Updates the current copy to the given version"""
    print 'Updating to version ' + version
    #return
    try:
        print 'Calling svn up'
        svn('up','-r',version)
    except Exception, e: 
        if re.search("svn cleanup" , e.stderr):
            print e.stderr
            print 'Calling svn cleanup'
            svn_cleanup()
            return 1
            #update(version)
        elif re.search("already exists",e.stderr):
            print e.stderr
            handle_unversionedFile(e.stderr)
            return 2
        elif re.search("Secure connection truncated", e.stderr) or re.search("503 Service Unavailable",e.stderr):
            print e.stderr
            return 3
            #update(version)
        else:
            print e.stderr
            return 4
    else:
        return 0    

def update_to_version(version):
    ret = update(version)
    while ret and ret != 4:
        ret = update(version)
    if not ret:
        print 'Success I think'
    else:
        print 'Some random error :( '    
    
if __name__ == "__main__":
    if len(sys.argv) == 2:
        update_to_version(sys.argv[1])
    else:
        print "Usage: python svn-up.py <revision>"    
