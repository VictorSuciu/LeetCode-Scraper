
import re
import time
import clipboard
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


URL = 'https://leetcode.com/problems/'
file_url = open('url_extensions.txt', 'r')
url_ext = file_url.readlines()

sign_in_css = '#nav-user-app > div > a.btn.sign-in-btn'
user_css = '#id_login'
pass_css = '#id_password'
sign_in_btn_css = '#signin_btn'
statement_css = '#app > div > div.main__2_tD > div > div > div.side-tools-wrapper__1TS9 > div > div.css-9z7f7i-Container.e5i1odf0 > div.css-jtoecv > div > div.tab-pane__ncJk.css-xailxq-TabContent.e5i1odf5 > div > div.content__u3I1.question-content__JfgR'
solution_class = 'CodeMirror-code'
copy_btn_class = 'btn copy-code-btn btn-default'
copy_btn_css = '.copy-code-btn'
html_re = re.compile(r'<.*?>|&.+?;')

statements_file = open('statements.txt', 'w')
solutions_file = open('solutions.txt', 'w')

driver = webdriver.Chrome()
driver.get('https://leetcode.com/problemset/all')


def strip_html(html_string):
    return re.sub(html_re, '', html_string)


action = ActionChains(driver)

WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sign_in_css)))
action.click(driver.find_element_by_css_selector(sign_in_css))
action.perform()

driver.find_element_by_css_selector(user_css).send_keys("")
driver.find_element_by_css_selector(pass_css).send_keys("")

driver.execute_script('document.querySelector("' + sign_in_btn_css + '").click()')

time.sleep(1)

index = 0
for extension in url_ext:
    index += 1
    driver.get(URL + extension)
    # print('1')
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, statement_css)))
    except:
        # print('2')
        driver.get(URL + extension)
        try:
            # print('3')
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, statement_css)))
        except:
            continue
    
    # print('4')
    statement = driver.find_element_by_css_selector(statement_css)
    # print('5')
    curr_statement = '\n~~~STATEMENT_START~~~\n' + str(index) + '\n' + strip_html(statement.get_attribute('innerHTML').split('Example')[0])
    # print('6')
    driver.get(URL + extension + '/solution')

    try:
        # print('7')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
    except:
        continue
    
    # print('8')
    solution_list = driver.find_elements_by_tag_name('iframe')
    # print('9')
    # print(str(index), '-', 'Length =', len(solution_list))
    found_a_solution = False

    for i in range(len(solution_list)):
        driver.switch_to.default_content()
        try:
            driver.switch_to.frame(i)
            WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.copy-code-btn')))
        except:
            continue

        try:
            driver.find_element(By.CSS_SELECTOR, '.copy-code-btn').click()
        except:
            continue

        found_a_solution = True
        # print('writing solution')
        solutions_file.write('\n~~~START_SOLUTION~~~\n')
        solutions_file.write(str(index) + '\n')
        solutions_file.write(clipboard.paste())
        solutions_file.write('\n~~~END_SOLUTION~~~\n')
        solutions_file.flush()

    if found_a_solution:
        # print('writing statement:', curr_statement)
        statements_file.write(curr_statement)
        statements_file.flush()
