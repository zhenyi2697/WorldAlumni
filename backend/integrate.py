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
    pattern = r'window.location.replace\(\"(?P<redirect_link>.+?)\"\);\<\/script\>' # script to 'redirect' merged page
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
        pattern2 = r'\\\/(?P<node_name>[^\/]+?)\?rf'
        m2 = re.search(pattern2, redirect_link)
        node_name =  m2.group('node_name')

        main_node = get_node(node_name) # Abuse of function get_node
        main_node_id = main_node['id']
        print node['id'], "'s main node is" #node['name'], 
        print main_node_id #, main_node['name']
        return main_node_id
    
  

     

class fb_update_school(threading.Thread):
    def __init__(self, schools):  
        threading.Thread.__init__(self)  
        self.schools = schools
    def new_ref_school(self, sid):
        new_school_node = get_node(sid)
        new_school = School(
                                name = new_school_node['name'],
                                sid = new_school_node['id'],
                            )
        new_school.save()
        new_school.ref = new_school
        new_school.save()
        print 'new ref school created:'#, new_school.name
        return new_school
    def suggest_merge(self, school):
        suggestions = School.objects.filter(name__iexact = school.name)
        sch_node = get_node(school.sid)
        for sug_school in suggestions:
            sug_node = get_node( sug_school.sid )
            if sug_node['likes'] >=  sch_node['likes']:
                school.ref = sug_school.ref
        return school
    def update_school(self, school): 
        print 'FB integration thread called'#, school.name
        if school.ref == None:
            fb_ref_id = get_main_node_id(school.sid)

            if fb_ref_id == school.sid:
                school.ref = school
            else:
                schools_by_id = School.objects.filter(sid=fb_ref_id)
                if schools_by_id.count() != 0:
                    school.ref = schools_by_id[0]
                else:
                    school.ref = self.new_ref_school(fb_ref_id).ref
            if school.ref == school:
                school = self.suggest_merge(school)
            school.save()
            return school
    def run(self):
        for school in self.schools:
            self.update_school(school)
        

def compare_school_name(li_school, fb_schools):
    li_str = li_school.name.lower()
    li_school.ref = li_school

    for school in fb_schools:
        fb_str = school.name.lower()
        print 'school strings to compare: '#, li_str, fb_str
        if (li_str in fb_str) or (fb_str in li_str):
            li_school.ref = school.ref
            print 'find fb ref school: '#, school.name
    li_school.save()
    return li_school
    
class li_update_school(threading.Thread):
    def __init__(self, schools):
        threading.Thread.__init__(self)  
        self.schools = schools
        #self.binding = binding
    def update_school(self, school):
        print 'LI integration thread called'#, self.school.name
        if (school.ref == None) or (school.ref.sid == None):
            # Compare to all fb school data
            comp_schools = School.objects.exclude(sid = None)
            ref_school = compare_school_name(school, comp_schools)
        return school
        
        
    def run(self):
        for school in self.schools:
            self.update_school(school)
    def run2(self): #deprecated
        print 'LI integration thread called'#, self.school.name
        if (self.school.ref == None) or (self.school.ref.sid == None):
            if self.binding.user != 'admin':     # Leave for admin routine
                fb_bindings = Binding.objects.filter(user = self.binding.user, bind_from = 'facebook ')
                if fb_bindings.count() == 2:    # Compare with same user Fb data
                    fb_binding = fb_bindings[0]
                    attendances = Attendance.objects.filter(binding = fb_binding)
                    schools = [att.school for att in attendances]
                    ref_school = compare_school_name(self.school, schools)
                else:               # Compare to all fb school data
                    schools = School.objects.exclude(sid = None)
                    ref_school = compare_school_name(self.school, schools)
        return self.school
                
        
def bind_school_fb(sid):    #deprecated
    
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
    
    
if __name__ == '__main__':

    DEBUG = True
    school_id = 112517705427268 # ID for Georgia-Institute-of-Technology
    if len(sys.argv)>1:
        school_id = sys.argv[1]
    main_node = get_main_node_id(school_id)    

    
