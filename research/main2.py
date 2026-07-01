import pafy

url_playlist='https://youtube.com/playlist?list=PL_DW1oF5je4ybgpmpck2DRds_l9w5OyQv&si=WkR_-e8JETiEZKjP'
url='https://www.youtube.com/watch?v=gm3-m2CFVWM&list=RDgm3-m2CFVWM&start_radio=1'
playlist = pafy.new(url)
print(playlist)