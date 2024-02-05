import playwright
import logging
from . import config
from .account import Account
from .cookies import Cookie
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page

logger = logging.getLogger(__name__)


class NotLoginError(Exception):
    pass


class AlreadyLoginError(Exception):
    pass


class LoginFailedError(Exception):
    pass


class Baha:
    browser: Browser
    context: BrowserContext
    page: Page
    account: Account
    headless: bool
    init_cookies: list[Cookie]

    def __init__(self, account: Account,
                 headless: bool = config.DEFAULT_HEADLESS,
                 cookies: list[Cookie] = config.DEFAULT_COOKIES) -> None:
        """Init Baha object.

        Args:
            account (Account): TypeDict Account with userid and password.
            headless (bool, optional): Arg of p.chromium.launch(). Defaults to config.DEFAULT_HEADLESS.
            cookies (list[Cookie], optional): Cookies that want to be added to the context. Defaults to config.DEFAULT_COOKIES.
        """
        self.account = account
        self.headless = headless
        self.init_cookies = cookies

    def __enter__(self) -> "Baha":
        """Start the browser when exit the context manager.

        Returns:
            self: Baha object
        """
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        self.context.add_cookies(self.init_cookies)
        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """Close the browser when exit the context manager.

        Args:
            exc_type
            exc_value
            traceback
        """
        self.page.close()
        self.context.close()
        self.browser.close()
        self.p.stop()

    @staticmethod
    def need_login(func) -> callable:
        """Decorator to check if the user is logged in.

        Args:
            func (Callable[..., T]): The function to be decorated.

        Raises:
            NotLoginError: If the user is not logged in.
        """

        def wrapper(self, *args, **kwargs):
            if not self.is_login():
                raise NotLoginError(
                    f"You need to login before call {func.__name__}()")
            return func(self, *args, **kwargs)
        return wrapper

    def login(self) -> None:
        """Login to the website.

        Raises:
            AlreadyLoginError: If the user is already logged in.
            LoginFailedError: If the login failed.
        """
        logger.debug("login")
        if self.is_login():
            raise AlreadyLoginError()
        self.page.goto("https://www.gamer.com.tw/")
        self.page.click('text=我要登入')
        self.page.fill('input[name="userid"]', self.account["userid"])
        self.page.fill('input[name="password"]', self.account["password"])
        self.page.click("#btn-login")
        logger.debug("submit login form")
        try:
            # redirect to the home page after login successfully
            self.page.wait_for_url("https://www.gamer.com.tw/", timeout=10000)
        except playwright._impl._errors.Error as e:
            # if the page doesn't redirect, check the error message
            message = self.get_login_failed_message()
            logger.error(message)
            raise LoginFailedError(message)

    @need_login
    def logout(self) -> None:
        """Logout from the website."""
        logger.debug("logout")
        self.page.goto("https://user.gamer.com.tw/logout.php")
        self.page.evaluate("logout();")
        self.page.wait_for_url("https://www.gamer.com.tw/", timeout=10000)

    def get_login_failed_message(self) -> str:
        """Get the login failed message.

        Returns:
            str: The login failed message.

        Raises:
            Exception: Can't find the login failed message element.
        """
        element = self.page.locator(
            ".caption-text.red.margin-bottom.msgdiv-alert").nth(0)
        if element.is_visible():
            return element.text_content()
        else:
            raise Exception("Can't find the login failed message element")

    def get_cookies(self) -> list[Cookie]:
        """Get the cookies of the current context.

        Returns:
            list[Cookie]
        """
        logger.debug("get_cookies")
        cookies = self.context.cookies()
        logger.debug("cookies: " + str(cookies))
        return cookies

    def is_login(self) -> bool:
        """Check if the user is logged in.

        Returns:
            True: The user is logged in.
            False: The user is not logged in.
        """
        logger.debug("check_login")
        self.page.goto("https://www.gamer.com.tw/")
        element = self.page.locator(".TOP-nologin").nth(0)
        if element.is_visible():
            logger.debug("element: " + str(element.inner_html()))
            return False
        else:
            return True

    def is_signin(self) -> bool:
        """Check if the user has signed in today.

        Returns:
            True: The user has signed in today.
            False: The user has not signed in today.
        """
        logger.debug("check_signin")
        self.page.goto("https://www.gamer.com.tw/")
        signin_text = self.page.locator("#signin-btn").text_content().strip()
        logger.debug("signin_text: " + str(signin_text))
        return signin_text == "check_box每日簽到已達成"

    @need_login
    def get_userid(self) -> str:
        """Get the userid from the top bar.

        Returns:
            str: userid
        """
        logger.debug("get_login_userid")
        self.page.click('#topBar_member')
        userid = self.page.text_content(".userid").strip()
        logger.debug("userid: " + str(userid))
        return userid
