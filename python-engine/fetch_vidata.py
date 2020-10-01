import youtube_dl
import requests


def get_transcript_yt(url: str) -> dict:
    """A simple function to get transcript of a YouTube Video

    Parameters
    ----------
    url : str
        The URL of the YouTube video whose transcript is to be fetched

    Returns
    -------
    subtitle_data : dict
        A dict with keys "subtitles" and "type" 
    """

    # Setting youtube_dl options to fetch subtitles
    ydl_options = {
        "writesubtitles": True,
        "allsubtitles": True,
        "writeautomaticsub": True,
    }
    # Creating a youtube_dl object
    subtitle_data = {"subtitles": None, "type": None}
    ydl = youtube_dl.YoutubeDL(ydl_options)

    # We try to fetch the subtitles but in case if it fails we
    # fake the response such that we return subtitle_data without any data.
    try:
        ydl_resp = ydl.extract_info(url, download=False)
    except:
        ydl_resp = {"requested_subtitles": {"en": False}}
        print(f"Error encountered")

    # Checking if the response from youtube_dl has got what we need or not.
    if all([ydl_resp["requested_subtitles"],
            ydl_resp["requested_subtitles"]["en"]]):

        subtitles_url = ydl_resp["requested_subtitles"]["en"]["url"]
        response = requests.get(subtitles_url, stream=True)

        subtitles_type = (
            "manual_captions"
            if len(ydl_resp["subtitles"]) > 0
            else "automatic_captions"
        )

        subtitle_data["subtitles"], subtitle_data["type"] = (
            response.text,
            subtitles_type,
        )

    return subtitle_data


if __name__ == "__main__":
    print(get_transcript_yt("https://www.youtube.com/watch?v=d1CDP6sMuLA"))
    print(get_transcript_yt("https://www.youtube.com/watch?v=nNz8Z1NsuvQ")["subtitles"])
