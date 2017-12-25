
[merry christmas](https://github.com/ftc300/ChrisHatByeWeChat/blob/master/image/deal.gif)
## Requirements 

Pillow, MoviePy, and NumPy etc ,如果安装了cv2调试更佳

## How to Use

1、先下载 [shape_predictor_68](https://github.com/davisking/dlib-models/blob/master/shape_predictor_68_face_landmarks.dat.bz2),放在根目录。

2、在终端输入如下命令：

```bash
$ python generate_christmas_gif.py -img sourcepath(eg:image/merry.jpg) 
```
3、最终生成的gif图为 image/deal.gif

确保图片中有人脸，否则程序会立即退出。


## FAQ:

1、遇到FFMPEG not downloaded的问题,可以查看[moviepy issue#493](https://github.com/Zulko/moviepy/issues/493) 

   Run in a python console/shell (e.g. IPython/IDLE shell):
````
>> import imageio
>> imageio.plugins.ffmpeg.download()
````

## Thanks：

@明星 (图片提供者)

@[burningion](https://github.com/burningion/automatic-memes)

