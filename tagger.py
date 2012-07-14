#/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import mutagen.id3
from mutagen.flac import FLAC
from mutagen.apev2 import APEv2
from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis


FORMAT = "artist/(date) - album/tracknumber - title"
TAGS = ['artist', 'date', 'album', 'tracknumber', 'title', 'genre']


def clear_tags(filename):
    try:
        if '.mp3' in filename:
            f = APEv2(filename)
        elif '.ogg' in filename:
            f = OggVorbis(filename)
        elif '.flac' in filename:
            f = FLAC(filename)
        for k in f.keys():
            f[k] = u''
        f.save()
    except:
        pass
    # again for mp3 with tags that are worse
    if '.mp3' in filename:
        try:
            f = EasyID3(filename)
            for k in f.keys():
                f[k] = [u'']
            f.save()
        except mutagen.id3.ID3NoHeaderError:
            pass


def write_tags(filename, tags):
    try:
        if '.mp3' in filename:
            f = APEv2(filename)
        elif '.ogg' in filename:
            f = OggVorbis(filename)
        elif '.flac' in filename:
            f = FLAC(filename)
        for t in TAGS:
            f[t] = unicode(tags[t])
        print f
        f.save()
    except:
        pass
    # again for mp3 with tags that are worse
    if '.mp3' in filename:
        f = EasyID3(filename)
        for t in TAGS:
            f[t] = [unicode(tags[t])]
        f.save()



def main(argv):
    directory = argv[1]
    dirname = directory.split(os.sep)[-1]
    if not dirname:           # it happens if you give directory with os.sep
        dirname = directory.split(os.sep)[-2]
    if len(sys.argv) > 2:
        genre = argv[2]
    else:
        genre = ''
    # get filenames from folder
    albums = os.listdir(directory)
    filenames = []
    for album in albums:
        try:
            filenames.extend(
                    [album + os.sep + f for f in \
                            os.listdir(directory + os.sep + album)]
                    )
        except OSError:
            print 'I refuse to work on ', album
    # filter out everything that is not in recognized format
    old_filenames = filenames
    filenames = []
    for f in old_filenames:
        if f.endswith('.mp3') or f.endswith('.ogg') or f.endswith('.flac'):
            filenames.append(f)
    # clear tags
    for f in filenames:
        print 'Cleaning tags for ', f
        clear_tags(directory + os.sep + f)
    # fill them with right info
    #tagnames = FORMAT.replace('(', ' ').replace(')', ' ').replace('/', ' ').replace('-', ' ').split()
    for f in filenames:
        print 'Writing tags for ', directory + os.sep + f
        try:
            # collect tags from filenames
            tags = {}
            # artist is the durectory
            tags['artist'] = dirname
            # year starts the name of the its subdirectory
            tags['date'] = f.split(os.sep)[0].split(')')[0][1:]
            # album is next
            tags['album'] = f.split(os.sep)[0].split(')')[1][1:]
            # filename is "track - title.extension"
            basename = f.split(os.sep)[1].split('.')[0]
            tags['tracknumber'] = str(int(basename.split('-')[0][:-1]))
            tags['title'] = basename.split('-')[1][1:]
            # genre can be given as an arbument
            tags['genre'] = genre
            # write tags
            write_tags(directory + os.sep + f, tags)
        except:
            print 'Error for %s, now it has empty tags' % f


if __name__ == '__main__':
    main(sys.argv)
