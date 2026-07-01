# Hackster iCE40 Cryptographic IP Core

## Introduction
This IP core implements a lightweight AES-128 cryptographic accelerator designed specifically for the Lattice iCE40 UltraPlus FPGA on the Hackster board. It is capable of encrypting or decrypting a 128-bit input block using a static-key Advanced Encryption Standard (AES) algorithm. To maintain a minimal resource footprint, the core omits a standard complex bus interface (like AXI or Wishbone) in favor of a raw SPI peripheral interface combined with discrete sideband I/O for direct application processor control.

## 2. IP Core Overview
The IP core operates by ingesting a 128-bit plaintext or ciphertext block via a Serial Peripheral Interface (SPI). The application device (RP2040) acts as the SPI Controller, while the FPGA acts as the SPI Peripheral.

**Critical Architectural Note:** This IP operates on a unified clock domain. The SPI clock (SCK) provided by the application processor directly drives the entire internal system, including the 128-bit shift registers and the cryptographic engine. The application device must provide a continuous or properly bursted SCK that does not exceed 1 MHz.

## 3. Port Descriptions

| Pin Name | Direction | Description |
| --- | --- | --- |
| `SCK` | Input | Unified system and SPI clock (Max 1 MHz). |
| `RST_N` | Input | Synchronous active-low reset. |
| `MOSI` | Input | SPI Controller Out, Peripheral In (Serial Data). |
| `MISO` | Output | SPI Controller In, Peripheral Out (Serial Data). |
| `NORM_CS_N` | Input | Active-low SPI chip-select. Acts as the shift-enable for the input buffer. |
| `START` | Input | Triggers the start of the encryption or decryption process. |
| `ENCRYPT_NDECRYPT` | Input | Mode select flag. `1`: Encrypt, `0`: Decrypt. |
| `BUSY` | Output | Status flag. High while the crypto engine is actively processing data. |
| `ICE_LED` | Output | Visual mirror of the `BUSY` signal, routed to an onboard LED. |


## 4. Usage Guideline## 4. Usage Guideline

To properly ingest data, process it, and read the result back, the application processor must adhere to the following sequence. 

**Note on Clocking:** Because `SCK` acts as both the SPI clock and the internal system clock, the application processor must hand off control of the `SCK` pin between the hardware SPI controller (for data transfer) and manual GPIO toggling (for state machine execution).

### Step 1: Initialization

1. Initialize the interface by setting `SCK` low, `NORM_CS_N` high, and `START` low.
2. **Reset the IP Core:** - Assert `RST_N` low.
   - Manually pulse `SCK` high, then low.
   - Assert `RST_N` high.
   - Manually pulse `SCK` high, then low one additional time.

### Step 2: Data Ingestion

1. Set the `ENCRYPT_NDECRYPT` pin to the desired operation (`1` for encryption, `0` for decryption).
2. Assert `NORM_CS_N` low to enable the shift register.
3. Using the application device's SPI controller, transmit 128 bits (16 bytes) of data over `MOSI`. The SPI controller will automatically generate the `SCK` pulses required to shift the data in.
4. Assert `NORM_CS_N` high to latch the full 128-bit block from the shift register into the internal AES data path.

### Step 3: Execution

1. Assert the `START` pin high.
2. Manually pulse `SCK` high, then low.
3. Assert the `START` pin low.
4. **Verify Active State:** Check the `BUSY` pin. It should immediately transition high (`1`), indicating the AES engine has entered the INIT state.
5. **Run the State Machine:** Manually pulse the `SCK` pin exactly 12 more times. The cryptographic engine requires exactly 13 total clock cycles to complete its operation (1 pulse during the `START` assertion, plus 12 pulses for the ROUND states).
6. **Verify Completion:** Check the `BUSY` pin. On the falling edge of the 13th clock cycle, the IP core automatically parallel-loads the processed ciphertext/plaintext back into the SPI shift register, and `BUSY` will return low (`0`).

### Step 4: Data Extraction

1. Assert `NORM_CS_N` low.
2. Using the application device's SPI controller, perform a 128-bit (16-byte) SPI read (simultaneously transmitting dummy data to generate the clock). The processed data will be shifted out over the `MISO` line.
3. Assert `NORM_CS_N` high.
