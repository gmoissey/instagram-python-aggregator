from instagrapi import Client
from instagrapi.exceptions import LoginRequired
import logging

logger = logging.getLogger()

USERNAME = ''
PASSWORD = ''

def login_user():
    """
    Attempts to login to Instagram using either the provided session information
    or the provided username and password.
    """

    cl = Client()
    # try to load session from file
    try:
        session = cl.load_settings("/Users/gleb/Documents/instagram-python-aggregator/app/utils/session.json")
    except Exception as e:
        logger.info("Couldn't load session from file: %s" % e)
        session = None

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(USERNAME, PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(USERNAME, PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % USERNAME)
            if cl.login(USERNAME, PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")
    
    cl.dump_settings("/Users/gleb/Documents/instagram-python-aggregator/app/utils/session.json")
    return