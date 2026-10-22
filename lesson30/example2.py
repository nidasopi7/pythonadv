from bs4 import BeautifulSoup

from lesson30.example1 import html_content

#Html content

html_content = """
<html>
    <head>
    </head>
    
    <body>
        <h1> Welcome to Beautiful soup</h1>
        <p class="intro">Beautiful Soup makes web scraping easy!</p>
        
        <div id="content">
            <p>here are some links:</p>
            <a >Link 1</a>
            <a >Link 2</a>
            <a >Link 3</a>
            </div>
        </body>
    </html>
"""

soup = BeautifulSoup(html_content, "html.parser")

print("Tittle of the page:",soup.tittle.text)
intro_text = soup.find( 'p', class='intro').text
print(intro_text)



div_content = soup.find('div',id="content")

links = div.content.find_all('a')

for link in links:
    print("")