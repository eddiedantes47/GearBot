import os
from datetime import date
import requests
from dotenv import load_dotenv
import easyocr
from fnmatch import fnmatch
from database import (del_gear, find_all, find_average, find_gear, update_gear, find_id)
from bin.models import GearData, Result, ServerMessages

load_dotenv()
HOME_PATH = os.getenv('HOME_PATH')
DB_PATH = f'{HOME_PATH}gearbotbd.db'


def add_gear(ctx, attachment):
    gear_data = GearData(
        user_id=ctx.author.id, gear_photo=attachment.url,
        family_name=ctx.author.display_name, server_id=ctx.guild.id,
        datestamp=date.today()
    )
    try:
        url = gear_data.gear_photo
        r = requests.get(url, allow_redirects=True)
        filename, file_ext = os.path.splitext(attachment.filename)
        photo_path = f'{HOME_PATH}screenshots/{ctx.author.id}_{file_ext}'
        gear_data.gear_photo = photo_path
        open(photo_path, 'wb').write(r.content)
    except Exception as error:
        return Result(False, f'Error getting photo from discord servers', obj=error)
    
    result = update_gear(gear_data)  # Update the gear data in the database
    if result:
        return Result(True, message=None, gear_data=gear_data)
    else:
        return Result(False, "Failed to update gear in the database")

def get_gear(user_id):
    results = find_gear(user_id)
    if results:
        gear_data = results[0]  # Extract the first (and presumably only) record
        return Result(True, message=None, gear_data=gear_data)
    else:
        return Result(False, message='No gear data found for the specified user.')

from database import find_gear

def get_ap(user_id):
    """Retrieve the AP value for a user."""
    gear_data = find_gear(user_id)
    if gear_data:
        ap_index = gear_data[0].index('ap') if 'ap' in gear_data[0] else None
        return gear_data[0][ap_index] if ap_index is not None else None
    else:
        return None  # Handle the case where no gear data is found

def get_aap(user_id):
    """Retrieve the AAP value for a user."""
    gear_data = find_gear(user_id)
    if gear_data:
        aap_index = gear_data[0].index('aap') if 'aap' in gear_data[0] else None
        return gear_data[0][aap_index] if aap_index is not None else None
    else:
        return None  # Handle the case where no gear data is found

def get_dp(user_id):
    """Retrieve the DP value for a user."""
    gear_data = find_gear(user_id)
    if gear_data:
        dp_index = gear_data[0].index('dp') if 'dp' in gear_data[0] else None
        return gear_data[0][dp_index] if dp_index is not None else None
    else:
        return None  # Handle the case where no gear data is found


def remove_gear(user_id):
    result = del_gear([user_id])
    if not result:
        return Result(True, 'There was no gear associated with your user to remove')
    print(str(result))
    return Result(True, f'Deleted {len(result)} gear entries')

def get_average(guild_id):
    results = find_average([guild_id])
    
    if not results:
        return Result(False, 'This Guild has no gear')
    else:
        gs_sum = sum(int(result[0]) for result in results)
        return Result(True, gs_sum / len(results))


def get_all(guild_id, page):
    if page < 0:
        return Result(False, 'Pages start at 1')

    results = find_all([guild_id], page)
    gear, pages = results if results else ([], 0)

    if page > pages:
        return Result(False, f'There are only {pages} pages of gear available')
    elif not gear:
        return Result(False, 'This Guild has no gear')
    else:
        gear_data = []
        for result in gear:
            gear_data.append(GearData(
                user_id=result[1],
                gear_photo=result[2],
                ap=result[4],
                aap=result[3],
                dp=result[5],
                gs=result[6],
                family_name=result[7],
                server_id=result[8],
                datestamp=result[9]
            ))
        return Result(True, 'done', obj=gear_data, code=pages)


def get_id(guild_id, page):
    if page < 0:
        return Result(False, 'Pages start at 1')

    results = find_id(guild_id, page)
    gear, pages = results if results else ([], 0)

    if page > pages:
        return Result(False, f'There are only {pages} pages of gear available')
    elif not gear:
        return Result(False, 'This Guild has no gear')
    else:
        server_messages = []
        for result in gear:
            server_messages.append(ServerMessages(0, result[1], result[0]))
        return Result(True, 'done', obj=server_messages, code=pages)
