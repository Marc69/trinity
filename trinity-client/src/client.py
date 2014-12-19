import os
from ConfigParser import SafeConfigParser
import json
import requests

#conf_file=os.path.join(os.path.dirname(os.path.abspath(__file__)),'trinity-client.conf')
conf_file='/etc/trinity/trinity-client.conf'
class Client(object):

  def __init__(self,username=None,password=None,tenant=None,token=None):
    self.username=username
    self.password=password
    self.tenant=tenant
    self.token=token
    if token:
      self.payload = { 
                  "tenant": self.tenant,
                  "token":    self.token
                }
    else:
      self.payload = { 
                  "tenant": self.tenant,
                  "username": self.username,
                  "password": self.password
                }
    self.headers = {'Content-Type': 'application/json', "Accept":"application/json"}
    
    # This will be in a conf file finder routine
    self.conf_file= conf_file
    self.config(self.conf_file)
    self.trinity_prefix=self.trinity_protocol+'://'+self.trinity_host+':'+self.trinity_port \
                         +'/'+self.trinity_collection+'/v'+self.trinity_version    

  def config(self,file):
    config=SafeConfigParser()
    config.read(file)
    for section in config.sections():
      for option in config.options(section):
        value=config.get(section,option)
        setattr(self,option,value)

############################################################################################################
 
  def hardwares_list(self):
    r = requests.get(self.trinity_prefix+'/hardwares', data=json.dumps(self.payload), headers=self.headers)
    return r.json()["hardwares"]
  
  def clusters_list(self):
    r = requests.get(self.trinity_prefix+'/clusters', data=json.dumps(self.payload), headers=self.headers)
    return r.json()["clusters"]

  def hardwares_detail(self):
    hardwares=self.hardwares_list()
    data=[]
    for hardware in hardwares:
      r = requests.get(self.trinity_prefix+'/hardwares/'+hardware, data=json.dumps(self.payload), headers=self.headers)
      datum={}
      res=r.json()
      datum['total']=res['total']
      datum['used']=res['allocated']
      datum['hardware']=hardware
      data.append(datum)
    return data

  def clusters_detail(self):
    clusters=self.clusters_list()
    data=[]
    for cluster in clusters:
      hardwares=self.cluster_hardware(cluster)
      datum={'cluster':cluster}
      for hardware in hardwares: 
        datum[hardware['type']]=hardware['amount']
      data.append(datum)
    return data

  def cluster_hardware(self,cluster):
    r = requests.get(self.trinity_prefix+'/clusters/'+cluster, data=json.dumps(self.payload), headers=self.headers)
    data=[]
    res=r.json()
    for key,value in res['hardware'].items():
      datum={}
      datum['type']=key
      datum['amount']=value
      data.append(datum) 
    return data

  def cluster_config(self,cluster):
#  Dummy
    data=[{'param': 'Operating System', 'value': 'Ubuntu-14.10'},
          {'param': 'Scheduler', 'value': 'SLURM-14.11'},
          {'param': 'Monitoring','value':'Ganglia-3.6.2'}]
    return data


  def cluster_modify(self,cluster,specs):
    self.payload.update({'specs':specs})
    r = requests.put(self.trinity_prefix+'/clusters/'+cluster, data=json.dumps(self.payload), headers=self.headers)
    return r.json() 

  def get_metrics(self):
#  Dummy
    return

if __name__ == "__main__":
  c=Client(username='admin',password='system',tenant='admin')
  print c.clusters_detail() 
#  print c.cluster_modify(cluster='b',specs={'hm':1,'gpu':1}) 
     
