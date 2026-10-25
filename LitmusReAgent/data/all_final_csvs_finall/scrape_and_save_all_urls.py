import os
import csv
import json
import sys
from pathlib import Path
import time


# Add the parent directory to the Python path to import the scraping function
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.tools.db_search_and_scrape_copy import scrape_url_with_firecrawl

def collect_urls_from_csvs(base_folder):
    """
    Collect all URLs from CSV files in subfolders.
    """
    urls = set()
    base_path = Path(base_folder)
    
    # Iterate through all subfolders
    for subfolder in base_path.iterdir():
        if subfolder.is_dir() and not subfolder.name.startswith('__'):
            print(f"Processing folder: {subfolder.name}")
            
            # Look for CSV files in the subfolder
            for csv_file in subfolder.glob("*.csv"):
                print(f"  Processing CSV: {csv_file.name}")
                
                try:
                    with open(csv_file, 'r', encoding='utf-8') as file:
                        reader = csv.DictReader(file)
                        
                        # Check if URL column exists
                        if 'URL' in reader.fieldnames:
                            for row in reader:
                                url = row['URL'].strip()
                                if url and url.startswith(('http://', 'https://')):
                                    urls.add(url)
                        else:
                            print(f"    Warning: No 'URL' column found in {csv_file.name}")
                            
                except Exception as e:
                    print(f"    Error reading {csv_file.name}: {e}")
    
    return urls

def load_existing_scraped_data(output_file):
    """
    Load existing scraped data if the file exists.
    """
    if os.path.exists(output_file):
        try:
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"Loaded existing data with {len(data)} URLs from {output_file}")
            return data
        except Exception as e:
            print(f"Error loading existing data: {e}")
            return {}
    return {}

def save_scraped_data(scraped_data, output_file):
    """
    Save scraped data to JSON file.
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(scraped_data, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False

def scrape_url_with_retry(url, max_retries=2):
    """
    Scrape a URL with retry logic.
    Retries up to max_retries times if the scraping fails or returns null content.
    """
    for attempt in range(max_retries + 1):
        try:
            time.sleep(10)
            result = scrape_url_with_firecrawl(url)
            
            # Check if scraping was successful and content is not null/empty
            if result.get('success') and result.get('markdown') and result.get('markdown').strip():
                if attempt > 0:
                    print(f"  ✓ Successfully scraped on attempt {attempt + 1}")
                else:
                    print(f"  ✓ Successfully scraped")
                return result
            else:
                error_msg = result.get('error', 'No content returned or content is null/empty')
                if attempt < max_retries:
                    print(f"  ⚠️ Attempt {attempt + 1} failed: {error_msg}. Retrying...")
                    time.sleep(5)  # Additional delay before retry
                else:
                    print(f"  ✗ Failed after {max_retries + 1} attempts: {error_msg}")
                    return result
                    
        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries:
                print(f"  ⚠️ Attempt {attempt + 1} failed with exception: {error_msg}. Retrying...")
                time.sleep(5)  # Additional delay before retry
            else:
                print(f"  ✗ Failed after {max_retries + 1} attempts with exception: {error_msg}")
                return {
                    'content': '',
                    'success': False,
                    'error': error_msg
                }
    
    # This should not be reached, but just in case
    return {
        'content': '',
        'success': False,
        'error': 'Unknown error after all retry attempts'
    }

def scrape_and_save_urls(urls, output_file="scraped_content.json"):
    """
    Scrape URLs and save the content with URL mapping.
    Resumes from where it left off if interrupted.
    Includes retry logic for failed scraping attempts.
    """
    # Load existing data
    scraped_data = load_existing_scraped_data(output_file)
    
    # Filter out URLs that have already been successfully processed
    remaining_urls = []
    for url in urls:
        if url not in scraped_data:
            remaining_urls.append(url)
        elif not scraped_data[url].get('success', False) or not scraped_data[url].get('content', '').strip():
            # Re-attempt failed URLs or URLs with null/empty content
            print(f"Re-queueing failed/empty URL: {url}")
            remaining_urls.append(url)
    
    total_urls = len(urls)
    already_scraped = len(scraped_data) - len([url for url in scraped_data if not scraped_data[url].get('success', False)])
    
    print(f"\nTotal URLs: {total_urls}")
    print(f"Already successfully scraped: {already_scraped}")
    print(f"Remaining to scrape (including retries): {len(remaining_urls)}")
    
    if not remaining_urls:
        print("All URLs have already been successfully scraped!")
        return scraped_data
    
    print(f"\nStarting scraping process...")
    
    
    for i, url in enumerate(remaining_urls, 1):
        print(f"[{i}/{len(remaining_urls)}] Scraping: {url}")
        
        result = scrape_url_with_retry(url)
        scraped_data[url] = {
            'content': result.get('markdown', ''),
            'success': result.get('success', False),
            'error': result.get('error', None)
        }
        
        # Save after each URL to preserve progress
        if save_scraped_data(scraped_data, output_file):
            print(f"  💾 Progress saved ({i}/{len(remaining_urls)})")
        else:
            print(f"  ⚠️ Failed to save progress")
    
    print(f"\nAll scraping completed! Final data saved to: {output_file}")
    
    # Print summary
    successful = sum(1 for data in scraped_data.values() if data.get('success', False) and data.get('content', '').strip())
    failed = sum(1 for data in scraped_data.values() if not data.get('success', False))
    empty_content = sum(1 for data in scraped_data.values() if data.get('success', False) and not data.get('content', '').strip())
    
    print(f"Summary:")
    print(f"  ✓ Successful with content: {successful}")
    print(f"  ✗ Failed: {failed}")
    print(f"  ⚠️ Success but empty content: {empty_content}")
    print(f"  Total URLs processed: {total_urls}")
    
    return scraped_data

def main():
    # Set the base folder path
    base_folder = os.path.dirname(os.path.abspath(__file__))
    
    print("Step 1: Collecting URLs from CSV files...")
    urls = collect_urls_from_csvs(base_folder)
    
    print(f"\nFound {len(urls)} unique URLs")
    
    if not urls:
        print("No URLs found. Exiting.")
        return
    
    # Convert set to sorted list for consistent ordering
    urls_list = sorted(list(urls))
    
    print("\nStep 2: Scraping URLs...")
    scraped_data = scrape_and_save_urls(urls_list)
    
    print("\nProcess completed!")

if __name__ == "__main__":
    main()
