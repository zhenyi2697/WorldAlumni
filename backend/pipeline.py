# -*- coding: utf-8 -*-
import datetime

from social_auth.models import UserSocialAuth

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
        facebook_binding = Binding.objects.filter(user=user, bind_from=FACEBOOK_PROVIDER)
        linkedin_binding = Binding.objects.filter(user=user, bind_from=LINKEDIN_PROVIDER)

        ### is new user, so we should create bindling object and associated user profile
        if strategy.backend.__class__.__name__ == 'FacebookOAuth2' and facebook_binding.count() == 0:

            social_auth = UserSocialAuth.objects.get(user=user, provider=FACEBOOK_PROVIDER)

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
                             )
            profile.save()

            ## profile schools if they do not exist
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
                    fb_th = integrate.fb_ref(school)
                    fb_th.start() 
                 
                #print school
                year = s.get('year', {}).get('name', '')

                attendance = Attendance(
                                binding=binding,
                                school=school,
                                type=s.get('type', ''),
                                attend_year=year
                        )
                attendance.save()
               
        if strategy.backend.__class__.__name__ == 'LinkedinOAuth2' and linkedin_binding.count() == 0:
            social_auth = UserSocialAuth.objects.get(user=user, provider=LINKEDIN_PROVIDER)
            ## create binding
            print "creating binding"
            binding = Binding(user=user,
                              bind_from=LINKEDIN_PROVIDER,
                             )
            binding.save()

            ## create profile
            print "creating profile"
            profile = Profile(binding=binding,
                             )
            profile.save()

            ## profile schools if they do not exist
            for s in response.get('educations', {}).get('values',[]):

                name = s.get('schoolName')
                schools_by_name = School.objects.filter(name=name, sid = None) ## This is only a very simple integration
                if schools_by_name.count() == 0:
                    school = School(
                                name=name,
                            )
                    school.save()
                    print "School created: ", #name
                    li_th = integrate.li_ref(school, binding)
                    li_th.start()                     
                else:
                    school = schools_by_name[0]
                    li_th2 = integrate.li_ref(school, binding)
                    li_th2.start() 

                ### create Attendance entry
                attend_year = s.get('startDate', {}).get('year', '')
                finish_year = s.get('endDate', {}).get('year', '')

                attendance = Attendance(
                                binding=binding,
                                school=school,
                                type=s.get('degree', ''),
                                attend_year=attend_year,
                                finish_year=finish_year
                        )
                attendance.save()
