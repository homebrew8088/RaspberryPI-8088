import spidev


MCP23S17_WRITE_00 = 0b01000000
MCP23S17_READ_00 =  0b01000001
MCP23S17_WRITE_01 = 0b01000010
MCP23S17_READ_01 =  0b01000011
MCP23S17_WRITE_10 = 0b01000100
MCP23S17_READ_10 =  0b01000101
IOCON_0A = 0x0A
IODIRA = 0x00
IODIRB = 0x01
GPIOA = 0x12;
GPIOB = 0X13;
ALL_OUT = 0x00;
ALL_IN = 0xFF;

spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 10000000


def Start_SPI():
    #Enable address pins
    spi.xfer([MCP23S17_WRITE_10, IOCON_0A, 0b00001000])
    #Setup ports
    #8 bit Data
    spi.xfer([MCP23S17_WRITE_00, IODIRA, ALL_IN])
    #Address 0-7
    spi.xfer([MCP23S17_WRITE_00, IODIRB, ALL_IN])
    #Address 8-15
    spi.xfer([MCP23S17_WRITE_01, IODIRA, ALL_IN])
    #Address 16-19
    spi.xfer([MCP23S17_WRITE_01, IODIRB, ALL_IN])
    #Control Port
    spi.xfer([MCP23S17_WRITE_10, IODIRB, 0b00111111])
    #Extra
    spi.xfer([MCP23S17_WRITE_10, IODIRA, ALL_OUT])

def Reset():
    #Write 0 to 8284 reset pin
    spi.xfer([MCP23S17_WRITE_10, GPIOB, 0b00000000])
    #Write 1 to 8284 reset pin 
    spi.xfer([MCP23S17_WRITE_10, GPIOB, 0b10000000])
    
def Hold(bool_val):
    if bool_val == True:
        #Writes 1 to the hold pin 0bx1xxxxxx, keeps reset pin high
        spi.xfer([MCP23S17_WRITE_10, GPIOB, 0b11000111])
        #Reads from the Control port checking for HOLDA pin to go high
        HoldA = spi.xfer([MCP23S17_READ_10, GPIOB, 0x00])
        HoldA[2] = HoldA[2] & 0b00100000
        #Waits for HoldA pin to go high
        while HoldA[2] != 0b00100000:
            HoldA = spi.xfer([MCP23S17_READ_10, GPIOB, 0x00])
            HoldA[2] = HoldA[2] & 0b00100000
        #Sets up Control port enables RD, WR, IO/M pins
        spi.xfer([MCP23S17_WRITE_10, IODIRB, 0b00111000])
        #8 bit Data out (this kind of doesn't mater becasue read and write operations change this port as needed)
        spi.xfer([MCP23S17_WRITE_00, IODIRA, ALL_OUT])
        #ADDRESS 0-7 port enabled as output
        spi.xfer([MCP23S17_WRITE_00, IODIRB, ALL_OUT])
        #ADDRESS 8-15 port enabled as output
        spi.xfer([MCP23S17_WRITE_01, IODIRA, ALL_OUT])
        #ADDRESS 16-19 port enabled as output
        spi.xfer([MCP23S17_WRITE_01, IODIRB, ALL_OUT])

    elif bool_val == False:
        #8 bit Data port disabled
        spi.xfer([MCP23S17_WRITE_00, IODIRA, ALL_IN])
        #ADDRESS 0-7 port disabled
        spi.xfer([MCP23S17_WRITE_00, IODIRB, ALL_IN])
        #ADDRESS 8-15 port disabled
        spi.xfer([MCP23S17_WRITE_01, IODIRA, ALL_IN])
        #ADDRESS 16-19 port disabled
        spi.xfer([MCP23S17_WRITE_01, IODIRB, ALL_IN])
        #Sets up Control port (sets RD, WR, IO/M to inputs)
        spi.xfer([MCP23S17_WRITE_10, IODIRB, 0b00111111])
        #Unholds
        spi.xfer([MCP23S17_WRITE_10, GPIOB, 0b10000111])
    
def Write_Memory_Array(Address, code_for_8088):
    #8 bit Data out put
    spi.xfer([MCP23S17_WRITE_00, IODIRA, ALL_OUT])
    for i in code_for_8088:
         spi.xfer([MCP23S17_WRITE_00, GPIOA, i])  
         spi.xfer([MCP23S17_WRITE_00, GPIOB, Address])
         spi.xfer([MCP23S17_WRITE_01, GPIOA, Address >> 8])
         spi.xfer([MCP23S17_WRITE_01, GPIOB, Address >> 16]) 

         spi.xfer([MCP23S17_WRITE_10, GPIOB, 0b11000001])
         spi.xfer([MCP23S17_WRITE_10, GPIOB, 0b11000111])   
         Address += 1       

        

