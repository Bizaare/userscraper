try:
    import os
    from time import sleep
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from bs4 import BeautifulSoup
    from colorama import Fore, Back, Style
except ModuleNotFoundError:
    print("Modules not installed, properly installing now")
    os.system("pip install selenium")
    os.system("pip install beautifulsoup4")
    os.system("pip install colorama")


print("Please enter a display name EXACTLY as seen\n\n (e.g. typing 'brinda' will only look for users who have a lower-case 'b'\n in their display name, and specifically the name 'brinda'.)\n")
userinput = input("> ")
print('\n\n')

if not isinstance(userinput, str):
    print('Please enter a valid str to scrape')
else:
    print('Please enter how many users you would like to scrape (max 500)')
    snipecount = int(input("> "))

    if snipecount <= 0:
        print('Please enter a valid integer to snipe')
    elif snipecount >= 501:
        print('Please enter a valid integer less than 501')
    elif not isinstance(snipecount, int):
        print('Please type a valid integer')
    else:

        
        url_template = 'https://www.roblox.com/search/users?keyword=' + userinput +'&startIndex={}'
        driver_options = Options()
        driver_options.add_argument("--headless")
        driver_options.add_argument('--log-level=3')
        driver_options.service_log_path = os.devnull
        driver = webdriver.Chrome(options=driver_options)

        usernamelist = []
        userdisplaylist = []
        useridlist = []

        for startIndex in range(0, snipecount, 48):
            url = url_template.format(startIndex)
            driver.get(url)
            sleep(6)
            source = driver.page_source
            soup = BeautifulSoup(source, "html.parser")
            usersnipecontainer = soup.find(id="player-search-page")

            if usersnipecontainer is None:
                print('found error in usersnipecontainer')
                driver.quit()
            else:
                usertypes = usersnipecontainer.find_all("div", class_="avatar-card-container")

            for usertype in usertypes:
                user_displayname = usertype.find("div", class_="text-overflow avatar-name ng-binding ng-scope")
                if user_displayname is not None and user_displayname.text == userinput:
                    user_username = usertype.find("div", class_="text-overflow avatar-card-label ng-binding ng-scope")
                    if user_username is not None and user_username.text.startswith('@'):
                        usernamelist.append(user_username.text)
                        userdisplaylist.append(user_displayname.text)
                    user_id = None
                    user_link = usertype.find("a")
                    if user_link is not None and "/users/" in user_link['href']:
                        user_id = user_link['href'].split("/users/")[1].split("/")[0]
                    if user_id is not None:
                        useridlist.append(user_id)
                
        with open("users.txt", "w") as file:
            formatted_usernames = [username[1:] for username in usernamelist]
            file.write(", ".join(formatted_usernames) + '\n')
            file.write(", ".join(useridlist))
        print('Usernames & their IDs (printed directly below their corresponding username) printed to the file')

        driver.quit()

        os.system('start notepad users.txt')