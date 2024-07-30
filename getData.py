import requests
from requests_html import HTMLSession
import collections
collections.Callable = collections.abc.Callable
from bs4 import BeautifulSoup
import pandas as pd

class getData():
    def __init__(self, campus, termyear, core_code, subj_code, schdtype, crse_number, crn, open_only, sess_code, inst_name):
        self.campus = campus
        self.termyear = termyear
        self.core_code = core_code
        self.subj_code = subj_code
        self.schdtype = schdtype
        self.crse_number = crse_number
        self.crn = crn
        self.open_only = open_only
        self.sess_code = sess_code
        self.inst_name = inst_name
        self.s = HTMLSession()
        self.url = 'https://apps.es.vt.edu/ssb/HZSKVTSC.P_ProcRequest'

    def getCampus(self):
        return self.campus

    def parseData(self):
        payload = {
            'CAMPUS': self.campus,
            'TERMYEAR': self.termyear,
            'CORE_CODE': self.core_code,
            'subj_code': self.subj_code,
            'SCHDTYPE': self.schdtype,
            'CRSE_NUMBER': self.crse_number,
            'crn': self.crn,
            'open_only': self.open_only,
            'sess_code': self.sess_code,
            'BTN_PRESSED': 'FIND class sections',
            'inst_name': self.inst_name
        }

        r = self.s.post(self.url, data=payload)
        df = pd.DataFrame(columns=['crn', 'course', 'title', 'schedule', 'modality', 'hours', 'capacity', 'instructor', 'days', 'begin', 'end', 'location'])
        
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.find('table', attrs={'class':'dataentrytable'})

            if table:
                index = 0
                for row in table.find_all('tr'):
                    print("count")
                    columns = row.find_all('td')
                    print(columns[0].text)
                    if columns and index != 0 and columns[0].text.strip().isdigit():
                        crn = columns[0].text.strip()
                        course = columns[1].text.strip()
                        title = columns[2].text.strip()
                        schedule = columns[3].text.strip()
                        modality = columns[4].text.strip()
                        hours = columns[5].text.strip()
                        capacity = columns[6].text.strip()
                        instructor = columns[7].text.strip()
                        days = columns[8].text.strip()
                        begin = columns[9].text.strip()
                        end = columns[10].text.strip()
                        location = columns[11].text.strip()
                        df = df._append({
                                'crn': crn,
                                'course': course,
                                'title': title,
                                'schedule': schedule,
                                'modality': modality,
                                'hours': hours,
                                'capacity': capacity,
                                'instructor': instructor,
                                'days': days,
                                'begin': begin,
                                'end': end,
                                'location': location
                        }, ignore_index=True)
                    index += 1
                print(df)
                return df
            else:
                print("No data table found.")
                return df
        else:
            print(f"Failed to retrieve data, status code: {r.status_code}")
            return df

    def isOpen(self, df):
        return df.empty
    
    def isEqual(self, other):
        if not isinstance(other, getData):
            return False

        # Check if all attributes are equal
        attributes_equal = (
            self.campus == other.campus and
            self.termyear == other.termyear and
            self.core_code == other.core_code and
            self.subj_code == other.subj_code and
            self.schdtype == other.schdtype and
            self.crse_number == other.crse_number and
            self.crn == other.crn and
            self.open_only == other.open_only and
            self.sess_code == other.sess_code and
            self.inst_name == other.inst_name
        )

        if not attributes_equal:
            return False

        # Check if dataframes are equal
        df_self = self.parseData()
        df_other = other.parseData()

        return df_self.equals(df_other)
    
    