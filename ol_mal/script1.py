from blog.models import DOI
in_file = "url.txt"
data_file = []

with open(in_file, 'r') as read_file:
    for line in read_file:
        data_file.append(line.strip('\n'))

for x in data_file:
	DOI(doi = str(x)).save()
print(len(data_file))




