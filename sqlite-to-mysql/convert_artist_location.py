import sys

def main():
	insert = "INSERT INTO artist_location (artist_id, artist_name, location) VALUES"
	dest = open("artist_location.sql", "w")
	with open(sys.argv[1], "r") as src:
		for line in src:
			lines = line.split("<SEP>")
			lines[3] = lines[3].replace('"', '\\"')

			new_line = insert + "(\"" + lines[0] + "\", \"" + lines[3] + "\", \"" + lines[4].strip('\n') + "\");\n"
			dest.write(new_line)

			
	dest.close()

if __name__ == "__main__":
	main()