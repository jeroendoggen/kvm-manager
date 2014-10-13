# KVM Manager
An tool to automate KVM virtual machine management
 * Start/stop virtual machines
 * Create clones
 * Show system status

## Screencast
 <a href="http://www.youtube.com/watch?feature=player_embedded&v=d6rVMrti_zo
" target="_blank"><img src="http://img.youtube.com/vi/d6rVMrti_zo/0.jpg" 
alt="Screencast" width="480" height="320" border="10" /></a>


Assuming you start from a basic Debian installation
 * ``aptitude install apache2`` (only needed if you want to show a status report on a website)
 * ``aptitude install python-pip`` (the Python Package Index: https://pypi.python.org/pypi)
 * ``pip install kvm_manager``

## Install from source:
 * Download the source and run ``python setup.py install``.
 * Python Package available in the Python Package Index at: https://pypi.python.org/pypi/kvm_manager/

## Dependencies:
 * KVM
 * libvirt
 * virt-clone
 *...

 
## Usage:
 * Coming soon

## Limitations:
 * Currently under active development (early Alpha!)
 * Not feature complete at all!

## License:
If not stated otherwise student_evaluator is distributed in terms of the MIT software license.
See LICENSE file in the distribution for details.

## Bug reports:
 * Jeroen Doggen <jeroendoggen@gmail.com>
 * Post issues to GitHub https://github.com/jeroendoggen/kvm-manager/issues.

## Changelog:
0.0.1: Basic features
 * Coming soon
 
## Benchmarks:
 * Create & boot 10 virtual servers (2 GB storage per server): 2 minutes

## Basic virst commands:
 * virsh --connect qemu:///system list --all
 * virsh --connect qemu:///system start Debian
 * virsh --connect qemu:///system stop Debian
