from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import date
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


BIOSPACESEARCHTERM = "https://www.biospace.com/news/?Keywords="
BIOSPACENEXTPAGE = "/html/body/div[1]/div[4]/div/div[2]/div[2]/div[3]/ul/li[8]/a/i"
DEFAULTFOLDER = "News_Searches"
HEADINGXPATH = "/html/body/div[1]/div[4]/div/div/article/h1" #heading
ARTICLEMETA = "/html/body/div[1]/div[4]/div/div/article/div[1]" #publishdate and author
#ARTICLEDATA = "/html/body/div[1]/div[4]/div/div/article/div[2]/p[x]" #article content, change the number in p[]
ARTICLELISTTYPE1 = "/html/body/div[z]/div[4]/div/div[2]/div[2]/ul/li[x]/div/div[2]/h3/a" #article, change the number in li[]
ARTICLELISTTYPE2 = "/html/body/div[z]/div[4]/div/div[2]/div[2]/ul/li[x]/h3/a" #article, change the number in li[]
TYPECHECKLIST = ["announcement", "blog", "editorial", "interview", "news", "opinion", "outlook", "press release"]
KEYWORDS = ["$", "appoint", "budget", "financing", "funding", "merger", "partners"]
#ARTICLEDATA2 = "/html/body/div[1]/div[4]/div/div/article/div[2]/table/tbody/tr[1]/td[2]/p[x]"
#ARTICLEDATA3 = "/html/body/div[1]/div[4]/div/div/article/div[2]/table[2]/tbody/tr[1]/td[2]/p[x]"
PUTYKEYWORDS = ["CSE", "NASDAQ", "NYSE", "OTCQB"]

userTopic = None
userProjectName = None
userFromTime = None
userToTime = None
userInput = None


userTopic = input("-->What topic would you like to search?\n")
userProjectName = input("\n-->What would you like to call this project?\n")

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(BIOSPACESEARCHTERM+userTopic.replace(" ", "+"))
driver.maximize_window()
time.sleep(2)
driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div/a").click()

today = date.today()
os.makedirs("C:/News_Searches/{}_SEARCH_{}_{}".format(userProjectName, userTopic, today.strftime("%Y%b%d")), exist_ok=True) 
def checkExistsByXpath(xpath):
  time.sleep(1)
  try:
    driver.find_element(By.XPATH, xpath)
  except NoSuchElementException:
    return False
  return True
  
def getTextFromElement(xpath):
  text = None
  try:
    text = driver.find_element(By.XPATH, xpath).text
  except Exception as e:
    print(e)
  return text

def handleDollarSign(text):
  am = text[text.find("$"):text.find(" ")]
  l = ["million", "billion", "thousand", "hundred", "m", "b"]
  for x in l:
    if x in text.lower():
      am = text[text.find("$"):text.find(x)] + x
      break
  return am

def getArticleLinkFlag(articleCount):
  flag = None
  if checkExistsByXpath(ARTICLELISTTYPE1.replace("x", "{}".format(articleCount)).replace("z", "1")):
    flag = 11
  elif checkExistsByXpath(ARTICLELISTTYPE1.replace("x", "{}".format(articleCount)).replace("z", "2")):
    flag = 12
  elif checkExistsByXpath(ARTICLELISTTYPE2.replace("x", "{}".format(articleCount)).replace("z", "1")):
    flag = 21
  elif checkExistsByXpath(ARTICLELISTTYPE2.replace("x", "{}".format(articleCount)).replace("z", "2")):
    flag = 22
  return flag

def num_there(s):
  return any(i.isdigit() for i in s)

def writeToFile(currentURL, title, dateOfArticle, authors, typeOfArticle, keywords, locationOfArticle, sourceOfArticle):
  print("+++++++++++++++++++++++++++++++++++++++")
  print("Title: {}".format(title))
  print("dateOfArticle: {}".format(dateOfArticle))
  print("authors: {}".format(authors))
  print("typeOfArticle: {}".format(typeOfArticle))
  print("keywords: {}".format(keywords))
  print("+++++++++++++++++++++++++++++++++++++++")
  file = open("C:/News_Searches/{}_SEARCH_{}_{}/MainOutput_{}_{}.txt".format(userProjectName, userTopic, today.strftime("%Y%b%d"), userTopic, today.strftime("%Y%b%d")), "a", encoding="utf-8")  # append mode
  file.write("\n")
  file.write("URL             -   {}\n\n".format(currentURL))
  file.write("TiAr             -   {}\n".format(title))
  file.write("AuAr             -   {}\n".format(authors))
  file.write("LoAr             -   {}\n".format(locationOfArticle))
  file.write("DaAr             -   {}\n".format(dateOfArticle))
  file.write("SoAr             -   {}\n".format(sourceOfArticle))
  for x in typeOfArticle:
    file.write("TyAr             -   {}\n".format(x))
  file.write("SeaDB             -   {}\n".format("BioSpace"))
  for x in keywords:
    if x[0] != "$" and (len(x[1]) <= 1000):
      file.write("Key             -   {}\n".format(x[0]))
      file.write("SenKey             -   {}\n".format(x[1]))
    elif x[0] == "$":
      if (x[1].strip() != x[2].strip()) and (x[1] != "" or x[2] != "") and (x[1] != " " or x[2] != " ") and num_there(x[1]) and (len(x[2]) <= 1000):
        file.write("Key             -   {}\n".format(x[0]))
        file.write("Am$             -   {}\n".format(x[1]))
        file.write("Sen$             -   {}\n".format(x[2]))
  file.write("\n")
  file.close()

def processArticlesInaPage():
    articleCount = 1
    while True:
      title = "Not Available"
      authors = "Not Available"
      locationOfArticle = "Not Available"
      dateOfArticle = "Not Available"
      sourceOfArticle = "Not Available"
      typeOfArticle = []
      keywords = []
      flag = getArticleLinkFlag(articleCount)
      if not flag:
        break
      if flag == 11:
        driver.find_element(By.XPATH, ARTICLELISTTYPE1.replace("x", "{}".format(articleCount)).replace("z", "1")).click()
      elif flag == 12:
        driver.find_element(By.XPATH, ARTICLELISTTYPE1.replace("x", "{}".format(articleCount)).replace("z", "2")).click()
      elif flag == 21:
        driver.find_element(By.XPATH, ARTICLELISTTYPE2.replace("x", "{}".format(articleCount)).replace("z", "1")).click()
      elif flag == 22:
        driver.find_element(By.XPATH, ARTICLELISTTYPE2.replace("x", "{}".format(articleCount)).replace("z", "2")).click()
      if checkExistsByXpath(HEADINGXPATH):
        title = getTextFromElement(HEADINGXPATH)
      if checkExistsByXpath(ARTICLEMETA):
        dateOfArticle = getTextFromElement(ARTICLEMETA)
        if "by" in dateOfArticle.lower():
              authors = dateOfArticle[dateOfArticle.find("By")+2:]
              dateOfArticle = dateOfArticle[:dateOfArticle.find("By")-1]
        if ":" in dateOfArticle:
              dateOfArticle = dateOfArticle[dateOfArticle.find(":")+1:]
      pElements = driver.find_elements(By.TAG_NAME, "p")
      if pElements:
        for element in pElements:
          text = element.text
          for x in TYPECHECKLIST:
            if x in text.lower() and x not in typeOfArticle:
              typeOfArticle.append(x)
          for x in KEYWORDS:
            textLower = text.lower()
            if x in textLower:
              temp = []
              if x != "$":
                temp.append(x)
                temp.append(text[text.rfind(". ", 0, textLower.find(x))+1:text.find(". ", textLower.find(x))])
              else:
                temp.append(x)
                temp.append(handleDollarSign(text[textLower.find(x):textLower.find(x)+11]))
                temp.append(text[text.rfind(". ", 0, textLower.find(x))+1:text.find(". ", textLower.find(x))])
              keywords.append(temp)
      if keywords:
        currentURL = driver.current_url
        writeToFile(currentURL, title, dateOfArticle, authors, typeOfArticle, keywords, locationOfArticle, sourceOfArticle)
      articleCount += 1
      driver.back()

processArticlesInaPage()
driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div[2]/div[2]/div[3]/ul/li[7]/a/i").click()
while checkExistsByXpath(BIOSPACENEXTPAGE):
  processArticlesInaPage()
  driver.find_element(By.XPATH, BIOSPACENEXTPAGE).click()
  time.sleep(2)
  
