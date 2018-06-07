from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint
from time import time
from IPython.core.display import clear_output
from warnings import warn
import csv

headers = {"Accept-Language": "en-US, en;q=0.5"}




pages = [str(i) for i in range(1,5)]
years_url =[str(i) for i in range(2000,2018)]






# Lists to store the scraped data in
names = []
years = []
imdb_ratings =[]
metascores = []
votes = []


start_time = time()
requests = 0

for year_url in years_url:

	for page in pages:
		response = get('http://www.imdb.com/search/title?release_date=' + year_url + '&sort=num_votes,desc&page=' + page, headers = headers)
		sleep(randint(8,15))
		
		requests += 1
		elapsed_time = time() - start_time
		print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
		clear_output(wait = True)

		if response.status_code !=200:
			warn('Request: {}; Status code: {}'.format(requests, response.status_code))
		if requests > 72:
			warn('Number of requests was greater than expected.')  
			break 

		page_html = BeautifulSoup(response.text,'html.parser')
		
		mv_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')



		# Extract data from individual movie container
		for container in mv_containers:
			# If the movie has Metascore, then extract:
			if container.find('div',class_='ratings-metascore') is not None:
				name = container.h3.a.text
				names.append(name)

				year= container.h3.find('span',class_='lister-item-year').text
				years.append(year)

				imdb = float(container.strong.text)
				imdb_ratings.append(imdb)

				m_score = container.find('span',class_='metascore').text
				metascores.append(m_score)

				vote = container.find('span',attrs={'name':'nv'})['data-value']
				votes.append(int(vote))

		

movie_ratings = pd.DataFrame({'movie': names,
                              'year': years,
                              'imdb': imdb_ratings,
                              'metascore': metascores,
                              'votes': votes})
print(movie_ratings.info())

movie_ratings = movie_ratings[['movie', 'year', 'imdb', 'metascore', 'votes']]

movie_ratings.loc[:, 'year'] = movie_ratings['year'].str[-5:-1].astype(int)

movie_ratings['n_imdb'] = movie_ratings['imdb'] * 10

movie_ratings.to_csv('movie_ratings.csv')




# print(test_df)



