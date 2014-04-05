import datetime

from social_auth.models import UserSocialAuth

from backend.models import *

FACEBOOK_PROVIDER='facebook'
LINKEDIN_PROVIDER='linkedin-oauth2'

def user_details(strategy, details, response, user=None, *args, **kwargs):
    """Update user details using data from provider."""

    print "User is: %s", user
    print "Details: %s", details
    print "Response is: %s", response
    for s in response.get('educations', {}).get('values',[]):
        print '  '
        print s
        print '  '

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

                name = s['school']['name']
                sid = s['school']['id']
                schools_by_id = School.objects.filter(sid=sid)
                schools_by_name = School.objects.filter(name=name)
                if schools_by_id.count() == 0 and schools_by_name.count() == 0:
                    school = School(
                                name=name,
                                sid=sid,
                            )
                    school.save()
                else:
                    if schools_by_id.count() != 0:
                        school = schools_by_id[0]
                    else:
                        school = schools_by_name[0]
                        school.sid = sid
                        school.save()

                ### create Attendance entry for this binding
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
                schools_by_name = School.objects.filter(name=name) ## This is only a very simple integration
                if schools_by_name.count() == 0:
                    school = School(
                                name=name,
                            )
                    school.save()
                    print "School created: %s", name
                else:
                    school = schools_by_name[0]

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
