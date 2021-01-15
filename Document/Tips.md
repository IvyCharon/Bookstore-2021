## Tips

### 关于文件IO

文本文件IO大家肯定都会，那么这里主要讲解二进制文件IO。

#### C语言形式

##### 访问文件

关于`FILE*`：

```cpp
FILE* f=fopen("a.bin", "r+b");
fclose(f);
```

其中打开文件参数为：

```
r	从头开始文件只读。
w	清零，从头开始只写。
a	追加、创建，只写。
r+	从头开始，读写。
w+	清零，读写。
a+	追加、创建，读写。
```

二进制文件访问在该参数后加`b`，例如`rb`, `r+b`。

##### 读写函数

```cpp
size_t fread(void *ptr, size_t size_of_elements, size_t number_of_elements, FILE *a_file);
size_t fwrite(const void *ptr, size_t size_of_elements, size_t number_of_elements, FILE *a_file);
```

参数分别为内存数组、单个元素大小(char数组为1)，操作元素数量、要读写的文件。

##### 寻址

这可能是大家最关心的一个问题。

```cpp
int fseek (FILE *fp, long offset, int origin);
```

其中：

```
fp 为文件指针
offset 为偏移量，正后负前。
origin 为起始位置，0开头，1当前，2末尾。(即：开始计算的位置)
```

返回值为0代表成功。

##### 类型转换

如何向一个文件的第100-103字节写入一个int？

强制类型转换！

```cpp
reinterpret_cast<new_type>(expression)
```

强行转换指针类型(将指向任意类型的指针转成`char*`，或将`char*`转成任意类型指针)。

示例代码为：

```cpp
auto f = fopen("a.bin", "w+b");
fseek(f, 100, 0);
int x = 0x3fffefcf;
fwrite(reinterpret_cast<char*>(&x), 1, 4, f);
fclose(f);
```

具体写入文件的字节流与你的测试平台相关(大端、小端)。但是，同一台机器上读写文件时，字节流顺序一定相同(这不是显然的吗)。

如何读取？

```cpp
auto f = fopen("a.bin", "r+b");
fseek(f, 100, 0);
int x = 0;
fread(reinterpret_cast<char*>(&x), 1, 4, f);
fclose(f);
```

注意`fwrite`和`fread`共用`FILE*`中的同一个位置指针。

#### C++形式

C++提供面向对象的方式(fstream类)供你完成相关操作。

```
ofstream 只写
ifstream 只读
fstream 可读写
```

`fstream.open(const char* filename, ios_base::openmode)`打开文件，第一额参数为文件名，第二个参数为操作模式。

操作模式有：

```
ios::in 可读
ios::out 可写
ios::ate 初始位置：文件尾
ios::app 尾部添加(此时无视输出寻址)
ios::trunc 清空现有文件
ios::binary 二进制操作
```

##### 寻址

`fstream.tellg(), fstream.tellp()`：分别输出读取、写入指针的位置。

`fstream.seekg(pos_type position), fstream.seekp(pos_type position)`：改变读、写指针的位置，参数为从文件开始的绝对位置。

`fstream.seekg(off_type offset, seekdir direction), seekp(off_type offset, seekdir direction)`：相对读写指针的位置，`offset`为相对距离，`direction`的取值及含义为：

```
ios::beg 从头开始
ios::cur 从当前开始
ios::end 从尾开始
```

`fstream.read(char* buffer, streamsize size), fstream.write(char* buffer, streamsize size)`，分别表示读写，第一个参数为内存地址，第二个参数为操作大小。

`fstream.flush()`刷新缓存。

`fstream.close()`关闭流。

示例代码：

写：

```cpp
fstream f;
f.open("a.bin", ios::ate | ios::binary | ios::in | ios::out);
f.seekp(10);
int x = 0x3fffefcf;
f.write(reinterpret_cast<char*>(&x), 4);
f.close();
```

读：

```cpp
fstream f;
f.open("a.bin", ios::ate | ios::binary | ios::in | ios::out);
f.seekg(10);
int x = 0;
f.read(reinterpret_cast<char*>(&x), 4);
```

### 关于环境

**推荐使用Clion**

对于这种级别的工程，VSCode不是不可以用，但需要认真调教。不推荐。

论IDE和Editor的差别。

### 秒懂Makefile/CMake

Makefile有什么用？**自动构建整个工程**

按照修改，重新编译引用该文件的可执行文件。

CMake有什么用？**以更加简单的方式生成makefile**

make需要参数文件makefile，简单的单文件makefile结构如下：

```makefile
targets : prerequisites; command
    command
```

例如：

```makefile
code: code.cpp
	g++ code.cpp -o code
clean:
	rm code
```

如果需要引用其他头文件，则为：

```makefile
code: src/code.cpp src/code.hpp 
	g++ src/code.cpp -o bin/code
clean:
	rm bin
```

这个文件代表将`src`目录中的`code.cpp`编译为`bin`目录中的`code`。

make会将第一个目标文件当作整个项目的最终目标文件，并递归构建其所需要的文件。

`clean`目标文件为清理所需命令，执行`make clean`将执行`clean`目标文件下的命令。

cmake需要参数文件CMakeList.txt，一个典型的CMakeList.txt结构如下：

```cmake
cmake_minimum_required(VERSION 2.6)
add_compile_options(-std=c++11 -Wextra -Ofast)
project(bookstore)
add_executable(code src/code.cpp)
```

分别指定版本号、编译选项、项目名称和第一个可执行文件。

如果想编译多个可执行文件，只要多加`add_executable()`即可。

另一个实例为

```cmake
cmake_minimum_required(VERSION 3.10.2)
project(TicketSystem_2020)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Ofast")
include_directories(
	${PROJECT_SOURCE_DIR}/src/
	${PROJECT_SOURCE_DIR}/BPlusTree/
	${PROJECT_SOURCE_DIR}/include/
)
add_executable(code src/code.cpp)
add_executable(backend backend.cpp)
add_executable(test_cache BPlusTree/test_cache.cpp)
```

`include_directories`可指定额外的头文件路径。加入这条语句可以让`#include`不再需要丑陋的相对路径，而只需要简短的文件名。

例如`#include "../BPlusTree/database_cached.hpp"`可改为`#include "database_cached.hpp"`。

