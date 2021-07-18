# Tradutor

#### How to enter Virtual Machine:
- install "virt-viewer"
- Create SSL Tunnel to address: "localhost:5920":
  -  Command "sudo ssh -f -L localhost:5920:v07.hlt.inesc-id.pt:5900 imcl@ssh.hlt.inesc-id.pt -N"
- Open "virt-viewer"
  - Type "spice://localhost:5920" 

#### Error: "Could not resolve host: github.com" or Error: "Temporary failure resolving..." in "sudo apt install/update"
- add "nameserver 8.8.8.8" in "etc/resolv.conf"
  - echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf > /dev/null

