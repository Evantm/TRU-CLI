import bs4
from bs4 import BeautifulSoup
import requests
from time import sleep
import urllib
import click


url = 'https://banssbprod.tru.ca/banprod/bwckctlg.p_disp_listcrse?term_in={0}{1}&subj_in={2}&crse_in={3}&schd_in=%'
# 30 is summer, 20 is winter, 10 is fall but YEAR is 1 greate
semester_List = {'Summer': 30, 'Winter': 20, 'Fall': 10}
class_Num = {} #1130 or 1230 etc
class_Name = {} #add list of possible classes later



loop = False


@click.command()
@click.option('-y','--year', prompt='Year',
              help='What year you want to scan.')
@click.option('-s','--semester', type=click.Choice(['Summer', 'Winter','Fall']), prompt='Semester',
              help='The semester you want to scan.')
@click.option('-num','--num', prompt='Class Number',
              help='The number of the class ex. 1130 or 1230. ')
@click.option('-name','--name', prompt='Subject Name',
              help='The name of the subject ex. COMP or PHIL. Use \'%\' as a wildcard ')


def scan(year, semester, num, name):
    while(True):

        if num == '%':
            loop = True
            num = 1000

        year = str(year).strip()
        semester = str(semester).strip()
        num = str(num).strip()
        name = str(name).strip()

        semester_num = semester_List[semester]
        year = year - 1 if semester == 10 else year


        req = urllib.request.Request(
            url=url.format(year,semester_num,name,num),
            data=None,
            headers={
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
            }
        )

        f = urllib.request.urlopen(req)
        soup = BeautifulSoup(f.read().decode('utf-8') , "lxml")

        # TH.ddtitle
        # TD.dddefault tbody

        found_titles = soup.select("th.ddtitle")
        found_desc = soup.select('td.dddefault')

        new_desc = []



        for tag in found_desc:
            bs = BeautifulSoup(str(tag) , "lxml")
            if bs.string is not None:
                new_desc.append(bs.string)

        list_of_desc = (str(new_desc).strip(']').split('\'Class\','))


        #we need to get it so it iterates 6 for ever one.
        for tag in found_titles:
            bs = BeautifulSoup(str(tag) , "lxml")
            print(bs.string)
            print(list_of_desc[found_titles.index(tag) + 1])

        if not loop:
            break
        else:
            num = int(num) + 10
            sleep(1)


if __name__ == '__main__':
    scan()