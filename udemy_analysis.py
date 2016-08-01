# -*- coding: utf-8 -*-
# Find out what is current hot topic on udemy --> follow this parttern to create the courses


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import sys

# create a new Firefox session
driver = webdriver.Chrome()

class Course():
	"""docstring for Course"""
	def __init__(self, name, price, enrolled, publish_date):
		self.name = name
		self.price = price
		self.enrolled = enrolled
		self.publish_date = publish_date
		self.revernue = price * enrolled


# python newest
def analysis_for_keyword(keyword, page_number, sort_type):

	# setting for encoding
	reload(sys)  
	sys.setdefaultencoding('utf8')

	driver.implicitly_wait(10)
	driver.maximize_window()
	

	# navigate to the application home page
	url = "https://www.udemy.com/courses/search/?ref=home&src=ukw&q={0}&lang=en&sort={1}".format(keyword, sort_type)

	result = []

	for page in range(page_number):

		# url builder
		if page == 0:
			url_page = url
		else:
			url_page = url + "&p={0}".format(page+1)


		driver.get(url_page)

		for item in range(12):

			try:
				link = driver.find_element_by_xpath('//*[@id="courses"]/li[{0}]/a'.format(item+1))
				link.click()
			except Exception, e:
				link = driver.find_elements_by_xpath('//*[@id="udemy"]/div[2]/div/div/div[3]/ul[1]/course-card-container[{0}]/li/course-card/div/a'.format(item+1)) 
				link[0].click()


			course_title = driver.find_element_by_class_name('course-title')
			price = driver.find_element_by_class_name('current-price ')
			publish_date = driver.find_element_by_class_name('pr10')
			enrolled = driver.find_element_by_class_name('rate-count')
			

			if price.text != 'Free':
				# not do some thing free hehe
				print price.text
				print course_title.text
				print publish_date.text
				print int(enrolled.text.decode('utf-8').split("•")[1].replace('students enrolled','').replace(' ','').replace(',',''))
				print '\n'

				c = Course(course_title.text, 
							int(price.text.replace('$','')), 
							int(enrolled.text.decode('utf-8').split("•")[1].replace('students enrolled','').replace(' ','').replace(',','')),
							publish_date.text)

				# add course to result
				result.append(c)

			driver.back()

	result.sort(key=lambda x: x.revernue, reverse=True)

	
	for course in result:
		print "total revernue     :" + str(course.revernue)
		print "number of enrolled :" + str(course.enrolled)
		print "course name        :" + course.name
		print "publish from       :" + course.publish_date
		print "\n"

	driver.quit()

	with open('{0}_{1}_{2}.txt'.format(keyword, sort_type, page_number), 'a') as f:

		# clean the file
		f.seek(0)		
		f.truncate()

		# write to file
		for course in result:
			f.write("total revernue USD :" + str(course.revernue) + "\n")
			f.write("total revernue VND :" + str(course.revernue * 22000) + "\n")
			f.write("number of enrolled :" + str(course.enrolled) + "\n")
			f.write("course name        :" + course.name + "\n")
			f.write("publish from       :" + course.publish_date + "\n")
			f.write("\n")


analysis_for_keyword('python', 4, 'newest')
#analysis_for_keyword('linux', 2, 'newest')