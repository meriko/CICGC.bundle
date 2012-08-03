###################################################################################################

NAME = 'Comedians in Cars Getting Coffee'

ART = 'art-default.jpg'
ICON = 'icon-default.png'

BASE_URL = 'http://www.comediansincarsgettingcoffee.com/'

###################################################################################################
def Start():
  ' Initializes the plugin '

  # Registers plugins for a specific type of file
  Plugin.AddPrefixHandler('/video/cicgc', MainMenu, NAME, ICON, ART)

  # Specifies what view groups the plugin supports
  Plugin.AddViewGroup('List', viewMode='List', mediaType='items')

  # Set default behavior for the menus
  ObjectContainer.view_group = 'List'
  ObjectContainer.art = R(ART)

  # Set default icons and art for directories and videos
  DirectoryObject.thumb = R(ICON)
  DirectoryObject.art = R(ART)
  VideoClipObject.thumb = R(ICON)
  VideoClipObject.art = R(ART)

  # Hard-code cache time-out and user agent
  HTTP.CacheTime = CACHE_1HOUR

###################################################################################################
def MainMenu():
  ''' Constructs the main episode listing.  Since each episode has the main episode
    plus bonus content, make each one a separate directory '''
  oc = ObjectContainer(view_group = 'List', title1 = NAME)

  # Grab the whole page
  page = HTML.ElementFromURL(BASE_URL)

  # Get the various episodes
  episodes = page.xpath('''//div[@class='viewport']//li''')
  
  for ep in episodes:
    Log("****************************************************************")

    # Use guest name as the title
    title = ep.xpath('''.//*[@class='thumb-guest-name']/text()''')[0].strip()
    ep_number = int(ep.xpath('.//a')[0].get('data-episode-id')) // 1000
    title = 'Ep. ' + str(ep_number) + ': ' + title
    Log('Got episode: ' + title)
    
    # Get episode page URL (translate if relative)
    url = ep.xpath('.//a')[0].get('href')
    if url.startswith("http") == False:
            url = BASE_URL + url
    Log('URL: ' + url)

    # Get the episode's summary
    try:
      summary = ep.xpath('''.//*[@class='show-desc']/text()''')[0].strip()
    except:
      summary = 'None'
    Log('Summary: ' + summary)

    # Get the episode's thumbnail URL (translate if relative)
    thumb = ep.xpath('.//img')[0].get('src')
    if thumb.startswith("http") == False:
            thumb = BASE_URL + thumb
    Log('Image: ' + thumb)
	
    key = Callback(EpisodeMenu, url=url)
    
    oc.add(DirectoryObject(key = key,
						   title = title,
		  	               thumb = thumb,
                           summary = summary))
	
    Log("****************************************************************")
	
  # TODO: next episode preview???
	
  return oc

def EpisodeMenu(url):
  ' Constructs the menu for a single episode (episode + bonus content) '
  oc = ObjectContainer(view_group = 'List', title1 = NAME)  
  
  Log("----------------------------------------------------------------")
  
  Log("url: " + url)
  
  Log("----------------------------------------------------------------")
  
  return oc