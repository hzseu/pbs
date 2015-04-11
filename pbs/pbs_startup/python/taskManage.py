#!/usr/bin/python

import re
import os
import sys
import subprocess
class taskManage():
    def __init__ (self):
        self.para={};
        self.snapshot={};
        self.rc=1;
        self.history=[];

    def make_cmd (self, cmd_template):
        cmd=[];
        for i in re.split(r"\s+", cmd_template):
            segment=self.make_word(i);
            if segment != '' :
                cmd.append(self.make_word(i));
        return cmd

    def make_word (self, string):
        optional_flag=False;
        key_not_exist_flag=False;
        key_empty_flag=False;
        if string[0]=='?':
            optional_flag=True;
        res_string=re.sub("^\?","",string);
        reg_key=re.compile("@([A-Za-z0-9_\-]+)@");
        while True:
            key_match=reg_key.search(res_string);
            if not key_match:
                break
            key=key_match.group(1);
            replace_key=re.compile("@"+key+"@");
            if not self.para.has_key(key):
                key_not_exist_flag=True;
                res_string=replace_key.sub("",res_string);
            else:
                if str(self.para[key])=='' :
                    key_empty_flag=True;
                res_string=replace_key.sub(str(self.para[key]),res_string);
            
        if optional_flag and key_not_exist_flag:
            return '';
        return res_string;
    
    def eval_cmd (self, cmd_template, bg=False):
        ''' use to snap the stdout of a command
        rc code is stored '''
        
        cmd=self.make_cmd(cmd_template);
        task=subprocess.Popen(cmd,shell=False, stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE);
        if not bg :
            # self.comment=task.stderr.read();
            return task.stdout.read();
        self.history.append(cmd);        
        return "";

    def run_cmd ( self, cmd_template, bg=False) :
        ''' use to run_cmd,  interactive, all the stdout and stderr are not buffed'''
        cmd=self.make_cmd(cmd_template);
        task=subprocess.Popen(cmd,shell=False);
        task.communicate();
        self.history.append(cmd);
        if not bg :
            self.rc=task.wait();
            return self.rc;
        return 0;
    


class Optistruct(taskManage) :
    def __init__ (self):
        taskManage.__init__(self);
        self.command_template="@OPTISTRUCT@ -len @MEM@ -cpu @NCPUS@ @FEM_FILE@ ?@EXTRA_OPTION@"
        self.license='6200@localhost'
        self.para['NCPUS']=1
        self.para['MEM']='100M'
        self.para['OPTISTRUCT']='/usr/local/bin/optistruct';
        self.para['EXTRA_OPTION']=' -test abc -j=222 -K"574"'

    def run(self):
        os.environ['ALTAIR_LICENSE_PATH']=self.license;
        return self.run_cmd(self.command_template);

class Fluent(taskManage):
    def __init__ (self):
        taskManage.__init__(self);
        self.command_template="@FLUENT@ -t@NCPUS@ -cnf=@HOSTFILE@ -ssh @BACKGROUND@ ?@IB@ @EXTRA_OPTION@ ?@REDIRECTION@"
        self.license='6200@localhost'
        self.para['IB']='-pib'
        self.para['FLUENT']='optistruct'
        self.para['NCPUS']=10
        self.para['BACKGROUND']='-g'
        self.para['REDIRECTION']=' > a.out'
        self.para['HOSTFILE']='$PBS_NODEFILE'
    
        
        
        
        
