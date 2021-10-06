import string

#Initialization 
new_map = dict()
alphabet = str("abcdefghijklmnopqrstuvwyxzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}[]!-+ #$%!@£$%^*(),./?:;'=& <>~_")
en_msg = str("6e0a9372ec49a3f6930ed8723f9df6f6720ed8d89dc4937222ec7214d89d1e0e352ce0aa6ec82bf622227bb70e7fb7352249b7d893c493d8539dec8fb7935d490e7f9d22ec89b7a322ec8fd80e7f8921")
dec_msg = str("")

#Making a map of letters - encrpyted values
def mapping(MSG):
	temp_map = dict()
	for char in MSG:
		v = (123 * ord(char) + 18) % 256
		v = bytes([v])
		v = v.hex()
		temp_map[char] = v
		print(char + " " + v)
	return temp_map


# Finding the corresponding value 
def matching(MSG):
	de_msg = ""
	for i in range(0, len(MSG) - 1, 2):
		value = MSG[i:i+2]
		if value in new_map.values():
			de_msg += list(new_map.keys())[list(new_map.values()).index(value)]
			 
	return de_msg

new_map = mapping(alphabet)
dec_msg = matching(en_msg)
print(dec_msg)
