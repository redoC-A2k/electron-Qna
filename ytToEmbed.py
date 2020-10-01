import sys
def ytlinktoembedlink(url):
    urlList = list(url)
    flag = 0 
    for i in urlList :
        if i == '?':
            flag = 1
            break 
    if flag == 1 :
        url = url.split('?') 
        id = url[1].split('=')
        id = id[1]
    else :
        url = url.split('/')
        id = url[3]
    embedlink = 'https://www.youtube.com/embed/'
    embedlink = embedlink + id + '?autoplay=1'
    return embedlink
link = ytlinktoembedlink(sys.argv[1])
print(link)
sys.stdout.flush()