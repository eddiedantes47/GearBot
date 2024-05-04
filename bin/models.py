from dataclasses import dataclass
from datetime import date


from dataclasses import dataclass
from datetime import date

from dataclasses import dataclass
from datetime import date

@dataclass
class GearData:
    user_id: int
    gear_photo: str
    ap: int
    aap: int
    dp: int
    gs: int
    family_name: str
    server_id: int
    datestamp: date



@dataclass
class Result:
    status: bool
    message: str = None
    photos: str = None
    gear_data: GearData = None
    obj: object = None
    code: int = 0

@dataclass
class ServerInfo:
    server_id: int
    server_admin_role_id: int
    requests_made: int = 500
    general_channel_id: int = None
    gear_channel_id: int = None

@dataclass
class ServerMessages:
    server_id: int
    message: str
    user_id: int