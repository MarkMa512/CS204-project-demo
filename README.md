# CS204 Project Demo - TraceRouteIXP

## Intro 
This program aims to provide a detailed analysis for the list of hops, their IP addresses, physical locations and IXPs they went through.  

### Directories and Files 

-  `/util`: 
    - `network.py`: contains functions used to obtain network information, such as the SSID and IP address 
    - `speed_test.py`: contains functions used to perform ping test and speed test 
    - `trace_route.py`: contains functions used to perform the traceroute and IP address analysis
- `/caida`: 
    - `ip_map_ixp.py`: contains functions that maps IP address to known IXPs. Obtained from [How to map an IP address to a Internet eXchange Point (IXP)](https://catalog.caida.org/recipe/how_to_map_ip_to_ixp). See [Acknowledgement and Citation](#acknowledgement-and-citation) for information. 
- `main.py`: main entry point of the program 


## Prerequisite
1. Ensure that you have Python 3.9 and above installed 
2. So far, the program runs only on macOS 13 and above 
3. Please download the latest dataset from: [CAIDA Internet eXchange Points (IXPs) Dataset](https://www.caida.org/catalog/datasets/ixps/) and put it in the project directory. 
    - File Name: `ixs_20YYMM.jsonl`

## Usage
### Install Relevant Packages 

```sh
pip install -r requirements.txt
```

Or  

```sh
pip3 install -r requirements.txt
```


### Run the program 
```sh 
python main.py url_to_be_queried
```

Or  


```sh 
pythons main.py url_to_be_queried
```


### Sample Output 

```


```

## Acknowledgement and Citation 

code and dataset from the following sources are used in this project: 

- Nathan Zak.  (2022). [How to map an IP address to a Internet eXchange Point (IXP)](https://catalog.caida.org/recipe/how_to_map_ip_to_ixp)

- [CAIDA Internet eXchange Points Dataset](https://catalog.caida.org/dataset/ixps) 

This project is purely intended for Academic purposes. 