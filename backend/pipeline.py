# -*- coding: utf-8 -*-
import datetime
import urllib2
import json
from social_auth.models import UserSocialAuth
from django.core.exceptions import ObjectDoesNotExist
from backend.models import *

import integrate

FACEBOOK_PROVIDER='facebook'
LINKEDIN_PROVIDER='linkedin-oauth2'

def associate_by_email(**kwargs):
    try:
        email = kwargs['details']['email']
        kwargs['user'] = User.objects.get(email=email)
    except:
        pass
    return kwargs

def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""

    print "User is: %s", user
    print "Details: %s", details
    print "Response is: %s", response
    for s in response.get('educations', {}).get('values',[]):
        print '  ', s, ' '
        
    if user:
        print "is user == True"
        
        if strategy.backend.__class__.__name__ == 'FacebookOAuth2':
             
            social_auth = UserSocialAuth.objects.get(user=user, provider=FACEBOOK_PROVIDER)
            facebook_binding = Binding.objects.filter(user=user, bind_from=FACEBOOK_PROVIDER)
            ### is new user, so we should create binding object and associated user profile
            if facebook_binding.count() == 0:

                ## create binding
                print "creating binding"
                binding = Binding(user=user,
                                  bind_from='facebook',
                                  
                                 )
                binding.save()

                ## create profile
                print "creating profile"
                profile = Profile(binding=binding,
                                  gender=response.get('gender', 'male'),
                                    #image_url= 'http://graph.facebook.com/{user_id}/picture'.format()

                                 )
                profile.save()
            else:
                assert( facebook_binding.count() == 1 )
                binding = facebook_binding[0]   # For use in attendances
                
            ## Check for schools, then attendances
            schools = []
            for s in response.get('education'):
                
                sid = s['school']['id']
                name = s['school']['name']
                schools_by_id = School.objects.filter(sid=sid)
                if schools_by_id.count() != 0:
                    assert(schools_by_id.count() == 1)
                    # No update for school data
                    print 'school found: '#, schools_by_id[0].name
                    school = schools_by_id[0]

                else:   # No existing shcool item
                    print 'new school: '#, name
                    school = School(
                                            name = name,
                                            sid = sid,
                                        )   
                    school.save()
#                    fb_th = integrate.fb_ref(school)
#                    fb_th.start() 
                schools.append(school)
                
                try:
                    attendance = Attendance.objects.get(binding = binding, school = school)
                except ObjectDoesNotExist:
                    
                    attendance = Attendance.objects.create(
                                binding=binding,
                                school=school,

                        )
                year = s.get('year', {}).get('name', '')
                school_type = s.get('type', '')
                attendance.type= school_type
                attendance.finish_year=year
                attendance.save()
                
            # Asynchronously update school information
            thread1 = integrate.fb_update_school(schools)
            thread1.start() 
               
        if strategy.backend.__class__.__name__ == 'LinkedinOAuth2': 
            social_auth = UserSocialAuth.objects.get(user=user, provider=LINKEDIN_PROVIDER)
            linkedin_binding = Binding.objects.filter(user=user, bind_from=LINKEDIN_PROVIDER)
            # linkedin extra data


            if linkedin_binding.count() == 0:
                ## create binding
                print "creating binding"
                binding = Binding(user=user,
                                  bind_from=LINKEDIN_PROVIDER,
                                 )
                binding.save()

                ## create profile
                print "creating profile"
                try:
                    pictureUrl = response['pictureUrl']
                except KeyError:
                    pictureUrl = None
                        
                profile = Profile(binding=binding,
                                  image_url= pictureUrl
                                 )
                profile.save()
            else:
                assert( linkedin_binding.count() == 1 )
                binding = linkedin_binding[0]

            ## Check schools
            schools = []
            for s in response.get('educations', {}).get('values',[]):

                name = s.get('schoolName')
                schools_by_name = School.objects.filter(name=name, sid = None) ## This is only a very simple integration
                if schools_by_name.count() == 0:
                    school = School(
                                name=name,
                            )
                    school.save()
                    print "School created: ", #name                
                else:
                    school = schools_by_name[0]
#                    li_th2 = integrate.li_ref(school, binding)
#                    li_th2.start() 
                schools.append(school)

                ### Check Attendance entry  
                attend_year = s.get('startDate', {}).get('year', '')
                finish_year = s.get('endDate', {}).get('year', '')
                school_type = s.get('degree', '')
                try:
                    attendance = Attendance.objects.get(binding = binding, school = school)
                except ObjectDoesNotExist:
                    attendance = Attendance.objects.create(
                                binding=binding,
                                school=school,
                                type= school_type,
                                attend_year=attend_year,
                                finish_year=finish_year
                        )
                    attendance.save()
                
            # Asynchronously update school information
            thread2 = integrate.li_update_school(schools)
            thread2.start()   