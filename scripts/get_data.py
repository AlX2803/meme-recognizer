import requests
from bs4 import BeautifulSoup
import os

path = os.path.join(os.getcwd(), 'data')


def get_imgs_urls(url):
    imgs_urls = []
    
    while len(imgs_urls) < 200:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        images = soup.find_all('img', {'class':'base-img'})
        
        for image in images:
            imgs_urls.append('https:' + image['src'])
        
        aa = soup.find_all('a', {'class':'pager-next l but'})
        for a in aa:
            url = 'https://imgflip.com' + a['href']

    return imgs_urls

def get_memes_urls_and_template_names():
    memes_urls = []
    template_names = []
    
    url = 'https://imgflip.com/memetemplates?sort=top-all-time'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    h3s = soup.find_all('h3', {'class':'mt-title'})
    aa = []
    
    for h3 in h3s:
        aa.append(h3.findChild("a" , recursive=False))
    
    for a in aa:
        memes_urls.append('https://imgflip.com' + a['href'])
        for content in a.contents:
            template_names.append(content)
            
            
    url = 'https://imgflip.com/memetemplates?sort=top-all-time&page=2'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    h3s = soup.find_all('h3', {'class':'mt-title'})
    aa = []
    
    for h3 in h3s:
        aa.append(h3.findChild("a" , recursive=False))
    
    for a in aa:
        memes_urls.append('https://imgflip.com' + a['href'])
        for content in a.contents:
            template_names.append(content)
            
            
    url = 'https://imgflip.com/memetemplates?sort=top-all-time&page=3'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    
    h3s = soup.find_all('h3', {'class':'mt-title'})
    aa = []
    
    for h3 in h3s:
        aa.append(h3.findChild("a" , recursive=False))
    
    for a in aa:
        memes_urls.append('https://imgflip.com' + a['href'])
        for content in a.contents:
            template_names.append(content)
            
    return memes_urls, template_names
            

def downimg(imgs_urls, folder):
    initial_path = path
    try:
        os.mkdir(os.path.join(initial_path, folder))
    except:
        pass
    os.chdir(os.path.join(initial_path, folder))
    
    for img_url in imgs_urls:
        name = img_url[len('https://i.imgflip.com/'): len(img_url)]
        with open(name, 'wb') as f:
            im = requests.get(img_url)
            f.write(im.content)
            print('Writing: ', name)
            
    os.chdir(initial_path)

def get_data():
    memes_urls, template_names = get_memes_urls_and_template_names()
    print(memes_urls)
    print(template_names)
    for i, _ in enumerate(memes_urls):
        if i != 0:
            imgs_urls = get_imgs_urls(memes_urls[i])
            downimg(imgs_urls, template_names[i])
        
        
def clean_data():
    i = 0
    for subdir, dirs, _ in os.walk(path):
        if i != 0:            
            for filename in os.listdir(subdir):
                file_path = os.path.join(subdir, filename)
                file_size = os.path.getsize(file_path) 
                if file_size < 1000:
                    os.remove(file_path)
        i = i + 1
        
                
    
clean_data()