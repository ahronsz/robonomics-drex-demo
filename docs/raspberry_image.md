# Prepared Image
We prepared an image to make it easier to use the Home Assistant with Xiaomi Miio and Robonomics with the Raspberry Pi.

You can get it here: [download image](https://ipfs.io/ipfs/bafybeihzzqoyycflxzxlxy2aplkzxo537ggqatdlbr24b4dnlyrtpkp2eu)

SHA256 checksum: `7ec5ea99d7e339b54cbeaaae58c8295411769d27732ec2b5464dbb495ba24120`

What preinstalled in the image:
- Ubuntu Server 21.10 (3/4/400): 64-bit server OS for arm64 archtectures
- Python 3.9.7
- Home Assistant Core 2021.11.5
- rustc 1.59.0-nightly (efec54529 2021-12-04)
- substrate-interface 1.1.2
- python-miio 0.5.8

# How To Use The Prepared Image
Install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your computer. Insert SD card into your PC and run the Imager program. In `Operating System` select `Use custom` and choose the previously downloaded `.img.gz` file. Then select your SD card in the `Storage` dropdown and click `WRITE`.

![imager](./media/use_custom_image.png)
![imager](./media/imager_prep.png)

After writing is comleted, open the SD card's files on your computer and navigate inside the root folder of the card. The name should be something similar to `system-boot`.

Find the file named `network-config` and open it in a text editor. Write this to the file:
```
version: 2
ethernets:
  eth0:
    dhcp4: true
    optional: true
wifis:
  wlan0:
    dhcp4: true
    optional: true
    access-points:
      "YOUR_WIFI_NAME":
        password: "YOUR_WIFI_PASSWORD"
```
**Make sure that you input your actual wifi name and your wifi password.** Then you need to save the file, and insert the SD card to the Raspberry Pi and turn it on. It must connect to your wi-fi network, now you need to find its address. Firstly find your address in the local network with:

Password is "ubuntu". Then follow the instructions to change the password.

```bash
ip a
```
It must look like `192.168.xx.xx` or `172.xx.xx.xx`.