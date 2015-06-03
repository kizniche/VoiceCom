This sets up pocketsphinx to recognize voice commands to raise and lower a projector screen, with the use of a RF remote controlled by the GPIO of a Raspberry Pi.

### Software install

`sudo apt-get update`
`sudo apt-get upgrade`
`sudo apt-get install vim bison libasound2-dev swig python-dev mplayer`

```
wget http://sourceforge.net/projects/cmusphinx/files/sphinxbase/5prealpha/sphinxbase-5prealpha.tar.gz
tar -zxvf ./sphinxbase-5prealpha.tar.gz
cd ./sphinxbase-5prealpha
./configure --enable-fixed
make clean all
make check
sudo make install
Building PocketSphinx
```

```
wget http://sourceforge.net/projects/cmusphinx/files/pocketsphinx/5prealpha/pocketsphinx-5prealpha.tar.gz
tar -zxvf pocketsphinx-5prealpha.tar.gz
cd ./pocketsphinx-5prealpha
./configure
make clean all
make check
sudo make install
```

### Microphone setup

Configure your USB microphone. The following command should show it's detected.

`cat /proc/asound/cards`

change the volume with and selecting the capture settings (F4)

`alsamixer -c 1`

### Creating a language model

Create a list of words/phrases such as:

```
Raise the screen
Lower the screen
Stop the screen
```

Upload this file to http://www.speech.cs.cmu.edu/tools/lmtool-new.html for processing and download the .tgz

Extract the contents with `tar xzvf file.tgz`

### Compile and run listener

`gcc listen_respond.c -o listen_respond -I/usr/local/include -I/usr/local/include/sphinxbase -I/usr/local/include/pocketsphinx -L/usr/local/lib -lpocketsphinx -lsphinxbase -lsphinxad`

`chmod +x listen_respond`

`sudo cp remote.py /usr/local/bin/`

replace file.lm and file.dic with the location of the .lm and .dic files extracted from the generated language model .tgz

`./listen_respond -adcdev hw:1,0 -hmm /usr/local/share/pocketsphinx/model/en-us/en-us -lm ./path/to/file.lm -dict ./path/to/file.dic -samprate 16000/8000/48000 -inmic yes`