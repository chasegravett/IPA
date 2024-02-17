def is_valid_ip(address):
    nums = []
    octets = address.split(".")
    if len(octets) != 4:
        return False
    
    for octet in octets:
        try:
            nums.append(int(octet))
        except:
            return False
        
    for num in nums:
        if num < 0 or num > 255:
            return False
    
    return True


if __name__ == "__main__":
    address = input("Enter IP Address: ")

    print(is_valid_ip(address))