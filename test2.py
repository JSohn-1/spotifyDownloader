from subsonic2 import subsonic as sc

s = sc("http://192.168.1.99:4533", "yacob", "Waterfire9$", legacy=True)
# s = sc("http://192.168.1.29:5082", "yacob", "Waterfire9$", legacy=True)

if s.isAdmin():
    print("Admin")

print(s.search2("Magic"))
# print(type(s.search("You")['song']))
# print(s.findSongId("Bad Memories (feat. Elley Duhé & FAST BOY)"))
# print(s.deletePlaylist(s.findPlaylistId("e")))