import requests
from operator import itemgetter
from django.conf import settings


def make_request(endpoint, data=None):
    headers = settings.STRAVA.get('headers', [])
    req = requests.get(endpoint, data=data, headers=headers)
    if req.ok:
        return req.json()
    return {}


def get_segments():
    segments_data = {"bounds": settings.BOUNDS_OF_ISTANBUL, "activity_type": "cycling"}
    endpoint = "https://www.strava.com/api/v3/segments/explore"
    data = make_request(endpoint, segments_data)
    return data['segments']
    

def get_score(entry):
    rank = 50 - entry['rank']
    score = (entry['distance'] / entry['elapsed_time']) + rank
    return score


def get_leaderboard():    
    endpoint_template = "https://www.strava.com/api/v3/segments/{id}/leaderboard"
    request_data = {"per_page": 50}
    leaderboard = {}
    segments = get_segments()

    for segment in segments:
        entries = make_request(endpoint_template.format(id=segment['id']), request_data)
        entries = entries.get('entries', [])
        for entry in entries:
            segment['rank'] = entry['rank']
            athlete = leaderboard.get(entry['athlete_id'])
            if athlete:
                athlete['segments'].append(segment.copy())
                athlete['score'] += get_score(entry)
                athlete['segment_count'] += 1
            else:
                leaderboard[entry['athlete_id']] = dict(id=entry['athlete_id'],
                                                        name=entry['athlete_name'],
                                                        profile=entry['athlete_profile'],
                                                        gender=entry['athlete_gender'],
                                                        segments=[segment.copy()],
                                                        score=get_score(entry),
                                                        segment_count=1)
    return leaderboard.values()


def get_sorted_leaderboard():
    leaderboard = get_leaderboard()
    return sorted(leaderboard, key=itemgetter('score'), reverse=True)