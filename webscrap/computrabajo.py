import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def write_to_file(data: dict):
    with open('./webscrap/data/computrabajo.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys(), delimiter='|')

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(data)


def get_page_job_cards(driver):
    job_cards = driver.find_elements(
        By.XPATH, '/html/body/main/div[8]/div/div[2]/div[1]/article')

    return job_cards


def get_data(driver):
    title = driver.find_element(
        By.XPATH, '/html/body/main/div[8]/div/div[2]/div[2]/p').text

    company = ''
    try:
        company = driver.find_element(
            By.XPATH, '/html/body/main/div[8]/div/div[2]/div[2]/div[1]/div[1]/p[2]/a').text
    except Exception:
        company = 'No disponible'

    location = driver.find_element(
        By.XPATH, '/html/body/main/div[8]/div/div[2]/div[2]/div[1]/div[1]/p[3]').text

    mode = driver.find_element(
        By.XPATH, '/html/body/main/div[8]/div/div[2]/div[2]/div[5]/div[1]/div[1]/div/p[3]'
    ).text

    schedule = driver.find_element(
        By.XPATH, '/html/body/main/div[8]/div/div[2]/div[2]/div[5]/div[1]/div[1]/div/p[2]').text

    description = driver.find_element(
        By.XPATH, '/html/body/main/div[8]/div/div[2]/div[2]/div[5]/div[1]/div[2]')
    description_cleaned = description.text.replace(
        '\n', ' ').replace('\r', ' ')

    published_at = driver.find_element(
        By.XPATH, '/html/body/main/div[8]/div/div[2]/div[2]/div[5]/div[1]/p[2]').text

    url = driver.current_url

    data = {
        'title': title,
        'company': company,
        'location': location,
        'mode': mode,
        'schedule': schedule,
        'description': description_cleaned,
        'url': url,
        'published_at': published_at,
    }

    return data


def next_page(driver):
    next_button = driver.find_element(
        By.XPATH, '//*[@id="offersGridOfferContainer"]/div[6]/span[2]')

    next_button.click()


def main():
    base_url = 'https://ec.computrabajo.com/empleos-en-guayas'

    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(base_url)

    while True:
        job_cards = get_page_job_cards(driver)
        for job_card in job_cards:
            job_card.click()
            time.sleep(1.5)

            try:
                data = get_data(driver)
            except Exception as error:
                print(f'url: {driver.current_url}')
                print(f'error: {error}')
            else:
                write_to_file(data)

        # Exit if there is no next page
        try:
            next_page(driver)

        except Exception:
            break


if __name__ == "__main__":
    main()
