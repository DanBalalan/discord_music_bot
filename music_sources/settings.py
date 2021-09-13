class RestreamerDispatcherException(Exception): pass


URL_TARGET_GROUP_NAME = 'service_name'
URL_PATTERN = rf'http(s)?://(www.)?(?P<{URL_TARGET_GROUP_NAME}>\w+)\.(\w+)'
