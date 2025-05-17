import requests
from halo import Halo
from datetime import datetime
import argparse
import time
from gnews import GNews # Add gnews import

def print_hello_world(args):
    """
    check if there is a name argument
    """
    spinner = Halo(text='Checking for name argument...', spinner='dots')
    try:
        spinner.start()
        time.sleep(2) # Add a 2-second delay
        if args.name:
            print(f"\nHello, {args.name}!")
        else:
            print("Hello, World!")
        spinner.succeed("Name argument checked successfully.")
    except Exception as e:
        spinner.fail(f"Error checking the argument: {e}")
        return None
    finally:
        spinner.stop()

def print_datetime():
    """
    Prints the current date and time in a specific format.
    """
    spinner = Halo(text='Getting current date and time...', spinner='dots')
    try:
        spinner.start()
        time.sleep(2) # Add a 2-second delay
        now = datetime.now()
        # Format: Sunday, May 4, 2025 6:15PM
        formatted_time = now.strftime("%A, %B %d, %Y %I:%M%p")
        print(f"\nCurrent date and time: {formatted_time}")
        spinner.succeed("Date and time retrieved successfully.")
    except Exception as e:
        spinner.fail(f"Error getting date and time: {e}")
    finally:
        spinner.stop()

def print_latest_news():
    """
    Fetches and prints the latest 5 news articles using gnews.
    """
    spinner = Halo(text='Getting latest news...', spinner='dots')
    try:
        spinner.start()
        google_news = GNews(language='en', country='US', period='7d', max_results=5)
        # Fetch general top news
        news = google_news.get_top_news()
        # Alternatively, you could search for specific topics:
        # news = google_news.get_news('Python programming')

        if not news:
            print("\nNo news articles found.")
            spinner.warn("No news articles found.")
            return

        print("\nLatest News:")
        for i, article in enumerate(news):
            print(f"{i+1}. {article['title']}")
            print(f"   Link: {article['url']}")

        spinner.succeed("Latest news retrieved successfully.")
    except Exception as e:
        spinner.fail(f"Error getting latest news: {e}")
    finally:
        spinner.stop()


def main():


    parser = argparse.ArgumentParser(description="Template app")
    parser.add_argument('--name',
                       help='The name to say hello to')
    args = parser.parse_args()


    print("Welcome to the Template App!")

    try:
        while True:
            try:
                print("\nMain Menu:")
                print("1. Say Hello, World!")
                print("2. Get time")
                print("3. Get latest news")
                print("4. Exit")
                choice = input("Enter your choice (1-4): ")
                print("\n")
                if choice == '1':
                    print_hello_world(args)
                elif choice == '2':
                    print_datetime()
                elif choice == '3':
                    print_latest_news()
                elif choice == '4':
                    print("\nExiting the program... Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 4.")
            except (KeyboardInterrupt, EOFError):
                print("\n\nExiting the program... Goodbye!")
                exit(0)
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting the program... Goodbye!")
        exit(0)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting the program... Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
