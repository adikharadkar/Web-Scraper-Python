from flask import Flask, request
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello():
	if request.method == "POST":
		job_position = request.json["job_position"]
		job_location = request.json["job_location"]

		url = f'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={job_position}&txtLocation={job_location}'
		r = requests.get(url)
		soup = BeautifulSoup(r.content, 'lxml')
		d1 = {}
		try:
			lis = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
		except:
			print("Could not find job profiles!")
		count = 0
		for li in lis:
			try:
				position = li.h2.find('a')
				position = position.text.strip()
				print(position)
			except:
				print("Position not available!")
			try:
				company_name = li.find('h3', class_='joblist-comp-name')	
				company_name = company_name.text.strip()
				print(company_name)
			except:
				print("Company Name not available!")
			try:
				experience = li.find('ul', class_='top-jd-dtl clearfix')
				experience = experience.find_all('li')[0]
				experience = experience.text[11:]
				print(experience)
			except:
				print("Experience not available!")
			try:
				location = li.find('ul', class_='top-jd-dtl clearfix')
				location = location.find_all('li')[1].span
				location = location.text
				print(location)
			except:
				print("Location not available!")
			try:
				job_desc = li.find('ul', class_='list-job-dtl clearfix')
				job_desc = job_desc.find_all('li')[0]
				job_desc = job_desc.text[19:-13]
				print(job_desc)
			except:
				print("Job Description not available!")
			try:
				link = li.find('ul', class_='list-job-dtl clearfix')
				link = link.li.find('a')
				link = link.get('href')
				print(link)
			except:
				print("Link not available!")
			
			print('-'*100)
			count += 1

			d = {}
			d["Position"] = position
			d["Company Name"] = company_name
			d["experience"] = experience
			d["Location"] = location
			d["Job Description"] = job_desc
			d["Apply Link"] = link

			d1[count] = d

		return d1

if __name__ == "__main__":
	app.run(debug=True)