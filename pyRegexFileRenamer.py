"""
Python-based Regex File Renamer
  by Andrew Pann

Uses:
  Python 3.5.2
  TkInter (included with Python 3)

This is a Python 3 and Tkinter port of the old .NET 2.0 (or 1.1) RegexFileRenamer utility.
"""

import os
import os.path
import sys
import re
import tkinter
import tkinter.scrolledtext
import tkinter.messagebox
import tkinter.filedialog

class RegexFileRenamer(object):

    def __init__(self):

        self.root = tkinter.Tk()
        self.root.title("Regex File Renamer")
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0,weight=1)

        self._setupMainFrame()
        self._setupWorkingDirElements()
        self._setupFindPatternElements()
        self._setupReplaceElements()
        self._setupOptionCheckboxes()
        self._setupCommandButtons()
        self._setupTextOutputBox()
        self._tweakUI()

    def run(self):
        self.root.mainloop()

    def _setupMainFrame(self):

        self.mainframe = tkinter.Frame(self.root)
        #self.mainframe.pack(fill="both",expand=True)
        self.mainframe.grid(column=0,row=0,sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))
        self.mainframe.grid_columnconfigure(0, weight=0)
        self.mainframe.grid_columnconfigure(1, weight=1)
        self.mainframe.grid_columnconfigure(2, weight=0)
        self.mainframe.grid_rowconfigure(0,weight=0)
        self.mainframe.grid_rowconfigure(1,weight=0)
        self.mainframe.grid_rowconfigure(2,weight=0)
        self.mainframe.grid_rowconfigure(3,weight=0)
        self.mainframe.grid_rowconfigure(4,weight=0)
        self.mainframe.grid_rowconfigure(5,weight=1)
        
    def _setupWorkingDirElements(self):

        self.workingDir = tkinter.StringVar()
        self.workingDir.set(os.getcwd())
        
        tkinter.Label(self.mainframe,text="Starting Folder").grid(row=0,column=0,sticky=tkinter.W)

        self.workingDirEntry = tkinter.Entry(self.mainframe,width=80,textvariable=self.workingDir)
        self.workingDirEntry.grid(row=0,column=1,sticky=(tkinter.W,tkinter.E))
        selectDirButton = tkinter.Button(self.mainframe, text="...", width=5, command=self._selectDirButtonCommand, relief=tkinter.RAISED)
        selectDirButton.grid(row=0,column=2, sticky=tkinter.W)

    def _setupFindPatternElements(self):
    
        self.findPattern = tkinter.StringVar()

        tkinter.Label(self.mainframe,text="Find Pattern").grid(row=1,column=0,sticky=tkinter.W)

        self.findPatternEntry = tkinter.Entry(self.mainframe,width=90,textvariable=self.findPattern)
        self.findPatternEntry.grid(row=1,column=1,columnspan=2,sticky=(tkinter.W,tkinter.E))

    def _setupReplaceElements(self):
        
        self.replacePattern = tkinter.StringVar()

        tkinter.Label(self.mainframe,text="Replace With").grid(row=2,column=0,sticky=tkinter.W)

        self.replacePatternEntry = tkinter.Entry(self.mainframe,width=90,textvariable=self.replacePattern)
        self.replacePatternEntry.grid(row=2,column=1,columnspan=2,sticky=(tkinter.W,tkinter.E))
        
    def _setupOptionCheckboxes(self):
        self.caseSensitiveCheckboxState = tkinter.IntVar()
        self.caseSensitiveCheckboxState.set(1)
        
        caseSensitiveCheckbox = tkinter.Checkbutton(self.mainframe,text="Case Sensitive",
                                                    variable=self.caseSensitiveCheckboxState)
        caseSensitiveCheckbox.grid(row=3,column=0,sticky=tkinter.W)

        self.recurseSubfoldersCheckboxState = tkinter.IntVar()
        
        recurseSubfoldersCheckbox = tkinter.Checkbutton(self.mainframe,text="Recurse Subfolders",
                                                        variable=self.recurseSubfoldersCheckboxState)
        recurseSubfoldersCheckbox.grid(row=4,column=0,sticky=tkinter.W)
        
    def _setupCommandButtons(self):
        # Buttons should be close together, so place in the same frame, side by side, and place the FRAME into the root grid cell.
        prButtonFrame = tkinter.Frame(self.mainframe)
        prButtonFrame.grid(row=4,column=1,columnspan=2, sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))

        # Lame hack to insert some space between the two buttons in the button-containing frame.
        prButtonFrame.columnconfigure(1,minsize=20)
        
        previewButton = tkinter.Button(prButtonFrame, text="Preview Changes", command = self._previewButtonCommand,
                                       relief=tkinter.RAISED)
        previewButton.grid(row=0,column=0, sticky=tkinter.W)

        renameFilesButton = tkinter.Button(prButtonFrame, text="Rename Files",command = self._renameFilesButtonCommand,
                                           relief=tkinter.RAISED)
        renameFilesButton.grid(row=0,column=2,sticky=tkinter.W)

    def _setupTextOutputBox(self):
        self.outputTextBox = tkinter.scrolledtext.ScrolledText(self.mainframe, height=20, width=100, state=tkinter.DISABLED, wrap=tkinter.WORD)
        self.outputTextBox.grid(row=5,column=0,columnspan=3,sticky=(tkinter.N, tkinter.W, tkinter.E, tkinter.S))

    def _tweakUI(self):
        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5,pady=5)

    def _selectDirButtonCommand(self):
        self.workingDir.set(os.path.normpath(tkinter.filedialog.askdirectory(title="Select working directory...",initialdir=os.getcwd())))

    def _processDirs(self,dirList,doRename):        
        for dirName in dirList:
            subDirList=[]
            for entry in os.scandir(dirName):
                if entry.is_dir() and self.recurseSubfoldersCheckboxState.get() == 1:
                    subDirList.append(entry.path)
                elif entry.is_file() and self.findRegex.search(entry.name):
                    newFileName = self.findRegex.sub(self.replacePattern.get(),entry.name)
                    if doRename:
                        self._writeOut("Renamed {0} to {1}\n".format(entry.path,os.path.join(dirName,newFileName)))
                        os.replace(entry.path,os.path.join(dirName,newFileName))
                        pass
                    else:
                        self._writeOut("Will rename {0} with {1}\n".format(entry.path,os.path.join(dirName,newFileName)))

            self._processDirs(subDirList,doRename)

    def _processInputs(self):
        self.reFlags = 0
        if not self.caseSensitiveCheckboxState.get():
            self.reFlags = re.IGNORECASE
    
        self.findRegex = re.compile(self.findPattern.get(),self.reFlags) 
        
    def _previewButtonCommand(self):
        self._clearOutput()
        if not self._checkInputs():
            return

        self._processInputs()
        self._processDirs([self.workingDir.get()],False)
                                                       
    def _renameFilesButtonCommand(self):
        self._clearOutput()
        if not self._checkInputs():
            return

        self._processInputs()
        self._processDirs([self.workingDir.get()],True)

    def _clearOutput(self):
        self.outputTextBox.configure(state=tkinter.NORMAL)
        self.outputTextBox.delete(1.0,tkinter.END)
        self.outputTextBox.configure(state=tkinter.DISABLED)    

    def _writeOut(self,text=""):
        self.outputTextBox.configure(state=tkinter.NORMAL)
        self.outputTextBox.insert(tkinter.END,text)
        self.outputTextBox.configure(state=tkinter.DISABLED)    
        

    def _checkInputs(self):
        '''
        Returns True on valid inputs.
        '''
        if self.findPattern.get() == "":
            tkinter.messagebox.showerror(title="Missing Input",message="Please specify a find pattern.",parent=self.root)
            return False
        elif self.replacePattern.get() == "":
            tkinter.messagebox.showerror(title="Missing Input",message="Please specify a replacement string/pattern.",parent=self.root)
            return False
        elif self.workingDir == "":            
            tkinter.messagebox.showerror(title="Missing Input",message="Please specify a working directory.",parent=self.root)
            return False
        else:
            return True
        

if __name__ == '__main__':

    try:
        rfr = RegexFileRenamer()
        rfr.run()
    except Exception as e:
        tkinter.messagebox.showerror(title="Fatal error - Sorry!",message=str(e))
    

