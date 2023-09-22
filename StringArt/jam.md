# String Art

### Mission
Place x dots in a circle or rectangle \
Take an image as the input \
Connect a continuos line from dot to dot in order to recreate the image as best as possible \
*or just watch the [video](https://youtu.be/WGccIFf6MF8)*

### How to use
- Copy a image (png or jpg) to ./img/
- Go into main.py and set the values you like to use (line 4-12)
- Run main.py and enter the name of your image
- Let it run until it closes it self
- Look into ./results/ and find your image
- Run gifmaker.py, enter the name of the folder in ./results, say if it should be a mp4 or a gif, give a number of frames it should render
- Done, you created some cool looking string art!

### Comment
Was super fun to make, the principal and basics are really easy, the optimizing part was the fun bit. In total I completely reworked this thing about 3 times and always improved a lot. According to my measurements I ended up with about 0.07 seconds per drawn line with an 500x500 pixel image and 2000 dots! I also finally got to know some numpy which is cool. The end result is something I can really be proud of and most definitely am :D

###### *I would like to do a web version but i think my motivation is drained out after this xd*