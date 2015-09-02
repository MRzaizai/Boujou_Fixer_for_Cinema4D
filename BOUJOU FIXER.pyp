#=============AboutThisPlugin================
#Copyright  2015.4.18  Daniel Xiang(MRzaizai)
#BOUJOU FIXER C4D Plugin
#http://mrzaizai.lofter.com
#https://www.behance.net/MRzaizai
#=============================================

import c4d
import os
from c4d import gui, storage, documents, bitmaps, plugins
__pluginname__ = "BOUJOU FIXER"
__version__ = 1.2
__author__ = "MRzaizai"
PLUGIN_ID = 1035159

def SplitPath(path):
    if type(path) == str:
        path_dir = os.path.dirname(path)
        path_base = os.path.basename(path)
        path_name = os.path.splitext(path_base)[0]
        path_exten = os.path.splitext(path_base)[-1]
        return [path_dir, path_base, path_name, path_exten]
    else:
        raise TypeError("A string is required")

def FixBoujouFile(FilePath, SavePath):
    File = open(FilePath)#Read
    #Parse
    try:
        p = 0;NewLines = []
        print "Parsing the file........."
        for index, line in enumerate(File):
            new_1 = line.replace("ParentItem 10000001", "ParentItem 10000002")
            if "-3.141593" in line:
                p = index
            new_2 = new_1.replace("-3.141593", "0.000000", 1)
            NewLines.append(new_2)
        FixedLines = []
        for index, line in enumerate(NewLines):
            if index == p - 6 and "-0.000000" in line:
                line = "  Key 0.000000 0.000000 3 0 0 0 0 0 0\n"
                FixedLines.append(line)
            else:
                FixedLines.append(line)
    finally:
        File.close()

    #Save
    print "Writing the new file........."
    Save = open(SavePath, "w")
    Save.write(str().join(FixedLines))
    Save.close()
    print "Done!\n"
    print "New file saved to:\n" + SavePath
    
class BoujouFixer(plugins.CommandData):
    def Execute(self, doc):
        while True:
            file_path = storage.LoadDialog(type = c4d.FILESELECTTYPE_SCENES, 
                                    title = "Selecte the .c4d file you exported from boujou", 
                                    force_suffix = ".c4d")
            if type(file_path) == str and file_path != "":
                if SplitPath(file_path)[-1] != ".c4d":
                    message = gui.MessageDialog("Needs to be .c4d file", c4d.GEMB_RETRYCANCEL)
                    if message == c4d.GEMB_R_CANCEL:
                        break
                elif SplitPath(file_path)[-1] == ".c4d":
                    new_name = str().join([SplitPath(file_path)[2], "(fixed)"])
                    save_path = os.path.join(SplitPath(file_path)[0], new_name+SplitPath(file_path)[-1])
                    FixBoujouFile(file_path, save_path)
                    storage.GeExecuteProgram(storage.GeGetStartupApplication(), save_path)
                    break
            elif file_path == None:
                break
        return True

if __name__ == '__main__':
    global fixer
    fixer = BoujouFixer()
    icon = bitmaps.BaseBitmap()
    icon_path = os.path.join(SplitPath(__file__)[0], "res", "icon.png")
    icon.InitWith(icon_path)
    reg = plugins.RegisterCommandPlugin(id = PLUGIN_ID, str = __pluginname__, 
                                    help = "Fix boujou export file", 
                                    icon = icon, info = 0, dat = fixer)
    if reg == True:
        print "=" * 50
        print "%s v%s(By %s) successfully loaded! _(:з」∠)_"%(__pluginname__, __version__, __author__)
        print "=" * 50