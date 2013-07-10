TITLE    = 'Comedians In Cars Getting Coffee'
PREFIX   = '/video/cicgc'
ART      = 'art-default.jpg'
THUMB    = 'icon-default.png'
BASE_URL = 'http://comediansincarsgettingcoffee.com'

###################################################################################################
def Start():
	# Set the default ObjectContainer attributes
	ObjectContainer.title1     = TITLE
	ObjectContainer.art        = R(ART)

	# Set the default cache time
	HTTP.CacheTime = CACHE_1HOUR

###################################################################################################
@handler(PREFIX, TITLE, thumb = THUMB, art = ART)
def MainMenu():
	oc = ObjectContainer()
	
	pageElement = HTML.ElementFromURL(BASE_URL)

	videosListElement = pageElement.xpath("//script[@type = 'application/json']")[0]
	videosDetails     = JSON.ObjectFromString(videosListElement.xpath("./text()")[0])
	
	seasons = []
	
	for item in videosDetails['videos']:
		video = videosDetails['videos'][item]
		
		if video['type'] == 'episode':
			if not video['season'] in seasons:
				oc.add(
					DirectoryObject(
						key = Callback(
								Episodes, 
								season = video['season']
						),
						title = "Season " + video['season']
					)
				)
				seasons.append(video['season'])			

	return oc

###################################################################################################
@route(PREFIX + '/episodes')
def Episodes(season):
	oc = ObjectContainer(title1 = "Season " + season)
	
	pageElement = HTML.ElementFromURL(BASE_URL)

	videosListElement = pageElement.xpath("//script[@type = 'application/json']")[0]
	videosDetails     = JSON.ObjectFromString(videosListElement.xpath("./text()")[0])
	
	episodes = []
	
	for item in videosDetails['videos']:
		video = videosDetails['videos'][item]
		
		if video['type'] == 'episode' and season == video['season']:
			episode = {}
			
			episode['url']                     = BASE_URL + "/" + video['slug']
			episode['title']                   = video['title']
			episode['summary']                 = video['description']
			episode['originally_available_at'] = Datetime.ParseDate(video['pubDate'].split('T')[0]).date()
			episode['season']                  = int(video['season'])
			episode['index']                   = int(video['episode'])
			episode['thumb']                   = video['images']['thumb']
			episode['art']                     = video['images']['poster']
			episode['duration']                = int(video['durationSeconds']) * 1000
			
			episodes.append(episode)		
			
	sortedEpisodes = sorted(episodes, key=lambda episode: episode['index'], reverse = True)
	
	for episode in sortedEpisodes:
		oc.add(
			EpisodeObject(
				url = episode['url'],
				title = episode['title'],
				summary = episode['summary'],
				originally_available_at = episode['originally_available_at'],
				show = TITLE,
				season = episode['season'],
				index = episode['index'],
				thumb = episode['thumb'],
				art = episode['art'],
				duration = episode['duration']
			)
		)
	
	return oc
