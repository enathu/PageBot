# -----------------------------------------------------------------------------
#
#     P A G E B O T
#
#     Copyright (c) 2016+ Type Network, www.typenetwork.com, www.pagebot.io
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
#     builddoc.py
#
#    
#    Run through the entire PageBot source tree. Run all .py for unit-test errors.
#    Create TOC.md and TOC.pdf in every folder, with descriptions of all code in 
#    that folder. The docs contains an HTML with all PageBot info.
#    If scripts make images in the local gallery folder with the same name as the
#    script, then use that image in the example.
#    Note that this applications script is an example of PageBot functions in itself.
# 
import runpy

import os   
import pagebot
from pagebot.publications.publication import Publication

SKIP = ('app', '_export', 'resources', 'pagebotapp', 'contributions', 'OLD', 'scripts-in-progress',
    'examples-in-progress', 'canvas3d', 'pagebotdoc.py')

class Node(object):
    """The *Node* class is used to build the PageBot file tree, for cleaning doc-building
    and unit tests.

    >>> improt pagebot
    >>> rootPath = pagebot.getRootPath()
    >>> node = Node(rootPath)
    >>> print node
    """
    def __init__(self, path=None):
        self.path = path
        self.nodes = []
        extension = None
        if path is not None and not os.path.isdir(path):
            extension = path.split('.')[-1]
        self.extension = extension # If filled, it's a folder. otherwise it's a file.
    
    def __repr__(self):
        return self.path
        
    def append(self, path):
        node = Node(path)
        self.nodes.append(node)
        return node
    
    def __eq__(self, node):
        return self.path == node.path
            
    def __ne__(self, node):
        return self.path != node.path
            
    def __le__(self, node):
        return self.path <= node.path
            
    def __lt__(self, node):
        return self.path < node.path
            
    def __ge__(self, node):
        return self.path >= node.path
            
    def __gt__(self, node):
        return self.path > node.path
            
class PageBotDoc(Publication):
    
    def __init__(self):
        Publication.__init__(self)

    def buildNode(self, node, level=0):
        print '\t'*level + `node`
        for child in sorted(node.nodes):
            self.build(child, level+1)        

    def build(self):
        # Collect data from all folders.
        rootPath = pagebot.getRootPath()
        rootNode = self.processPath(rootPath)
        self.buildNode(rootNode)
    
    def clearPyc(self, path=None):
        if path is None:
            path = pagebot.getRootPath()
        for fileName in os.listdir(path):
            filePath = path + '/' + fileName
            if fileName.startswith('.') or fileName in SKIP:
                continue
            if os.path.isdir(filePath):
                self.clearPyc(filePath)
            elif fileName.endswith('.pyc'):
                os.remove(filePath)
                print '#### Removed', filePath
                continue
            
    def processPath(self, path=None, node=None):
        if path is None:
            path = pagebot.getRootPath()
        if node is None:
            node = Node('root')
        
        for fileName in os.listdir(path):
            filePath = path + '/' + fileName
            if fileName.startswith('.') or fileName in SKIP:
                continue
            child = node.append(filePath)
            if os.path.isdir(filePath):
                self.processPath(filePath, child)
            if filePath.endswith('.py'):
                try:
                    runpy.run_path(filePath)
                except:
                    print 'Run', filePath
                    runpy.run_path(filePath)
                                  
        return node
    
    def runModules(self, m, level=0):
        #help(m)
        print m.__doc__
        
    
DO_CLEAR = False
CHECK_ERRORS = True
RUN_MODULES = False
if __name__ == '__main__':
    # Execute all cleaning, docbuilding and unittesting here.
    pbDoc = PageBotDoc()
    if DO_CLEAR:
        pbDoc.clearPyc()
    if CHECK_ERRORS:
        pbDoc.processPath()
    if RUN_MODULES:
        pbDoc.runModules(pagebot)

    print 'Done'
      