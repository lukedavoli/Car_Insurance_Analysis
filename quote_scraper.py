from bs4 import BeautifulSoup
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.support.select import Select
import time
import winsound

WEBDRIVER_PATH = r"C:\Program Files (x86)\geckodriver.exe"
CTM_ADDR = "https://www.comparethemarket.com.au/car-insurance/journey/start"
PRODIDS = ["BUDD-05-04", "HUDD-01-01", "WOOL-01-02", "REIN-01-02"]


def complete_survey(person_id, car_id, updates=True):
    name, age, gender = get_person(person_id)
    rego_num = get_rego(car_id)

    if updates:
        print("filling survey for pid:{}, cid:{}...".format(person_id, car_id))
    opts = Options()
    opts.headless = True
    driver = webdriver.Firefox(options=opts, executable_path=WEBDRIVER_PATH)
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

    # Are there any factory/dealer options or non-standard accessories fitted
    # to the car?
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
        "(//span[contains(.,'Private and/or commuting to work only')])[2]")\
        .click()

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
        "//input[@name='coverDetail.overnightParking.address.streetNumber']")\
        .send_keys("61")
    driver.find_element_by_xpath(
        "//input[@name='coverDetail.overnightParking.address.streetName']")\
        .send_keys("Parker Street")
    driver.find_element_by_xpath(
        "//input[@name='coverDetail.overnightParking.address.postcode']")\
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

    # And their date of birth?
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

    # Has the regular driver had any motor insurance claims in the last 5
    # years, regardless of who was at fault?
    driver.find_element_by_xpath("//label[contains(.,'No')]").click()

    # What is the regular driver's current Rating or No Claims Discount (NCD)?
    try:
        driver.find_element_by_xpath(
            "//label[contains(@for,'6')]").click()
    except NoSuchElementException:
        pass

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

    if updates:
        print("survey complete, getting quotes...")

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located(
            (By.XPATH, "//div[contains(@class,'1Nszt')]")))
    except TimeoutException:
        print("None of the chosen providers provided a quote")

    quotes = retrieve_quotes(driver.page_source)
    if updates:
        winsound.Beep(1500, 1000)
    driver.close()

    if updates:
        print(quotes)
        print("")
    with open('data/quotes.csv', mode='a', newline='\n') as quotes_csv:
        fieldnames = ['person_id', 'car_id', 'budd_quote', 'hudd_quote',
        'wool_quote', 'real_quote']
        quotes_writer = csv.DictWriter(quotes_csv, fieldnames=fieldnames,
                                       delimiter=',', quotechar='"', 
                                       quoting=csv.QUOTE_MINIMAL)
        quotes_writer.writerow({'person_id': person_id,
                                'car_id': car_id,
                                'budd_quote': quotes[PRODIDS[0]],
                                'hudd_quote': quotes[PRODIDS[1]],
                                'wool_quote': quotes[PRODIDS[2]],
                                'real_quote': quotes[PRODIDS[3]]})


def get_person(person_id):
    with open('data/people.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row[0] == str(person_id):
                return row[1], row[2], row[3]
        return "not found", -1, "not found"


def get_rego(car_id):
    with open('data/cars.csv') as csv_file:
        reader = csv.reader(csv_file, delimiter=',')
        for row in reader:
            if row[0] == str(car_id):
                return row[1]
        return "rego not found"


def retrieve_quotes(page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    results_container = soup.find(id='resultsContainer')
    quotes = {PRODIDS[0]: 'nan', PRODIDS[1]: 'nan', 
              PRODIDS[2]: 'nan', PRODIDS[3]: 'nan'}

    for prodid in PRODIDS:
        if results_container is not None:
            result = results_container.find("div", {"data-productid": prodid})
            if result is not None:
                quote_price = result.find(
                    "span", {"data-id": "quote-price-dollar"}).get_text()
                quotes[prodid] = quote_price
    return quotes

existing_quotes = []
with open('data/quotes.csv') as quotes_csv:
    quotes_reader = csv.DictReader(quotes_csv, delimiter=',')
    for quote_row in quotes_reader:
        existing_quotes.append([quote_row['person_id'], quote_row['car_id']])

with open('data/people.csv') as people_csv:
    people_reader = csv.reader(people_csv, delimiter=',')
    next(people_reader)
    for people_row in people_reader:
        with open('data/cars.csv') as cars_csv:
            cars_reader = csv.reader(cars_csv, delimiter=',')
            next(cars_reader)
            for cars_row in cars_reader:
                if [people_row[0], cars_row[0]] not in existing_quotes:
                    complete_survey(people_row[0], cars_row[0])    
            
