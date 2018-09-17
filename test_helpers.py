import selenium


def find_element(driver, selector):
    if selector[0] == 'id':
        return driver.find_element_by_id(selector[1])
    elif selector[0] == 'css':
        return driver.find_element_by_css_selector(selector[1])
    elif selector[0] == 'xpath':
        return driver.find_element_by_xpath(selector[1])
    elif selector[0] == 'text':
        return driver.find_element_by_xpath("//*[contains(text(), '" + selector[1] + "')]")
    else:
        return


def find_elements(driver, selector):
    if selector[0] == 'css':
        return driver.find_elements_by_css_selector(selector[1])
    elif selector[0] == 'xpath':
        return driver.find_elements_by_xpath(selector[1])
    elif selector[0] == 'class':
        return driver.find_elements_by_class_name(selector[1])
    else:
        return []
