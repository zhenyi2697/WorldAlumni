import urllib2
import json
import re
import sys

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
    #print type(content)
    # Use regular expression to locate redirect link
    pattern = r'window.location.replace\(\"(?P<redirect_link>.{1,100}?)\"\);\<\/script\>' # script to 'redirect' merged page
    m = re.search(pattern, content)
    
    if m==None:
        # This is a main page, because no window.location.raplace in response
        print node['id'], node['name'], "is main node" 
        return id
    else:
        redirect_link = m.group('redirect_link')
        if DEBUG:
            print 'Mateched location.replace script: ', m.group(0)
            print 'Redirect page link: ', redirect_link
        pattern2 = r'www\.facebook\.com\\\/(?P<node_name>.{1,100}?)\?rf'
        m2 = re.search(pattern2, redirect_link)
        node_name =  m2.group('node_name')
#        rlink2 = redirect_link.replace('www', 'graph')
#        response = urllib2.urlopen(rlink2)
#    
#        main_node = json.loads(response.read())
        main_node = get_node(node_name) # Abuse of function get_node
        main_node_id = main_node['id']
        print node['id'], node['name'], "'s main node is";
        print main_node_id, main_node['name']
        return main_node_id
    
if __name__ == '__main__':

    DEBUG = True
    school_id = 112517705427268 # ID for Georgia-Institute-of-Technology
    if len(sys.argv)>1:
        school_id = sys.argv[1]
    main_node = get_main_node_id(school_id)    

    
