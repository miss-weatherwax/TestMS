#!/usr/bin/python

import unittest
import configparser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from test_helpers import find_element, find_elements


class Selectors():
    # test case 1
    sing_in_button = [
        'css', '#desktopNavBtns > nav.collapse.navbar-collapse.bs-navbar-collapse.navbar-menu-desktop > ul > li:nth-child(5) > a']
    username = ['id', 'login-form_username']
    password = ['id', 'login-form_password']

    # test case 2
    musala_soft_link = ['css', 'div.leftPartFooter > a']
    company_logo = ['css', 'a.brand > p > span.logo']
    linkedin_link = ['css', 'div.rightPartFooter > a.pull-left']
    musala_linkedin_logo = [
        'css', '.org-top-card-module__container > .org-top-card-module__logo']
    facebook_link = ['css', 'div.rightPartFooter > a.pull-right']
    musala_facebook_logo = ['css', '#u_0_f > div > a > img']

    # LinkedIn
    linkedin_signin = ['css', '#join-form > p.form-subtext.login > a']
    linkedin_username = ['id', 'login-email']
    linkedin_password = ['id', 'login-password']
    linkeedin_profile = ['id', 'nav-settings__dropdown-trigger']

    # test case 3
    archive_button = [
        'css', '#desktopNavBtns > nav.collapse.navbar-collapse.bs-navbar-collapse.navbar-menu-desktop > ul > li:nth-child(3) > a']
    last_event = ['css', '#events-cont > div:last-child']
    schedule = ['class', 'list-group']
    speaker_info = ['class', 'speaker-info']
    speaker = ['css', 'div > li > div.list-group-item-header > div.speaker-info']

    # google maps
    map_canvas = ['id', 'map-canvas']
    google_maps_images = ['xpath', '//img[contains(@src, "maps.google")]']


class MusalaTest(unittest.TestCase):

    def setUp(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        web_page = config['Basic']['WebPage']

        self.driver = webdriver.Chrome()
        self.driver.get(web_page)

    def test_case_1(self):
        driver = self.driver
        sign_in = find_element(driver, Selectors.sing_in_button)
        self.assertEqual(sign_in.text, 'Sign In')
        sign_in.click()
        user_name = find_element(driver, Selectors.username)
        user_name.send_keys('invalid_username')
        password = find_element(driver, Selectors.password)
        password.send_keys('invalid_password' + Keys.ENTER)

        expected_text = 'Wrong user or password.'
        msg_found = False
        try:
            find_element(driver, ['text', expected_text])
            msg_found = True
        except Exception:
            pass
        self.assertTrue(msg_found, 'Invalid credentials warning not found')

        print self._testMethodName + ': Pass'

    def test_case_2(self):
        driver = self.driver

        initial_tab = driver.window_handles[0]

        # http://www.musala.com/
        musala_soft_link = find_element(driver, Selectors.musala_soft_link)
        self.assertEqual(musala_soft_link.get_attribute(
            'href'), 'http://www.musala.com/')
        musala_soft_link.click()

        driver.switch_to_window(driver.window_handles[-1])

        # verify the URL of the loaded page
        self.assertEqual(driver.current_url, 'http://www.musala.com/')

        # verify the logo is present on the page
        company_logo = find_element(driver, Selectors.company_logo)

        expected_website_logo = \
            'url("http://www.musala.com/website/wp-content/themes/' + \
            'musalasoft/dist/assets/img/Musala_Logo_white.svg")'
        self.assertEquals(company_logo.value_of_css_property('background-image'),
                          expected_website_logo, 'Incorrect logo')
        self.assertTrue(company_logo.is_displayed(),
                        'The logo is not displayed on the company website')

        # switch back to the initial page
        driver.switch_to_window(initial_tab)

        # LinkedIn
        linkedin_link = find_element(driver, Selectors.linkedin_link)
        self.assertEqual(linkedin_link.get_attribute('href'),
                         'https://www.linkedin.com/company/musala-soft')
        linkedin_link.click()

        driver.switch_to_window(driver.window_handles[-1])

        # sign in to LinkedIn
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, Selectors.linkedin_signin[1]))
        )
        find_element(driver, Selectors.linkedin_signin).click()

        # wait for linkedin signin page to load
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, Selectors.linkedin_username[1]))
        )

        # use dummy linkedin account in order to sign in
        find_element(driver, Selectors.linkedin_username).send_keys(
            'musala.soft.test@abv.bg')
        find_element(driver, Selectors.linkedin_password).send_keys(
            'musalasoft' + Keys.ENTER)

        # wait for linkedin page to load
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.ID, Selectors.linkeedin_profile[1]))
        )

        # verify the URL of the loaded page
        self.assertEqual(driver.current_url,
                         'https://www.linkedin.com/company/musala-soft/',
                         'LinkedIn company page not loaded')

        # verify the logo is present on the page
        expected_linkedin_logo = \
            'https://media.licdn.com/dms/image/C4D0BAQGCRgI5NqX3Bg/' + \
            'company-logo_200_200/0?e=1545264000&v=beta&t=' + \
            '1usHtfoN8DrWs6E3o5zJAkkj0LM3Y3KAA_qB6HpppYU'
        musala_linkedin_logo = find_element(
            driver, Selectors.musala_linkedin_logo)
        self.assertEquals(musala_linkedin_logo.get_attribute(
            'src'), expected_linkedin_logo, 'Incorrect logo')
        self.assertEquals(musala_linkedin_logo.get_attribute(
            'alt'), 'Musala Soft Logo')
        self.assertTrue(musala_linkedin_logo.is_displayed(
        ), 'The logo is not displayed on the company\'s linkedin page')

        # switch back to the initial page
        driver.switch_to_window(initial_tab)

        # Facebook
        facebook_link = find_element(driver, Selectors.facebook_link)
        self.assertIn('https://www.facebook.com/pages/MUFFIN-Conference',
                      facebook_link.get_attribute('href'))
        facebook_link.click()

        driver.switch_to_window(driver.window_handles[-1])

        # verify the URL of the loaded page
        self.assertEqual(driver.current_url,
                         'https://www.facebook.com/MUFFINconference/',
                         'Facebook conference page not loaded')

        # verify the logo is present on the page
        expected_fb_logo = \
            'https://scontent.fsof3-1.fna.fbcdn.net/v/t1.0-1/p200x200/' + \
            '11900034_509046765936307_4811519138851319223_n.png?_nc_cat=' + \
            '0&oh=6d8770eb4582fc113fa3a3339ffa1b40&oe=5C374E80'
        musala_facebook_logo = find_element(
            driver, Selectors.musala_facebook_logo)
        self.assertEquals(musala_facebook_logo.get_attribute('src'),
                          expected_fb_logo, 'Incorrect logo')
        self.assertTrue(musala_facebook_logo.is_displayed(),
                        'The logo is not displayed Facebook')

        print self._testMethodName + ': Pass'

    def test_case_3(self):
        driver = self.driver

        archive = find_element(driver, Selectors.archive_button)
        self.assertEqual(archive.text, 'Archive')
        archive.click()

        # wait for the last event to be clickable
        WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        Selectors.last_event[1]))
        )

        # open last event
        last_event = find_element(driver, Selectors.last_event)
        last_event.click()

        WebDriverWait(driver, 5).until(
            EC.visibility_of_all_elements_located(
                (By.CLASS_NAME, Selectors.schedule[1]))
        )

        # print schedule
        print '----- SCHEDULE -----'
        schedule = find_elements(driver, Selectors.schedule)
        for item in schedule:
            speaker_info = find_elements(item, Selectors.speaker_info)
            driver.find_elements
            inner_text = ''
            if len(speaker_info) > 0:
                speaker = find_element(item, Selectors.speaker)
                inner_html = driver.execute_script(
                    "return arguments[0].innerHTML;", speaker)
                inner_text = inner_html.split("</span>", 1)[1]
            else:
                inner_text = driver.execute_script(
                    "return arguments[0].innerText;", item)
            inner_text = inner_text.strip()
            print inner_text.encode('utf-8')
        print '--------------------'

        # google maps
        map_canvas = find_element(driver, Selectors.map_canvas)
        google_maps_images = find_elements(map_canvas,
                                           Selectors.google_maps_images)
        for google_image in google_maps_images:
            self.assertTrue(google_image.is_displayed(),
                            'google maps image "' +
                            google_image.get_attribute('src') +
                            '" not displayed')

        # uncomment when [BUG-ID] is fixed
        # [BUG-ID] - bug about not displaying google maps correctly
        # google_error_text = 'This page can\'t load Google Maps correctly.'
        # msg_found = False
        # try:
        #     find_element(driver, ['text', google_error_text])
        #     msg_found = True
        # except Exception:
        #     pass
        # self.assertTrue(msg_found, 'Google Maps not loaded correctly.')

        print self._testMethodName + ': Pass'

    def tearDown(self):
        self.driver.close()


if __name__ == "__main__":
    unittest.main()
