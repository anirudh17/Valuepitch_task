from bs4 import BeautifulSoup
import pandas as pd
import time
import requests

table_data = {'Diary No.': [], 'Case No. ': [], 'Present/Last Listed On': [], 'Status/Stage': [], 'Disp.Type': [], 'Admitted': [], 'Category': [],
              'Act': [], 'Petitioner(s)': [], 'Respondent(s)': [], 'Pet. Advocate(s)': [], 'Resp. Advocate(s)': [], 'U/Section': [], "Not Found": [], "Tentatively case may be listed on (likely to be listed on)": [], "Impleader(s)": [], "Impleaders Advocate(s)": [], "Intervenor Advocate(s)": []}


def main():
    global table_data
    time.sleep(1)
    url = 'https://main.sci.gov.in/php/case_status/case_status_process.php'
    captcha = 'https://main.sci.gov.in/php/captcha_num.php'
    for year in range(2001, 2020):
            for diary in range(1,101):
                time.sleep(1)
                res_cap = requests.post(url=captcha)
                response = requests.post(url=url, data = {'d_no': diary, 'd_yr': year,'ansCaptcha':res_cap.text},headers= {'Referer': 'https://main.sci.gov.in/case-status'})
                if response.status_code == 200 and response.text != "" :
                    table = BeautifulSoup(response.text, "html.parser")
                    all_tr = table.find_all('tr')
                    td = all_tr[0].find_all('td')
                    if td[0].get_text().replace("\xa0", "").replace("\n", "") == 'Diary No.':
                        temp = []
                        for tr in all_tr:
                            td = tr.find_all('td')
                            if table_data.get(td[0].get_text().replace("\xa0", "").replace("\n", "")) != None:
                                temp.append(td[0].get_text().replace("\xa0", "").replace("\n", ""))
                                table_data[td[0].get_text().replace("\xa0", "").replace("\n", "")].append(td[1].get_text().replace("\xa0", "").replace("\n", ""))
                        for key in table_data:
                            if key not in temp and key != "Not Found":
                                table_data[key].append("")
                        table_data["Not Found"].append("False")
                        df = pd.DataFrame(table_data)
                        df.to_csv('court.csv', index=False)
                        print("================Diary No. : %d/%d Record Found===============" %(diary,year))

                    else:
                        for key in table_data:
                            if key != "Not Found":
                                if key == 'Diary No.':
                                    table_data[key].append("/".join([str(diary),str(year)]))
                                else:    
                                    table_data[key].append("")
                        table_data["Not Found"].append("True")
                        print("****************Diary No. : %d/%d Record Not Found***********" %(diary,year))

if __name__ == "__main__":
    main()
