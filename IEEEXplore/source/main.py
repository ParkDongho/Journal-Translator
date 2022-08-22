from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup

def forfor(input):
  a = []
  for j in input.contents:
    if j.name == 'h1' or j.name == 'h2' or j.name == 'h3' or j.name == 'h4'\
            or j.name == 'h5' or j.name == 'kicker' or j.name == 'li' \
            or (j.name == 'p' and len(j.contents)) or (j.name == 'div' and j.attrs['class'][0] == 'figure'):
      a.append(j)
    elif j.name == 'div' or j.name == 'ul' or j.name == 'ol':
      a = a + forfor(j)
    else :
      print("\n\n\nERROR\n\n\n")
  return a

def title2Text(i):
  if i.name == 'h2':  # 제목
    return ['# ', i.text]
  elif i.name == 'h3':  # 제목
    return ['## ', i.text]
  elif i.name == 'h4':  # 제목
    return ['### ', i.text]
  elif i.name == 'h5':  # 제목
    return ['#### ', i.text]
  else:
    return ['error', 'a']

def fig2Text(i):
  if i.name == 'div' and (i.attrs['class'][0] == 'figure') and len(i.attrs['class']) == 2:
    addr = i.contents[1].contents[0].attrs['href']
    title = i.contents[2].contents[0].text
    description = i.contents[2].contents[1].text
    return ['https://ieeexplore.ieee.org' + addr, title, description]
  elif i.name == 'div' and (i.attrs['class'][2] == 'table'):
    addr = i.contents[1].contents[0].attrs['href']
    title = i.contents[0].contents[0].text
    description = i.contents[0].contents[1]
    return ['https://ieeexplore.ieee.org' + addr, title, description]
  else:
    return ['error', 'a', 'a']

def body2Text(i):
  if i.name == 'p':  # 본문
    text = ''
    ref_cont = 0
    ref_start = 0
    inline_formula_num = 0
    inline_formula = []
    for j in i.contents:
      if j.name == 'disp-formula':
        print("disp-formula")
      elif j.name == 'inline-formula':
        text = text + '{inline_formula_'+str(inline_formula_num)+'}'
        inline_formula.append(j.contents[0].text)
        inline_formula_num = inline_formula_num + 1
      # anchor
      elif j.name == 'a' and j.attrs['ref-type'] == 'table': #table
        text = text + '{' + str(j.attrs['anchor']) + '}'
      elif j.name == 'a' and j.attrs['ref-type'] == 'sec':  # ref
        text = text + '{' + str(j.attrs['anchor']) + '}'
      elif j.name == 'a' and j.attrs['ref-type'] == 'disp-formula':  # ref
        text = text + '{' + str(j.attrs['anchor']) + '}'
      elif j.name == 'a' and j.attrs['ref-type'] == 'fig':  # ref
        text = text + '{' + str(j.attrs['anchor']) + '}'
      elif j.name == 'a' and j.attrs['ref-type'] == 'bibr': #ref
        if ref_start == 0:
          #text = text + '[\\REF_1]'
          ref_start = 1
        ref_cont = 0
      elif (j == '–' or j == ', ') and ref_start == 1:
        ref_cont = 1
      elif (j.name == 'i'):
        text = text + j.text
      else:
        if ref_cont == 1:
          text = text + '//'
        ref_start = 0
        text = text + str(j)
    return [text, inline_formula]
  else:
    print('나머지')

google_tran_click = '//*[@id="ow70"]/div/span/button/div[3]'
google_tran_korean = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[8]/div/div[1]/span[1]'
google_tran_english = '//*[@id="yDmH0d"]/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[1]/span/span/div/textarea'
google_tran_english_click = '//*[@id="i8"]/span[3]'
google_tran_addr = 'https://translate.google.com/?sl=en&tl=ko&op=translate'

#file_path = input("주소를 입력 하시오")
id_ieee = input("IEEE ID : ")
pw_ieee = input("PASSWD : ")

# driver = webdriver.Chrome('/Users/parkdongho/dev/Web Crawler/IEEEXplore/chromedriver')
driver = webdriver.Chrome('../chromedriver')
driver_trans = webdriver.Chrome('../chromedriver')

driver.get("https://ieeexplore.ieee.org/Xplore/home.jsp")
driver_trans.get(google_tran_addr)
sleep(3)


driver.find_element(By.XPATH,'//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/xpl-meta-nav/div/div/div/div[2]/ul/li/div[3]/ul/li[2]').click()
sleep(1)
driver.find_element(By.XPATH,'//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/xpl-meta-nav/div/div/div/div[2]/ul/li/xpl-personal-signin/div/div/form/div[1]/input').send_keys(id_ieee)
sleep(1)
driver.find_element(By.XPATH,'//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/xpl-meta-nav/div/div/div/div[2]/ul/li/xpl-personal-signin/div/div/form/div[2]/input').send_keys(pw_ieee)
sleep(1)
driver.find_element(By.XPATH,'//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/xpl-meta-nav/div/div/div/div[2]/ul/li/xpl-personal-signin/div/div/form/div[3]/button').click()
sleep(3)
print("login complete")

link = input("site num : ")

driver.get("https://ieeexplore.ieee.org/document/" + str(link))

sleep(3)
html = driver.page_source
sleep(3)
soup = BeautifulSoup(html, 'html.parser')
sleep(3)

article = driver.find_elements(By.CLASS_NAME,'section')
section_length = len(article)
print(section_length)

title = driver.find_element(By.XPATH, '//*[@id="LayoutWrapper"]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/section[2]/div/xpl-document-header/section/div[2]/div/div/div[1]/div/div[1]/h1/span').text
abstract = driver.find_element(By.XPATH, '/html/body/div[6]/div/div/div/div[3]/div/xpl-root/div/xpl-document-details/div/div[1]/div/div[2]/section/div[2]/div/xpl-document-abstract/section/div[2]/div[1]/div/div[1]/div').text

file_name = title.replace(':', '')
file_name = "../papers/" + file_name + '.md'

file = open(file_name, 'w')


driver_trans.find_element(By.XPATH, google_tran_english).send_keys(abstract)
sleep(3)
abstract = driver_trans.find_element(By.XPATH,google_tran_korean).text
abstract = abstract.replace('\n', "")
driver_trans.get(google_tran_addr)

file.write('# ' + title + '\n\n')
file.write('# Abstract\n\n')
file.write(abstract + '\n\n')

file.close()

text = ''
formula_text = ''
converted_data = []

for sec_num in range(1, section_length+1):
    file = open(file_name, 'a')
    body = soup.select_one('#sec' + str(sec_num))
    body = forfor(body)
    for data in body:
        converted_data = title2Text(data)
        if converted_data[0] != "error":
            if converted_data[0] == '# ':
                text = converted_data[0] + 'SECTION ' + str(sec_num) + ' ' + converted_data[1] + '\n'
            else:
                text = converted_data[0] + converted_data[1] + '\n'
            print(text)
            file.write(text)
        else:
            converted_data = fig2Text(data)
            if(converted_data[0] != "error"):
                text = '\n' + '![](' + converted_data[0] + ')\n' + converted_data[1] + '\n' + converted_data[2] + '\n\n'
                file.write(text)
                print(text)
            else:
                if data.name == 'li':
                    converted_data = body2Text(data.contents[0])
                    driver_trans.find_element(By.XPATH, google_tran_english).send_keys(converted_data[0])
                    sleep(3)
                    translated = driver_trans.find_element(By.XPATH,google_tran_korean).text
                    translated = translated.replace('\n', "")
                    for inline_formula_num in range(0, len(converted_data[1])):
                        formula_text = '{inline_formula_' + str(inline_formula_num) + '}'
                        translated = translated.replace(formula_text, converted_data[1][inline_formula_num])
                    sleep(3)
                    driver_trans.get(google_tran_addr)
                    sleep(3)
                    text = '- ' + translated + '\n'
                    file.write(text)
                    print(text)
                else:
                    converted_data = body2Text(data)
                    driver_trans.find_element(By.XPATH, google_tran_english).send_keys(converted_data[0])
                    sleep(3)
                    translated = driver_trans.find_element(By.XPATH, google_tran_korean).text
                    translated = translated.replace('\n', "")
                    translated = translated.replace('deqn', "Equation")
                    translated = translated.replace('pable', "Table")
                    for inline_formula_num in range(0, len(converted_data[1])):
                        formula_text = '{inline_formula_' + str(inline_formula_num) + '}'
                        translated = translated.replace(formula_text, converted_data[1][inline_formula_num])
                    sleep(3)
                    driver_trans.get(google_tran_addr)
                    sleep(3)
                    text = translated + '\n\n'
                    file.write(text)
                    print(text)
    file.close()
print("finish")


