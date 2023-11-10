import requests
from bs4 import BeautifulSoup
import csv

# Define the list of tags and the generic URL
# tags = ["intezar", "sad", "tamanna", "romantic", "judai", "ishq", "deshbhakti", "bachpan", "peace", "husn"]
genericUrl = "https://www.rekhta.org/shayari/100-famous-ghazals/?lang=hi"

# Function to scrape and save Shayari data to CSV files
def scrape_and_save_shayari():
    # sher_data = {}  # Dictionary to store sher and their associated tags
    urlList = []
    response = requests.get(genericUrl)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        gazal_list = soup.find_all('div', class_='contentListItems')
        for gazal_item in gazal_list:
            gazal_url = [anchor['href'] for anchor in gazal_item.find_all('a', href=True)]
            gazal_url = [anchor for i, anchor in enumerate(gazal_url) if i & 1 != 0]
            urlList.extend(gazal_url)
    

    # making requests to each of the url: 
    

    sherList = []
    sher_count = 0
    for i, url in enumerate(urlList):
        res = requests.get(url)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            sher_section = soup.find_all('div', class_='w')
            for sher in sher_section:
                sher_lines = sher.find_all('p')
                if len(sher_lines) >= 2:
                    line1 = ' '.join([span.text for span in sher_lines[0].find_all('span')]).strip()
                    line2 = ' '.join([span.text for span in sher_lines[1].find_all('span')]).strip()
                    shayari_text = f"{line1} | {line2}"
                    sherList.append(shayari_text)
                    sher_count += 1
                    # print("Through the {}th sher: ", i+1)
                    # print()
                    # print(shayari_text, '\n\n')
                    
                    
    
    with open('gazal-sher.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['sher'])
        
        for sher in sherList:
            writer.writerow([sher])
        
    
    print("Total sher Count: ", sher_count)
    
    
    
    
    # for tag in tags:
    #     url = genericUrl.format(tag=tag)
    #     response = requests.get(url)
    #     if response.status_code == 200:
    #         soup = BeautifulSoup(response.text, 'html.parser')
    #         sher_section = soup.find_all('div', class_='sherSection')
    #         for sher in sher_section:
    #             sher_lines = sher.find_all('p')
    #             if len(sher_lines) >= 2:
    #                 line1 = ' '.join([span.text for span in sher_lines[0].find_all('span')]).strip()
    #                 line2 = ' '.join([span.text for span in sher_lines[1].find_all('span')]).strip()
    #                 shayari_text = f"{line1} | {line2}"

    #                 if shayari_text not in sher_data:
    #                     sher_data[shayari_text] = [tag]
    #                 else:
    #                     sher_data[shayari_text].append(tag)

    # # Create the original CSV file with unique sher
    # with open('shayari.csv', 'w', newline='', encoding='utf-8') as csvfile:
    #     writer = csv.writer(csvfile)
    #     writer.writerow(['sher', 'tags'])

    #     for sher, tag_list in sher_data.items():
    #         if len(tag_list) == 1:
    #             writer.writerow([sher, ', '.join(tag_list)])

    # # Create a separate CSV file for duplicate shers
    # with open('duplicate_shayari.csv', 'w', newline='', encoding='utf-8') as duplicate_csvfile:
    #     duplicate_writer = csv.writer(duplicate_csvfile)
    #     duplicate_writer.writerow(['sher', 'tags'])

    #     for sher, tag_list in sher_data.items():
    #         if len(tag_list) > 1:
    #             duplicate_writer.writerow([sher, ', '.join(tag_list)])

# Call the function to scrape and save Shayari
scrape_and_save_shayari()
