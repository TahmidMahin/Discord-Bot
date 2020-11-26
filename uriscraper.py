from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from bs4 import BeautifulSoup
import re

path = "./chromedriver"
driver = None

def scrape():
	global driver
	driver = webdriver.Chrome(path)
	driver.get("https://www.urionlinejudge.com.br/judge/en/categories")

	page_elements = driver.find_element_by_id("category-list").find_elements_by_tag_name("li")
	categories = [element.find_element_by_tag_name("a").text+":\n"+element.find_element_by_tag_name("p").text for element in page_elements]
	return page_elements, categories

def select_problem(page_elements, serial):
	global driver
	page_elements[serial].click()

	pages = int(driver.find_element_by_id("table-info").text.split(" ")[-1])
	selected_page = random.randint(1, pages)

	for _ in range(selected_page-1):
		try:
			next_button = WebDriverWait(driver, 10).until(
				EC.presence_of_element_located((By.LINK_TEXT, "NEXT")))
			next_button.click()
		except Exception as e:
			raise e

	problem_list = driver.find_elements_by_class_name("par") + driver.find_elements_by_class_name("impar")
	selected_problem = random.choice(problem_list)
	problem_link = selected_problem.find_element_by_tag_name("a")
	problem_link.click()

	driver.switch_to.frame("description-html")

	bs = BeautifulSoup(driver.page_source, "html.parser")
	driver.close()

	title = bs.title.get_text()

	problem = bs.find("div", {"class": "problem"})

	description = problem.find("div", {"class": "description"})
	description_text = []
	for element in description.find_all("p"):
		image = element.find("img")
		if image:
			description_text.append(image.attrs["src"])
		else:
			description_text.append(element.get_text())

	input_txt = problem.find("div", {"class": "input"})
	input_text = []
	for element in input_txt.find_all("p"):
		image = element.find("img")
		if image:
			input_text.append(image.attrs["src"])
		else:
			input_text.append(element.get_text())		

	output_txt = problem.find("div", {"class": "input"})
	output_text = []
	for element in output_txt.find_all("p"):
		image = element.find("img")
		if image:
			output_text.append(image.attrs["src"])
		else:
			output_text.append(element.get_text())

	raw_table = problem.table.tbody.get_text()
	table = re.split("\n{2,}", raw_table)
	input_sample = "\n".join([line.lstrip() for line in table[1].splitlines()])
	output_sample = "\n".join([line.lstrip() for line in table[2].splitlines()])

	return title, description_text, input_text, output_text, input_sample, output_sample