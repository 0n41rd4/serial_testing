import serial
import time

def send_commands_via_tty(tty_device: str, file_path: str, baudrate: int = 115200, timeout: float = 1):
    try:
        with serial.Serial(tty_device, baudrate, timeout=timeout) as ser:
            print(f"Opened serial connection on {tty_device}")
            responses = []

            # Open the file containing the commands and expectations
            with open(file_path, 'r') as file:
                for line in file:
                    line = line.strip()

                    if line.startswith('s:'):
                        # Send message (after 's:')
                        msg = line[2:].strip()  # Get the message after 's:'
                        print(f"Sending: {repr(msg)}")
                        ser.flushOutput()
                        ser.write((msg + "\n").encode("utf-8"))
                        time.sleep(1)

                    elif line.startswith('e:'):
                        # Expect message(s) (after 'e:')
                        expected_str = line[2:].strip()  # Get the expected pattern(s) after 'e:'
                        expected_patterns = [x.strip() for x in expected_str.split(',')]  # Split into list
                        print(f"Expecting: {repr(expected_patterns)}")
                        
                        if expected_patterns:
                            res = ""
                            while True:
                                line_received = ser.readline().decode("utf-8", errors="ignore").strip()
                                if line_received:
                                    print(f"[{tty_device}] {line_received}")
                                    res += line_received + "\n"
                                    # Check if any of the expected patterns match
                                    if any(expected in line_received for expected in expected_patterns):
                                        print(f"Matched one of: {repr(expected_patterns)}")
                                        break
                            responses.append(res.strip())

            return responses

    except Exception as exc:
        print(f"Failed to send message via TTY {tty_device}: {exc}")
        raise

# Example usage
if __name__ == "__main__":
    tty_path = "/dev/ttyUSB0"  # Adjust as needed
    file_path = "commands.txt"  # File containing the list of commands and expected patterns
    results = send_commands_via_tty(tty_path, file_path)
    print("Test succeeded")
