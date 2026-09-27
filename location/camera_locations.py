CAMERA_LOCATIONS = {
    "CAM-01": {
        "name": "KIIT Main Gate",
        "latitude": 20.35349,
        "longitude": 85.81928
    },
    "CAM-02": {
        "name": "Campus Road",
        "latitude": 20.35400,
        "longitude": 85.82000
    },
    "CAM-03": {
        "name": "Hostel Road",
        "latitude": 20.35500,
        "longitude": 85.81900
    }
}


def get_location(camera_id):
    return CAMERA_LOCATIONS.get(camera_id)


def get_location_name(camera_id):
    location = get_location(camera_id)
    return location["name"] if location else "Unknown Location"


def get_coordinates(camera_id):
    location = get_location(camera_id)

    if not location:
        return None

    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"]
    }


def camera_exists(camera_id):
    return camera_id in CAMERA_LOCATIONS