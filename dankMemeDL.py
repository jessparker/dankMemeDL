__author__ = 'jungletech'
import praw, requests, glob, re, os
from bs4 import BeautifulSoup

MIN_SCORE = 20

r = praw.Reddit(user_agent='dankMemeDL')
submissions = r.get_subreddit('me_irl').get_hot(limit=5)

imgurUrlPattern = re.compile(r'(http://i.imgur.com/(.*))(\?.*)?')


def download_image(imageUrl, localFileName):
    response = requests.get(imageUrl)
    if response.status_code == 200:
        print('Downloading %s...' % localFileName)
        with open(localFileName, 'wb') as fo:
            for chunk in response.iter_content(4096):
                fo.write(chunk)

for submission in submissions:
    if "imgur.com/" not in submission.url:
        continue # skip non imgur submissions
    if submission.score < MIN_SCORE:
        continue # skip submissions lower than minimum score threshold
    if len(glob.glob('reddit_%s_*' % submission.id)) > 0:
        continue # already downloaded images from this submission

    # download images from album pages
    if 'http://imgur.com/a/' in submission.url:
        albumId = submission.url[len('http://imgur.com/a/'):]
        htmlSource = requests.get(submission.url).text

        soup = BeautifulSoup(htmlSource, "lxml")
        matches = soup.select('.album-view-image-link a')
        for match in matches:
            imageUrl = match['href']
            if '?' in imageUrl:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
            else:
                imageFile = imageUrl[imageUrl.rfind('/') + 1:]
            localFileName = 'reddit_me_irl_%s_album_%s_imgur_%s' % (submission.id, albumId, imageFile)
            download_image('http:' + match['href'], localFileName)

    # download images from single image pages
    elif 'http://imgur.com/' in submission.url:
        htmlSource = requests.get(submission.url).text
        soup = BeautifulSoup(htmlSource, "lxml")
        imageUrl = soup.select('.image a')[0]['href']
        print('soup.select[0]:')
        print(soup.select('.image a')[0])
        print('imageUrl = ' + imageUrl)
        if imageUrl.startswith('//'):
            # if no schema is suplied with the url, prepend 'http:' to it
            imageUrl = 'http:' + imageUrl
        imageId = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('.')]

        if '?' in imageUrl:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:imageUrl.rfind('?')]
        else:
            imageFile = imageUrl[imageUrl.rfind('/') + 1:]

        localFileName = 'reddit_me_irl_%s_album_None_imgur_%s' % (submission.id, imageFile)
        download_image(imageUrl, localFileName)

    # download images from direct links
    elif 'http://i.imgur.com/' in submission.url:
        mo = imgurUrlPattern.search(submission.url)
        imgurFilename = mo.group(2)
        if '?' in imgurFilename:
            # the regex does not catch a '?' at the end of the filename, so we remove it here.
            imgurFilename = imgurFilename[:imgurFilename.find('?')]

        localFileName = 'reddit_me_irl_%s_album_None_imgur_%s' % (submission.id, imgurFilename)
        download_image(submission.url, localFileName)