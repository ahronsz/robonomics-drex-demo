## Installation
- Prepare the RPI for Substrate libs ([source](https://www.rust-lang.org/tools/install)):
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
rustup default nightly
```
- Install gpiozero library ([source](https://gpiozero.readthedocs.io/en/stable/installing.html)) and reboot:
```bash
sudo apt update
sudo apt install python3-gpiozero
sudo reboot
```
- Clone the repository
```bash
git clone https://github.com/ahronsz/robonomics-drex-demo.git
```
- Install project requirements
```bash
pip3 install -r requirements.txt
```

## Account management
Crearemos una cuenta de robonomics en la red de Kusama:
(https://polkadot.js.org/apps/)

1. First, entramos a la red de Kusama & Parachains. En la parachain Robonomics.

![imager](../media/create-account-1.png)

2. Entra a la pestaña de "Accounts" y crea una cuenta. **Importante**
Guarda esta clave mnemonic seed, para las futuras operaciones.

![imager](../media/create-account-2.png)

3. Una vez finalizada, debemos de guardar el siguiente archivo generado. **Importante** Esta cuenta puede ser utilizada en las diversas parachains que se encuentra en Polkadot.js, seleccionar la opcion de Restore Json y luego importar el archivo generado.

![imager](../media/create-account-3.png)


## Run Robonomics coffee
Run this in repo folder:
```bash
python3 main.py <previously saved seed>
```
You can send tokens from another account created the same way via `assets:transfer` *extrinsic* on 
[Statemine](https://polkadot.js.org/apps/?rpc=wss%3A%2F%2Fkusama-statemine-rpc.paritytech.net#/explorer).

As soon as there is an income (positive change in `assets:account` *storage function* for address 
derived from seed and for token id `102`)

## Things to point out
- This is a POC of a blockchain-driven IoT device, it has things to improve, wires to hide and functionality to implement
- Token ID, the one, solar-panel is waiting to receive is edited
[here](https://github.com/Multi-Agent-io/robonomics-coffee-maker/blob/master/statemine_monitor.py#L27), so you can use your own token
- Right now the only thing that matters for income tracker is the positive difference between current and previous
asset balance. This may be filtered [code](https://github.com/ahronsz/robonomics-drex-demo/blob/main/services/statemine_monitor.py).
- Powered by [Robonomics](https://robonomics.network/).
