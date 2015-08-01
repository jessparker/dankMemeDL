__author__ = 'jungletech'
import praw
import requests
import glob
import fo
from bs4 import BeautifulSoup

MIN_SCORE = 20

r = praw.Reddit(user_agent='dankMemeDL')
submissions = r.get_subreddit('me_irl').get_hot(limit=5)

def downloadImage(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % localFileName)
        with open(localFileName 'wb') as fo:
            or chunk in response.iter_content(4096):
                fo.write(chunk)




for submission in submissions:
    if "imgur.com/" not in submission.url:
        continue # skip non imgur submissions
    if submission.score < MIN_SCORE:
        continue # skip submissions lower than minimum score threshold
    if len(glob.glob('reddit_%s_*' % (submission.id))) > 0:
        continue # already downloaded images from this submission

    if 'http://imgur.com/a/' in submission.url:
        albumId = submission.url[len('http://imgur.com/a/'):]
        htmlSource = requests.get(submission.url).text

        soup = BeautifulSoup(htmlSource)
        matches = soup.select('.album-view-image-link a')
        for match in matches:
            imageUrl = match['href']
            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]

        localFileName = 'reddit_me_irl_%s_album_%s_imgur_%s' % (submission.id, albumId, imageFile)
        downloadImage('http:' + match['href'], localFileName)

