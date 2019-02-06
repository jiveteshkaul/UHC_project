from selenium import webdriver
import time
import sys
import traceback
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json


def convert_text_to_csv(tmp_file,final_op_csv):
    file = open(tmp_file, 'r')
    f = open(final_op_csv, 'w')
    for line in file:

        if line.strip() == "":
            f.write("\n")
                  
        else:
            f.write(line.strip().replace(",","|")+'|')
             
    f.close()            
    
def data_extractor(driver,page_count):

    tmp_file='C:/Users/Komal/Desktop/uhc/Output/tmp_data_file.txt' #Temporary file path
    f = open(tmp_file, "w")
    
    #FOR 1st Page
    cont1=driver.find_element_by_class_name('resultsWrapper')
    time.sleep(5)
    container=cont1.find_elements_by_class_name('outer-container')
    for item in container:
        f.write(item.text) # Write data to file
        f.write("\n")    # Separate by new line
    f.close()
    
    #For remaining pages
    count=1
    next_button_xpath='//*[@id="skip-to-main-content"]/div/div[3]/div[2]/div/button[2]'
    f = open(tmp_file, "a")
    
    while(count < page_count):
        driver.find_element_by_xpath(next_button_xpath).click()
        time.sleep(5)
        cont1=driver.find_element_by_class_name('resultsWrapper')
        time.sleep(5)
        container=cont1.find_elements_by_class_name('outer-container')
        for item in container:
            f.write(item.text) # Write data to file
            f.write("\n")   # Separate by new line
        count+=1
    f.close()
    
    convert_text_to_csv(tmp_file,final_op_csv)
    
def navigate_to_page(state):
    driver = webdriver.Chrome(chrome_driver_loc)
    driver.get('https://connect.werally.com/plans/allSavers/1') # SITE
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[2]/ul/li[2]/h2/div/button')))
    driver.find_element_by_xpath('//*[@id="step-1"]/div[2]/ul/li[2]/h2/div/button').click() # click choice plus
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="changeLocationBtn"]/div[2]/span')))
    driver.find_element_by_xpath('//*[@id="changeLocationBtn"]/div[2]/span').click() # click change location
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="location"]')))
    driver.find_element_by_xpath('//*[@id="location"]').send_keys(state) # send state
    
    time.sleep(8)
    driver.find_element_by_xpath('//*[@id="ngdialog1"]/div[2]/div/div/div/div/div/div/div/location-form/div/autocomplete/div/div/form/div[2]/div/button[2]').click() # click update location
    
    time.sleep(5)
    #WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-0"]/div[3]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img')))
    driver.find_element_by_xpath('//*[@id="step-0"]/div[3]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img').click() # click people
    
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-1"]/div[2]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img')))
    driver.find_element_by_xpath('//*[@id="step-1"]/div[2]/div[1]/ul/li[1]/guided-search-link/button/div[1]/img').click() # click primary care
    
    time.sleep(5)
    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="step-6"]/div[2]/div[1]/ul/li[1]/h2/div/guided-search-link/button')))
    driver.find_element_by_xpath('//*[@id="step-6"]/div[2]/div[1]/ul/li[1]/h2/div/guided-search-link/button').click() # click all primary care physi
    
    time.sleep(5)
    pg_txt=driver.find_element_by_class_name('pagCopy').text #get total number of pages
    page_count=int(pg_txt.split(" ")[-1])
    
    data_extractor(driver,page_count)

def main():
    global state_from_config, final_op_csv, chrome_driver_loc
    filename="C:/Users/Komal/Desktop/uhc/UHC_conf.json"
    configFile = open(filename)
    root = json.load(configFile)
    configFile.close()
    
    for config in root:
        state_from_config = config['state']
        final_op_csv=config['csv_op_file']
        chrome_driver_loc=config['chrome_driver_location']
    
#convert state to crrect format   
    args=state_from_config
    words=args.split(" ")
    state=""
    for item in words:
        state=state+item.capitalize()+" "
             
    chrome_driver=navigate_to_page(state)
    
if __name__=="__main__":
    
    try:
        main()
        print('Done !!')
    except Exception as e:
        print(traceback.format_exc())
        print("Error: {0}".format(e))
