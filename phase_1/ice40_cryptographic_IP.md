# Hackster iCE40 Cryptographic IP Core

## Introduction
This IP core implements a simple, lightweight cryptographic accelerator designed specifically for the Lattice iCE40 UltraPlus FPGA on the Hackster board. It is capable of encrypting or decrypting a 32-bit input word using a simplified lightweight cryptographic algorithm. To maintain a minimal resource footprint, the core omits a standard complex bus interface (like AXI or Wishbone) in favor of a raw SPI peripheral interface combined with discrete sideband I/O for direct application processor control.

## 2. IP Core Overview

The IP core operates by ingesting a 32-bit plaintext or ciphertext word via a Serial Peripheral Interface (SPI). The application device (RP2040) acts as the SPI Controller, while the FPGA acts as the SPI Peripheral.

**Critical Architectural Note:** This IP operates on a unified clock domain. The SPI clock (`SCK`) provided by the application processor directly drives the entire internal system, including the shift registers and the cryptographic engines. The application device must provide a continuous or properly bursted `SCK` that does not exceed 1 MHz.

## 3. Port Descriptions

| Pin Name | Direction | Description |
| --- | --- | --- |
| `SCK` | Input | Unified system and SPI clock (Max 1 MHz). |
| `RST_N` | Input | Synchronous active-low reset. |
| `MOSI` | Input | SPI Controller Out, Peripheral In (Serial Data). |
| `MISO` | Output | SPI Controller In, Peripheral Out (Serial Data). |
| `NORM_CS_N` | Input | Active-low SPI chip-select. Acts as the shift-enable for the input buffer. |
| `START` | Input | Triggers the start of the encryption or decryption process. |
| `ENC_DEC` | Input | Mode select flag. `0`: Encrypt, `1`: Decrypt. |
| `BUSY` | Output | Status flag. High while the crypto engine is actively processing data. |
| `ICE_LED` | Output | Visual mirror of the `BUSY` signal, routed to an onboard LED. |


## 4. Usage Guideline

To properly ingest data, process it, and read the result back, the application processor must adhere to the following sequence:

### Step 1: Initialization

1. Ensure `SCK` is running or prepared to pulse.
2. Assert `RST_N` low for at least one clock cycle to clear internal registers, then drive `RST_N` high.
3. Drive `NORM_CS_N` high (inactive) and `START` low.

### Step 2: Data Ingestion

1. Set the `ENC_DEC` pin to the desired operation (`0` for encryption, `1` for decryption).
2. Drive `NORM_CS_N` low to enable the shift register.
3. Clock 32 bits of data out from the RP2040 over `MOSI` using `SCK`.
4. Drive `NORM_CS_N` high to latch the full 32-bit word into the internal bus.

### Step 3: Execution

1. Assert the `START` pin high for at least one `SCK` cycle, then drive it low.
2. Monitor the `BUSY` pin. It will transition high while the encryption or decryption operations are processing the word. This should take 4 clock cycles.
3. **Wait for Completion:** Continue monitoring `BUSY`. Do not initiate any SPI transactions.
4. When `BUSY` falls from high to low (the falling edge), the IP core automatically parallel-loads the processed ciphertext/plaintext back into the SPI shift register.

### Step 4: Data Extraction

1. Drive `NORM_CS_N` low.
2. Provide 32 clock cycles on `SCK`. The processed data will be shifted out over the `MISO` line.
3. Drive `NORM_CS_N` high.
