from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
import csv

country_text = "Africa"
country_link = 'https://muckrack.com/beat/africa'

# journalist CSV file
jn_headers = ["Name", "Job Title", "Outlet Name", "Outlet URL", "Biography", "X url", "Linkedin url", "Instagram Url", "facebook url", "threads url", "Topics", "Country", "State", "Suburb", "Email", "Phone", "Picture Url", "Source url", "Last Article Url", "Author Url"]
with open(f"{country_text}jndata.csv", mode="w", newline='') as jn_file:
    jn_writer = csv.writer(jn_file)
    jn_writer.writerow(jn_headers)

#  host csv file
host_headers = ["Name", "Url", "Description", "X Url", "Linkedin url", "instagram Url", "facebook url", "threads url",  "Email", "Phone", "Topics", "Country", "logo Url", "Rss",  "Source Url" ]
with open(f"{country_text}hostdata.csv", mode="w", newline='') as hs_file:
    hs_writer = csv.writer(hs_file)
    hs_writer.writerow(host_headers)


driver = uc.Chrome(headless=False,use_subprocess=True)
driver.get(country_link)
time.sleep(3)


container = driver.find_element(By.CSS_SELECTOR, ".mr-directory-body")
links = container.find_elements(By.CSS_SELECTOR, ".mr-directory-item a")
dir_links = []
for link in links:
    href = link.get_attribute("href")
    dir_links.append(href)
    print(href)

while True:
    # driver.find_element(By.CSS_SELECTOR, "")
    try:
        # Find the "Next" link element using CSS selector
        next_link = driver.find_element(By.CSS_SELECTOR, "ul.pager li:nth-of-type(2) a")
        next_href = next_link.get_attribute('href')

        if next_href is None:
            print("next None breaking ")
            break

        driver.execute_script("arguments[0].scrollIntoView(true);", next_link)
        print(f"Next href: {next_href}")

        next_link.click()
        time.sleep(2)

        container = driver.find_element(By.CSS_SELECTOR, ".mr-directory-body")
        links = container.find_elements(By.CSS_SELECTOR, ".mr-directory-item a")

        for link in links:
            href = link.get_attribute("href")
            dir_links.append(href)
            # print(href)

    except Exception as e:
        print(e)
        
        break

    
print("List Length")
print(len(dir_links))


#  login
login_btn = driver.find_element(By.CSS_SELECTOR, "li.nav-item.me-2 > a")
login_btn.click()
time.sleep(2)

email_input = driver.find_element(By.NAME, "auth-username")
pass_input = driver.find_element(By.NAME, "auth-password")

email_input.send_keys("mianhaseeb.ce@gmail.com")
pass_input.send_keys("gggg2001")

final_login_btn = driver.find_element(By.CSS_SELECTOR, "input.btn.btn-primary.btn-block")
final_login_btn.click()
time.sleep(2)

# iterate links here

for link in dir_links:
    driver.get(link)
    time.sleep(2)


    # scrape the journalist profile data below here
    try:
        name = driver.find_element(By.CLASS_NAME, "profile-name").text
    except:
        name = ''

    try:
        job_title = driver.find_element(By.CSS_SELECTOR, 'li.mr-person-job-item > span').text
    except:
        job_title = ''

    try:
        outlet_name = driver.find_element(By.CSS_SELECTOR, 'li.mr-person-job-item > span > a').text
    except:
        outlet_name = ''

    try:
        outlet_url = driver.find_element(By.CSS_SELECTOR, 'li.mr-person-job-item > span > a').get_attribute('href')
    except:
        outlet_url = ''

    try:
        biography = driver.find_element(By.CSS_SELECTOR, "div.profile-bio > div.mr-card-content > div > p").text
    except:
        biography = ''

    try:
        x_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-x-twitter").get_attribute('href')
    except:
        x_url = ''

    try:
        linkedin_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-linkedin").get_attribute('href')
    except:
        linkedin_url = ''

    try:
        facebook_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-facebook").get_attribute('href')
    except:
        facebook_url = ''

    try:
        insta_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-instagram").get_attribute('href')
    except:
        insta_url = ''

    try:
        threads_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-threads").get_attribute('href')
    except:
        threads_url = ''

    try:
        # Find all topic links within the div
        topic_links = driver.find_elements(By.CSS_SELECTOR, 'div.person-details-item.person-details-beats > div > a')
        
        # Extract topic texts and join them with commas
        topics = ", ".join([link.text for link in topic_links])

    except Exception as e:
        topics = ''
        print(f"An error occurred: {e}")

    try:
        country = driver.find_element(By.CSS_SELECTOR, 'div.person-details-location > span').text.strip()
    except:
        country = ''

    try:
        state = ""
    except:
        state = ''

    try:
        suburb = ""
    except:
        suburb = ''

    try:
        email =  ""
    except:
        email = ''

    try:
        phone = ""
    except:
        phone = ''

    try:
        picture_url = driver.find_element(By.CSS_SELECTOR, 'div.mr-avatar-image > img').get_attribute('src')
    except:
        picture_url = ''

    try:
        source_url = driver.current_url
    except:
        source_url = ''

    try:
        # last_article_url = 
        first_item = driver.find_element(By.CSS_SELECTOR, ".news-story:first-of-type")
        title_element = first_item.find_element(By.CSS_SELECTOR, ".news-story-title a")
        last_article_url = title_element.get_attribute("href")

    except:
        last_article_url = ''

    try:
        author_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-link").get_attribute('href')
    except:
        author_url = ''

    with open(f'{country_text}jndata.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            name, job_title, outlet_name, outlet_url, biography,
            x_url, linkedin_url, insta_url, facebook_url, threads_url, topics, country, state,
            suburb, email, phone, picture_url, source_url, last_article_url, author_url
            ])
    
    name = ""
    job_title = ""
    outlet_name = ""
    biography = ""
    x_url = ""
    linkedin_url = ""
    insta_url = ""
    facebook_url = ""
    threads_url = ""
    topics = ""
    country = ""
    state = ""
    suburb = ""
    email = ""
    phone= ""
    picture_url = ""
    source_url = ""
    last_article_url = ""
    author_url = ""

        
    
    # move to the host page
    try:
        hostPage_btn = driver.find_element(By.CSS_SELECTOR, "li.mr-person-job-item > span > a")
        hostPage_btn.click()
        time.sleep(2)
    except Exception as e:
        print(e)
        print("company not found")
        continue



     # Host profiel scrape code
    try:
        company_name = driver.find_element(By.CSS_SELECTOR, "div.mr-card-content > div > div > h1").text
    except:
        company_name = ""

    try:
        company_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-link").get_attribute('href')
    except:
        company_url = ""


    try:
        topics_div = driver.find_element(By.CLASS_NAME, 'row-item.topic-list.profile-block')

        # Find all topic links within the div
        topic_links = topics_div.find_elements(By.CSS_SELECTOR, 'a.action-link')
        
        # Extract topic texts and join them with commas
        topics = ", ".join([link.find_element(By.CSS_SELECTOR, 'span.topic-label.label-default').text for link in topic_links])
    except:
        topics = ""

    try:
        x_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-x-twitter").get_attribute('href')
    except:
        x_url = ''

    try:
        linkedin_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-linkedin").get_attribute('href')
    except:
        linkedin_url = ''

    try:
        facebook_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-facebook").get_attribute('href')
    except:
        facebook_url = ''
    
    try:
        insta_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-instagram").get_attribute('href')
    except:
        insta_url = ''

    try:
        threads_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-threads").get_attribute('href')
    except:
        threads_url = ''

    try:
        phone = ""
    except:
        phone = ''


    try:
        email = ""
    except:
        email = ''


    try:
        picture_url = driver.find_element(By.CSS_SELECTOR, 'img.ronuded-circle').get_attribute('src')
    except:
        picture_url = ''

    try:
        source_url = driver.current_url
    except:
        source_url = ''
    
    try:
        third_row = driver.find_element(By.CSS_SELECTOR, "tbody tr:nth-child(3)")
        data = third_row.find_element(By.CSS_SELECTOR, "td").text
        country = data
    
    except:
        country = ""

    try:
        rss = driver.find_element(By.CSS_SELECTOR, "a.mr-podcast-url").get_attribute('href')
    except:
        rss = ''

    try:
        description = driver.find_element(By.CSS_SELECTOR, "div.mr-card-content > div > div > div.mt-4").text
    except:
        description = ""

    with open(f"{country_text}hostdata.csv", mode="a", newline='') as hs_file:
            hs_writer = csv.writer(hs_file)
            hs_writer.writerow([company_name, company_url, description, x_url, linkedin_url, insta_url, facebook_url, threads_url, email, phone, topics, country, picture_url, rss, source_url])

    

    






# cols = driver.find_elements(By.CSS_SELECTOR, "div.row.mb-7 > .col-md-3")

# for col_i in range(len(cols)):
#     cols = driver.find_elements(By.CSS_SELECTOR, "div.row.mb-7 > .col-md-3")
#     selected_col = cols[col_i]

#     col_items = driver.find_elements(By.CSS_SELECTOR, ".mr-directory-item > a")

#     for col_index in range(len(col_items)):
#         col_items = driver.find_elements(By.CSS_SELECTOR, ".mr-directory-item > a")
#         col_items[col_index].click()
#         time.sleep(5)




        # scrape the journalist profile data below here


        # try:
        #     name = driver.find_element(By.CLASS_NAME, "profile-nam").text
        # except:
        #     name = ''

        # try:
        #     job_title = driver.find_element(By.CSS_SELECTOR, 'li.mr-person-job-item > span').text
        # except:
        #     job_title = ''

        # try:
        #     outlet_name = driver.find_element(By.CSS_SELECTOR, 'li.mr-person-job-item > span > a').text
        # except:
        #     outlet_name = ''

        # try:
        #     outlet_url = driver.find_element(By.CSS_SELECTOR, 'li.mr-person-job-item > span > a').get_attribute('href')
        # except:
        #     outlet_url = ''

        # try:
        #     biography = driver.find_element(By.CSS_SELECTOR, "div.profile-bio > div.mr-card-content > div > p").text
        # except:
        #     biography = ''

        # try:
        #     x_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-x-twitter").get_attribute('href')
        # except:
        #     x_url = ''

        # try:
        #     linkedin_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-linkedin").get_attribute('href')
        # except:
        #     linkedin_url = ''

        # try:
        #     facebook_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-facebook").get_attribute('href')
        # except:
        #     facebook_url = ''

        # try:
        #     insta_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-instagram").get_attribute('href')
        # except:
        #     insta_url = ''

        # try:
        #     threads_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-threads").get_attribute('href')
        # except:
        #     threads_url = ''

        # try:

        #     topics_div = driver.find_element(By.CLASS_NAME, 'row-item.topic-list.profile-block')

        #     # Find all topic links within the div
        #     topic_links = driver.find_elements(By.CSS_SELECTOR, 'div.person-details-item.person-details-beats > div')
            
        #     # Extract topic texts and join them with commas
        #     topics = ", ".join([link.find_element(By.CSS_SELECTOR, 'a').text for link in topic_links])

        # except:
        #     topics = ''

        # try:
        #     country = driver.find_element(By.CSS_SELECTOR, 'div.person-details-location > span"').text.strip()
        # except:
        #     country = ''

        # try:
        #     state = ""
        # except:
        #     state = ''

        # try:
        #     suburb = driver.find_element(By.XPATH, f'(//div[@class="profile"])[{i+1}]//div[@class="suburb"]').text
        # except:
        #     suburb = ''

        # try:
        #     email =  ""
        # except:
        #     email = ''

        # try:
        #     phone = ""
        # except:
        #     phone = ''

        # try:
        #     picture_url = driver.find_element(By.CSS_SELECTOR, 'div.mr-avatar-image > img').get_attribute('src')
        # except:
        #     picture_url = ''

        # try:
        #     source_url = driver.current_url
        # except:
        #     source_url = ''

        # try:
        #     # last_article_url = 
        #     first_item = driver.find_element(By.CSS_SELECTOR, ".news-story:first-of-type")
        #     title_element = first_item.find_element(By.CSS_SELECTOR, ".news-story-title a")
        #     last_article_url = title_element.get_attribute("href")

        # except:
        #     last_article_url = ''

        # try:
        #     author_url = driver.find_element(By.CSS_SELECTOR, "a.js-icon-link").get_attribute('href')
        # except:
        #     author_url = ''

        # with open('jndata.csv', mode='a', newline='') as file:
        #     writer = csv.writer(file)
        #     writer.writerow([
        #         name, job_title, outlet_name, outlet_url, biography,
        #         x_url, linkedin_url, facebook_url, threads_url, topics, country, state,
        #         suburb, email, phone, picture_url, source_url, last_article_url, author_url
        #         ])

        # # move to the host page
        # hostPage_btn = driver.find_element(By.CSS_SELECTOR, "li.mr-person-job-item > span > a")
        # hostPage_btn.click()
        # time.sleep(2)
        # driver.back()
        # driver.back()
        # time.sleep(2)





# locations_div = driver.find_element(By.CSS_SELECTOR, "div.mr-beats > div.row > div:nth-child(2)")
# location_items = locations_div.find_elements(By.CSS_SELECTOR, ".mr-directory-group-item > a")

# # Iterate over location_items
# for index in range(len(location_items)):

#     # Re-find location_items in each iteration to avoid StaleElementReferenceException
#     time.sleep(1)

#     locations_div = driver.find_element(By.CSS_SELECTOR, "div.mr-beats > div.row > div:nth-child(2)")
#     location_items = locations_div.find_elements(By.CSS_SELECTOR, ".mr-directory-group-item > a")
#     print(location_items[index].text)
#     driver.execute_script("arguments[0].scrollIntoView(true);", location_items[index])

    
#     # Click on the current location item
#     location_items[index].click()
#     print("Clicked on item", index + 1)
#     # time.sleep(2)

#     # Navigate back to the previous page
#     driver.back()
#     print("Navigated back")
#     time.sleep(3)

# print("Finished iterating over", len(location_items), "items")




