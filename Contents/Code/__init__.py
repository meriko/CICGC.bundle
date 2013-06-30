TITLE = 'Comedians In Cars Getting Coffee'

ART  = 'art-default.jpg'
ICON = 'icon-default.png'

BASE_URL = 'http://comediansincarsgettingcoffee.com'

###################################################################################################

def Start():
	Plugin.AddPrefixHandler('/video/cicgc', MainMenu, TITLE, ICON, ART)
	Plugin.AddViewGroup('List', viewMode = 'List', mediaType = 'items')

	# Set the default ObjectContainer attributes
	ObjectContainer.title1     = TITLE
	ObjectContainer.view_group = 'List'
	ObjectContainer.art        = R(ART)

	# Default icons for DirectoryObject and VideoClipObject in case there isn't an image
	DirectoryObject.thumb = R(ICON)
	DirectoryObject.art   = R(ART)
	VideoClipObject.thumb = R(ICON)
	VideoClipObject.art   = R(ART)

	# Set the default cache time
	HTTP.CacheTime = CACHE_1HOUR

###################################################################################################
def MainMenu():
	oc = ObjectContainer()
	
	pageElement = HTML.ElementFromURL(BASE_URL)
	
	# Add shows by parsing the site
	for item in pageElement.xpath("//*[contains(@class, 'all-episodes')]//li"):
		video = {}

		video["url"]  = BASE_URL + item.xpath(".//a/@href")[0]
		video["img"]  = item.xpath(".//img/@src")[0]
		video["name"] = item.xpath(".//h2//span/text()")[0]
		video["desc"] = item.xpath(".//p/text()")[0].strip()

		oc.add(
			EpisodeObject(
				url = video["url"],
				title = video["name"],
				show = TITLE,
				summary = video["desc"],
				thumb = video["img"])
		)
			 
	return oc

