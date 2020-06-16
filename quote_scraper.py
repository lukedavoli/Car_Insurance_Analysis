from bs4 import BeautifulSoup
import csv
import requests
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.select import Select
import time

WEBDRIVER_PATH = r"C:\Program Files (x86)\geckodriver.exe"
CTM_ADDR = "https://www.comparethemarket.com.au/car-insurance/journey/start"


def complete_survey(person_id, car_id, updates=True):
    name, age, gender = get_person(person_id)
    rego_num = get_rego(car_id)
    
    if updates: print("getting quote from Compare the Market...")
    opts = Options()
    #opts.headless = True
    driver = webdriver.Firefox(
        options = opts, executable_path = WEBDRIVER_PATH)
    driver.get(CTM_ADDR)

    # Do you know the rego of the car?
    driver.find_element_by_xpath(
        "//input[@name='helpers.regoLabel']").send_keys(rego_num)
    driver.find_element_by_xpath(
        "//button[contains(.,'Next')]").click()

    # In which state is the car registered?
    driver.find_element_by_xpath(
        "//label[@for='coverDetail.vehicle.state.VIC']").click()

    # What level of cover are you looking for?
    comp_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//input[@value='COMPREHENSIVE']")))
    comp_btn.click()

    # Are there any factory/dealer options or non-standard accessories fitted to the car?
    driver.find_element_by_xpath("//label[contains(.,'No')]").click()
    
    # Has the car been modified?
    driver.find_element_by_xpath(
        "//label[@for='coverDetail.vehicle.modified.N']").click()

    # What about any unrepaired accident or hail damage to the car?
    driver.find_element_by_xpath(
        "//label[@for='coverDetail.vehicle.damaged.N']").click()

    try:
        driver.find_element_by_xpath(
            "//label[contains(.,'No security features')]").click()
    except NoSuchElementException:
        pass

    # Is there any finance on the car?
    driver.find_element_by_xpath(
        "//label[@for='coverDetail.financeType.NONE']").click()
    
    # How is the car used?
    driver.find_element_by_xpath(
        "(//span[contains(.,'Private and/or commuting to work only')])[2]").click()

    # Is the car currently insured?
    driver.find_element_by_xpath(
        "//label[@for='coverDetail.currentlyInsured.N']").click()
    
    # Roughly how many kilometres is the car driven per year?
    driver.find_element_by_xpath(
        "//input[@name='coverDetail.annualKilometres']").send_keys("10000")
    driver.find_element_by_xpath("//button[contains(.,'Next')]").click()

    # What's the address where the Bmw is normally kept at night?
    driver.find_element_by_xpath(
        "//a[contains(.,'Enter it manually')]").click()
    driver.find_element_by_xpath(
        "//input[@name='coverDetail.overnightParking.address.streetNumber']") \
            .send_keys("21")
    driver.find_element_by_xpath(
        "//input[@name='coverDetail.overnightParking.address.streetName']") \
            .send_keys("Pamela Grove")
    driver.find_element_by_xpath(
        "//input[@name='coverDetail.overnightParking.address.postcode']") \
            .send_keys("3107")
    time.sleep(1)
    driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
    

    # And where at address is the Bmw usually parked?
    driver.find_element_by_xpath("//label[contains(.,'Garaged')]").click()
    
    # What's the regular driver's gender?
    if gender == "male":
        driver.find_element_by_xpath("//label[contains(.,'Male')]").click()
    elif gender == "female":
        driver.find_element_by_xpath("//label[contains(.,'Female')]").click()

    #And their date of birth?
    dob = datetime.now() - relativedelta(years=int(age))

    day_slct = Select(driver.find_element_by_xpath(
        "//select[contains(@name,'day')]"))
    day_slct.select_by_visible_text(str(dob.day))
    month_slct = Select(driver.find_element_by_xpath(
        "//select[@name='coverDetail.driver.dob_month']"))
    month_slct.select_by_visible_text(dob.strftime("%b"))
    year_slct = Select(driver.find_element_by_xpath(
        "//select[contains(@name,'year')]"))
    year_slct.select_by_visible_text(str(dob.year))

    driver.find_element_by_xpath("//button[contains(.,'Next')]").click()

    # What about their employment status?
    driver.find_element_by_xpath(
        "//label[contains(.,'Employed full-time')]").click()

    # At what age did the regular driver obtain their drivers licence?
    driver.find_element_by_xpath(
        "//input[@name='coverDetail.driver.licenceAge']").send_keys("18")
    driver.find_element_by_xpath("//button[contains(.,'Next')]").click()
    
    # Has the regular driver had any motor insurance claims in the last 5 years, regardless of who was at fault?
    driver.find_element_by_xpath("//label[contains(.,'No')]").click()

    # What is the regular driver's current Rating or No Claims Discount (NCD)?
    driver.find_element_by_xpath(
        "//label[contains(@for,'6')]").click()

    # Does the regular driver own another car?
    driver.find_element_by_xpath(
        "//label[@for='coverDetail.ownsAnotherCar.N']").click()

    # Will anyone younger be driving the Bmw?
    driver.find_element_by_xpath(
        "//label[@for='coverDetail.hasYoungerDriver.N']").click()

    # Do you want to exclude any drivers on the policy?
    try:
        driver.find_element_by_xpath(
            "//label[@for='coverDetail.driverOption.NO_RESTRICTION']").click()
    except NoSuchElementException:
        pass

    # What are the policy holders contact details?
    driver.find_element_by_xpath(
        "//input[contains(@name,'applicant.firstName')]").send_keys(name)
    driver.find_element_by_xpath(
        "//input[@name='applicant.lastName']").send_keys(name[::-1])
    driver.find_element_by_xpath("//button[contains(.,'Next')]").click()

    # When would you like the policy for the Mini to commence?
    driver.find_element_by_xpath(
        "//input[@name='applicant.optInPrivacy']").click()
    driver.find_element_by_xpath(
        "//button[contains(.,'Get Quotes')]").click()

    quotes = retrieve_quotes()


    #driver.close()


def get_person(person_id):
    with open('people.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row[0] == str(person_id):
                return row[1], row[2], row[3]
        return "not found", -1, "not found"


def get_rego(car_id):
    with open('cars.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row[0] == str(car_id):
                return row[1]
        return "rego not found"


def retrieve_quotes():
    pass


complete_survey(12, 5)
