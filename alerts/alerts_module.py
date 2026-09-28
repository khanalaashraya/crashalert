def generate_alert(is_accident, severity, location, camera_id, coordinates):
    if not is_accident:
        return {
            "alert_generated": False,
            "maps_url": None
        }

    maps_url = None

    if coordinates:
        lat = coordinates["latitude"]
        lon = coordinates["longitude"]
        maps_url = f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map=18/{lat}/{lon}"

    return {
        "alert_generated": True,
        "maps_url": maps_url
    }