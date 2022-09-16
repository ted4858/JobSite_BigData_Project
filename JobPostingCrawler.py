from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import datetime

def job_posting(result):
    for page in range(1,8):
        Job_url = 'https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=default_mysearch&loc_mcd=105000&cat_mcls=2&recruitPage=%d&recruitSort=relation&recruitPageCount=100'%page
        print(Job_url)
        html = urllib.request.urlopen(Job_url)
        soupJob = BeautifulSoup(html, 'html.parser')
        tag_div_item = soupJob.find(id="recruit_info_list")
        for job in tag_div_item.select("div.item_recruit"):
            try:
                if len(job) <= 3:
                    break
                job_h2 = job.select("h2.job_tit>a.data_layer>span")
                job_title = job_h2[0].string
                job_a = job.select("div.job_condition>span>a")
                region_list = []
                for li in job_a:
                    region_list.append(li.string)
                job_region = " ".join(region_list)
                job_span = job.select("div.job_condition>span")
                job_career = job_span[1].string
                job_education = job_span[2].string
                job_working_mode = job_span[3].string
                job_strong = job.select("strong.corp_name>a")
                job_company_name = job_strong[0].string
                job_company_name = job_company_name.strip()
                job_job_sector = job.select("div.job_sector>a")
                by_job_list = []
                for li in job_job_sector:
                    by_job_list.append(li.string)
                job_by_job = " ".join(by_job_list)
                result.append([job_title]+[job_region]+[job_career]+[job_education]+[job_working_mode]+[job_company_name]+[job_by_job])
            except:
                continue
    return

def main():
    result = []
    print('Job post crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    job_posting(result)
    job_tbl = pd.DataFrame(result, columns = ('제목', '지역', '경력', '학력', '근무형태', '기업명', '직업별직무'))
    job_tbl.to_csv('D:/Code/Python/job_posting.csv', encoding = 'utf-8-sig', mode = 'w', index = True)
    del result[:]
                      
if __name__ == '__main__':
    main()
