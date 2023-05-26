import requests
import sys
from datetime import datetime
from time import sleep
from selenium import webdriver

def main():
    
    #define webbrowser driver
    #define firefox headless
    option = webdriver.FirefoxOptions()
    option.add_argument("--headless")
    driver=webdriver.Firefox(options=option)
    
    # Get the input file name from the user.
    input_file_name = input("Enter the input file name: ")
#    input_file_name = "short_dns.txt"
    # Open the input file and read the lines.
    with open(input_file_name, "r") as input_file:
        lines = input_file.readlines()
        print("Total URLS : " + str(len(lines)))
    # Do a GET request to each domain name.
    up_domains = []
    count = 0
    for line in lines:
        domain_name = line.strip()
        try:
            count += 1
            print(str(count) + " out of " + str(len(lines)))
            response = requests.get("http://{}/".format(domain_name),timeout=5)
            print("URL is http://" + domain_name + " " + str(response))
            if response.status_code :
                up_domains.append(domain_name)
                driver.get("http://{}/".format(domain_name))
                sleep(1)
                driver.get_screenshot_as_file("http_"+domain_name+".png")
            response = requests.get("https://{}/".format(domain_name),timeout=5)
            print("URL is https://" + domain_name + " " + str(response))
            if response.status_code :
                up_domains.append(domain_name)
                driver.get("https://{}/".format(domain_name))
                sleep(1)
                driver.get_screenshot_as_file("https_"+domain_name+".png")
        except requests.exceptions.RequestException:
            print(domain_name + " is ded")
            pass

    # Print the list of up domains.
    print("The following domains are up:")
#    for domain in up_domains:
    domains = list(set(up_domains))
    print(domains)
    f=open(str(datetime.today().strftime('%Y-%m-%d'))+'_log.txt','w')
    f.write(str(domains))
    f.close()

if __name__ == "__main__":
    main()
