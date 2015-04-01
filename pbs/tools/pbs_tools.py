#!/usr/bin/python 


import sys;
import os;
import subprocess
import re;



class pbs_tools(): 
	def __init__ (self):
		self.set_pbs_env;	
		self.table={};
		self.table['pbsnodes']=self.get_node_table();
		self.sep=';'
		self.pestat_default=['Mom','state','resources_available.pas_applications_enabled','resources_available.platform','resources_available.ncpus','resources_assigned.ncpus','resources_available.mem','resources_assigned.mem','jobs']

		self.table['job']=self.get_job_table();
	def set_pbs_env(self):
		f=open("/etc/pbs.conf","w");
		for i in f.readlines(): 
			pair=i.split("=");
			os.environ[pair[0]]=pair[1];
		os.environ['PATH']=os.environ['PBS_EXEC']+"bin:"+os.environ['PATH'];
	def pbsnodes (self, args='-av'): 
		cmd=['pbsnodes' , args];
		pbsnodes_task=subprocess.Popen(cmd,shell=False, stdout=subprocess.PIPE);
		pbs_node_out,pbs_node_err=pbsnodes_task.communicate();
		return pbs_node_out,pbs_node_err
		
	def qstat(self, args='-f') : 
		cmd=['qstat', args];
		qstat_task=subprocess.Popen(cmd,shell=False,stdout=subprocess.PIPE);
		qstat_out,qstat_err=qstat_task.communicate();
		cl_reg=re.compile("\n\t");
		qstat_out_2=cl_reg.sub("",qstat_out);
		return qstat_out_2,qstat_err
		
	def get_node_table(self): 
		pbs_nodes_table={}
		current_host='';
		output,error=self.pbsnodes();
		host_reg=re.compile("^[A-Za-z0-9]+");
		res_reg=re.compile("\s+([^=]+)=([^=]+)");
		for i in output.split('\n'):
			if not i : 
				continue
			host_match=host_reg.search(i);	
			if host_match: 
				current_host=host_match.group(0);
				pbs_nodes_table[current_host]={};
			res_match=res_reg.search(i.strip('\n'));

			if res_match : 
				if not (current_host == "" ) :
					key=res_match.group(1).strip(' ');
					value=res_match.group(2).strip(' ').split(',');
					pbs_nodes_table[current_host][key]=value;
		return pbs_nodes_table;
					
	def pestat (self):
		keylist=self.pestat_default; 
		short=self.table['pbsnodes'];
		content=''
		for i in short.keys():
			for j in keylist: 
				if short[i].has_key(j):	
					content+=','.join(short[i][j])+self.sep;
				else: 
					content+='-'+self.sep
			content+='\n'
		print content
		return ;
	def get_job_table (self): 
		qstat_f={};
		jobid_reg=re.compile("^Job Id");
		res_reg=re.compile("\s+([^=]+)=(.+)");
		qstat_out,qstat_err=self.qstat();
		current_id="";
		print qstat_out
		for i in qstat_out.split('\n'):
			id_match=jobid_reg.search(i);
			if id_match: 
				jobid=i.split(':')[-1].strip(' ');	
				qstat_f[jobid]={};
				current_jobid=jobid
			res_match=res_reg.search(i.strip('\n'));
			if res_match:
				if not (current_jobid == "") :
					key=res_match.group(1).strip(' ');
					value=res_match.group(2).strip(' ').split(',');
					qstat_f[current_jobid][key]=value;
		return qstat_f
