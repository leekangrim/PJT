# Ubuntu Tensorflow GPU 설치

>참고 주소 : https://seonghyuk.tistory.com/58





## 0. 세팅 환경 확인

### 0) 우분투 버전 확인

```bash
$ cat /etc/issue
```

```
Ubuntu 20.04.1 LTS \n \l
```



### 1) SSAFY GPU 사양

```bash
$ lspci | grep -i VGA
```

```
*-display
       description: VGA compatible controller
       product: SVGA II Adapter [15AD:405]
       vendor: VMware [15AD]
       physical id: f
       bus info: pci@0000:00:0f.0
       version: 00
       width: 32 bits
       clock: 33MHz
       capabilities: vga_controller bus_master cap_list rom
       configuration: driver=vmwgfx latency=64
       resources: irq:16 ioport:1140(size=16) memory:e8000000-efffffff memory:f9000000-f97fffff memory:c0000-dffff


*-display
       description: 3D controller
       product: GV100GL [Tesla V100 PCIe 32GB] [10DE:1DB6]
       vendor: NVIDIA Corporation [10DE]
       physical id: 0
       bus info: pci@0000:03:00.0
       version: a1
       width: 64 bits
       clock: 33MHz
       capabilities: bus_master cap_list
       configuration: driver=nvidia latency=248
       resources: iomemory:7f00-7eff iomemory:7f80-7f7f irq:85 memory:fb000000-fbffffff memory:7f000000000-7f7ffffffff memory:7f800000000-7f801ffffff
```



## 1. 우분투에서 20.04 cuda 10.1을 설치하기

```bash
$ sudo apt install nvidia-cuda-toolkit
```



### 1.1. 쿠다 버전 확인하기

```bash
$ nvcc -V
```



### 1.2. 쿠다 설치된 곳 확인하기

```bash
$ whereis cuda
```



## 2. cuDNN 설치하기

> cuDNN 7.6.5 버전을 다운받아줍니다. CUDA버젼에 따라 호환되는 cuDNN 버전이 다릅니다.

0. https://developer.nvidia.com/rdp/cudnn-archive

1. Download cuDNN 7.6.5 for cuda10.1 클릭
3. Download cuDNN 7.6.5 for cuda10.1에 들어가서 cuDNN Library for Linux를 클릭하셔서 다운
3. 다운이 완료가 되면 압축을 풀어줍니다.

```bash
$ tar -xvzf cudnn-10.1-linux-x64-v7.6.5.32.tgz
```

4. 압축을 풀었으면 아까 cuda가 설치된 곳으로 복사

```bash
$ sudo cp cuda/include/cudnn.h /usr/lib/cuda/include/
$ sudo cp cuda/lib64/libcudnn* /usr/lib/cuda/lib64/
```



### 2.1. cuDNN 권한 설정

```bash
$ sudo chmod a+r /usr/lib/cuda/include/cudnn.h 
$ sudo chmod a+r /usr/lib/cuda/lib64/libcudnn*
```



## 3. 환경변수 설정

- vim으로 환경변수를 직접 설정하거나 아니면
- 커맨드 라인에서 바로 아래처럼 echo를 써서 적용시켜 줘도 됩니다.

```bash
$ sudo vim ~/.bashrc 
```

```bash
$ echo 'export LD_LIBRARY_PATH=/usr/lib/cuda/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
$ echo 'export LD_LIBRARY_PATH=/usr/lib/cuda/include:$LD_LIBRARY_PATH' >> ~/.bashrc
```

- 환경변수 설정해주시고 재부팅하지않고 source를 써서 환경변수를 적용시켜줍니다.

```bash
$ source ~/.bashrc
```



## 4. 텐서플로 gpu 설치하기

```python
# tensorflow-gpu
!pip install tesnsorflow-gpu==2.2.0
!pip install tensorflow=2.2.0
!pip install keras

# pytorch
!pip install torch==1.7.1+cu101 torchvision==0.8.2+cu101 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

# etc
!pip install gensim
!pip install scikit-learn
```

