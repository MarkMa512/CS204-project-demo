# CS204 Project Demo - TraceRouteIXP

## Intro 
This program aims to provide a detailed analysis for the list of hops, their IP addresses, physical locations and possible IXPs when we queries a specific URL. 

### Directories and Files 

-  `/util`: 
    - `csv_helper.py`: contains function that writes the IXP data found into csv file 
    - `gpt_whois.py`: contains function that queries an IP address via `whois` program and uses OpenAI GPT API to extract the essential information
    - `network.py`: contains functions used to obtain network information, such as the SSID and IP address 
    - `speed_test.py`: contains functions used to perform ping test and speed test 
    - `trace_route.py`: contains functions used to perform the traceroute and IP address analysis
    -  `whois.py`: retired whois module that uses regular expression to analyze whois result 
- `/caida`: 
    - `ip_map_ixp.py`: contains functions that maps IP address to known IXPs via exact matching. Obtained from [How to map an IP address to a Internet eXchange Point (IXP)](https://catalog.caida.org/recipe/how_to_map_ip_to_ixp). See [Acknowledgement and Citation](#acknowledgement-and-citation) for information. 
    - ``
- `key`: file containing your OpenAI API Key 
- `ixs_yyyymm.jsonl`: CAIDA IXP Dataset 
- `main.py`: main entry point of the program 
- `main_ip_match.py`: retired main entry point of the program via ip address matching 
- `requirement.txt`: contains the relevant python package to be installed. 

### Features 

1. Network Information 

    The program will provide information such as the SSID of the current network, and IP address of current host. In addition, by adding additional flags, the program is able to perform additional test on the network. `-p` will allow the program to perform a Ping Test to the target URL, while the `-s` flag will allow the program to perform a speed test of current network. Using `-u custom.target.url`, you are able to specify the URL to be queried. 

2. TraceRoute 

    The program will perform a `traceroute` query to the target URL, and record the IP addresses of each hops, and display the latency to each hop. 

3. IP address Analysis 

    For the list of IP addresses obtained above, the program provides the following analysis: 

    a. Location Identification 
    b. Compare the IP Address against a know database of IXP IP addresses through exact matching and longest prefix matching. Please uncomment the corresponding code in `main.py`. 
    c. Run `whois` query on the IP addresses, and use OpenAI's `gpt-3.5-turbo` model to identify the relevant information of the organization owning the IP address range. 

4. Logging and Data Aggregation  

    After successful execution:  
    - The execution log will be stored as `yyyymmdd_hhmmss.log` in the project root directory. 
    - A summary 

## Prerequisite
1. Ensure that you have Python 3.9 and above installed  
2. Operating system: macOS 13 and above  
3. Ensure that you have `traceroute` and `whois` command installed on your OS. You can install them via [Home Brew](https://brew.sh/) package manager:  
    a. Install Home Brew: 
    ```sh 
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
    b. Install traceroute  
    ```sh
    homebrew install traceroute
    ```
    c. Install whois  
    ```sh
    homebrew install whois
    ```
4. For `gpt_whois.py` to work properly, kindly ensure that you have a valid OpenAI API key. Please refer to: [GPT-OpenAI API](https://platform.openai.com/docs/guides/gpt)
5. If you wish to compare the IP address you have obtained in `traceroute` against the database of known IXP database. Please download the latest dataset from: [CAIDA Internet eXchange Points (IXPs) Dataset](https://www.caida.org/catalog/datasets/ixps/) and put it in the project directory. 
    - File Name: `ixs_yyyymm.jsonl`

## Usage

### Preparation 

1. Clone the repository: 
    ```sh 
    git clone https://github.com/MarkMa512/cs204-project-demo.git
    ```
2. Prepare the `key` file shown as [Prerequisite](#prerequisite) in the project root directory

3. Install Relevant Python Packages 
    ```sh
    pip install -r requirements.txt
    ```

### Run the program 

#### Perform traceroute to default Target URL: `cmu.edu`

```sh 
python main.py 
```

#### Perform traceroute to specified Target URL: `custom.target.url`

```sh 
python main.py -u custom.target.url
```

#### Add Speed Test for current network 

```sh 
python main.py -u custom.target.url -s
```

#### Add Ping Test to the Target URL

```sh 
python main.py -u custom.target.url -s -p
```

Note: Depending on your Python installation and configuration. You may need to use `python3` and `pip3` instead of `python` and `pip` in the command above. 

### Exit the program 

Press `Ctrl + C` on your keyboard to interrupt the program 

## Acknowledgement

`ip_map_ixp.py` and dataset from the following sources are used in this project: 

- Nathan Zak.  (2022). [How to map an IP address to a Internet eXchange Point (IXP)](https://catalog.caida.org/recipe/how_to_map_ip_to_ixp)

- [CAIDA Internet eXchange Points Dataset](https://catalog.caida.org/dataset/ixps) 

This project is purely intended for Academic purposes. 