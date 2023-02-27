import requests
from bs4 import BeautifulSoup
import pandas as pd

class SU_WebScraper():
  def __init__(self, department=None) -> None:
    self.department = department

  def select_department(self, dept: str) -> None:
    '''
    Initializes the self.department variable for finding the correct staff page.
    '''
    self.department = dept.lower()

  def find_webpage(self) -> object:
    '''
    Finds and returns the webpage's html, and specifically grabs the staff-item div to navigate.
    '''
    URL = "https://www.shepherd.edu/"+self.department+"/staff"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(class_='content')
    staff_members = results.find_all('div', class_='staff-item')
    return staff_members

  def scrape_webpage(self) -> dict:
    '''
    Iterates through the staff-item div from self.find_webpage() and will grab the staff name, title,
    and email. Email is a bit annoying as it has some extra characters but is taken care of in 
    two built-in string methods. Returns the department in dict form if self.department is a valid department.
    '''
    staff_members = self.find_webpage()
    name_list, title_list, email_list = [], [], []
    for member in staff_members:
      name = member.find("h2").text.strip()
      title = member.find('th', text="Title").find_next('td').text.strip()
      email = member.find('th', text="Email").find_next('td').text.strip()
      email = email.rstrip("                                                           ( Email )")
      email = email.replace('\t', '')
      name_list.append(name)
      title_list.append(title)
      email_list.append(email)
    staff_dict = {
      'Name': name_list,
      'Title': title_list,
      'Email': email_list,
    }
    return staff_dict

  def execute(self) -> object:
    '''
    Executes the webscraper. Takes the dict it returns and converts into a pandas dataframe for
    .csv conversion.
    '''
    staff_dict = self.scrape_webpage()
    df = pd.DataFrame(data=staff_dict)
    return df
  
  def webscrape_rec_loop(self) -> None:
    '''
    Simple recursive loop that allows a user to go through as many departments as they want.
    '''
    string = input("Input your department name to scrape from (ie. CME, Biology, HPERS), or hit enter to close the program. ")
    if string == "":
      quit()
    else:
      self.select_department(string)
      df = self.execute()
      df.to_csv(string+" Department.csv")
      self.webscrape_rec_loop()


if __name__ == "__main__":
  ws = SU_WebScraper()
  ws.select_department('CME')
  df = ws.execute()
  print("The following is a sample of the webscraper:")
  print(df)
  df.to_csv('CME Department.csv')
  ws.webscrape_rec_loop()
