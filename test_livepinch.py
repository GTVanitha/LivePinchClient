import live_pinch_client

apikey = "abcdef123"
obj = live_pinch_client.Client(apikey)
print obj.update_profile("   profilekey   ", {"first_name": "vani"})
print obj.track_event("   profilekey   ", "event name ", {"first_name": "vani"})
