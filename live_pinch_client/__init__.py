import requests

END_POINT = "https://api.livepinch.com/api/"


class Client:
    """Client class for livepinch Profile and Events API """

    """Global declaration for uri paths"""
    uris = {"profile_update": "/profile/update", "track_event": "/events/push"}

    def __init__(self, api_key, api_version=None):

        if not api_version:
            self.api_version = '1.0'
        else:
            self.api_version = api_version

        self.api_key = api_key

    def _validate_params(arg_type):
        """decorator function for validating payloads"""

        def validate_decorator(func):
            def validate_wrapper(*args, **kwargs):
                if (args[1] and isinstance(args[1], str)):
                    profile_key = args[1].strip()
                else:
                    raise Exception("Not a valid profile key!")

                if arg_type == 'profile':
                    if (len(args) != 3):
                        raise Exception(
                            "Invalid parameters!. Excepting 2 parameters instead {} given!".format(len(args)-1))
                    profile_data = args[2]

                elif arg_type == 'event':
                    if (len(args) != 4):
                        raise Exception(
                            "Invalid parameters!. Excepting 3 parameters instead {} given!".format(len(args)-1))
                    event_name = args[2]
                    profile_data = args[3]

                if not profile_key:
                    raise Exception(
                        "Invalid Profile Key: {}".format(profile_key))
                if arg_type == 'event' and not event_name:
                    raise Exception(
                        "Invalid Event Name: {}".format(event_name))

                if not profile_data or (profile_data and not isinstance(profile_data, dict)):
                    raise Exception(
                        "Invalid Profile Data: {}".format(profile_data))

                # check for valid key
                valid_profile_keys = ['first_name',
                                      'last_name', 'email', 'gender']
                for key in profile_data.keys():
                    if key not in valid_profile_keys:
                        raise Exception(
                            "Invalid profile data: {}".format(profile_data))
                func(*args, **kwargs)
            return validate_wrapper
        return validate_decorator

    def get_url(self, path):
        return END_POINT + self.api_version + (path if (path.find("/") == 0) else "/{}".format(path))

    def get_headers(self):
        return {
            "Content-Type": "application/json",
            "X-Api-Key": self.api_key
        }

    def send_request(self, path, payload):

        res = requests.post(self.get_url(path), data=payload,
                            headers=self.get_headers())
        return res

    @_validate_params("profile")
    def update_profile(self, profile_key, profile_data):
        """Update method to update profile information"""
        payload = {"profile_key": profile_key, "profile_data": profile_data}
        self.send_request(self.uris['profile_update'], payload)

    @_validate_params("event")
    def track_event(self, profile_key, event_name, profile_attributes):
        """Method to track profile events"""
        payload = {
            'profile_key':  profile_key,
            'event_name': event_name,
            'profile_data':  profile_attributes
        }
        self.send_request(self.uris['track_event'], payload)
