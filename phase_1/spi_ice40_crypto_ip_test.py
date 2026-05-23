import machine
import binascii

def main():
    ice_done = machine.Pin(3, machine.Pin.IN)

    SCK = machine.Pin(6, machine.Pin.OUT)
    RST_N = machine.Pin(7, machine.Pin.OUT)
    MOSI = machine.Pin(8, machine.Pin.OUT)
    MISO = machine.Pin(9, machine.Pin.IN)
    NORM_CS_N = machine.Pin(10, machine.Pin.OUT)
    START = machine.Pin(12, machine.Pin.OUT)
    BUSY = machine.Pin(14, machine.Pin.IN)
    ENC_DEC = machine.Pin(13, machine.Pin.OUT) # 0 = encrypt, 1 = decrypt

    SCK.value(0)
    RST_N.value(1)
    NORM_CS_N.value(1)
    START.value(0)

    spi = machine.SoftSPI(baudrate=50000, polarity=0, phase=0, bits=8, firstbit=machine.SPI.MSB, sck=SCK, mosi=MOSI, miso=MISO)

    #reset the AES core

    RST_N.value(0)
    SCK.value(1)
    SCK.value(0)
    RST_N.value(1)
    SCK.value(1)
    SCK.value(0)

    # engage the input SPI
    plaintext = bytearray([0x59, 0xC3, 0x59, 0xC3])
    ciphertext = bytearray([0x8D, 0x86, 0x9B, 0xBB])
    
    #############################################################
    ## Test SPI readback
    #############################################################
    txdata = plaintext
    rxdata = bytearray(4)
    NORM_CS_N.value(0)
    spi.write(txdata)
    NORM_CS_N.value(1)

    #do a test readout
    NORM_CS_N.value(0)
    spi.write_readinto(txdata, rxdata)
    NORM_CS_N.value(1)

    if txdata == rxdata:
        print("SPI functional test pass")
    else:
        print("Error: SPI error")
        return
       
    #############################################################
    ## Test encryption
    #############################################################
    ENC_DEC.value(0) # encrypt

    START.value(1)
    SCK.value(1)
    SCK.value(0)
    START.value(0)
    
    if(BUSY.value() == 1):
        print("IP core successfully busy")
    else:
        print("Error: IP core did not go busy")
        return
    
    #run 3 clock cycles to finish the system
    # (4 clock cycles total:
    for i in range(7):
        SCK.value(1)
        SCK.value(0)
          
    if(BUSY.value() == 0):
        print("IP core successfully finished")
    else:
        print("Error: IP core did not finish")
        return
    
    #do the readout
    NORM_CS_N.value(0)
    spi.write_readinto(txdata, rxdata)
    NORM_CS_N.value(1)
    if rxdata != ciphertext:
        print("Encryption failed, got", binascii.hexlify(rxdata), "expected", binascii.hexlify(ciphertext))
    else:
        print("Encryption value correct:", binascii.hexlify(rxdata))

    #############################################################
    ## Test decryption
    #############################################################
    ENC_DEC.value(1) # decrypt

    #reset the AES core

    RST_N.value(0)
    SCK.value(1)
    SCK.value(0)
    RST_N.value(1)
    SCK.value(1)
    SCK.value(0)

    txdata = ciphertext
    rxdata = bytearray(4)
    NORM_CS_N.value(0)
    spi.write(txdata)
    NORM_CS_N.value(1)

    START.value(1)
    SCK.value(1)
    SCK.value(0)
    START.value(0)
    
    #run 3 clock cycles to finish the system
    # (4 clock cycles total:
    for i in range(7):
        SCK.value(1)
        SCK.value(0)
          
    if(BUSY.value() == 0):
        print("IP core successfully finished")
    else:
        print("Error: IP core did not finish")
        return
    
    #do the readout
    NORM_CS_N.value(0)
    spi.write_readinto(txdata, rxdata)
    NORM_CS_N.value(1)
    if rxdata != plaintext:
        print("Decryption failed, got", binascii.hexlify(rxdata), "expected", binascii.hexlify(plaintext))
    else:
        print("Decryption value correct:", binascii.hexlify(rxdata))
    

main()
    




