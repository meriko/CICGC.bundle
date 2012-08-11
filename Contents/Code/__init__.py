###################################################################################################

NAME = 'Comedians in Cars Getting Coffee'

ART = 'art-default.jpg'
ICON = 'icon-default.png'

BASE_URL = 'http://www.comediansincarsgettingcoffee.com/'
ASSET_URL = 'http://assets.comediansincarsgettingcoffee.com/%s/%s-%s-%s'

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
  oc = ObjectContainer(title1 = NAME)

  # Grab the whole page
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
        
          Log(str(ep))
        
          Log("****************************************************************")

          title = 'Coming Soon: ' + ep['guest']
          Log('Title: ' + title)

          summary = ep['title']
          Log('Summary: ' + summary)
          
          url = '/'.join([BASE_URL, ep['slug']])
          Log('URL: ' + url)

          thumb = ASSET_URL % (ep['slug'], ep['type'], ep['key'], 'poster.jpg')
          Log('Thumb: ' + thumb)
          
          # Get duration in milliseconds
          dur = ep['videos'][0]['duration'].split(':')
          duration = (int(dur[0])*60 + int(dur[1])) * 1000
    
          oc.add(VideoClipObject(url = url,
                                 title = title,
                                 thumb = thumb,
                                 summary = summary,
                                 duration = duration))

          Log("****************************************************************")

      # Now get the full episodes
          
      for ep in eplist:
        if ep['type'] == 'full':
        
          Log(str(ep))
          
          Log("****************************************************************")
        
          title = 'Ep. ' + str(int(ep['id']) // 1000) + ': ' + ep['guest']
          Log('Title: ' + title)
        
          summary = ep['title']
          Log('Summary: ' + summary)
        
          url = '/'.join([BASE_URL, ep['slug']])
          Log('URL: ' + url)
        
          thumb = ASSET_URL % (ep['slug'], ep['video_slug'], ep['key'], 'poster.jpg')
          Log('Thumb: ' + thumb)
          
          key = Callback(EpisodeMenu, ep=ep, title=title)
    
          oc.add(DirectoryObject(key = key,
					                       title = title,
		  	                         thumb = thumb,
                                 summary = summary))

          Log("****************************************************************")
          
  return oc

def EpisodeMenu(ep, title):
  ' Constructs the menu for a single episode (episode + bonus content) '
  oc = ObjectContainer(title1 = title)  
  
  for vid in ep['videos']:
   
    Log(str(vid))
  
    Log("----------------------------------------------------------------")
    
    if vid['title'] == '':
      title = ep['title']
    else:
      title = vid['title']
    Log('Title: ' + title)
    
    url = '/'.join([BASE_URL, ep['video_slug'], vid['slug']])
    Log('URL: ' + url)
    
    thumb = ASSET_URL % (ep['slug'], vid['slug'], ep['key'], 'poster.jpg')
    Log('Thumb: ' + thumb)

    # Get duration in milliseconds
    dur = vid['duration'].split(':')
    duration = (int(dur[0])*60 + int(dur[1])) * 1000
    
    oc.add(VideoClipObject(url = url,
                           title = title,
                           thumb = thumb,
                           duration = duration))

    Log("----------------------------------------------------------------")

  return oc