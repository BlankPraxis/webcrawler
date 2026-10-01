from crawl import crawl_site_async
from json_report import write_json_report
import sys
import asyncio

async def main():
    if len(sys.argv) < 2:
        print("usage python main.py <base_url> <max_concurrency> <max_pages")
        sys.exit(1)
    elif len(sys.argv) > 4:
        print("too many arguments provided")
        sys.exit(1)

    args = sys.argv
    base_url = args[1]
    if not args[2].isdigit():
        print("max_concurrency must be an integer")
        sys.exit(1)
    if not args[3].isdigit():
        print("max_pages must be an integer")
        sys.exit(1)

    max_concurrency = int(args[2])
    max_pages = int(args[3])

    print(f"starting crawl of: {base_url}")

    page_data = await crawl_site_async(base_url, max_concurrency, max_pages)
    write_json_report(page_data)

    print(f"found {len(page_data)} pages")

    sys.exit(0)

if __name__ == "__main__":
    asyncio.run(main())
