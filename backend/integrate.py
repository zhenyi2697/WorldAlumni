# -*- coding: utf-8 -*-
import urllib2
import json
import re
import sys
import threading  

from backend.models import *


def get_node(entry):
    # This function retrieves node information from Facebook Graph API
    # Input entry can be either the name or the id of the node
    response = urllib2.urlopen('https://graph.facebook.com/{}'.format(entry))
    
    node = json.loads(response.read())
    #print node
    return node
    
def get_main_node_id(id):
    # This function takes in a Facebook page(school, company) ID (its node ID), and finds out if it is the main page, or if it is a duplicate/has been merged to another page. In the latter case, the main page id is returned.
    node = get_node(id)
    content = urllib2.urlopen(node['link']).read()
    # Use regular expression to locate redirect link
    pattern = r'window.location.replace\(\"(?P<redirect_link>.{1,100}?)\"\);\<\/script\>' # script to 'redirect' merged page
    m = re.search(pattern, content)
    
    if m==None:
        # This is a main page, because no window.location.raplace in response
        print node['id'], "is main node" #node['name'],  
        return id
    else:
        redirect_link = m.group('redirect_link')
        if False:
            print 'Mateched location.replace script: ', m.group(0)
            print 'Redirect page link: ', redirect_link
        pattern2 = r'\\\/(?P<node_name>[^\/]{1,100}?)\?rf'
        m2 = re.search(pattern2, redirect_link)
        node_name =  m2.group('node_name')

        main_node = get_node(node_name) # Abuse of function get_node
        main_node_id = main_node['id']
        print node['id'], "'s main node is" #node['name'], 
        print main_node_id #, main_node['name']
        return main_node_id
    
  
def bind_school_fb(sid):
    
    print 'bind_school_fb called'
    
    schools_by_id = School.objects.filter(sid=sid)
    if schools_by_id.count() != 0:
        assert(schools_by_id.count() == 1)
        # No update for school data
        print 'school found: ', #schools_by_id[0].name
        return schools_by_id[0] 
    else:   # No existing shcool item
        print 'new school: '
        fb_ref_id = get_main_node_id(sid)
        new_school_node = get_node(sid)
        new_school = School(
                                name = new_school_node['name'],
                                sid = new_school_node['id'],

                            )   
        new_school.save()
        if fb_ref_id == sid:
            new_school.ref = new_school
        else:
            new_school.ref = bind_school_fb(fb_ref_id)   
        new_school.save()
        return new_school
     
    # A step to compare newly added fb school info to L items.

class fb_ref(threading.Thread):
    def __init__(self, school):  
        threading.Thread.__init__(self)  
        self.school = school
    def new_ref_school(self, sid):
        new_school_node = get_node(sid)
        new_school = School(
                                name = new_school_node['name'],
                                sid = new_school_node['id'],
                            )
        new_school.save()
        new_school.ref = new_school
        new_school.save()
        print 'new ref school created:', new_school.name
        return new_school
        
    def run(self): #Overwrite run() method, put what you want the thread do here  
        print 'integration thread called', self.school.name

        fb_ref_id = get_main_node_id(self.school.sid)
        
        if fb_ref_id == self.school.sid:
            self.school.ref = self.school
        else:
            schools_by_id = School.objects.filter(sid=fb_ref_id)
            if schools_by_id.count() != 0:
                self.school.ref = schools_by_id[0]
            else:
                self.school.ref = self.new_ref_school(fb_ref_id)
        self.school.save()
        return self.school
    
    
def bind_school_li():
    
    pass
    
if __name__ == '__main__':

    DEBUG = True
    school_id = 112517705427268 # ID for Georgia-Institute-of-Technology
    if len(sys.argv)>1:
        school_id = sys.argv[1]
    main_node = get_main_node_id(school_id)    

    
