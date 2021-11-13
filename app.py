from re import search
from flask import Flask,request,render_template,url_for,redirect
from bs4 import BeautifulSoup
import requests
import datetime

app = Flask(__name__,static_url_path='/static',static_folder='static')
#86dfae1f211047f48500518cf4fd818f
url = ('https://newsapi.org/v2/top-headlines?'
       'country=in&'
       'apiKey=86dfae1f211047f48500518cf4fd818f')
def get_data(url):
    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    return articles

articles = get_data(url)
@app.route('/')
def home():
    data = requests.get('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true').json()
    
    
    a = data['activeCases']
    r = data['recovered']
    d = data['deaths']
    url = 'https://www.timeanddate.com/weather/'

    res = requests.get(url).content
    soup = BeautifulSoup(res,'html.parser')
    date = datetime.datetime.today().date()
    dataa = soup.find('span',class_='my-city__city')
    data1 = soup.find('span',class_='my-city__temp')
    
    city = dataa.text
    temp = data1.text
   

   

    states=[]
    for i in range(len(data['regionData'])):
        states.append(data['regionData'][i]['region'])
    return render_template('index.html',data = r,states=states,a=a,r=r,d=d,city=city,temp=temp,date=date,articles=articles)    

@app.route('/state/',methods=['POST']) 
def get_results():
    states = []
    data = requests.get('https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST?disableRedirect=true').json()
    keyword = request.form['keyword'] 
    a = data['activeCases']
    r = data['recovered']
    de = data['deaths']
    url = 'https://www.timeanddate.com/weather/'
    



    res = requests.get(url).content
    soup = BeautifulSoup(res,'html.parser')
    date = datetime.datetime.today().date()
    dataa = soup.find('span',class_='my-city__city')
    data1 = soup.find('span',class_='my-city__temp')
    
    city = dataa.text
    temp = data1.text


    for i in range(len(data['regionData'])) :
        if data['regionData'][i]['region'] == keyword :
            name=  data['regionData'][i]['region']
            ac=  data['regionData'][i]['activeCases']
            re=  data['regionData'][i]['recovered']
            ti=  data['regionData'][i]['totalInfected']

            
    for i in range(len(data['regionData'])):
        states.append(data['regionData'][i]['region'])

   
    return render_template('index.html',states= states,a=a,r=r,d=de,name=name[0:5],active=ac,recovered=re,totalInfected=ti,city=city,temp=temp,date=date,articles=articles)

@app.route('/search', methods=['POST','GET'])
def search():
    if request.method =='POST':
            data =request.form['search']
            if not data:
                return redirect(url_for('invalid'))
            else:
                url= ('https://newsapi.org/v2/everything?q='+data+'&apiKey=65729ab9862c408a85621220be43ee5f')
                articles = get_data(url)
                return render_template('search.html',articles=articles,data=data)
        

    
    
if __name__ == '__main__':
    app.run(debug=True)
