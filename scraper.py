from selenium import webdriver
import json
import time 
from webdriver_manager.chrome import ChromeDriverManager
import re

# driver options
from selenium.webdriver.chrome.options import Options 


def get_driver():
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    return driver
def get_text(element):
    return element.text if element else ''


def extract_number(text):
    
    # extract number from text
    number_list = re.findall(r'\d+', text)
    if number_list:
        return ''.join(number_list)
    else:
        return ''
    
if __name__ == '__main__':
    print('Starting scraper...')
    JSON_FILE = 'valpak_sparks_nv_14_11.json'
    
    json_file_list = []
    driver = get_driver()
    driver.get('https://www.valpak.com/local/dallas-tx')
    counter = 1
    while True:
        element = driver.find_elements_by_xpath('//button[contains(@class,"text-blue-900")]/span[contains(text(),"Show More")]')
        if counter == 50:
            break
        if len(element) > 0:
            print('Found show more button')
            element[0].click()
            time.sleep(2)
            counter = counter + 1
        else:
           
            break
    print('Scraping data...')
    a_elem = a_elem =  driver.find_elements_by_xpath("//div/a")
    a_list = [a.get_attribute('href') for a in a_elem if 'store' in a.get_attribute('href') ]
    print('Found {} stores'.format(len(a_list)))
    a_list = list(set(a_list))
    # creating the json file
    

    for a in a_list:
        print("Running the url :::",a)
        time.sleep(2)
        driver.refresh()
        driver.get(a)
        try:
            business_name =  get_text(driver.find_element_by_xpath("//h2[contains(@class,'uppercase')]"))
        except:
            business_name = None
        try:
            address = get_text(driver.find_element_by_xpath("//address"))
        except:
            try:
                address = get_text(driver.find_element_by_xpath("//div[contains(@class,'leading-5')]"))
            except:
                address = ''
        try:
            phone =  get_text(driver.find_element_by_xpath("//span[@itemprop='telephone']"))
            phone = extract_number(phone)
        except:
            phone = ''
        try:
            about = get_text(driver.find_element_by_xpath("//aside//p"))
        except:
            try:
                try:
                    about = get_text(driver.find_element_by_xpath("//div[contains(@class,'text-sm')]/p"))
                except:
                    try:
                        about = get_text(driver.find_element_by_xpath("//div[contains(@class,'mb-4 mx-3 text-sm tracking-wide')]/"))
                    except:
                        about = ''
            except:
                    about = ''
        website_element = driver.find_elements_by_xpath('//div[contains(text(),"Visit Website")]/parent::div/parent::a')
        if website_element:
            website = website_element[0].get_attribute('href')
        else:
            website = ''
        
        social_links_elements = driver.find_elements_by_xpath("//th[contains(text(),'Social Links')]/following-sibling::td/div/a")
        social_links = [{social_link.get_attribute('title'):social_link.get_attribute('href')} for social_link in social_links_elements]
        try:
            element_email = driver.find_element_by_xpath('//a[contains(@title, "Email")]')
        except:
            element_email = None
        if element_email:
            email = element_email.get_attribute('href')
        else:
            email = ''

        if about == '':
            about_text = (driver.find_elements_by_xpath("//aside//div[contains(@class, 'text-sm')]"))
            about  = ' '.join([a.text for a in about_text])
            
        # offers 
        
       
        data = {
            'business_name':business_name,
            'address':address,
            'phone':phone,
            'about':about,
            'website':website,
            'social_links':social_links,
            'email':email,
            'product_link':a
        }
        print(data)
        json_file_list.append(data)
        if business_name:
            # writing the json file
            with open(JSON_FILE, 'w') as f:
                json_file = json.dumps(json_file_list, indent=4)
                f.write(json_file)



    

    # save the a_list to a json file
    # with open('a_list.json', 'w') as f:
    #     json.dump(a_list, f)
    

    
