from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup,SoupStrainer
import pandas as pd
import time
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome("/usr/bin/chromedriver") 
driver.get('https://main.sci.gov.in/case-status')



def wait():
    time.sleep(1)
    table = driver.find_element_by_id("DNdisplay")
    print("========","waiting for response","==========")
    if table.get_attribute('innerText') == "":
        return wait()
    else:
        return "ok"


table_data = {'Diary No.': [], 'Case No. ': [], 'Present/Last Listed On': [], 'Status/Stage': [], 'Disp.Type': [], 'Admitted': [], 'Category': [],
              'Act': [], 'Petitioner(s)': [], 'Respondent(s)': [], 'Pet. Advocate(s)': [], 'Resp. Advocate(s)': [], 'U/Section': [], "Not Found": [], "Tentatively case may be listed on (likely to be listed on)": [], "Impleader(s)": [], "Impleaders Advocate(s)": [], "Intervenor Advocate(s)": []}


def main():
    count = 1
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

                if wait() == "ok":
                    only_tags_with_id_DNdisplay = SoupStrainer(id="collapse1")
                    table = BeautifulSoup(driver.page_source, "html.parser", parse_only=only_tags_with_id_DNdisplay )
                    if table.get_text() == "":
                        for key in table_data:
                            if key != "Not Found":
                                table_data[key].append("")
                        table_data["Not Found"].append("True")

                    elif table.get_text() != "":
                        temp = []
                        all_tr = table.find_all('tr')
                        for tr in all_tr:
                            td = tr.find_all('td')
                            temp.append(td[0].get_text())
                            table_data[td[0].get_text()].append(td[1].get_text().replace("\xa0", "").replace("\n", ""))
                        for key in table_data:
                            if key not in temp and key != "Not Found":
                                table_data[key].append("")
                        table_data["Not Found"].append("False")
                        df = pd.DataFrame(table_data)
                        df.to_csv('court.csv', index=False)
                time.sleep(1)
                print("===========In Try==============",count)
                count += 1
            except:
                print("===========In except==============",count)
                count += 1
                pass


if __name__ == "__main__":
    main()