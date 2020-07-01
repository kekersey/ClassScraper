from bs4 import BeautifulSoup
import requests
import time
import winsound


def get_class_numbers():
    courses = open("courses.txt", "r")
    raw_numbers = courses.readlines()
    courses.close()
    stripped_numbers = list()
    for course in raw_numbers:
        stripped_numbers.append( course.strip() )
    return stripped_numbers

def get_course_urls(stripped_numbers):
    class_urls = list()
    with open("index.html", "r") as f:
        page = f.read()
    index_soup = BeautifulSoup( page, 'html.parser')
    for course_number in stripped_numbers:
        for url in index_soup.find_all('a', id="class_nbr_" + course_number):
            class_urls.append( url.get('href') )
    return class_urls

def check_classes( class_urls ):
    class_and_seats = list()
    for i in class_urls:
        class_page = requests.get( i )
        class_soup = BeautifulSoup( class_page.content, "html.parser" )
        class_name = class_soup.find( 'h2' ).string.strip().replace("\xa0", "")
        available_seats = int(class_soup.find( 'dt', text='Available Seats').findNext( 'dd' ).string)
        class_and_seats.append( (class_name, available_seats) )
        if( available_seats > 0 ):
            notify()
    return class_and_seats

def notify():
    winsound.Beep( 440, 1000 )

def main():
    classes = get_class_numbers()
    classes = get_course_urls(classes)
    try:
        while True:
            check_classes( classes )
            time.sleep(10)
    except KeyboardInterrupt:
        print("KeyboardInterrupt has been caught.")

if __name__ == "__main__":
    main()