


# Install G++ for Vertica CentOS7.9
```shell
# On CentOS 7, you can install GCC 8 from Developer Toolset. First you need to enable the Software Collections repository
yum install centos-release-scl


# Then you can install GCC 8 and its C++ compiler:
yum install devtoolset-8-gcc devtoolset-8-gcc-c++

# To switch to a shell which defaults gcc and g++ to this GCC version, use:
scl enable devtoolset-8 -- bash
```