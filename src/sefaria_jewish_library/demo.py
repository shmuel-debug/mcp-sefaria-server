from sefaria_handler import *
import os
import asyncio



import os

async def print_search   ():
    results = await search_texts( "לכשאפנה אשנה")
    
    print(results)
    
async def main():
    print ("searching...")
    await print_search()
    
if __name__ == "__main__":
    asyncio.run(main())
    
