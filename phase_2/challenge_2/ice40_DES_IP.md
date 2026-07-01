# Hackster iCE40 DES Cryptographic IP Core with Scan Chain

## 1. Introduction
This IP core implements a Data Encryption Standard (DES) cryptographic accelerator designed for the Lattice iCE40 UltraPlus FPGA on the Hackster board. It encrypts or decrypts a 64-bit input block using a static 64-bit key. Additionally, this specific IP core includes a hardware scan chain interface, allowing users to shift out internal state data for hardware security evaluation, testing, or fault injection analysis. It utilizes a raw SPI peripheral interface combined with discrete sideband I/O for direct application processor control.

## 2. IP Core Overview
The IP core operates by ingesting a 64-bit plaintext or ciphertext block via a Serial Peripheral Interface (SPI). The application device (RP2040) acts as the SPI Controller, while the FPGA acts as the SPI Peripheral. 

The data output multiplexer on the `MISO` line is controlled by the chip-select pins. Standard operation uses `NORM_CS_N` to shift standard SPI data in and out. Driving `SCAN_CS_N` low allows the user to shift data through the internal scan chain.

**Critical Architectural Note:** This IP operates on a unified clock domain. The SPI clock (`SCK`) provided by the application processor directly drives the entire internal system, including the 64-bit shift registers, the scan chain, and the DES cryptographic engine. The application device must provide a continuous or properly bursted `SCK` that does not exceed 1 MHz.

## 3. Port Descriptions

| Pin Name | Direction | Description |
| :--- | :--- | :--- |
| `SCK` | Input | Unified system and SPI clock (Max 1 MHz). |
| `RST_N` | Input | Synchronous active-low reset. |
| `MOSI` | Input | SPI Controller Out, Peripheral In (Serial Data). |
| `MISO` | Output | SPI Controller In, Peripheral Out. Multiplexed between standard SPI out and scan chain out. |
| `NORM_CS_N` | Input | Active-low SPI chip-select for standard operations. Enables the standard 64-bit input buffer. |
| `SCAN_CS_N` | Input | Active-low SPI chip-select for scan operations. Enables shifting via the internal scan chain. |
| `START` | Input | Triggers the start of the encryption or decryption process. |
| `ENCRYPT_NDECRYPT` | Input | Mode select flag. `1`: Encrypt, `0`: Decrypt. |
| `BUSY` | Output | Status flag. High while the crypto engine is actively processing data. |
| `ICE_LED` | Output | Visual mirror of the `BUSY` signal, routed to an onboard LED. |

## 4. Usage Guideline

To properly ingest data, process it, and read the result back, the application processor must adhere to the following sequence. 

**Note on Clocking:** Because `SCK` acts as both the SPI clock and the internal system clock, the application processor must hand off control of the `SCK` pin between the hardware SPI controller (for data transfer) and manual GPIO toggling (for state machine execution).

### Step 1: Initialization

1. Initialize the interface by setting `SCK` low, `NORM_CS_N` high, `SCAN_CS_N` high, and `START` low.
2. **Reset the IP Core:** - Assert `RST_N` low.
   - Manually pulse `SCK` high, then low.
   - Assert `RST_N` high.
   - Manually pulse `SCK` high, then low one additional time.

### Step 2: Data Ingestion (Normal Mode)

1. Set the `ENCRYPT_NDECRYPT` pin to the desired operation (`1` for encryption, `0` for decryption).
2. Assert `NORM_CS_N` low to enable the standard shift register. Ensure `SCAN_CS_N` remains high.
3. Using the application device's SPI controller, transmit 64 bits (8 bytes) of data over `MOSI`. The SPI controller will automatically generate the `SCK` pulses required to shift the data in.
4. Assert `NORM_CS_N` high to latch the full 64-bit block from the shift register into the internal DES data path.

### Step 3: Execution

1. Assert the `START` pin high.
2. Manually pulse `SCK` high, then low.
3. Assert the `START` pin low.
4. **Verify Active State:** Check the `BUSY` pin. It should transition high (`1`), indicating the DES engine has entered the active state.
5. **Run the State Machine:** Manually pulse the `SCK` pin exactly 18 more times. The cryptographic engine requires exactly 19 total clock cycles to complete its operation (1 pulse during the `START` assertion, plus 18 pulses for the round operations and output latching).
6. **Verify Completion:** Check the `BUSY` pin. On the falling edge of the 19th clock cycle, the IP core automatically parallel-loads the processed ciphertext/plaintext back into the SPI shift register, and `BUSY` will return low (`0`).

### Step 4: Data Extraction (Normal Mode)

1. Assert `NORM_CS_N` low.
2. Using the application device's SPI controller, perform a 64-bit (8-byte) SPI read (simultaneously transmitting dummy data to generate the clock). The processed data will be shifted out over the `MISO` line.
3. Assert `NORM_CS_N` high.

### Step 5: Scan Chain Extraction (Optional)

To extract internal state via the scan chain instead of reading the standard output:
1. Ensure `NORM_CS_N` is driven high. 
2. Drive `SCAN_CS_N` low. 
3. Provide continuous clock pulses on `SCK` to shift the internal scan data out over the `MISO` line.
4. Drive `SCAN_CS_N` high when complete.
