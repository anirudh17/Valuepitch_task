from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd
import time

from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/usr/bin/chromedriver") 

driver.get('https://main.sci.gov.in/case-status')
time.sleep(2)


previous = ""


def find_tag_p(table):
    try:
        if table.find_element_by_tag_name('p').get_attribute('innerText') == 'Case Not Found':
            return "Case Not Found"
        else:
            return "repeat"
    except:
        return 'go_ahead'


def click_response():
    global previous
    time.sleep(2)
    if True:
        table = driver.find_element_by_id("DNdisplay")
        if table.get_attribute('innerText') == "":
            return click_response()
        elif find_tag_p(table) == "Case Not Found":
            return "Case Not Found"
        elif table.find_element_by_tag_name('h5').get_attribute('innerText') == previous:
            return click_response()
        else:
            previous = table.find_element_by_tag_name(
                'h5').get_attribute('innerText')
            return table
        click_response()
    else:
        click_response()


table_data = {'Diary No.': [], 'Case No.': [], 'Present/Last Listed On': [], 'Status/Stage': [], 'Disp.Type': [], 'Admitted': [], 'Category': [],
              'Act': [], 'Petitioner(s)': [], 'Respondent(s)': [], 'Pet. Advocate(s)': [], 'Resp. Advocate(s)': [], 'U/Section': [], "Not Found": [], "Tentatively case may be listed on (likely to be listed on)": [], "Impleader(s)": [], "Impleaders Advocate(s)": [], "Intervenor Advocate(s)": []}


def main():
    global table_data
    diary_book = driver.find_element_by_xpath(
        "//a[contains(text(),'Diary Number')]")
    diary_book.click()
    time.sleep(2)
    for year in range(2001, 2021):
        for diary in range(1, 101):
            try:
                captcha = driver.find_element_by_id('cap').find_element_by_tag_name(
                    'font').get_attribute('innerText')

                captcha_box = driver.find_element_by_id('ansCaptcha')
                captcha_box.clear()
                captcha_box.send_keys(str(captcha))

                diary_no = driver.find_element_by_id('CaseDiaryNumber')
                diary_no.clear()
                diary_no.send_keys(str(diary))

                year_select = Select(
                    driver.find_element_by_id('CaseDiaryYear'))
                year_select.select_by_value(str(year))

                driver.find_element_by_id('getCaseDiary').click()

                table_response = click_response()

                if table_response != 'Case Not Found':
                    table = table_response.find_element_by_id(
                        'collapse1').find_element_by_tag_name('table')
                    temp = []
                    for i in table.find_elements_by_tag_name('tr'):
                        tem = i.find_elements_by_tag_name('td')
                        temp.append(tem[0].get_attribute('innerText'))
                        table_data[tem[0].get_attribute('innerText')].append(
                            tem[1].get_attribute('innerText').replace("\xa0", "").replace("\n", ""))
                    for key in table_data:
                        if key not in temp and key != "Not Found":
                            table_data[key].append("")
                    table_data["Not Found"].append("False")
                    temp = []

                else:
                    for key in table_data:
                        if key != "Not Found":
                            table_data[key].append("")
                    table_data["Not Found"].append("True")

                df = pd.DataFrame(table_data)
                df.to_csv('court.csv', index=False)
            except:
                pass


if __name__ == "__main__":
    main()
