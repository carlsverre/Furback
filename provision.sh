#!/bin/bash

sudo apt-get update

sudo apt-get install -y vim git-core espeak python-dev python-pip bison libasound2-dev libportaudio-dev python-pyaudio build-essential
sudo apt-get install -y subversion autoconf libtool automake gfortran g++ redis-server portaudio19-dev
sudo apt-get install -y espeak libespeak1 mbrola mbrola-en1 alsa-utils

echo 'LD_LIBRARY_PATH="/usr/local/lib"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH' >> ~/.bashrc
echo 'PATH=$PATH:/usr/local/lib/' >> ~/.bashrc
echo 'export PATH' >> ~/.bashrc

export LD_LIBRARY_PATH="/usr/local/lib"
source ~/.bashrc

cd /tmp
wget http://downloads.sourceforge.net/project/cmusphinx/sphinxbase/0.8/sphinxbase-0.8.tar.gz
tar -zxf sphinxbase-0.8.tar.gz
wget http://downloads.sourceforge.net/project/cmusphinx/pocketsphinx/0.8/pocketsphinx-0.8.tar.gz
tar -zxf pocketsphinx-0.8.tar.gz

cd /tmp/sphinxbase-0.8/
./configure --enable-fixed
make
sudo make install

cd /tmp/pocketsphinx-0.8/
./configure
make
sudo make install

cd /tmp
svn co https://svn.code.sf.net/p/cmusphinx/code/trunk/cmuclmtk/
cd /tmp/cmuclmtk/
sudo ./autogen.sh && sudo make && sudo make install

cd /tmp
wget http://distfiles.macports.org/openfst/openfst-1.3.3.tar.gz
wget https://mitlm.googlecode.com/files/mitlm-0.4.1.tar.gz
wget https://m2m-aligner.googlecode.com/files/m2m-aligner-1.2.tar.gz
wget https://phonetisaurus.googlecode.com/files/phonetisaurus-0.7.8.tgz
wget http://phonetisaurus.googlecode.com/files/g014b2b.tgz
tar -xvf m2m-aligner-1.2.tar.gz
tar -xvf openfst-1.3.3.tar.gz
tar -xvf phonetisaurus-0.7.8.tgz
tar -xvf mitlm-0.4.1.tar.gz
tar -xvf g014b2b.tgz

cd /tmp/openfst-1.3.3/
sudo ./configure --enable-compact-fsts --enable-const-fsts --enable-far --enable-lookahead-fsts --enable-pdt
sudo make install

cd /tmp/m2m-aligner-1.2/
sudo make

cd /tmp/mitlm-0.4.1/
sudo ./configure
sudo make install

cd /tmp/phonetisaurus-0.7.8/
cd src
sudo make

sudo cp /tmp/m2m-aligner-1.2/m2m-aligner /usr/local/bin/m2m-aligner
sudo cp /tmp/phonetisaurus-0.7.8/phonetisaurus-g2p /usr/local/bin/phonetisaurus-g2p

cd /tmp/g014b2b/
./compile-fst.sh

mv /tmp/g014b2b ~/phonetisaurus

sudo chmod 777 -R ~
