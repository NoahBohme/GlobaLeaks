# -*- coding: UTF-8
#
# exception

import json

from globaleaks.handlers.base import BaseHandler
from globaleaks.handlers.authentication import transport_security_check, unauthenticated
from globaleaks.rest import requests
from globaleaks.settings import GLSetting
from globaleaks.utils.mailutils import send_exception_email
from globaleaks.utils.utility import log


class ExceptionHandler(BaseHandler):
    """
    """
    @transport_security_check("unauth")
    @unauthenticated
    def post(self):
        """
        """
        request = self.validate_message(self.request.body,
                                        requests.ExceptionDesc)

        if not GLSetting.disable_client_exception_notification:
            exception_email = "Exception generated by client: %s\n\n" % request['agent']
            exception_email += "URL: %s\n\n" % request['errorUrl']
            exception_email += "Error Message: %s\n\n" % request['errorMessage']
            exception_email += "Stacktrace:\n"
            exception_email += json.dumps(request['stackTrace'], indent=2)
            send_exception_email(exception_email)
            log.debug("Received client exception and notified to exception email")

        self.set_status(201)  # Created
        self.finish()

