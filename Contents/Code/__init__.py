NAME = 'Comedians in Cars Getting Coffee'
ART = 'art-default.jpg'
ICON = 'icon-default.png'

BASE_URL = 'http://www.comediansincarsgettingcoffee.com'
ASSET_URL = 'http://assets.comediansincarsgettingcoffee.com/%s/%s-%s-%s'

###################################################################################################
def Start():

	ObjectContainer.art = R(ART)
	ObjectContainer.title1 = NAME

	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art = R(ART)
	VideoClipObject.thumb = R(ICON)

	HTTP.CacheTime = CACHE_1HOUR
	HTTP.Headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:18.0) Gecko/20100101 Firefox/18.0'

###################################################################################################
@handler('/video/cicgc', NAME, thumb=ICON, art=ART)
def MainMenu():

	# Constructs the main episode listing.	Since each episode has the main episode
	# plus bonus content, make each one a separate directory
	oc = ObjectContainer()

	page = HTML.ElementFromURL(BASE_URL)

	# All the episode info is passed as a dictionary to a javascript function --
	# let that do all the work for us...

	# The script is javascript and has no source
	scripts = page.xpath('''//script[@type='text/javascript' and not(@src)]/text()''')

	for s in scripts:
		# The one we want runs on $(document).ready
		if(s.find("$(document).ready(function()") != -1):
			# Use the JSON parser to get python objects
			eplist = JSON.ObjectFromString(s[s.find("["):s.rfind("]")+1])

			# Purely for cosmetic reasons, I want the preview to be the first item in the list
			# However, it is listed last, so parse the list twice, looking for the preview first...
			for ep in eplist:
				if ep['type'] == 'preview':
					title = 'Coming Soon: ' + ep['guest']
					summary = ep['title']
					url = '/'.join([BASE_URL, ep['slug']])
					thumb = ASSET_URL % (ep['slug'], ep['type'], ep['key'], 'poster.jpg')

					# Get duration in milliseconds
					dur = ep['videos'][0]['duration'].split(':')
					duration = (int(dur[0])*60 + int(dur[1])) * 1000

					oc.add(VideoClipObject(
						url = url,
						title = title,
						thumb = thumb,
						summary = summary,
						duration = duration
					))

			# Now get the full episodes
			for ep in eplist:
				if ep['type'] == 'full':
					title = 'Ep. ' + str(int(ep['id']) // 1000) + ': ' + ep['guest']
					summary = ep['title']
					url = '/'.join([BASE_URL, ep['slug']])
					thumb = ASSET_URL % (ep['slug'], ep['video_slug'], ep['key'], 'poster.jpg')

					oc.add(DirectoryObject(
						key = Callback(EpisodeMenu, ep=ep, title=title),
						title = title,
						thumb = thumb,
						summary = summary
					))

	return oc

####################################################################################################
@route('/video/cicgc/episodes', ep=dict)
def EpisodeMenu(ep, title):

	# Constructs the menu for a single episode (episode + bonus content)
	oc = ObjectContainer(title2=title)

	for vid in ep['videos']:
		if vid['title'] == '':
			title = ep['title']
		else:
			title = vid['title']

		url = '/'.join([BASE_URL, ep['slug'], vid['slug']])
		thumb = ASSET_URL % (ep['slug'], vid['slug'], ep['key'], 'poster.jpg')

		# Get duration in milliseconds
		dur = vid['duration'].split(':')
		duration = (int(dur[0])*60 + int(dur[1])) * 1000

		oc.add(VideoClipObject(
			url = url,
			title = title,
			thumb = thumb,
			duration = duration
		))

	return oc
